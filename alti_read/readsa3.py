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


# ------ Directory contains sentinel3A SRAL data
path0 = r"D:\s3a_land"
dir_name = os.listdir(path0)
# print(dir_name)
s3ak = []  # parameter names

#  ---------------------------------------------------------------------------------------------------------------------
# Define input parameters
# define the pass number: 152 Poyang, 260 Poyang(2)
pass_num = 260  # 152,260 for S3A; 317 For S3B
s_model = "LAN"  # define the data mode: `LAN` (land) or `MAR` (marine)
plot_wave = "no"  # Plot wave form. `yes` or `no`
site = "jiujiang"  # choose the site. `jiujiang`| `py_lake`
output_name = "no"  # If output the names of the variables.
# define the latitude boundary
if pass_num == 152:
    lat_min = 29.
    lat_max = 30
    lat_out_min = 29.0833
    lat_out_max = 29.2
    plot_cycle = 60  # choose the cycle to plot
    outfile = "wsl_152.npy"
    file_out = os.path.join('..', 'data', 'wsl_152.npy')
    if os.path.exists(file_out):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(file_out)
        # os.unlink(path)
    else:
        print('no such file:%s' % file_out)  # 则返回文件不存在
elif pass_num == 260:
    if site == "py_lake":
        lat_min = 29
        lat_max = 30.5
        lat_out_min = 29.358
        lat_out_max = 29.3727
        plot_cycle = 60  # choose the cycle to plot
        outfile = "wsl_260.npy"
        file_out2 = os.path.join('..', 'data', 'wsl_260.npy')
        if os.path.exists(file_out2):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(file_out2)
            # os.unlink(path)
    elif site == "jiujiang":
        lat_min = 29
        lat_max = 30.5
        lat_out_min = 29.8301
        lat_out_max = 29.8369
        plot_cycle = 60  # choose the cycle to plot
        outfile = "wsl_260jj.npy"
        file_out2 = os.path.join('..', 'data', 'wsl_260_jj.npy')
        if os.path.exists(file_out2):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(file_out2)
            # os.unlink(path)
elif pass_num == 317:
    lat_min = 28.6
    lat_max = 29.3
    lat_out_min = 29.0
    lat_out_max = 29.0333
    plot_cycle = 40  # choose the cycle to plot
    outfile = "wsl_317.npy"
    file_out2 = os.path.join('..', 'data', 'wsl_317.npy')
    if os.path.exists(file_out2):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(file_out2)
        # os.unlink(path)
    else:
        print('no such file:%s' % file_out2)  # 则返回文件不存在
#  ---------------------------------------------------------------------------------------------------------------------

for file_s3a in dir_name[::-1]:
    # print(np.array(file_s3a[69:72]))
    # print("The baseline is %s"%(file_s3a[92:94]))
    # print(type(file_s3a))
    if int(file_s3a[73:76]) == pass_num and file_s3a[9:12] == s_model and int(file_s3a[92:94]) > 2:
        # ------ Name of the SRAL file. There have three kinds of S3A data which are the enhanced,standard and the reduced data.
        # ------ Here we choose the enhanced data because it contains the waveform data.
        file_path = os.path.join(path0, file_s3a, 'enhanced_measurement.nc')

        print("The Sentinel3A SRAL file is:%s" %(file_path))
        # print('\n')
        # ------ Finish loading file

        # -----------------------#
        # Open nc file using NetCDF tools
        # -----------------------#
        ncs3 = Dataset(file_path)

        # print(ncs3.variables.keys()) #keys 是字典数据类型的元素名称，对应这里就是经纬度时间等参数名字
        # print(ncs3.variables)
        s3ak = ncs3.variables.keys()
        # print(type(s3ak))  # 注意数据类型
        # print(len(s3ak))  # 数据的维度？
        s3ak2 = str(s3ak)
        # print(type(s3ak2))
        # print(len(s3ak2))  #　字符串的长度



        #  read variables
        lat = ncs3.variables['lat_20_ku'][:]  # 20Hz
        lon = ncs3.variables['lon_20_ku'][:]
        tim = ncs3.variables['time_20_ku'][:]
        wav = ncs3.variables['waveform_20_ku'][:]
        r_ku = ncs3.variables['range_ocog_20_ku'][:]

        lat1 = ncs3.variables['lat_01'][:]  # 1Hz
        lon1 = ncs3.variables['lon_01'][:]
        alt = ncs3.variables['alt_20_ku'][:]
        tim1 = ncs3.variables['time_01'][:]
        alt1 = ncs3.variables['alt_01'][:]
        r_ku1 = ncs3.variables['range_ocean_01_ku'][:]
        r_c1 = ncs3.variables['range_ocean_01_c'][:]

        dry = ncs3.variables['mod_dry_tropo_cor_meas_altitude_01'][:]
        wet = ncs3.variables['mod_wet_tropo_cor_meas_altitude_01'][:]
        # wet_m = ncs3.variables['model_wet_tropo_corr'][:]

        ino = ncs3.variables['iono_cor_gim_01_ku'][:]  # iono_cor_alt_01_ku
        ssb = ncs3.variables['sea_state_bias_01_ku'][:]
        sig_ku = ncs3.variables['sig0_ocean_01_ku'][:]
        inv = ncs3.variables['inv_bar_cor_01'][:]
        hff = ncs3.variables['hf_fluct_cor_01'][:]
        ots = ncs3.variables['ocean_tide_sol1_01'][:]
        sot = ncs3.variables['solid_earth_tide_01'][:]
        pot = ncs3.variables['pole_tide_01'][:]
        geo = ncs3.variables['geoid_01'][:]
        ssha = ncs3.variables['ssha_01_ku'][:]

        ssh = alt1-r_ku1-dry-wet-ino-inv-sot-pot

        # ssh = double(alt(i) - r_ku(i)) / 10000 - ...
        # double(dry(i) + wet(i) + ino(i) + ssb(i) + inv(i) + hff(i) + set(i) + pt(i)) / 1E4 - double(ots(i)) / 1E4; % SSH is the
        # stable
        # measurements
        # for geodesy, oceanography..

        # vlz = nc.variables['z'][:]
        #
        # print("data dimention")
        # print(np.shape(lon))
        # print(np.shape(lat))
        # print(np.shape(r_ku))
        # print(np.shape(wav))  # 数据是二维的
        # print(np.shape(lat1))  # 数据是二维的

        # --------------------------
        # 查看数据的类型，注意python和MATLAB的差异
        # print(type(wav)) #查看数据类型
        # print(type(tim))
        # print(wav[1, :]) #注意大括号和小括号的使用。
        # --------------------------

        # --------------------------
        # Plot wavform
        maxd = len(lat)
        interv = 10
        # select area
        lat_select = []

        # define the latitude boundary
        k = 0
        for i in lat:
            k = k+1
            if i > lat_min and i < lat_max:
                # print('location:', i)
                lat_select.append(k)
        myslice = lat_select[0::1]  # This is a slice. [a:b:c] means begin a ,end b, step c.
        k = 0
        lat_select = []
        for i in lat1:
            k = k+1
            if i > lat_min and i < lat_max:
                lat_select.append(k)
        myslice_1hz = np.array(lat_select)[0::1]

        # myslice = slice(29000, maxd, interv)  # Here you can control the interval by 'interv'.
                                          # Then the figures will show different waveforms.
        x = np.arange(1, 129, 1)  # This is the bin index. Is constant number for each satellite.
        y = np.array(wav[myslice, :])
        r = np.array(r_ku[myslice])

        lat2 = np.array(lat[myslice])
        lon2 = np.array(lon[myslice])
        print("The length of 20Hz data is %d" % (len(lon2)))
        # print(len(lon2))

        # Plot waveforms on one figure
        if plot_wave == "yes" and int(file_s3a[69:72]) == plot_cycle:
            for i in range(1, 16):
                plt.plot(x, y[i], 'r')
            # Plot waveforms on sub figures
            figsize = (10, 8)
            gs = gridspec.GridSpec(4, 4)
            # print(type(gs))
            gs.update(hspace=0.4)
            fig1 = plt.figure(num="waveform", figsize=figsize)
            ax = []

            for i in range(16):
                row = (i // 4)
                # print(i, row)
                col = i % 4
                # print(i, col)
                ax.append(fig1.add_subplot(gs[row, col]))
                ax[-1].set_title('lat=%s' % str(round(lat2[i], 4)))
                ax[-1].plot(x, y[i], 'ro', ms=2, ls='-', linewidth=0.5)
            plt.show()
        #
        # ----------------------------------------------------------------------------------------------------------------------
        # latinfo = nc.variables['latitude']

        # vlzinfo = nc.variables['u']
        # print (vlzinfo)

        # ----------------------------------------------------------------------------------------------------------------------
        # Fit 1Hz to 20 Hz
        # The method needs to be improved. Some parameters not interp well.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        z = np.polyfit(lat1[myslice_1hz], wet[myslice_1hz], 1)
        wet_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], dry[myslice_1hz], 1)
        dry_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], sot[myslice_1hz], 1)
        sot_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], pot[myslice_1hz], 1)
        pot_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], inv[myslice_1hz], 1)
        inv_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], ino[myslice_1hz], 1)
        ino_20 = np.polyval(z, lat[myslice])
        z = np.polyfit(lat1[myslice_1hz], geo[myslice_1hz], 1)
        geo_20 = np.polyval(z, lat[myslice])
        ssh_20 = alt[myslice] - r_ku[myslice] - dry_20 - wet_20 - ino_20 - inv_20 - sot_20 - pot_20 - geo_20

        # plt.plot(lat1[myslice_1hz], ino[myslice_1hz], 'o')
        # plt.plot(lat[myslice], ino_20, '+')
        # plt.show()
        # ----------------------------------------------------------------------------------------------------------------------

        # Save data
        file_out = os.path.join('..', 'data', outfile)
        first_line = file_s3a[69:72]+' lat  lon  tim  \n'
        # print(first_line)
        with open(file_out, 'a') as fileobj:
            # fileobj.write(first_line)
            for i in range(len(np.array(lat[myslice]).tolist())):
                if np.array(r_ku[myslice])[i] != 2147483647 and np.array(lat[myslice])[i] > lat_out_min and np.array(lat[myslice])[i] < lat_out_max:

                    fileobj.write(str('%15.5f' % np.array(lat[myslice]).tolist()[i]) + ' ')
                    fileobj.write(str('%15.5f' % np.array(lon[myslice]).tolist()[i]) + ' ')
                    fileobj.write(str('%15.5f' % np.array(tim[myslice]).tolist()[i]) + ' ')
                    # fileobj.write(str('%15.5f' % np.array(alt[myslice]).tolist()[i]) + ' ')
                    fileobj.write(str('%15.5f' % np.array(ssh_20).tolist()[i]) + ' \n ')
                    # fileobj.write(str('%15.5f' % np.array(r_ku[myslice]).tolist()[i]) + '\n ')

        file_out2 = os.path.join('..', 'data', 'wsl_1hz.npy')
        with open(file_out2, 'a') as fileobj:
            fileobj.write(first_line)
            for i in range(len(np.array(lat1[myslice_1hz]).tolist())):
                # print(i)
                fileobj.write(str('%15.5f' % np.array(lon1[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(lat1[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(tim1[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(alt1[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(sig_ku[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(dry[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(wet[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(ino[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(inv[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(sot[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(pot[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(r_ku1[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(geo[myslice_1hz]).tolist()[i]) + ' ')
                fileobj.write(str('%15.5f' % np.array(ssh[myslice_1hz]).tolist()[i]) + '\n ')
        # OR
        # np.savetxt("WSL.npy", (lat2, lon2, r), fmt="%10.5f", delimiter=",")


# Save names of s3a variables
if len(s3ak) != 0 and output_name == "yes":
    fh = open("s3adata.txt", "w")
    for i in s3ak:
        fh.write(str(i)+'\n')
    fh.close()
else:
    print("data are not correct")
