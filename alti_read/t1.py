#!/usr/bin/python
# coding=utf-8

from netCDF4 import Dataset
import numpy as np
# import matplotlib.pyplot as plt
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
print(len(s3ak))
s3ak2 = str(s3ak)
print(type(s3ak2))
print(len(s3ak2))

#
# lat = nc.variables['latitude'][:]
# lon = nc.variables['longitude'][:]
tim = ncs3.variables['time_20_ku'][:]
# vlz = nc.variables['z'][:]
#
# print (np.shape(lon))
# print (np.shape(lat))
# print(np.shape(tim))
# print (np.shape(vlz))

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








