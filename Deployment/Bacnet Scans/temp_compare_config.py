__author__ = 'prateek'
__author__ = 'prateek'
import sys
from BeautifulSoup import BeautifulSoup
import re
import operator

def find_val_in_dict(dic, keys, val):
    for key in keys:
        if dic[key]==val:
            return str(key)

args = sys.argv[1:]

if len(args) < 1:
    print "Usage: temp_compare_config new_scan_results.htm"
    sys.exit(1)

new_scan_file_path = args[0]

new_scan_file = open(new_scan_file_path, 'r').read()

new_soup = BeautifulSoup(new_scan_file)

inst_id = [279, 1, 278, 277, 8, 275, 280, 282, 281, 67, 71, 72, 73, 77, 80, 82, 83, 84, 85, 89, 90, 91, 95, 98, 100,
           101, 102, 103, 107, 108, 109, 113, 116, 118, 119, 120, 121, 125, 126, 127, 131, 134, 136, 137, 138, 139, 143,
           144, 145, 149, 152, 154, 155, 156, 157, 161, 162, 163, 167, 170, 172, 173, 174, 175, 179, 180, 181, 185, 188,
           190, 191, 192, 193, 197, 198, 199, 203, 206, 208, 209, 210, 211, 215, 216, 217, 221, 224, 226, 227, 228, 229,
           233, 234, 235, 239, 242, 244, 245, 246, 247, 251, 252, 253, 257, 260, 262, 263, 264, 265, 269, 270, 271, 284,
           287, 289, 290, 291, 292, 296, 297, 298, 302, 305, 307, 308, 309, 310, 314, 315, 316, 320, 323, 325, 326, 327,
           328, 332, 333, 334, 338, 341, 343, 344, 345, 346, 350, 351, 352, 356, 359, 361, 362, 363, 364, 368, 369, 370,
           374, 377, 379, 380, 381, 382, 386, 387, 388, 392, 395, 397, 398, 399, 400, 404, 405, 406, 410, 413, 415, 416,
           417, 418, 422, 423, 424, 428, 431, 433, 434, 435, 436, 440, 441, 442, 446, 449, 451, 452, 453, 9, 78, 96,
           114, 132, 150, 168, 186, 204, 222, 240, 258, 285, 303, 321, 339, 357, 375, 393, 411, 429, 447]
value_type = ["Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "PowerIntr",
              "OnHours", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy",
              "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power",
              "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor",
              "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL",
              "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage",
              "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency",
              "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current",
              "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr",
              "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours",
              "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy",
              "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power",
              "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor",
              "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL",
              "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage",
              "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency",
              "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current",
              "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr",
              "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours",
              "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power", "ApparentEnergy",
              "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor", "Power",
              "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL", "PowerFactor",
              "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage", "VoltageLL",
              "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Current", "Frequency", "Voltage",
              "VoltageLL", "PowerFactor", "Power", "ApparentEnergy", "OnHours", "PowerIntr", "Energy", "Energy",
              "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy",
              "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy", "Energy"]
meterid = ["01", "01", "01", "01", "01", "01", "01", "01", "01", "02", "02", "02", "02", "02", "02", "02", "02", "02",
           "03", "03", "03", "03", "03", "03", "03", "03", "03", "04", "04", "04", "04", "04", "04", "04", "04", "04",
           "05", "05", "05", "05", "05", "05", "05", "05", "05", "06", "06", "06", "06", "06", "06", "06", "06", "06",
           "07", "07", "07", "07", "07", "07", "07", "07", "07", "08", "08", "08", "08", "08", "08", "08", "08", "08",
           "09", "09", "09", "09", "09", "09", "09", "09", "09", "10", "10", "10", "10", "10", "10", "10", "10", "10",
           "11", "11", "11", "11", "11", "11", "11", "11", "11", "12", "12", "12", "12", "12", "12", "12", "12", "12",
           "13", "13", "13", "13", "13", "13", "13", "13", "13", "14", "14", "14", "14", "14", "14", "14", "14", "14",
           "15", "15", "15", "15", "15", "15", "15", "15", "15", "16", "16", "16", "16", "16", "16", "16", "16", "16",
           "17", "17", "17", "17", "17", "17", "17", "17", "17", "18", "18", "18", "18", "18", "18", "18", "18", "18",
           "19", "19", "19", "19", "19", "19", "19", "19", "19", "20", "20", "20", "20", "20", "20", "20", "20", "20",
           "21", "21", "21", "21", "21", "21", "21", "21", "21", "22", "22", "22", "22", "22", "22", "22", "22", "22",
           "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18",
           "19", "20", "21", "22"]

value_type_to_bacnet_name = {'Current':'Total Current Avg',
                             'Frequency': 'Freq.',
                             'Voltage':'Line to neutral average Voltage',
                             'VoltageLL':'Line to line average voltage',
                             'PowerFactor':'Avg PF',
                             'Energy':'Active Energy Wh',
                             'Power':'Active Power Avg Watt',
                             'ApparentEnergy':'Apparent Energy Vah',
                             'OnHours':'On Hours',
                             'PowerIntr':'Power Interruptions'}

new_points = {}
old_points = {}

## Generate old_points dict from above variables
for x in xrange(0,len(inst_id)):
    key_string = '(EM6400-%s.%s)' %(str(meterid[x]), str(value_type_to_bacnet_name[value_type[x]]))
    val = inst_id[x]
    old_points[key_string] = val


new_streams = {}
changed_streams = {}

## Find parent div for all meter BACnet points in new scan file
li_tag = new_soup.find('li', text=re.compile(r'^device 4')).parent

## Iterate over all analog points
for li in li_tag.findAll('li', text=re.compile(r'^analog')):
    point_desc = li.parent.text
    split_desc = point_desc.split('  ')
    point_id = int(split_desc[0].split(' ')[1])
    point_stream = split_desc[1]
    new_points[point_stream] = point_id

for key in new_points.keys():
    if key not in old_points:
        new_streams[key] = new_points[key]
    elif new_points[key] != old_points[key]:
        changed_streams[key] = (old_points[key], new_points[key])

sorted_new_streams = sorted(new_streams.iteritems(), key=operator.itemgetter(1))
sorted_changed_streams = sorted(changed_streams.iteritems(), key=operator.itemgetter(1))

# print
# print "--------------New Streams-----------"
# for x in sorted_new_streams:
#     print "%s - %s" % (str(x[0]), str(x[1]))

## We are only concerned with stream IDs that have changed.
old_keys = old_points.keys()
print
print "-----------Changed Streams : %s ----------" %str(len(changed_streams))
for x in sorted_changed_streams:
    print "%s - Old ID: %s, New ID: %s, Stream currently going to: %s" % (str(x[0]), str(x[1][0]), str(x[1][1]), find_val_in_dict(old_points, old_keys, x[1][1]))