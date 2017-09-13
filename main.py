from python_vicon import PyVicon
import time
import socket
import VectorField
import vfpathtest
import numpy as np
import posq

#Connect to Vicon Machine
def vicon_connect():
    print "Connecting to Vicon..."
    client = PyVicon()
    client.connect("192.168.0.197", 801)

    if not client.isConnected():
        print "Failed to connect to Vicon!"
        return 1
    print "Connected!"
    return(client)


#Get the current position of the differential drive robot and return x,y and heading
def getPos():
    client.frame()
    subjects = client.subjects()
    for s in subjects:
        if (s == 'diffDrive'):
            trans = client.translation(s)
            if (trans[0] == 0.0 and trans[1] == 0.0 and trans[2] == 0.0):
                print('dead packet')
                continue
            rot = client.rotation(s)
            trans_scale = 1000
            x_ENU = trans[0] / trans_scale
            y_ENU = trans[1] / trans_scale
            z_ENU = trans[2] / trans_scale
            x_NED = y_ENU
            y_NED = x_ENU
            z_NED = -z_ENU
            heading = rot[2]

            if heading < 0.0:
                heading += np.pi * 2
            return (x_ENU, y_ENU, heading)


#First connect to the ground robot
client = vicon_connect()
time.sleep(1)

#Connect to diffDrive through UDP
print "Connecting to diffDrive"
UDP_IP = "192.168.0.195"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)

#Initalize variables for VF and output
t = 0
ts = time.time()
xnow = getPos()
xend = [xnow[0]+1,xnow[1]+1,xnow[2]]
direction = 0
old_beta = xnow[2]
vmax = 1
base =  .215
old_beta = []
carrot_d = 1
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
dt = 0.01
VFTarget = [0, 0]
cvf = VectorField.CircleVectorField('Gradient')
# cvf.bUsePathFunc = True
# cvf.velPathFunc = vfpathtest.vPath
cvf.mCircleRadius = 1
cvf.xc = VFTarget[0]
cvf.yc = VFTarget[1]


time.sleep(1)
while True:
    #Get current position of vehicle from Vicon Function
    xnow = getPos()
    if xnow[0] > 2 or xnow[1] > 2:
        print('geofence breached!    :(')
        break

    #Calculate the VF
    params = VectorField.VFData()
    params.x = xnow[0]
    params.y = xnow[1]
    T = time.time() - ts
    dt = (T - params.t)
    params.t = T
    newVF = cvf.GetVF_at_XY(params)
    heading_cmd = np.arctan2(newVF.F[1], newVF.F[0])

    print ("sending messages . . .")

    x_cmd = carrot_d*np.cos(heading_cmd)
    y_cmd = carrot_d*np.sin(heading_cmd)
    XCMD = [x_cmd,y_cmd,heading_cmd]
    output = []

    #Writes data to file (Future update)
    #data.update_data(xnow[0], xnow[1], np.rad2deg(xnow[2]), x_cmd, y_cmd, np.rad2deg(heading))

    output = posq.step(t, xnow, XCMD, direction, old_beta, vmax, base)

    vl = output[0]
    vr = output[1]

    vl = (((vl) * (servoMax - 375) / (1)) + 450)
    vr = (((vr) * (servoMax - 375) / (1)) + 450)


    MESSAGE = str(vl) + "    " + str(vr)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(0.01)

#     # print(output)
#
#     vl = output[0]
#     vr = output[1]
#
#     vl = (((vl) * (servoMax - 375) / (1)) + 450)
#     vr = (((vr) * (servoMax - 375) / (1)) + 450)
#
#     # print(vl,vr)
#
#     # Change speed of continuous servo on channel O
#     pwm.setPWM(0, 0, int(vl))
#     pwm.setPWM(1, 0, int(vr))
#     # time.sleep(.5)
#
#     if abs(xnow[0] - xend[0]) < .02 and abs(xnow[1] - xend[1]) < .02:
#         break
#
# pwm.setPWM(0, 0, 367)
# pwm.setPWM(1, 0, 372)

