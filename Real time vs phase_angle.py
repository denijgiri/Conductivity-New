# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 07:23:21 2024

@author: Denij Giri
"""
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re
import pathlib

def extract_time_from_path(file_list):
    pattern =  r'((\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2}\.\d+))'
    file_list = str(file_list)
    match = re.search(pattern,file_list)    
    
    if match:
        datetime_str = match.group(1)
        time_part_dt = datetime_str.split('T')[0]
        year = int(time_part_dt.split('-')[0])
        month = int(time_part_dt.split('-')[1])
        day = int(time_part_dt.split('-')[2])
        time_part = datetime_str.split('T')[1]
        hour = int(time_part.split('-')[0])
        minute = int(time_part.split('-')[1])
        second = float(time_part.split('-')[2])
        second = int(second)

        dt = datetime(year, month, day, hour,minute,second)
        return dt
    
        
def phase_calculation(data_ad):
    data_td = np.loadtxt(data_ad)
    fourier = np.fft.fft(data_td[:,1])
    phase_angle = np.angle(fourier)
    phase_angle_unwrap = phase_angle
    n = data_td[:,1].size
    timestep = 5 * 10 ** -14
    freqs = np.fft.fftfreq(n, d = timestep)
    #freqs_range = np.array([0.999, 1.01])
    freqs = freqs / 10 ** 12
    freqs_slice_idx = (freqs >= 0.99) * (freqs <= 1)
    freqs = freqs[freqs_slice_idx]
    phase_angle_unwrap = phase_angle_unwrap[freqs_slice_idx]
    #print(phase_angle_unwrap.size)
    return phase_angle_unwrap


data_dir =  r'C:\Users\Denij Giri\Desktop\Conductivity\Silver Sample\sample3\img0'
data_path = pathlib.Path(data_dir)
data_list = list(data_path.glob("*"))


Real_clock_time = []
Phase_angle = []

for i in range(len(data_list)):
    data_refs = data_list[i]
    time_hours = extract_time_from_path(data_refs)
    phase_angle = phase_calculation(data_refs)
    Real_clock_time.append(time_hours)
    Phase_angle.append(phase_angle)
    
plt.figure()
plt.xlabel('Real_clock_time ( Date and hours)')
plt.ylabel('Phase_angle(Radians)')
plt.plot(Real_clock_time, Phase_angle)
plt.title('Phase_Angle Vs Real_Time')
plt.legend()
    
    
    