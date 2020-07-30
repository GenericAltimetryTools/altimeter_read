from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

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
files = sorted(os.listdir(dir_setup))  # sort the file name list


# define function
def read_aviso_mss(filelist, lon_min, lon_max, lat_min, lat_max):
    msla = []
    tims = []

    for filename in filelist[0:]:  # Try to select a small set of data and test it (like one year [0:12]).
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
        # print('time is:', tim)
        # print(asla[0, 0:10, 0:10])
        # print(lat[0:10])

        # -----------------------#
        # select data in the south china sea at about 5-20 110-120. You can change the boundary as you need.
        # Here we can change the selection from 'if' to 'slice' later to get faster. Need to fix.
        # The resolution is 15 minute at latitude and longitude direction.
        lat_min_ind = (lat_min + 90) * 4
        lat_max_ind = (lat_max + 90) * 4
        lon_min_ind = lon_min * 4
        lon_max_ind = lon_max * 4
        tmp = asla[0, lat_min_ind:lat_max_ind, lon_min_ind:lon_max_ind]

        # print(tmp)
        # -----------------------#
        # This is a original method to select data. low speed.

        # tmp = []
        # for i in range(720):  # 720 this is the resolution along latitude and 1440 is longitude.
        #     for j in range(1440):
        #         if lat[i] > 15 and lat[i] < 20:
        #             if lon[j]>115 and lon[j]<120:
        #                 if isinstance(asla[0, i, j], float):
        #                     tmp2 = asla[0, i, j]
        #                     tmp.append(tmp2)
        # -----------------------#

        # print(len(tmp))
        tmp3 = np.mean(tmp)
        msla.append(tmp3)
        tims.append(tim)
        print('\n')
    # #  plot the time series of sea surface level over south china sea
    # plt.plot(tims, msla)
    # plt.show()
    return [tims, msla]


# call function

lat_min = 0  # set the extent
lat_max = 20
lon_min = 110
lon_max = 120
# call read_aviso_mss
out = read_aviso_mss(files, lon_min, lon_max, lat_min, lat_max)  # the out format is 'list'
# print(out[0])

#  plot the time series of sea surface level over south china sea
plt.plot(out[0], out[1])
plt.show()

