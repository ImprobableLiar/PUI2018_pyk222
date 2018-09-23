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

def get_buslocation(line, length):
    global count
    count = 0
    buslocation = []
    for i in range(length):
        tempname = jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['PublishedLineName']
        if tempname == line:
            count += 1
            buslocation.append(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation'])
    return buslocation

def get_busstop(line, length):
    busstop = []
    for i in range(length):
        tempname = jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['PublishedLineName']
        if tempname == line:
            busstop.append(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall'])
    return busstop

def get_busstop_distance(line, length):
    busstop_distance = []
    for i in range(length):
        tempname = jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['PublishedLineName']
        if tempname == line:
            busstop_distance.append(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances'])
    return busstop_distance

def fout_businfo(buslocation, busstop, busstop_distance):
    for i in range(count):
        fout.write(str(buslocation[i]['Latitude']))
        fout.write(', ')
        fout.write(str(buslocation[i]['Longitude']))
        fout.write(', ')
        fout.write(busstop[i]['StopPointName'])
        fout.write(', ')
        fout.write(busstop_distance[i]['PresentableDistance'])
        fout.write('\n')
                   
if not len(sys.argv) == 4:
    print("Invalid number of arguments. Run as: python get_bus_info_pyk222.py <MTA_KEY> <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()

MTAurl = 'http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=' + sys.argv[1]
line = sys.argv[2]

fout = open(sys.argv[3], "w")
fout.write("Latitude,Longitude,Stop Name,Stop Status\n")

jsonData = get_jsonparsed_data(MTAurl)

length = len(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
                   
buslocation = get_buslocation(line, length)
busstop = get_busstop(line, length)
busstop_distance = get_busstop_distance(line, length)

fout_businfo(buslocation, busstop, busstop_distance)

fout.close()
