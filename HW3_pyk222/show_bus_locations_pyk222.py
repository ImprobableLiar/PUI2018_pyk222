from __future__ import print_function
import pandas as pd
import pylab as pl
import os
import sys
import json
import requests
from collections import defaultdict
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib
#%pylab inline

def get_jsonparsed_data(url):
    response = urllib.urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def get_businfo(line, length):
    global count
    count = 0
    businfo = []
    for i in range(length):
        tempname = jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['PublishedLineName']
        if tempname == line:
            count += 1
            businfo.append(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation'])
    return businfo

def print_bus_locations(businfo):
    for i in range(count):
        long = businfo[i]['Longitude']
        lat = businfo[i]['Latitude']
        print("Bus " + str(i) + " is at latitude " + str(lat) + " and longitude " + str(long))

if not len(sys.argv) == 3:
    print("Invalid number of arguments. Run as: python show_bus_locations_pyk222.py <MTA_KEY> <BUS_LINE>")
    sys.exit()
    
MTAurl = 'http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=' + sys.argv[1]
line = sys.argv[2]
    
print("Bus Line: " + line)

#My API KEY: 8dddf24d-3719-4eaf-9d47-e6eed4ccafac
#Lines to test: B52

jsonData = get_jsonparsed_data(MTAurl)
#print(type(jsonData))

length = len(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])

businfo = get_businfo(line, length)
print("Number of Active Buses: " + str(count))

print_bus_locations(businfo)