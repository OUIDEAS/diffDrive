import sys
import socket

def main(sysargs):

    import sys, os
    from python_vicon import PyVicon
    import time

    print "Connecting to Vicon..."
    client = PyVicon()
    client.connect("192.168.0.197", 801)


    if not client.isConnected():
        print "Failed to connect to Vicon!"
        return 1
    print "Sending Mocap data"
    csvfiles = []
    csvwriters = {}
    time_usec = 0#time.clock() * 1000 * 1000
    trans_scale = 1000

    print("Sending Vision Data")
    itime_usec=100000
    i=0.01
    dt = 0.1
    while True:
        i=i+0.01
        time.sleep(0.01)#0.05, working
        client.frame()
        subjects = client.subjects()
        for s in subjects:
            if(s=='diffDrive'):

                trans = client.translation(s)
                if(trans[0] == 0.0 and trans[1] == 0.0 and trans[2] == 0.0):
                    print('dead packet')
                    continue
                rot = client.rotation(s)

                x_ENU = trans[0]/trans_scale
                y_ENU = trans[1]/trans_scale
                z_ENU = trans[2]/trans_scale
                x_NED = y_ENU
                y_NED = x_ENU
                z_NED = -z_ENU

                heading = rot[2]

                #Sending data to PI
                # MESSAGE = (str(x_NED)+','+str(y_NED)+','+str(heading))
                # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                time.sleep(.05)
        time_usec += 1000

