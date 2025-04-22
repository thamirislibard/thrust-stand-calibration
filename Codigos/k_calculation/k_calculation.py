# -*- coding: utf-8 -*-
"""
Editor Spyder

Este é um arquivo de script temporário.
"""
import csv
import matplotlib.pyplot as plt
import numpy as np

g=9.81
l=0.005 #Distance of hanging mass to pivot
L=0.3 #Vertical distance of nozzle to pivot

M=[]
d=[]
Mteq=[]
Theta=[]
err=[]

filename = open('data.csv', 'r')
file = csv.DictReader(filename)
for row in file :
    M.append(row['M'])
    d.append(row['d'])
    err.append(row['e'])
filename.close()

for i in range(len(M)):
    M[i]=float(M[i])
    d[i]=float(d[i])
    err[i]=float(err[i])
    Mteq.append(M[i]*g*l)
    Theta.append(d[i]/L)
    
k, a = np.polyfit(Theta, Mteq, deg=1)
x=np.linspace(Theta[0],Theta[-1], num=10)

fig, [ax1, ax2] = plt.subplots(1,2)
ax1.plot(d, M, 'x')
ax1.set(xlabel='d [m]', ylabel='M [kg]')



ax2.errorbar(Theta, Mteq, xerr=err, fmt="o", color="r")
ax2.plot(x, a + k * x, '--k', label=f'k={k:.5f} Nm/rad')
ax2.set(xlabel='Theta [rad]', ylabel='Mteq [Nm]')
ax2.legend()
plt.show()

print('k=',k,'Nm/rad')
print('k zero error =',a,'Nm/rad')