import socket

#Simple UDP to recieve and print out data on the pi

UDP_IP = "192.168.0.195"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(128)  # buffer size is 1024 bytes
    # print "received message:", data
    output = data.split(",")
    x = float(output[0])
    y = -float(output[1])
    heading = float(output[2])
    print ("X:" + "\t\t" + str(x) + "Y:" + "\t\t" + str(y)+ "Heading:" + "\t\t" + str(heading))