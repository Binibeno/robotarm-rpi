import serial
import serial.tools.list_ports
import time
from staticvar import *
import math

def descartesToPolar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)  # radius
    theta = (-math.atan2(y, x) * 180 / math.pi) + 90  # angle in degrees, adjusted by +90 degrees

    if theta < 0:
        theta += 360  # adjust negative angles to the range of 0 to 360

    return [r, theta]

def updateMotor(ser):
    ser.write(b"u\r\n")


def sysprint(a):
    print('\033[92m' + "SYS: " +'\033[0m' + str(a))

def moveMotor(ser, index, pos):
    # ! WARNING: NO SAFETY!
    pad_rot = str(pos).rjust(3, "0")
    # sysprint(pad_rot)
    command = "m" + str(index) + pad_rot + "\r\n"
    bytes = str.encode(command)
    ser.write(bytes)
    time.sleep(0.001)


def init_serial():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    sysprint(ports)
    
    
    
    if (ports.__len__() == 0):
        sysprint("No ports available")
        exit()
    
    port = ports[0]
    
    #  countiously read port and print data
    ser = serial.Serial(port, 9600, timeout=1)
    ser.close()
    ser.open()
    time.sleep(0.001)

    ser.write(b"check\r\n")
    time.sleep(0.001)
    while True:
        # read_val = ser.read(size=64)
        # if (read_val != '' )and (read_val != b''):
        #     read_val = read_val.decode('utf-8')
        #     print(read_val)
        # time.sleep(0.1)
    
        #  read serial line by line
        line = ser.readline()
        if (line != '' )and (line != b''):
            nice = line.decode('utf-8')
            print('\033[92m' + "COM: " +'\033[0m' + nice)
            if (line == b'READY\r\n'):
                sysprint("Arm Ready. Start sending commands.")
                break
            
            
            
    ser.write(b"m1090\r\n")
    time.sleep(0.001)
    
    ser.write(b"m2040\r\n")
    time.sleep(0.001)
    
    ser.write(b"m0100\r\n")
    time.sleep(0.001)
    
    ser.write(b"u\r\n")
    return ser



def armToCM(ser, cmx):

    radius = cmx

    radiusMin = 14.5; #14,5 cm
    radiusMax = 43.5; #43,5 cm
    aMin = 90; # if a=90-70=20 then b=90+70=160 
    aMax = 20; # m1 fully extended

    # m2
    bMin = 0; #   fully retracted
    bMax = 70; # fully extended
    # m3
    cMin = 0; #   fully retracted
    cMax = 70; # fully extended


    b = map_range(radius, radiusMin, radiusMax, bMin, bMax);
    def calcAfromB(b):
        return 90 - b; 

    a = calcAfromB(b);



    moveMotor(ser, 2, b)
    moveMotor(ser, 1, a)
    moveMotor(ser, 3, b) 
    # if motor 4 would be at a different place it would be set to a

    ser.write(b"u\r\n")
    time.sleep(0.001)
