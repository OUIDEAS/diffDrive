import sys
import time
import numpy as np


def vPath(t):
#   no path
#     vel=[0;0];
#     return;
#slow moving path
    v = 0.005
    if(t<=5):
        vel = np.array([0,0])

    elif(t<10):
        theta = np.array([0, 1])
        ang = np.arctan2(theta[1], theta[0])
        vel = v * np.array([np.sin(ang), np.cos(ang)])
    elif (t<15):
        theta = np.array([0, -1])
        ang = np.arctan2(theta[1], theta[0])
        vel = v * np.array([np.sin(ang), np.cos(ang)])
    else:
        vel = np.array([0,0])

    return vel


func_pointer = vPath


print(func_pointer(0))
print(func_pointer(1.5))