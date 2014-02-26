"""
Copyright (c) 2011, 2012, Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions 
are met:

 - Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""Driver to poll data from a Weather Underground weather station,
using their json api.

Optional Parameters:

"ID" [default IDELHINE8] : wunderground station id.
"Key" [default None] : API key to use for fetching data.
"Rate" [default 60] : number of seconds between polls.
"Timezone" [default Asia/Kolkata] : Timezone for the location
"""

import urllib2
import json
from datetime import datetime
from calendar import timegm
from twisted.python import log
from smap import driver, util
from dateutil.tz import gettz, tzutc


class WunderGround(driver.SmapDriver):
    def setup(self, opts):
        self.id = opts.get("ID", "IDELHINE8")
        self.key = opts.get("Key", "")
        self.url = "http://api.wunderground.com/api/%s/conditions/astronomy/q/pws:%s.json" % (self.key, self.id)
        self.rate = int(opts.get("Rate", 60))
        self.last_weather = None
        self.last_sun_phase = None
        self.timezone = opts.get('Timezone', 'Asia/Kolkata')

        self.weather_series = [
            {"path": "/humidity", "unit": "", "get_val": self.get_rh, "data_type": "long"},
            {"path": "/temperature", "unit": "C", "get_val": self.get_temp, "data_type": "double"},
        ]

        self.sun_series = [{"path": "/sunrise", "unit": "", "get_val": self.get_sunrise, "data_type": "long"},
                           {"path": "/sunset", "unit": "", "get_val": self.get_sunset, "data_type": "long"}]

        for ts in self.weather_series:
            self.add_timeseries(ts["path"], ts["unit"], data_type=ts["data_type"],
                                timezone=self.timezone)

        for ts in self.sun_series:
            self.add_timeseries(ts["path"], ts["unit"], data_type=ts["data_type"],
                                timezone=self.timezone)

    def get_rh(self, js_res):
        assert len(js_res['current_observation']['relative_humidity']) > 1
        return int(js_res['current_observation']['relative_humidity'][:-1])

    def get_temp(self, js_res):
        return js_res['current_observation']['temp_c']

    def get_sunrise(self, js_res):
        local_epoch = int(js_res['current_observation']['local_epoch'])
        local_datetime = datetime.fromtimestamp(local_epoch, gettz(self.timezone))
        sunrise_hour = int(js_res['sun_phase']['sunrise']['hour'])
        sunrise_minute = int(js_res['sun_phase']['sunrise']['minute'])
        sunrise_datetime = local_datetime.replace(hour=sunrise_hour, minute=sunrise_minute)
        utc_sunrise = sunrise_datetime.astimezone(tzutc())
        utc_stamp = timegm(utc_sunrise.timetuple())
        return utc_stamp

    def get_sunset(self, js_res):
        local_epoch = int(js_res['current_observation']['local_epoch'])
        local_datetime = datetime.fromtimestamp(local_epoch, gettz(self.timezone))
        sunset_hour = int(js_res['sun_phase']['sunset']['hour'])
        sunset_minute = int(js_res['sun_phase']['sunset']['minute'])
        sunset_datetime = local_datetime.replace(hour=sunset_hour, minute=sunset_minute)
        utc_sunset = sunset_datetime.astimezone(tzutc())
        utc_stamp = timegm(utc_sunset.timetuple())
        return utc_stamp

    def start(self):
        util.periodicSequentialCall(self.update).start(self.rate)

    def update(self):
        try:
            url = self.url
            fh = urllib2.urlopen(url)
        except urllib2.URLError, e:
            log.err("URLError getting reading: [%s]: %s" % (url, str(e)))
            return
        except urllib2.HTTPError, e:
            log.err("HTTP Error: [%s]: %s" % (url, str(e)))
            return
        except Exception, e:
            log.err("Exception: %s" % (str(e)))
            return

        try:
            resp = fh.read()
            js_res = json.loads(resp)
            observation_epoch = int(js_res['current_observation']['observation_epoch'])
            local_epoch = int(js_res['current_observation']['local_epoch'])
            local_datetime = datetime.fromtimestamp(local_epoch, gettz(self.timezone))
        except ValueError, e:
            log.err("ValueError: %s" % (str(e)))
            return
        except KeyError, e:
            log.err("KeyError: %s" % (str(e)))
            return

        if not self.last_weather or self.last_weather < observation_epoch:
            self.last_weather = observation_epoch

            try:
                for ts in self.weather_series:
                    get_val = ts['get_val']
                    val = get_val(js_res)
                    self.add(ts["path"], observation_epoch, val)

            except KeyError, e:
                log.err("KeyError: %s" % (str(e)))
                return

        if not self.last_sun_phase or local_datetime.day != self.last_sun_phase.day:
            self.last_sun_phase = local_datetime

            try:
                for ts in self.sun_series:
                    get_val = ts['get_val']
                    val = get_val(js_res)
                    self.add(ts["path"], observation_epoch, val)

            except KeyError, e:
                log.err("KeyError: %s" % (str(e)))
                return