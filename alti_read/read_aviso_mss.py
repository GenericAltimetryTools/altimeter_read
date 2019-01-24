
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
# ------ Directory contains AVISO SLA data
dir_setup = os.path.join(home, 'alti_data', 'avisoMMS')
# 定义变量
msla = []
tims = []
for filename in os.listdir(dir_setup)[1:2]:
    print(filename)
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

    print(tim)
    # print(asla[0, 1:300, 1000])
    # print(lat[100])

    # -----------------------#
    # select data in the south china sea at about 5-20 110-120
    # -----------------------#
    tmp = []
    for i in range(720):
        for j in range(1440):
            if lat[i] > 15 and lat[i] < 20:
                if lon[j]>115 and lon[j]<120:
                    if isinstance(asla[0, i, j], float):
                        tmp2 = asla[0, i, j]
                        tmp.append(tmp2)
    # ii = 0
    # jj = 0
    # for i in lat:
    #
    #     for j in lon:
    #
    #         if isinstance(asla[0, ii, jj], float):
    #             tmp2 = asla[0, ii, jj]
    #             print(ii, jj)
    #             ii = ii+1
    #             jj = jj+1
    #             tmp.append(tmp2)

    print(len(tmp))
    tmp3 = np.mean(tmp)
    msla.append(tmp3)
    tims.append(tim)
    print('\n')
#  绘图，时间序列
plt.plot(tims, msla)
plt.show()



