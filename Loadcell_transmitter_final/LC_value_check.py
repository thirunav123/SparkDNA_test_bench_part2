import serial
import time

ser= serial.Serial(port="/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)
x=100

rs232_rreq_AW=[1, 3, 0, 0]
rs232_rreq_LCC=[1, 3, 0, 1]
rs232_rreq_RW=[1, 3, 0, 16]
rs232_wreq_tare=[1, 6, 0, 25, 0, 1]
rs232_wreq_RW=[1, 6, 0, 16, 0, x]

RS232_rreq_AW = bytes(rs232_rreq_AW)
RS232_rreq_LCC = bytes(rs232_rreq_LCC)
RS232_rreq_RW = bytes(rs232_rreq_RW)
RS232_wreq_tare = bytes(rs232_wreq_tare)
RS232_wreq_RW = bytes(rs232_wreq_RW)
print(RS232_rreq_RW)

while 1:
    
    ser.write(RS232_wreq_tare)
    time.sleep(3)
    ser.write(RS232_wreq_RW)
    print("Place")
    time.sleep(3)
    ser.write(RS232_rreq_AW)
    for i in range(3):
        X=ser.read()
        a=int.from_bytes(X, byteorder='big',signed=True)
        print(X)
    X=ser.read(a)
    print(X)
    data=int.from_bytes(X,byteorder='big',signed=True)
    print("AW=",data)
    break 
    