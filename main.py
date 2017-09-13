from python_vicon import PyVicon
import time
import socket



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
            return(x_ENU,y_ENU,heading)


#First connect to the ground robot
client = vicon_connect()

#Connect to diffDrive through UDP
UDP_IP = "192.168.0.195"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))



#Initalize variables for VF and output
output = []

while True:
    #Get current position of vehicle from Vicon Function


    xnow = getPos()
# MESSAGE = (str(x_NED)+','+str(y_NED)+','+str(heading))
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#     if xnow[0] > 2 or xnow[1] > 2:
#         print('geofence breached')
#         break
#
#     params = VectorField.VFData()
#     params.x = xnow[0]
#     params.y = xnow[1]
#     T = time.time() - ts
#
#     dt = (T - params.t)
#     params.t = T
#
#     newVF = cvf.GetVF_at_XY(params)
#     cvf.UpdatePosition(params.t, dt)
#
#     print("Heading:\t" + str(np.rad2deg(xnow[2])) + " \tVF:\t" + str(
#         np.rad2deg(np.arctan2(newVF.F[1], newVF.F[0]))) + " \tX:\t" + str(xnow[0]) + " \tY:\t" + str(
#         xnow[1]) + "\t" + str(cvf.xc))
#
#     d = 1
#     heading = np.arctan2(newVF.F[1], newVF.F[0])
#     x_cmd = d * np.cos(heading)
#     y_cmd = d * np.sin(heading)
#     XCMD = [x_cmd, y_cmd, heading]
#     output = []
#
#     data.update_data(xnow[0], xnow[1], np.rad2deg(xnow[2]), x_cmd, y_cmd, np.rad2deg(heading))
#     continue
#
#     output = posq.step(t, xnow, XCMD, direction, old_beta, vmax, base)
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

