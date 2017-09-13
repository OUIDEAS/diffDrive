import time
from datetime import datetime
import os

class writedata:
    def __init__(self):
        self.name = time.strftime("%I_%M") +'.txt'
        self.f = open(self.name,'w')
        self.f.write('time')
        self.f.write('\t \t \t')
        self.f.write('x')
        self.f.write('\t \t \t')
        self.f.write('y')
        self.f.write('\t \t \t')
        self.f.write('theta')
        self.f.write('\t \t \t')
        self.f.write('xcmd')
        self.f.write('\t \t \t')
        self.f.write('ycmd')
        self.f.write('\t \t \t')
        self.f.write('thetacmd')
        self.f.write(os.linesep)

    def update_data(self,x,y,t,xc,yc,tc):
        self.f.write(os.linesep)
        self.f.write(str(time.time()))
        self.f.write('\t \t \t')
        self.f.write(str(x))
        self.f.write('\t \t \t')
        self.f.write(str(y))
        self.f.write('\t \t \t')
        self.f.write(str(t))
        self.f.write('\t \t \t')
        self.f.write(str(xc))
        self.f.write('\t \t \t')
        self.f.write(str(yc))
        self.f.write('\t \t \t')
        self.f.write(str(tc))
