from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer,QBasicTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMessageBox,QWidget,QApplication,QProgressBar,QPushButton,QDialog)
from PyQt5.QtGui import QIcon
import time
import serial
import sys
import csv

ser= serial.Serial(port="/dev/ttyUSB0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)

RS232_check_time=5 #maximum waitning time for RS232 1count=1s
RS485_check_time=5 #maximum waitning time for RS485 1count=1s
LC_range_min=3000 #Lower limit for Loadcell range
LC_range_max=4000 #Upper limit for Loadcell range
stability_check_time=10 #Timing limit for checking stability
Tolenrance=5 #Loadcell count tolenrance for stability check
RW=754  #Reference weight in grams
DIP_check_time=1 #Timing limit of on state for DIP check(Delay time to turn of relay)




rs232_rreq_AW = [ 1, 3, 0, 0]
rs232_rreq_LCC = [ 1, 3, 0, 1]
rs232_rreq_RW = [ 1, 3, 0, 16]
rs232_rreq_DIP=[ 1, 3, 0, 14]


tcu_wreq_power_on_dut = [ 0, 6, 0, 14, 0, 1]
tcu_wreq_power_off_dut = [ 0, 6, 0, 14, 0, 0]
tcu_dop1_on = [ 0, 6, 0, 13, 0, 1]
tcu_dop1_off = [ 0, 6, 0, 13, 0, 0]
rs232_wreq_tare = [ 1, 6, 0, 14, 0, 1]
rs232_wreq_RW = [ 1, 6, 0, 16]
rs232_wreq_calibration = [ 1, 6, 0, 15, 0, 1]

RS232_rreq_AW = bytes(rs232_rreq_AW)
RS232_rreq_LCC = bytes(rs232_rreq_LCC)
RS232_rreq_RW = bytes(rs232_rreq_RW)
RS232_rreq_DIP= bytes(rs232_rreq_DIP)
RS232_wreq_tare = bytes(rs232_wreq_tare)
RS232_wreq_RW = bytes(rs232_wreq_RW)+(RW.to_bytes(2,"big"))
RS232_wreq_calibration = bytes(rs232_wreq_calibration)

rs485_rreq_AW = [ 2, 3, 0, 0]
rs485_rreq_LCC = [ 2, 3, 0, 1]
rs485_rreq_RW = [ 2, 3, 0, 16]
rs485_rreq_DIP=[ 2, 3, 0, 14]


rs485_wreq_tare = [ 2, 6, 0, 14, 0, 1]
rs485_wreq_RW = [ 2, 6, 0, 16]
rs485_wreq_calibration = [ 2, 6, 0, 15, 0, 1]

RS485_rreq_AW = bytes(rs485_rreq_AW)
RS485_rreq_LCC = bytes(rs485_rreq_LCC)
RS485_rreq_RW = bytes(rs485_rreq_RW)
RS485_rreq_DIP= bytes(rs485_rreq_DIP)
TCU_wreq_power_on_DUT=bytes(tcu_wreq_power_on_dut)
TCU_wreq_power_off_DUT=bytes(tcu_wreq_power_off_dut)
TCU_DOP1_on=bytes(tcu_dop1_on)
TCU_DOP1_off=bytes(tcu_dop1_off)

RS485_wreq_tare = bytes(rs485_wreq_tare)
RS485_wreq_RW = bytes(rs485_wreq_RW)+(RW.to_bytes(2,"big"))
RS485_wreq_calibration = bytes(rs485_wreq_calibration)


a=0
X=0
data=0
rs_232_connection=0
rs_485_connection=0
state=0
q=0
serialno_of_DUT=""
index=0
old1=False
old2=False
old3=False
RS232_connection="Not Done"
RS485_connection="Not Done"
range_check="Not In Range"
stability_check="Not Stable"
LCC=0
DIP_working="Not Okay"
DIP_onoff="Not Done"

#secondpage1

def get_data_via_rs232(rd):
    global a
    global data
    if rd=="AW":
        ser.write(RS232_rreq_AW)
        ser.flushInput()
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        return data
    
    if(rd=="LCC"):
        ser.write(RS232_rreq_LCC)
        ser.flushInput()
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        return data

def get_data_via_rs485(rd):
    global a
    global data
    a=0
    if rd=="AW":
        ser.write(RS485_rreq_AW)
        ser.flushInput()
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        return data
    
    elif rd=="LCC":
        ser.write(RS485_rreq_LCC)
        ser.flushInput()
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        return data

def get_DIP_status():
    global a
    global data
    ser.write(RS485_rreq_DIP)
    ser.flushInput()
    for i in range(3):
        res=ser.read()
        a=int.from_bytes(res, byteorder='big',signed=True)
    res=ser.read(a)
    data=int.from_bytes(res,byteorder='big',signed=True)
    return data


'''def rs232_progress_bar_count():
    RS232_CT=time.time()+RS232_check_time
    ct=0
    while time.time() < RS232_CT:
        count = (RS232_check_time-(RS232_CT-time.time())//RS232_check_time)*100
        time.sleep(.01)
    return ct'''

def power_on_DUT():
    ser.write(TCU_wreq_power_on_DUT)
    time.sleep(0.1)
    ser.flushInput()
    
def power_off_DUT():
    ser.write(TCU_wreq_power_off_DUT)
    time.sleep(0.1)
    ser.flushInput()

def power_on_TCU_DOP():
    ser.write(TCU_DOP1_on)
    time.sleep(0.1)
    ser.flushInput()   


def power_off_TCU_DOP():
    ser.write(TCU_DOP1_off)
    time.sleep(0.1)
    ser.flushInput()

class firstDialog(QDialog):
    
    def __init__(self):
        super(firstDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/firstDialog.ui",self)#load the UI file 
        self.nextbutton.clicked.connect(self.secondpage)
        old1=True
               
    def secondpage(self):
        global old2
        old2=False
        global secondpage1
        if old2:
            widget.addWidget(secondpage1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #connect the next page
        else:
                
            global serialno_of_DUT
            serialno_of_DUT=self.serialnumber.text()  #value of serial number
            if serialno_of_DUT[:6]=='ECLC02':
                secondpage1=secondDialog(serialno_of_DUT)
                widget.addWidget(secondpage1)
                widget.setCurrentIndex(widget.currentIndex()+1)
                old2=True    #open the next page
                
            elif(serialno_of_DUT!=""):
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nEnter a valid format")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
            else:
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nEnter a serial number")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
                
    
        
      
class secondDialog(QDialog):
    def __init__(self,serialno):
        super(secondDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/secondDialog.ui",self) #loadui
        self.initUI()
        self.stablelabel=self.stablevaluelabel
        self.backbutton.clicked.connect(self.backfunction)#connect the back page function
        self.productlineEdit.setText(serialno)        
        self.runbutton.clicked.connect(self.onButtonClick)
        self.thirdnextbutton.clicked.connect(self.checking_connection)
        
        
    def checking_connection(self):
        if RS232_connection=="Done" and RS485_connection=="Done":
            self.thirdpage()
        else:
            if RS232_connection=="Not Done":
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nRS232 connection not done")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
                self.thirdpage()
            elif RS485_connection=="Not Done":
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nRS485 connection not done")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
        
    def thirdpage(self):
            '''global old3
        global thirdpage1
        if old3:
            widget.addWidget(thirdpage1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            ser.write(RS232_wreq_tare)
            time.sleep(1)
            ser.flushInput()
            power_on_TCU_DOP() #connect the next page
        else:'''
            ser.write(RS485_wreq_tare)
            time.sleep(1)
            ser.flushInput()
            thirdpage1=thirdDialog()
            widget.addWidget(thirdpage1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #old3=True
            ser.write(RS485_wreq_RW)
            time.sleep(0.1)
            ser.flushInput()
            power_on_TCU_DOP()
            
        
    def oldNext3(self):
        widget.addWidget(thirdpage1)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def backfunction(self):
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)   #connect the first page
        old1=False
        old2=False
        old3=False
        RS232_connection="Not Done"
        RS485_connection="Not Done"
        range_check="Not In Range"
        Stability_check="Not stable"
        DIP_working="Not Okay"
        currentpage=firstDialog()
        widget.addWidget(currentpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        power_off_DUT()
        
    def initUI(self):
        self.rs232progressBar.setMaximum(100)  #maxmium limit of progress bar
        self.rs485progressBar.setMaximum(100)
        self.stabilityprogressBar.setMaximum(100)
        self.rs232progressBar.setValue(0)
        self.rs485progressBar.setValue(0)
        self.stabilityprogressBar.setValue(0)
        self.rs232progressBar.show()
        self.rs485progressBar.show()
        self.stabilityprogressBar.show()
        self.labelcompletestatus232=self.rs232complelabel   #object definition
        self.labelcompletestatus232.hide()       
        self.labelcompletestatus485=self.rs485complelabel
        self.labelcompletestatus485.hide()
        self.resvalue=self.resultlabel
        self.resvalue.setStyleSheet("background-color: ")
        self.stabilityresult=self.stablecomplelabel
        self.stabilityresult.hide()
        self.testprogress=self.testinprogresslabel
        self.testprogress.hide()
        
       

    def onButtonClick(self):
        global RS232_connection
        global RS485_connection
        global a
        self.initUI()
        power_on_DUT()
        RS232_CT=time.time()+RS232_check_time
        count = 0
        while time.time() <= RS232_CT:
            count = int((RS232_check_time-(RS232_CT-time.time()))*100/RS232_check_time)
            get_data_via_rs232("LCC")
            if a!=0:
                count=100
                self.rs232progressBar.setValue(count)
                break
            else:   
                self.rs232progressBar.setValue(count)   #set the value to the progress bar
        if a!=0:
            self.rs232progressBar.hide()  #hide the progress bar
            self.labelcompletestatus232.setText("   Connection done  ")
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: lightgreen")  #CHANGE the background
            RS232_connection="Done"
        else:
            self.rs232progressBar.hide()
            self.labelcompletestatus232.setText("            Not found  ")
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: red")
            RS232_connection="Not Done"   
        RS485_CT=time.time()+RS485_check_time
        count = 0
        while time.time() <= RS485_CT:
            count =int((RS485_check_time-(RS485_CT-time.time()))*100/RS485_check_time)
            get_data_via_rs485("LCC")
            if a!= 0:
                count=100
                self.rs485progressBar.setValue(count)
                break
            else:   
                self.rs485progressBar.setValue(count)
      
        if a!=0:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setText("   Connection done  ")
            self.labelcompletestatus485.setStyleSheet("background-color: lightgreen")
            RS485_connection="Done"

        else:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setText("            Not found  ")
            self.labelcompletestatus485.setStyleSheet("background-color: red")
            RS485_connection="Not Done"
        self.maxminvalue()

    def maxminvalue(self):
        global range_check
        global stability_check
        global LCC
        global a
        if RS485_connection=="Done":
            loadvalue=get_data_via_rs485("LCC")
            
            if loadvalue > LC_range_min and LC_range_max >loadvalue:
                self.resvalue.setStyleSheet("background-color: lightgreen")
                self.resvalue.setText("   Done")
                range_check="In Range"
            else:
                self.resvalue.setStyleSheet("background-color: red")
                self.resvalue.setText("Not okay")
                range_check="Not In Range"
            stability_CT=time.time()+stability_check_time
            count = 0
            test_case=get_data_via_rs485("LCC")
            while time.time() <= stability_CT+0.05:
                count = int((stability_check_time-(stability_CT-time.time()))*100/stability_check_time)
                LCC=get_data_via_rs485("LCC")
                if (LCC>=(test_case-Tolenrance) and LCC<=(test_case+Tolenrance)):
                    self.stabilityprogressBar.setValue(count)
                    self.stablelabel.setText(str(LCC))
                else:
                    break
                
            if count>99:
                self.stabilityprogressBar.hide()
                self.stablecomplelabel.show()
                self.stablecomplelabel.setStyleSheet("background-color: lightgreen") 
                self.stablecomplelabel.setText("   Stable")
                stability_check="Stable"
            else:
                self.stabilityprogressBar.hide()
                self.stablecomplelabel.show()
                self.stablecomplelabel.setText("Not stable")
                self.stablecomplelabel.setStyleSheet("background-color: red")
                stability_check="Not Stable"
            diff=abs(get_data_via_rs485("LCC") - get_data_via_rs485("LCC"))
            if (diff<=Tolenrance):
                self.testprogress.show()   #show the text completed text
                self.testprogress.setText("                Click next")
            else:
                self.testprogress.show()
                self.testprogress.setText("Data of RS232&RS485 not same")
        else:
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("oops...  \nRS485 connection not done")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()

class thirdDialog(QDialog):
    def __init__(self):
        global tare_time,DIP_check_time
        tare_time=time.time()+DIP_check_time
        super(thirdDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/thirddialog - Copy.ui",self) #loadui
        self.backbutton3.clicked.connect(self.pagetwo)
        self.savebutton.clicked.connect(self.savetofile)
        self.clickherebutton.clicked.connect(self.calibration)
        self.tarebutton.clicked.connect(self.tare)
        self.weightlabel1=self.weightlabel
        self.countlabel1=self.countlabel
        self.showweight()
        self.DIPlabel=self.DIP1label
        self.calibratelabel1=self.calibratelabel
        self.inputdevicestatus()
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(10) # 10 ms 
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.showweight)
        self.qTimer.timeout.connect(self.inputdevicestatus)
        self.qTimer.start()
        self.calibratelabel1.setText("To calibrate with Ref. weight of "+ str(RW) +"g")
        
        
    def tare(self):
        ser.write(RS485_wreq_tare)
        time.sleep(.1)
        ser.flushInput()
        
    def pagetwo(self):
        global tare_time,DIP_check_time
        global DIP_onoff
        widget.addWidget(secondpage1)
        widget.setCurrentIndex(widget.currentIndex()+1)
        tare_time=time.time()+DIP_check_time
        DIP_onoff="Not Done"
        self.qTimer.stop()
        power_off_TCU_DOP()
        
        
        
    def showweight(self): 
        global tare_time
        global DIP_onoff
        self.weightlabel1.setText(str(get_data_via_rs485("AW"))+" g")
        self.countlabel1.setText(str(get_data_via_rs485("LCC")))
        self.countlabel1.show()
        self.weightlabel1.show()
        if(DIP_onoff!="Done"):
            if (tare_time>time.time()):
                pass
            else:
                power_off_TCU_DOP()
                DIP_onoff="Done"
                time.sleep(0.5)
            
        
    def calibration(self):
        ser.write(RS485_wreq_calibration)
        time.sleep(0.5)
        ser.flushInput()
        
    def inputdevicestatus(self):
        global DIP_working
        if get_DIP_status():   
            self.DIPlabel.setStyleSheet("background-color: lightgreen")
            DIP_working="Okay"
        else:
            self.DIPlabel.setStyleSheet("background-color: red")
        
        
            
    def savetofile(self):
        global old1,old2,old3
        global serialno_of_DUT,RS232_connection,RS485_connection
        global range_check,stability_check,LCC,DIP_working
        if range_check=="Not In Range":
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("Load cell count Not in range")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()
        if stability_check=="Not Stable":
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("Load cell count Not stable")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()
        if DIP_working=="Not Okay":
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("      DIP : Not okay       ")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()
    
        with open(r'/home/pi/Desktop/ECLC02_report.csv', 'a') as f:
           writer = csv.writer(f)
           writer.writerow([serialno_of_DUT,RS232_connection,RS485_connection,range_check,stability_check,LCC,DIP_working])
        mbox=QMessageBox()              #popup the message box widget
        mbox.setWindowTitle("Success")
        mbox.setText("Below Data Saved to file\n   serialno_of_DUT : "+serialno_of_DUT+"\n   RS232 : "+RS232_connection+"\n   RS485 : "+RS485_connection+ "\n   Range : "+range_check+"\n   Stability : "+stability_check+"\n   LCC : "+str(LCC)+"\n   DIP : "+DIP_working)
        mbox.setIcon(QMessageBox.Warning)
        x=mbox.exec_()
        old1=False
        old2=False
        old3=False
        RS232_connection="Not Done"
        RS485_connection="Not Done"
        range_check="Not In Range"
        Stability_check="Not Stable"
        DIP_working="Not Okay"
        currentpage=firstDialog()
        widget.addWidget(currentpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        power_off_DUT()
        self.qTimer.stop()
    
               

app=QApplication(sys.argv)
mainwindow=firstDialog()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Spark Drives And Automation")
widget.setWindowIcon(QIcon(r'/home/pi/Desktop/Loadcell_transmitter/spark.ico'))
widget.showMaximized()
widget.show()
app.exec_()


