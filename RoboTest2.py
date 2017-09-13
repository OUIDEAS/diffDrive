#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import time
import posq
import numpy as np
import socket
import VectorField
import sys
import writedata
import vfpathtest


def getPos():
 #Rec UDP DATA
  data, addr = sock.recvfrom(128) # buffer size is 1024 bytes
  # print "received message:", data
  output = data.split(",")
  x = float(output[0])
  y = -float(output[1])
  heading = float(output[2])

  if heading < 0.0:
        heading += np.pi*2
  return [x, y, heading]

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# dt = 0.01
# VFTarget = [0, 0]
# cvf = VectorField.CircleVectorField('Gradient')
# cvf.mCircleRadius = 20
# cvf.xc = VFTarget[0]
# cvf.yc = VFTarget[1]
#
# #uav = VFUAV(dt)
# #vf = cvf.GetVF_XYUV(0, dt, uav, IncludeUAVPos=True)
# params = VectorField.VFData()
# params.x = 0
# params.y = 1
# params.t = 0
# newVF = cvf.GetVF_at_XY(params)
# print(np.rad2deg(np.arctan2(newVF.F[1],newVF.F[0])))
#print(vf['xc'], vf['yc'])
#print(vf['u'], vf['v'])
#Q = plt.quiver(Xd, Yd, Ud, Vd, units='width')
#sys.exit(1)

UDP_IP = "192.168.0.195"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

pwm = PWM(0x6F)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

t = 0
xnow = getPos()
xend = [xnow[0]+1,xnow[1]+1,xnow[2]]
direction = 0
old_beta = xnow[2]
vmax = 1
base =  .215
old_beta = []

dt = 0.01
VFTarget = [0, 0]
cvf = VectorField.CircleVectorField('Gradient')
cvf.bUsePathFunc = True
cvf.velPathFunc = vfpathtest.vPath
cvf.mCircleRadius = 1
cvf.xc = VFTarget[0]
cvf.yc = VFTarget[1]
data = writedata.writedata()

ts = time.time()
#uav = VFUAV(dt)
#vf = cvf.GetVF_XYUV(0, dt, uav, IncludeUAVPos=True)

while True:
    xnow = getPos()

    if xnow[0] >2 or xnow[1]>2:
        print('geofence breached')
        break


    params = VectorField.VFData()
    params.x = xnow[0]
    params.y = xnow[1]
    T = time.time()-ts

    dt = (T-params.t)
    params.t = T

    newVF = cvf.GetVF_at_XY(params)
    cvf.UpdatePosition(params.t,dt)




    print("Heading:\t" + str(np.rad2deg(xnow[2])) + " \tVF:\t"+str(np.rad2deg(np.arctan2(newVF.F[1], newVF.F[0]))) + " \tX:\t"+str(xnow[0]) + " \tY:\t"+str(xnow[1]) + "\t" + str(cvf.xc))



    d = 1
    heading = np.arctan2(newVF.F[1], newVF.F[0])
    x_cmd = d*np.cos(heading)
    y_cmd = d*np.sin(heading)
    XCMD = [x_cmd,y_cmd,heading]
    output = []

    data.update_data(xnow[0], xnow[1], np.rad2deg(xnow[2]), x_cmd, y_cmd, np.rad2deg(heading))
    continue

    output = posq.step(t, xnow, XCMD, direction, old_beta, vmax, base)
    #print(output)

    vl = output[0]
    vr = output[1]

    vl = (((vl)*(servoMax-375)/(1))+450)
    vr = (((vr)*(servoMax-375)/(1))+450)

    #print(vl,vr)

    # Change speed of continuous servo on channel O
    pwm.setPWM(0, 0, int(vl))
    pwm.setPWM(1, 0, int(vr))
    #time.sleep(.5)

    if abs(xnow[0]-xend[0])<.02 and abs(xnow[1]-xend[1])<.02:
        break


pwm.setPWM(0, 0, 367)
pwm.setPWM(1, 0, 372)