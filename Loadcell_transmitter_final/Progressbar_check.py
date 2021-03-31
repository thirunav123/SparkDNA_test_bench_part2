import time
RS232_check_time =5
count=0
RS232_CT=time.time()+RS232_check_time
def rs232_progress_bar_count():
        
        
        #while time.time() <= RS232_CT+0.05:
        count = int((RS232_check_time-(RS232_CT-time.time()))*100//RS232_check_time)
            #time.sleep(.005)
        print(count)
        return count
while 1:
  print(rs232_progress_bar_count())