import serial
import time
i=0
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