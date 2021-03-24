import tkinter as tk
import serial
import time 
from tkinter import *
from tkinter import messagebox
import os


root = Tk()
root.title ("SPARKDNA")
root.configure(bg="#fbb917")
#root.iconbitmap("C:/Users/user/Downloads/spark-drives-120x120.ico")
root.geometry("500x300")
#bg = PhotoImage(file="C:/Users/user/Desktop/test_2/lines-clipart-circuit.png")
#my_label13 = Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

serial_rs232 = serial.Serial("/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=1 )


rs458=0
lcr=0
lcs=0

 


def myClick(): 
    button=e.get()
    if button=='':
        global myLabel
        myLabel = Label(root, text="please enter the serial no. ",fg="#000000", font="timesnewroman 10 bold italic")
        myLabel.grid(row=14, column=1, columnspan=15)
        root.after(2000, myLabel.destroy) 
    else:
     #while 1:
        
        #send_data="connected.."
        #res = send_data.encode('utf-8')
        #time.sleep(1)
        myLabel2.destroy()        
        e.destroy()
        mymyButton4.destroy()
        myButton2.destroy()        
        my_label8 = Label(root, text="Serial No. of the product           :    ", font="timesnewroman 12 bold italic" ).grid(row=2, column=0, rowspan=2, columnspan=8) 
        my_label8 = Label(root, text="    "+button, font="timesnewroman 12 bold italic", ).grid(row=2, column=9, rowspan=2, columnspan=4) 
        my_label3 = Label(root, text="SPARKDNA TEST CONTROL UNIT \n ", fg="#000000", font="timesnewroman 20 bold italic").grid(row=0, column=1, rowspan=2, columnspan=30)   
        my_label4 = Label(root, text="Checking RS232 port              :",  font="timesnewroman 12 bold italic").grid(row=4, column=1, rowspan=2, columnspan=7)
        
        my_label5 = Label(root, text="Checking RS485 port             :",  font="timesnewroman 12 bold italic").grid(row=6, column=1, columnspan=7, rowspan=2)
        my_label6 = Label(root, text="Checking Loadcell range       :",  font="timesnewroman 12 bold italic").grid(row=8, column=1, columnspan=7, rowspan=2)
        my_label7 = Label(root, text="Checking Loadcell stability   :", font="timesnewroman 12 bold italic").grid(row=10, column=1, columnspan=7, rowspan=2)
        myButton3 = Button(root, text=" FINISH & SAVE ", bg="skyblue",  font="timesnewroman 10 bold italic").grid(row= 12, column=2, columnspan=4, rowspan=2)
        myButton4 = Button(root, text=" NEXT PRODUCT ", bg="skyblue", font="timesnewroman 10 bold italic", ).grid(row= 12, column=9, columnspan=5, rowspan=2)
 
        rs_232_time_to_wait=time.time()+4
        while time.time()<rs_232_time_to_wait:
          rs232 = serial_rs232.read()
          if rs232>b'0':
            my_label9= Label(root, text="Yes", bg="green", font="timesnewroman 12 bold italic" ).grid(row=4, column=8, rowspan=2, columnspan=7)
          else:
            my_label9 = Label(root, text="No", bg="red", font="timesnewroman 12 bold italic").grid(row=4, column=8, rowspan=2, columnspan=7)
          if rs458==1:
            my_label10 = Label(root, text="Yes", bg="green", font="timesnewroman 12 bold italic").grid(row=6, column=8, rowspan=2,columnspan=7)
          else:
            my_label10 = Label(root, text="No", bg="red", font="timesnewroman 12 bold italic").grid(row=6, column=8, columnspan=7, rowspan=2)
          if lcr==1:
            my_label11 = Label(root, text="Yes", bg="green", font="timesnewroman 12 bold italic" ).grid(row=8, column=8, rowspan=2,columnspan=7)
          else:
            my_label11 = Label(root, text="No", bg="red", font="timesnewroman 12 bold italic").grid(row=8, column=8, columnspan=7, rowspan=2)
          if lcs==1:    
            my_label12 = Label(root, text="Yes", bg="green", font="timesnewroman 12 bold italic" ).grid(row=10, column=8, columnspan=7, rowspan=2)
          else:
            my_label12 = Label(root, text="No", bg="red", font="timesnewroman 12 bold italic" ).grid(row=10, column=8, columnspan=7, rowspan=2)
   
          #root.mainloop()
myLabel1 = Label(root, text="SPARKDNA TEST CONTROL UNIT \n ", fg="#000000", font="timesnewroman 20 bold italic").grid(row=0, column=1, rowspan=2, columnspan=15)
myLabel2 = Label(root, text=" ENTER THE SERIAL NO.    :", fg="#000000", font="timesnewroman 12 bold italic")
e = Entry(root, bg="blue", fg="white",  borderwidth=5, font="timesnewroman 12 bold italic")



mymyButton4 = Button(root, text=" START ", command= myClick, bg="palegreen", borderwidth=2, font="timesnewroman 10 bold italic")
myButton2 = Button(root, text="  EXIT  ", bg="pink", borderwidth=2, command=root.quit, font="timesnewroman 10 bold italic") 


myLabel2.grid(row=3, column=1, columnspan=7,  rowspan=2)
e.grid(row=3, column=9, columnspan=7,  rowspan=2) 
mymyButton4.grid(row=10, column=9, rowspan=2, columnspan=7)
myButton2.grid( row=10, column=1, rowspan=2, columnspan=7) 
root.mainloop()
