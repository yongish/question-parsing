import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

#read in the file, get data of sensor of interest, create a plot of voltage versus time.

filename = '20230419T0000_0_5000.csv'
initial_datestring = '20230419'
unix_timestamp = time.mktime(datetime.datetime.strptime(initial_datestring, "%Y%m%d").timetuple())

f = open(filename, 'r')
f.readline()
plot_data = []
for line in f.readlines():
  try:
    split_line = line.split(',')
    time_delta = float(split_line[1]) / 1000
    unix_timestamp += time_delta
    voltage = float(split_line[2])
    print([unix_timestamp, voltage])
    plot_data.append([unix_timestamp, voltage])
    
  except:
    pass
  
print(plot_data[:50])
print('number of data points', len(plot_data))

  
plt.plot(
  [datetime.datetime.utcfromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S') for x in plot_data],
  [x[1] for x in plot_data]
)  
plt.show()
  
  
  
  

