import serial
import time

ser= serial.Serial(port="/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)


rs232_rreq_DOP1=[1, 3, 1, 14]
rs232_rreq_DOP2=[1, 3, 1, 15]
rs232_rreq_DOP3=[1, 3, 1, 16]
rs232_rreq_DOP4=[1, 3, 1, 17]
rs232_rreq_DIP1=[1, 3, 0, 250]
rs232_rreq_DIP2=[1, 3, 0, 251]
rs232_rreq_DIP3=[1, 3, 0, 252]

            
rs232_wreq_DOP1_H=[1, 6, 1, 14, 0, 0]
rs232_wreq_DOP2_H=[1, 6, 1, 15, 0, 0]
rs232_wreq_DOP3_H=[1, 6, 1, 16, 0, 0]
rs232_wreq_DOP4_H=[1, 6, 1, 17, 0, 0]
rs232_wreq_DOP1_L=[1, 6, 1, 14, 0, 1]
rs232_wreq_DOP2_L=[1, 6, 1, 15, 0, 1]
rs232_wreq_DOP3_L=[1, 6, 1, 16, 0, 1]
rs232_wreq_DOP4_L=[1, 6, 1, 17, 0, 1]

RS232_rreq_DOP1= bytes(rs232_rreq_DOP1)
RS232_rreq_DOP2= bytes(rs232_rreq_DOP2)
RS232_rreq_DOP3= bytes(rs232_rreq_DOP3)
RS232_rreq_DIP1= bytes(rs232_rreq_DIP1)
RS232_rreq_DIP2= bytes(rs232_rreq_DIP2)
RS232_rreq_DIP3= bytes(rs232_rreq_DIP3)
RS232_wreq_DOP1_H= bytes(rs232_wreq_DOP1_H)
RS232_wreq_DOP2_H= bytes(rs232_wreq_DOP2_H)
RS232_wreq_DOP3_H= bytes(rs232_wreq_DOP3_H)
RS232_wreq_DOP4_H= bytes(rs232_wreq_DOP4_H)
RS232_wreq_DOP1_L= bytes(rs232_wreq_DOP1_L)
RS232_wreq_DOP2_L= bytes(rs232_wreq_DOP2_L)
RS232_wreq_DOP3_L= bytes(rs232_wreq_DOP3_L)
RS232_wreq_DOP4_L= bytes(rs232_wreq_DOP4_L)





while 1:
    ser.write(RS232_wreq_DOP4_L)
    time.sleep(.5)
    ser.write(RS232_rreq_DIP2)
    for i in range(3):
        X=ser.read()
        a=int.from_bytes(X, byteorder='big',signed=True)
        print(X,end='')
        print(a)        
    X=ser.read(a)
    rs232_data=int.from_bytes(X,byteorder='big',signed=True)
    print("rs232=",rs232_data)
    #print("rs485:")
    '''ser.write(RS485_wreq)
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
    print("rs485=",rs485_data)'''
    time.sleep(1)
    break 
   