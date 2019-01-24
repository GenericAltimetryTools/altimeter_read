#!/usr/bin/python
# coding=utf-8

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import netCDF4 as ncf
# import pandas as pd
import sys
import pickle

## -- Get the user home directory
from os.path import expanduser
import os

home = expanduser("~")
# ------ Directory contains sentinel3A SRAL data
dir_setup = os.path.join(home, 'alti_data', 'S3A_SR_2_WAT____20170119T125426_20170119T134245_20170214T065922_2899_013_223______MAR_O_NT_002.SEN3')
# ------ Name of the SRAL file. There have three kinds of S3A data which are the enhanced,standard and the reduced data.
# ------ Here we choose the enhanced data because it contains the waveform data.
file_path = os.path.join(dir_setup, 'enhanced_measurement.nc')
print("The Sentinel3A SRAL file is:")
print(file_path)
print('\n')

# -----------------------#
# Open nc file using NetCDF tools
# -----------------------#
ncs3 = Dataset(file_path)

print(ncs3.variables.keys()) #keys 是字典数据类型的元素名称，对应这里就是经纬度时间等参数名字
# print(ncs3.variables)
s3ak = ncs3.variables.keys()
print(type(s3ak)) # 注意数据类型
print(len(s3ak)) # 数据的维度？
s3ak2 = str(s3ak)
print(type(s3ak2))
print(len(s3ak2)) #　字符串的长度

#
lat = ncs3.variables['lat_20_ku'][:]
lon = ncs3.variables['lon_20_ku'][:]
tim = ncs3.variables['time_20_ku'][:]
wav = ncs3.variables['waveform_20_ku'][:]

# vlz = nc.variables['z'][:]
#
print("data dimention")
print(np.shape(lon))
print(np.shape(lat))
print(np.shape(tim))
print(np.shape(wav)) # 数据是二维的

# --------------------------
# 查看数据的类型，注意python和MATLAB的差异
print(type(wav)) #查看数据类型
print(type(tim))
# print(wav[1, :]) #注意大括号和小括号的使用。
# --------------------------

# --------------------------
# Plot wavform
myslice = slice(34980, 20000, -500)
x = np.arange(1, 129, 1)
y = np.array(wav[myslice, :])
lat2 = np.array(lat[myslice])
# Plot waveforms on one figure
# for i in range(1, 200):
#     plt.plot(x, y[i], 'r')

# Plot waveforms on sub figures
figsize = (10, 8)
gs = gridspec.GridSpec(4, 4)
print(type(gs))
gs.update(hspace=0.4)
fig1 = plt.figure(num=2, figsize=figsize)
ax = []

for i in range(16):
    row = (i // 4)
#    print(i, row)
    col = i % 4
#    print(i, col)
    ax.append(fig1.add_subplot(gs[row, col]))
    ax[-1].set_title('lat=%s' % str(round(lat2[i], 4)))
    ax[-1].plot(x, y[i], 'ro', ms=2, ls='-', linewidth=0.5)
plt.show()

# --------------------------
# latinfo = nc.variables['latitude']

# vlzinfo = nc.variables['u']
# print (vlzinfo)

# Save data
np.savetxt("tt.npy", tim, fmt="%10.5f", delimiter=",")
# Save names of s3a variables

fh = open("s3adata.txt", "w")
for i in s3ak:
    fh.write(str(i)+'\n')
fh.close()
