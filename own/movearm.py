import serial
import time
import serial.tools.list_ports


def sysprint(a):
    print('\033[92m' + "SYS: " +'\033[0m' + str(a))
    

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
        print(nice)
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
time.sleep(0.001)



def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# motor index (0-5), motor angle
def moveMotor(index, pos):
    # ! WARNING: NO SAFETY!
    pad_rot = str(pos).rjust(3, "0")
    sysprint(pad_rot)
    command = "m" + str(index) + pad_rot + "\r\n"
    bytes = str.encode(command)
    ser.write(bytes)
    time.sleep(0.001)

def armToCM(cmx):

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



    moveMotor(1, a)
    moveMotor(2, b)
    moveMotor(3, b) 
    # if motor 4 would be at a different place it would be set to a

    ser.write(b"u\r\n")
    time.sleep(0.001)



# armToCM(14.5)

# time.sleep(10)

armToCM(43.5)

moveMotor(0, 90)
moveMotor(5, 90)


ser.write(b"u\r\n")
time.sleep(0.001)

time.sleep(3)

# time.sleep(3)
# read_val = ser.read(size=64)

# for modem in PortList:
#     for port in modem:
#         try:
#             ser = serial.Serial(port, 9600, timeout=1)
#             ser.close()
#             ser.open()
#             ser.write("ati")
#             time.sleep(3)
#             read_val = ser.read(size=64)
#             print read_val
#             if read_val != '':
#                 print port
#         except serial.SerialException:
#             continue
#         i+=1