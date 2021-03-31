import serial
import time

ser= serial.Serial(port="/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)
RW=754
rs232_rreq_RW = [1, 3, 0, 16]
rs232_wreq_RW = [1, 6, 0, 220]
RS232_rreq_RW = bytes(rs232_rreq_RW)
print(RW.to_bytes(2,"little"))
print(bytes(rs232_wreq_RW))
RS232_wreq_RW = bytes(rs232_wreq_RW)+(RW.to_bytes(2,"big"))
print(RS232_wreq_RW )
while 1:
    
    ser.write(RS232_wreq_RW)
    time.sleep(3)
    ser.write(RS232_rreq_RW)
    for i in range(3):
        X=ser.read()
        a=int.from_bytes(X, byteorder='big',signed=True)
        print(X)
    X=ser.read(a)
    print(X)
    data=int.from_bytes(X,byteorder='big',signed=True)
    print("data=",data)
    break
