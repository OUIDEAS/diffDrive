#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import socket
import time

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)



pwm = PWM(0x6F)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
UDP_IP = "192.168.0.195"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

ts = time.time()
tnow = ts
T = 10

while True:
    data, addr = sock.recvfrom(128)  # buffer size is 1024 bytes
    # print "received message:", data
    output = data.split(",")
    vl = output[0]
    vr = output[1]

    # Change speed of continuous servo on channel O
    pwm.setPWM(0, 0, int(vl))
    pwm.setPWM(1, 0, int(vr))

    tnow = time.time()

    if tnow > ts+T:
       break


pwm.setPWM(0, 0, 367)
pwm.setPWM(1, 0, 372)