import serial
import time

ser= serial.Serial(port="/dev/ttyUSB0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)


rs232_rreq=[1, 3, 0, 1]
rs485_rreq=[2, 3, 0, 1]
            
rs232_wreq=[0, 6, 0, 11, 0, 0]
#rs485_wreq=[2, 6, 0, 1]
RW=270
RS232_rreq = bytes(rs232_rreq)
RS485_rreq = bytes(rs485_rreq)
RS232_wreq = bytes(rs232_wreq)
#RS485_wreq = bytes(rs485_wreq)

while 1:
    ser.write(RS232_wreq)
    time.sleep(.1)
    ser.flushInput()
    time.sleep(1)
    ser.write(RS232_rreq)
    for i in range(3):
        X=ser.read()
        a=int.from_bytes(X, byteorder='big',signed=True)
        print(X,end='')
        print(a)        
    X=ser.read(a)
    rs232_data=int.from_bytes(X,byteorder='big',signed=True)
    print("rs232=",rs232_data)
    #print("rs485:")'''
   # time.sleep(.5)
    '''ser.write(RS485_rreq)
    for i in range(3):
        X=ser.read()
        a=int.from_bytes(X, byteorder='big',signed=True)
        print(X,end='')
        print(a)
       # time.sleep(.5)
    X=0
    X=ser.read(a)
    print(X)
    rs485_data=0
    rs485_data=int.from_bytes(X,byteorder='big',signed=True)
    print("rs485=",rs485_data)
    time.sleep(1)'''
    break 
    