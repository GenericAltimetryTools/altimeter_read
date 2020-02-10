#!/usr/bin/python
# coding=utf-8

import numpy as np
import numpy.ma as ma
import os
import subprocess
import operator
from functools import reduce
#
#
# subprocess.call(['ls', '-l'])
# subprocess.call(['ls -l'], shell=True)
#
# subprocess.call(["awk '!/2147483647.00000/ && !/32767/ && NR>1 {print $0}' tt.npy >tt2.dat"], shell=True)
#
# #  ===================================
# x = np.array([1,2,3,5,7,4,3,2,8,0])
# mask = x < 5
# mask2 = x < 3
# mx = ma.array(x, mask=mask)
# mxx = ma.array(x, mask=mask2)
#
# print(np.shape(mx))
# print(mx)
#
# print(type(mx))
# mx2 = ma.filled(mx, [-999999])
# print(mx2)
#
#
# with open('test.npy', 'w') as fileobj:
#     fileobj.write('test \n')
#
#     for i in range(len(mx2.tolist())):
#         fileobj.write(str('%.5f' % mx2.tolist()[i])+' ')
#
#
# # file = open('data.txt', 'w')
# # file.write(str(outdata))
# # file.close()
#
#
# #
# # ou = [mx2, mx2]
# # print(ou)
# # print(type(ou))
# # np.savetxt("test2.npy", ou, fmt="%10.5f", delimiter=",")
#
# mx3 = ma.getmaskarray(mx)
# mx4 = ma.nonzero(mx)
# mx5 = ma.getmask(mx)
# mx6 = ma.getdata(mx)
# mx7 = ma.MaskedArray.nonzero(mxx)
#
# # print(type(mx6))
#
# print("ma.getmaskarray", mx3)
# print(mx4)
# # print(mx[mx4])
# print(mx5)
# # print(mx6)
# print(mx7)
#
# a = [2, 3, 4, 5]
# b = [2, 5, 8]
# print(type(a))
#
# # mx4 = list(mx4)
# # mx7 = list(mx7)
# print(type(list(mx4)))
# print(mx4)
#
# tmp = [val for val in mx4 if val in mx7]
# print(tmp)
#
# # print(list(set(mx4).intersection(set(mx7))))


# a = np.array([[1, 2, 3], [4, 6,5], [ 8, 9, 8],[4,9,3]])
#
# print(type(a))
# print(a)
# c=a.reshape((3, 4))
# print(c)

ste = int(1953/16)
print("ste", ste)

