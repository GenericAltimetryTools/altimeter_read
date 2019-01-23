#!/usr/bin/python
# coding=utf-8

from netCDF4 import Dataset
import numpy as np
import sys

file_path = "/home/yl/Documents/python3_stu/netCDF4/data/deal_nc.nc"
print (file_path)
nc = Dataset(file_path)
print (nc.variables.keys())

lat = nc.variables['latitude'][:]
lon = nc.variables['longitude'][:]
tim = nc.variables['time'][:]
vlz = nc.variables['z'][:]

print (np.shape(lon))
print (np.shape(lat))
print (np.shape(tim))
print (np.shape(vlz))
# print lat
# latinfo = nc.variables['latitude']
vlzinfo = nc.variables['u']
print (vlzinfo)
#np.savetxt("tt.npy", (lon.data), fmt="%10.5f", delimiter=",")

