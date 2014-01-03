import os
from os.path import join
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from smap.driver import SmapDriver, util
import struct
from smap import core, actuate
from serial import SerialException


class RateActuator(actuate.NStateActuator):
    """Actuator to set the Polling Rate for a meter.
    """

    def setup(self, opts):
        actuate.NStateActuator.setup(self, opts)
        self.meter = opts.get('meter')

    def get_state(self, request):
        return str(self.meter.Rate)

    def set_state(self, request, state):
        self.meter.Rate = int(state)
        return str(self.meter.Rate)


class Meter:
    def __init__(self, Id, Rate, Floor, Type, Model, FlatNum, Block, Wing, LoadType, SubLoadType, SupplyType):
        self.Id = Id
        self.Rate = Rate
        self.Floor = Floor
        self.Type = Type
        self.Model = Model
        self.FlatNum = FlatNum
        self.Block = Block
        self.Wing = Wing
        self.LoadType = LoadType
        self.SubLoadType = SubLoadType
        self.SupplyType = SupplyType


class ModbusUSBDriver(SmapDriver):
    def setup(self, opts):

        self.read_configurations(opts)

        ## Get number of meters by reading the length of the METERS list.
        self.meter_count = len(self.METERS)

        self.meters = []
        for x in xrange(0, self.meter_count):
            self.meters += [
                Meter(self.METERS[x], self.RATES[x], self.FLOORS[x], self.TYPES[x], self.MODELS[x], self.FLATNUMS[x],
                      self.BLOCKS[x], self.WINGS[x], self.LOADTYPES[x], self.SUBLOADTYPES[x], self.SUPPLYTYPES[x])]

        del (self.RATES)
        del (self.METERS)
        del (self.FLOORS)
        del (self.TYPES)
        del (self.MODELS)
        del (self.FLATNUMS)
        del (self.BLOCKS)
        del (self.WINGS)
        del (self.LOADTYPES)
        del (self.SUBLOADTYPES)
        del (self.SUPPLYTYPES)

        self.configure_parameters()

        self.current = 0            ##Index for the queue

        self.SLOWEST_POSSIBLE_RATE = 30
        self.queue = []

        ##Create 30 queues each representing a second. If the nth queue contains a meter ID x ==> That meter x is to be polled in the nth second.
        ##We will use the modulo operation to maintain a circular loop.
        for x in xrange(0, self.SLOWEST_POSSIBLE_RATE):
            self.queue += [[]]

        for self.current in xrange(0, self.meter_count):
            self.queue[self.current].append(self.meters[self.current])

        self.current = 0

        self.configure_meter_streams_metadata()

        ##Connect using parameters and return the handle.
        self.client = self.CONNECT_TO_METER()
        self.res = None
        self.current = 0

    def start(self):
        util.periodicSequentialCall(self.read).start(1)

    def read(self):
        for x in self.queue[self.current]:
            try:
                t = util.now()
                self.res = self.client.read_holding_registers(3900, 100, unit=x.Id)

                if (self.res == None):
                    continue

                for y in xrange(0, len(self.parameters[x.Model])):
                    read_reg = self.reading_registers[x.Model][y]
                    if (read_reg==92 or read_reg==98):
                        decoder = BinaryPayloadDecoder.fromRegisters(self.res.registers[read_reg:read_reg+2], endian=Endian.Big)
                        value = decoder.decode_32bit_uint()
                    else:
                        value = convert((self.res.registers[read_reg + 1] << 16) + self.res.registers[read_reg])
                    self.add('/Meter' + str(x.Id) + '/' + self.parameters[x.Model][y], t, value)

            except SerialException:
                print "Serial Exception encountered. Looking for new tty port."
                self.client = self.CONNECT_TO_METER()

        pop_count = len(self.queue[self.current])
        for x in xrange(0, pop_count):
            popped = self.queue[self.current].pop(0)
            next_index = (self.current + popped.Rate) % self.SLOWEST_POSSIBLE_RATE

            while (len(self.queue[next_index]) == 2):
                next_index += 1
                if (next_index == self.SLOWEST_POSSIBLE_RATE):
                    next_index = 0

            self.queue[next_index].append(popped)

        self.current = (self.current + 1) % self.SLOWEST_POSSIBLE_RATE

    def read_configurations(self, opts):
    ##Get information from config file about meters to be polled and the rates at which they are to polled.
        ##Get meter specific Metadata that is supplied by the config file.

        ## In case there is just one meter whose configuration is supplied in the file.
        if (type(opts.get('METERS')) == str):
            self.METERS = [int(opts.get('METERS'))]
            self.RATES = [int(opts.get('RATES'))]
            self.FLOORS = [int(opts.get('FLOORS'))]
            self.MODELS = [str(opts.get('MODELS'))]
            self.TYPES = [str(opts.get('TYPES'))]
            self.FLATNUMS = [str(opts.get('FLATNUMS'))]
            self.BLOCKS = [str(opts.get('BLOCKS'))]
            self.WINGS = [str(opts.get('WINGS'))]
            self.LOADTYPES = [str(opts.get('LOADTYPES'))]
            self.SUBLOADTYPES = [str(opts.get('SUBLOADTYPES'))]
            self.SUPPLYTYPES = [str(opts.get('SUPPLYTYPES'))]

        ## For multiple meters to be configured.
        else:
            self.METERS = [int(x) for x in opts.get('METERS')]
            self.RATES = [int(x) for x in opts.get('RATES')]

            self.FLOORS = [int(x) for x in opts.get('FLOORS')]
            self.TYPES = [str(x) for x in opts.get('TYPES')]
            self.MODELS = [str(x) for x in opts.get('MODELS')]
            self.FLATNUMS = [str(x) for x in opts.get('FLATNUMS')]
            self.BLOCKS = [str(x) for x in opts.get('BLOCKS')]
            self.WINGS = [str(x) for x in opts.get('WINGS')]
            self.LOADTYPES = [str(x) for x in opts.get('LOADTYPES')]
            self.SUBLOADTYPES = [str(x) for x in opts.get('SUBLOADTYPES')]
            self.SUPPLYTYPES = [str(x) for x in opts.get('SUPPLYTYPES')]

            ##Connection Parameters.
        self.BAUD_RATE = int(opts.get('BAUD_RATE', 9600))
        self.STOP_BITS = int(opts.get('STOP_BITS', 1))
        self.BYTE_SIZE = int(opts.get('BYTE_SIZE', 8))
        self.PARITY = opts.get('PARITY', 'E')
        self.COM_METHOD = opts.get('COM_METHOD', 'rtu')
        self.TIME_OUT = float(opts.get('TIME_OUT', 0.2))
        self.RETRIES = int(opts.get('RETRIES', 1))
        self.ID_VENDOR = opts.get('ID_VENDOR', '0403')
        self.ID_PRODUCT = opts.get('ID_PRODUCT', '6001')


    def configure_parameters(self):
        self.reading_registers = {'EM6400': [2, 6, 12, 14, 24, 26, 58, 60, 92, 98],
                                  'EM6433': [2, 12, 18, 32, 46, 60, 92, 98],
                                  'EM6436': [2, 6, 12, 18, 26, 32, 46, 60, 92, 98]}

        self.parameters = {
            'EM6400': ['Power', 'PowerFactor', 'Current', 'Frequency', 'VoltagePhase1Phase2', 'VoltagePhase1', 'ApparentEnergy',
                       'Energy', 'OnHours', 'PowerIntr'],
            'EM6433': ['Power', 'Current', 'PowerPhase1', 'PowerPhase2', 'PowerPhase3', 'Energy', 'OnHours',
                       'PowerIntr'],
            'EM6436': ['Power', 'PowerFactor', 'Current', 'PowerPhase1', 'VoltagePhase1', 'PowerPhase2', 'PowerPhase3',
                       'Energy', 'OnHours', 'PowerIntr']}

        self.units = {'Power': 'Watts',
                      'PowerFactor': '',
                      'Voltage': 'Volts',
                      'VoltagePhase1Phase2': 'Volts',
                      'VoltagePhase1': 'Volts',
                      'Frequency': 'Hertz',
                      'Energy': 'Watt-Hours',
                      'ApparentEnergy': 'Volt-Ampere-Hours',
                      'Current': 'Amperes',
                      'PowerPhase1': 'Watts',
                      'PowerPhase2': 'Watts',
                      'PowerPhase3': 'Watts',
                      'PowerFactorPhase1': '',
                      'PowerFactorPhase2': '',
                      'PowerFactorPhase3': '',
                      'OnHours': '',
                      'PowerIntr': ''}

    def configure_meter_streams_metadata(self):
    ##Adding collections to represent meters.
        for x in self.meters:
            path = ('/Meter' + str(x.Id))
            self.add_collection(path)
            self.meter_coll = self.get_collection(path)
            self.meter_coll['Metadata'] = {
                'Instrument': {
                    'Manufacturer': 'Schneider Electric',
                    'Model': x.Model,
                    'SamplingPeriod': '1 Second',
		    'MeterID': x.Id,
		    'LoadType': x.LoadType,
                    'SubLoadType': x.SubLoadType,
                    'SupplyType': x.SupplyType
                },
                'Location': {
                    'Floor': x.Floor,
		    'FlatNumber': x.FlatNum,
		    'Wing': x.Wing
                },
                'Extra': {
                    'Type': x.Type,
                    'Block': x.Block
                }
            }
            ## Add actuator to meter.
            self.add_actuator('/Meter' + str(x.Id) + '/Rate', 'Seconds', RateActuator, data_type='long',
                              timezone='Asia/Kolkata', setup={'states': [str(i) for i in range(1, 31)], 'meter': x})

            for y in self.parameters[x.Model]:
                if y == 'PowerIntr' or y == 'OnHours':
                    ts = self.add_timeseries('/Meter' + str(x.Id) + '/' + y, self.units[y], data_type='long',
                                             timezone='Asia/Kolkata')
                else:
                    ts = self.add_timeseries('/Meter' + str(x.Id) + '/' + y, self.units[y], data_type='double',
                                             timezone='Asia/Kolkata')
                ts['Metadata'] = {'Extra': {'PhysicalParameter': y}}


    def CONNECT_TO_METER(self):

        try:
            clt = None
            METER_PORT = self.find_tty_usb(self.ID_VENDOR,
                                           self.ID_PRODUCT)        #reading to which port rs485(client) is connected
            clt = ModbusClient(retries=self.RETRIES, method=self.COM_METHOD, port=METER_PORT, baudrate=self.BAUD_RATE,
                               stopbits=self.STOP_BITS, parity=self.PARITY, bytesize=self.BYTE_SIZE,
                               timeout=self.TIME_OUT)
            self.iftrue = clt.connect()

            if self.iftrue:
                print "Connection successful. " + str(clt)

            return clt

        except Exception as e:
            #lgr.error('Error while connecting client: ', exc_info = True)
            print "Error while connecting client: \n" + e.__str__()

    def find_tty_usb(self, idVendor, idProduct):
        """find_tty_usb('067b', '2302') -> '/dev/ttyUSB0'"""
        # Note: if searching for a lot of pairs, it would be much faster to search
        # for the enitre lot at once instead of going over all the usb devices
        # each time.
        for dnbase in os.listdir('/sys/bus/usb/devices'):
            dn = join('/sys/bus/usb/devices', dnbase)
            if not os.path.exists(join(dn, 'idVendor')):
                continue
            idv = open(join(dn, 'idVendor')).read().strip()
            if idv != idVendor:
                continue
            idp = open(join(dn, 'idProduct')).read().strip()
            if idp != idProduct:
                continue
            for subdir in os.listdir(dn):
                if subdir.startswith(dnbase + ':'):
                    for subsubdir in os.listdir(join(dn, subdir)):
                        if subsubdir.startswith('ttyUSB'):
                            return join('/dev', subsubdir)


def convert(s):
    '''Function to convert data into float'''
    return struct.unpack("<f", struct.pack("<I", s))[0]
