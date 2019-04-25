#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:25:51 2019

@author: omprakash
"""

import matplotlib.pyplot as plt
import numpy as np


x1,y1 = np.loadtxt("1.csv", delimiter=",", unpack=True)
x2,y2 = np.loadtxt("2.csv", delimiter=",", unpack=True)
x3,y3 = np.loadtxt("3.csv", delimiter=",", unpack=True)
x4,y4 = np.loadtxt("4.csv", delimiter=",", unpack=True)
x5,y5 = np.loadtxt("5.csv", delimiter=",", unpack=True)
x6,y6 = np.loadtxt("6.csv", delimiter=",", unpack=True)
x7,y7 = np.loadtxt("7.csv", delimiter=",", unpack=True)
x8,y8 = np.loadtxt("8.csv", delimiter=",", unpack=True)
x9,y9 = np.loadtxt("9.csv", delimiter=",", unpack=True)

m1,m2 = np.loadtxt("mine.csv", delimiter=",", unpack=True)

plt.plot(m1,m2,'--s', color='red', label='Our model')
plt.plot(x1,y1,'--bv', label='UDG') #UDG
plt.plot(x2,y2,'--^',color='violet',label='LAEE')
plt.plot(x4,y4,'--go',label='DTG')
#plt.plot(x5,y5,'--yd',label='try2')
#plt.plot(x6,y6,'--m*',label='try2')
plt.plot(x7,y7,'--+', color='brown', label='KNN')
plt.plot(x8,y8,'--x', color='orange',label='LEACH + DTG')
plt.plot(x9,y9,'--p',color='pink',label='LEACH + KNN')
plt.xlabel('Ratio of nodes removed from network toplogy')
plt.ylabel('Largest component size')
plt.title('Robustness Comparison')

legend = plt.legend(loc='lower', shadow=True, fontsize='large')
plt.show()






