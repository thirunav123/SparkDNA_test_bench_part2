import serial
import time



serial_rs232 = serial.Serial("/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=1)
count = 0
while 1:
   rs_232_time_to_wait=time.time()+2
   X = serial_rs232.read()
   while time.time()<rs_232_time_to_wait:
     X = serial_rs232.read()
     if X>b'0':
        break
 
   #count+=1
   #print(count),#end=' ')
   print(X)
   send_data="1"
   res = send_data.encode('utf-8')
  # print(bytes(res))
   serial_rs232.write(res)
   #serial_rs232.flush()  # send_byte= ''.jo(ord(i), 'b') for i in send_data)
   #print(send_byte)
   #time.sleep(1)
  # print(X)

