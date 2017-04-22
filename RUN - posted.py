import serial
import numpy as np
import matplotlib.pyplot as plt
import biosppy as bio
import time
from drawnow import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

ard = serial.Serial('COM9',9600)

length = 6000
make_matrix = [length,2]
ecg_data = np.zeros(make_matrix)
ecg_intermed = np.zeros(5,dtype=int)
difference_track = [0,0,0,0,0,0,0,0,0,0]
time_track = [0,0]
index_track = [0,0]
y_max = []
heart_rate = []
time_max = []
y_max_all = []
time_max_all = []
hrv_plot = []
tme_start = time.time()
data_transfer = 0


## loop until the arduino tells us it is ready
connected = False
while not connected:
    serin = ard.read()
    connected = True

for i in range(length): 
    data_transfer = ard.readline()
    ecg_data[i,0] = float(data_transfer)
    ecg_data[i,1] = time.time()
    
    if ecg_data[i,0] > 700:
        y_max_all.append(ecg_data[i,0])
        time_max_all.append(ecg_data[i,1])
        
        if len(time_max_all) > 2:
                time_diff = time_max_all[-1]-time_max_all[-2]
                if time_diff > 0.05:
                    hr_instant = 1/time_diff*60
                    heart_rate.append(hr_instant)
                    y_max.append(y_max_all[-1])
                    hrv_plot.append(hr_instant)

                    if len(hrv_plot) < 1000:
                        pass
                    else:
                        hrv_plot.pop(0)
                        
    
    print('ECG Data:',str(ecg_data[i,0]))
    
ard.close()

tme_end = time.time()
d_tme = (tme_end - tme_start)#/60 #min
tme = np.linspace(0,d_tme,length)
tme_hr = np.linspace(0,d_tme,len(heart_rate))

resp_min = 5
run = 'A'
resp = 2*np.sin(2*np.pi*resp_min*tme_hr/60)
file = 'resp_' + str(resp_min) + run

def heart_rate_plot():
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(tme,ecg_data[:,0])
    plt.title('Resp:'+str(resp_min))
    plt.ylabel('ECG')
    plt.subplot(3,1,2)
    plt.plot(tme_hr,heart_rate)
    plt.ylabel('Heart Rate (BPM)')
    plt.subplot(3,1,3)
    plt.plot(tme_hr,resp)
    plt.ylabel('Respiration')
    plt.xlabel('Time (sec)')
    plt.savefig(file+'.png')
    plt.show()

heart_rate_plot()


data_save = np.transpose(np.array([tme_hr,heart_rate,resp]))
np.savetxt(file+'.csv',data_save,delimiter=',')

