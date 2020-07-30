
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import netCDF4 as ncf
# import pandas as pd
import sys
import pickle

# ---------------Introduction-----------------------------
# This is a simple program to read and process the AVISO monthly MSS data.
# First, you should download some data from AVISO FTP site. Then run this program and get the similar result.
# leiyang@fio.org.cn
# 2020-07
# --------------------------------------------------------


# Get the user home directory
from os.path import expanduser
import os
home = expanduser("~")

# set directory containing AVISO SLA data. You should change this to your data location.
dir_setup = os.path.join(home, 'alti_data', 'avisoMMS')
# define variables
msla = []
tims = []

filelist = sorted(os.listdir(dir_setup))  # sort the file name list


for filename in filelist[1:]:  # Try to select a small set of data and test it (like one year [1:12]). Otherwise, it will be slow to run all the data.
    # print(filename)
    # ------ Here we choose the enhanced data because it contains the waveform data.
    file_path = os.path.join(dir_setup, filename)
    print("The Aviso  MSS grid file is:")
    print(file_path)


    # -----------------------#
    # Open nc file using NetCDF tools
    # -----------------------#
    ncs3 = Dataset(file_path)

#    print(ncs3.variables.keys())  # keys 是字典数据类型的元素名称，对应这里就是经纬度时间等参数名字

    lat = ncs3.variables['lat'][:]
    lon = ncs3.variables['lon'][:]
    tim = ncs3.variables['time'][:]
    asla = ncs3.variables['sla'][:]  # 注意asla表示海面高度异常，是一个三维数组。时间、经、纬度

    # print("data dimention")
    # print(np.shape(lon))
    # print(np.shape(lat))
    # print(np.shape(tim))
    # print(np.shape(asla))  # 数据是二维的

    print('time is:', tim)
    # print(asla[0, 1:300, 1000])
    # print(lat[100])


    # -----------------------#
    # select data in the south china sea at about 5-20 110-120
    # Here we can change the selection from 'if' to 'slice' later to get faster. Need to fix.
    # -----------------------#
    tmp = []
    for i in range(720):  # 720 this is the resolution along latitude and 1440 is longitude.
        for j in range(1440):
            if lat[i] > 15 and lat[i] < 20:
                if lon[j]>115 and lon[j]<120:
                    if isinstance(asla[0, i, j], float):
                        tmp2 = asla[0, i, j]
                        tmp.append(tmp2)

    # print(len(tmp))
    tmp3 = np.mean(tmp)
    msla.append(tmp3)
    tims.append(tim)
    print('\n')

#  plot the time series of sea surface level over south china sea

plt.plot(tims, msla)
plt.show()



