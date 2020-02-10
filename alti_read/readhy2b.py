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
from os.path import expanduser
import os
import subprocess
import operator
from functools import reduce


#  -- Get the user home directory

home = expanduser("~")
# ------ Directory contains sentinel3A SRAL data
dir_setup = os.path.join(home, '/home/yl/Documents/download/testdata/H2B_OPER_SDR_2PT_0018_0181_20190701T084456_20190701T093033')
# ------ Name of the SRAL file. There have three kinds of S3A data which are the enhanced,standard and the reduced data.
# ------ Here we choose the enhanced data because it contains the waveform data.
file_path = os.path.join(dir_setup, 'H2B_OPER_SDR_2PT_0018_0181_20190701T084456_20190701T093033.nc')
print("The HY2B ALt file is:")
print(file_path)
print('\n')

# -----------------------#
# Open nc file using NetCDF tools
# -----------------------#
ncs3 = Dataset(file_path)

print(ncs3.variables.keys()) #keys 是字典数据类型的元素名称，对应这里就是经纬度时间等参数名字
# print(ncs3.variables)
s3ak = ncs3.variables.keys()
print(type(s3ak))  # 注意数据类型
print(len(s3ak))  # 数据的维度？
s3ak2 = str(s3ak)
print(type(s3ak2))
print(len(s3ak2))  # 字符串的长度

# save variable names
fh = open("hy2b_sdr.txt", "w")
for i in s3ak:
    fh.write(str(i)+'\n')
fh.close()

# -----------------------#
# 测高数据的赋值
# -----------------------#
lat = ncs3.variables['lat_20hz'][:]
lon = ncs3.variables['lon_20hz'][:]
tim = ncs3.variables['time_20hz'][:]
alt = ncs3.variables['alt_20hz'][:]
r_ku = ncs3.variables['range_20hz_ku'][:]

lat1 = ncs3.variables['lat'][:]
lon1 = ncs3.variables['lon'][:]
tim1 = ncs3.variables['time'][:]
alt1 = ncs3.variables['alt'][:]
r_ku1 = ncs3.variables['range_ku'][:]
r_c1 = ncs3.variables['range_c'][:]

dry = ncs3.variables['model_dry_tropo_corr'][:]
wet = ncs3.variables['rad_wet_tropo_corr'][:]
wet_m = ncs3.variables['model_wet_tropo_corr'][:]

ino = ncs3.variables['iono_corr_alt_ku'][:]
ssb = ncs3.variables['sea_state_bias_ku'][:]
sig_ku = ncs3.variables['sig0_ku'][:]
inv = ncs3.variables['inv_bar_corr'][:]
hff = ncs3.variables['hf_fluctuations_corr'][:]
ots = ncs3.variables['ocean_tide_sol1'][:]
sot = ncs3.variables['solid_earth_tide'][:]
pot = ncs3.variables['pole_tide'][:]


wav = ncs3.variables['waveforms_20hz_ku'][:]

# vlz = nc.variables['z'][:]
#
print("data dimention")
print(np.shape(lon1))  # 数据是二维的,(1953, 20),20 means 20hz
print(np.shape(lat1))
print(np.shape(tim))
print(np.shape(alt))
print(np.shape(wav))  # 数据是二维的,(1953, 2560) 2560=128*20

# print(wav[1, 0:128])

# --------------------------
# 查看数据的类型，注意python和MATLAB的差异
print(type(wav))  #查看数据类型
print(type(tim))
print(type(lat1))
print(r_ku1)
# print(wav[1, :])  #注意大括号和小括号的使用。
# --------------------------

# --------------------------
# Plot wavform

num = len(lon1)  # define the length and step, used in for loop, num=1953
print("num", num)
ste = -int(num/16)
print("ste", ste)

myslice = slice(num-1, 0, ste)  # 采用切片的形式，均分整个数据集
x = np.arange(1, 129, 1)
y = np.array(wav[myslice, :])

lat2 = np.array(lat[myslice])


# print(y[1, 0:128])  # 需要了解数据的结构，HY-2B的数据格式和Sentinel 3A B 不一样，20Hz的数据做成了二维数组。波形则是【num，20*128】

# Plot waveforms on one figure
# for i in range(1, 10):
#     plt.plot(x, y[i, 0:128], 'r')
# plt.show()

# Plot waveforms on sub figures
figsize = (10, 8)
gs = gridspec.GridSpec(4, 4)
# print(type(gs))
gs.update(hspace=0.4)
fig1 = plt.figure(num=2, figsize=figsize)
ax = []

for i in range(16):
    row = (i // 4)
#    print(i, row)
    col = i % 4
#    print(i, col)
    ax.append(fig1.add_subplot(gs[row, col]))
    ax[-1].set_title('lat=%s' % str(round(lat2[i, 0], 4)))
    # 2B的数据格式使然,[i, 0]表示第i个点（按照1hz的统计点数）里面的第一个波形（共有20个波形）
    ax[-1].plot(x, y[i, 0:128], 'ro', ms=2, ls='-', linewidth=0.5)
    # y表示波形，x表示横坐标轴，128个数据
# plt.show()

#  ===================================

# plot the waveform over selected area
# First reshape the two-D array to one-D, the same with the Sentinel-3A B

lat = np.ma.getdata(lat).reshape((num*20,))
lon = np.ma.getdata(lon).reshape((num*20,))
tim = np.ma.getdata(tim).reshape((num*20,))
alt = np.ma.getdata(alt).reshape((num*20,))
r_ku = np.ma.getdata(r_ku).reshape((num*20,))
wav = np.ma.getdata(wav).reshape((num*20, 128))

print("=================test for and if")
num = 0  # count the number of the waveforms over the selected area
sel = []  # save the index of selected area
for i in range(len(lat.tolist())):
    # print(i)
    if lat[i] > 37.3 and lat[i] < 37.6:
        # print(lat[i], wav[i, :])
        num = num + 1
        sel.append(i)
print(num)
print(len(sel))


myslice = slice(sel[num-1], 0, -10)  # 采用切片的形式，均分整个数据集
x = np.arange(1, 129, 1)
y = np.array(wav[myslice, :])
lat2 = np.array(lat[myslice])
lon2 = np.array(lon[myslice])
print(lon2, lat2)

with open('cst.npy', 'w') as fileobj:  # save points over the CST
    fileobj.write('lon  lat    \n')

    for i in range(len(lat2.tolist())):
        fileobj.write(str('%15.5f' % lon2.tolist()[i])+' ')
        fileobj.write(str('%15.5f' % lat2.tolist()[i]) + ' \n ')

subprocess.call(["awk '!/2147483647.00000/ && NR>1 {print $0}' cst.npy > cst2.npy"], shell=True)

# Plot waveforms on sub figures
figsize = (10, 8)
gs = gridspec.GridSpec(4, 4)
# print(type(gs))
gs.update(hspace=0.4)
fig1 = plt.figure(num=3, figsize=figsize)
ax = []

num = 0  # count the number of the waveforms over the selected area
sel = []  # save the index of selected area
with open('cst3.npy', 'w') as fileobj:  # save points over the CST
    fileobj.write('lon  lat    \n')

    for i in range(16):
        row = (i // 4)
    #    print(i, row)
        col = i % 4
    #    print(i, col)
        ax.append(fig1.add_subplot(gs[row, col]))
        ax[-1].set_title('lat=%s' % str(round(lat2[i], 4)))
        # 2B的数据格式使然,[i, 0]表示第i个点（按照1hz的统计点数）里面的第一个波形（共有20个波形）
        ax[-1].plot(x, y[i, 0:128], 'ro', ms=2, ls='-', linewidth=0.5)
        # y表示波形，x表示横坐标轴，128个数据
        num = num + 1
        sel.append(i)
        fileobj.write(str('%15.5f' % lon2.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % lat2.tolist()[i]) + ' \n ')

    plt.show()

subprocess.call(["awk '!/2147483647.00000/ && NR>1 {print $0}' cst3.npy > cst4.npy"], shell=True)
print(num)
print(sel)

print("=================test for and if")

#  ===================================
#  ===================================
#  write 1hz data to file

#  fill masked data with other data, such as -999999
# r_ku1 = np.ma.filled(r_ku1, [-999999])
# ino = np.ma.filled(ino, [-999999])
# ots = np.ma.filled(ots, [-999999])
# hff = np.ma.filled(hff, [-999999])
# ssb = np.ma.filled(ssb, [-999999])
# sig_ku = np.ma.filled(sig_ku, [-999999])

#  the masked value  is 2147483647

r_ku1 = np.ma.getdata(r_ku1)
ino = np.ma.getdata(ino)
ots = np.ma.getdata(ots)
hff = np.ma.getdata(hff)
ssb = np.ma.getdata(ssb)
sig_ku = np.ma.getdata(sig_ku)

print(type(r_ku1))

#  save data including the masked data, which is set to -999999
with open('tt.npy', 'w') as fileobj:
    fileobj.write('lat  lon  tim  \n')

    for i in range(len(lat1.tolist())):
        fileobj.write(str('%15.5f' % lat1.tolist()[i])+' ')
        fileobj.write(str('%15.5f' % lon1.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % tim1.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % alt1.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % r_ku1.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % wet_m.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % dry.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % ino.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % ots.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % pot.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % inv.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % hff.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % ssb.tolist()[i]) + ' ')
        fileobj.write(str('%15.5f' % sig_ku.tolist()[i]) + '\n ')

#  ===================================
#  save data excluding the masked data
print("===================== test mask")
subprocess.call(["awk '!/2147483647.00000/ && $8!=32767 && $13!=32767 && NR>1{print $0}' tt.npy >tt2.dat"], shell=True)
subprocess.call(["awk '{print $2,$1,$4-$5-($6+$7+$8+$9+$10+$11+$13)}' tt2.dat  >result.dat"], shell=True)
subprocess.call(["sed -i '$d' result.dat"], shell=True)

#  调用系统命令awk提取有效数据
#  the bad value of 32767 is still exist.
#  the hff data are not valid
#  ===================================

#  ===================================

# print(np.shape(lat))

#  write 20hz data to file

# with open('tt20.npy', 'w') as fileobj:
#     fileobj.write('lat20  lon20  tim20  \n')
#
#     for i in range(len(lat.tolist())):
#         fileobj.write(str('%15.5f' % lat.tolist()[i])+' \n ')
#         fileobj.write(str('%15.5f' % lon.tolist()[i]) + ' ')
#         fileobj.write(str('%15.5f' % tim.tolist()[i]) + ' ')
#         fileobj.write(str('%15.5f' % alt.tolist()[i]) + ' ')
#         fileobj.write(str('%15.5f' % r_ku.tolist()[i]) + ' ')


#  ===================================
# 1\编写目录和文件循环,数据批量处理.

# 2\波形分类，机器学习。极地的应用。
# 研究波形的各种参数，提出一种计算方法。可以分离海冰、海水。
# 可以计算出海冰高度。海冰的密集度。

# 3\改写定标程序
# 4\开源程序

