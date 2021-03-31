
from tkinter import *
import tkinter as tk # proper way to import tkinter
import serial
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")
import threading

class Dee(tk.Frame):
    def __init__(self, master=None, title='', ylabel='', label='', color='c', ylim=1, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []
        fig = Figure(figsize = (7,6))
        self.plot = fig.add_subplot(111)
        self.plot.set_title(title)
        self.plot.set_ylabel(ylabel)
        self.plot.set_ylim(0, ylim)
        self.line, = self.plot.plot([], [], color, marker = 'o',label = label)
        self.plot.legend(loc='upper left')

        label = Label(self, text = ylabel, relief = "solid", font = "Times 22 bold")
        label.grid(row = 0, column = 3)
        button_1 = Button(self, text = "Back To Homepage", command = F1.tkraise)
        button_1.grid(row = 1, column = 2)
        label_1 = Label(self, text = "Current Value: ", relief = "solid", font = "Verdana 10 bold")
        label_1.grid(row = 2, column = 2)
        self.label_data = Label(self, font = "Verdana 10")
        self.label_data.grid(row = 2, column = 3)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row = 3, column = 3)

        ani = animation.FuncAnimation(fig, self.update_graph, interval = 1000, blit = False)
        canvas.draw()

    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))

    def set(self, value):
        self.data.append(value)
        self.label_data.config(text=value)

my_window = Tk()
my_window.title("Graphical User Interface Demo#1")
my_window.geometry("720x720")

F1 = Frame(my_window, relief = RAISED)
F2 = Dee(my_window, title='Temperature Graph', ylabel='Temperature', color='c', label='Degrees C', ylim=40, relief = RAISED)
F3 = Dee(my_window, title='Humidity Graph', ylabel='Humidity', color='g', label='Percentage %', ylim=100, relief = RAISED)
F4 = Dee(my_window, title='Solved Water Graph', ylabel='Water Volume', color='b', label='mL', ylim=55, relief = RAISED)

#For Frame One
label_1 = Label(F1, text = "Homepage of GUI", relief = "solid", font = "Times 22 bold")
label_1.grid(row = 0, column = 3)
button_1 = Button(F1, text = "Page of Humidity", relief = GROOVE, bd = 8, command = F2.tkraise)
button_1.grid(row = 1, column = 2)
button_2 = Button(F1, text = "Page of Temperature", relief = GROOVE, bd = 8, command = F3.tkraise)
button_2.grid(row = 1, column = 3)
button_3 = Button(F1, text = "Page of Water", relief = GROOVE, bd = 8, command = F4.tkraise)
button_3.grid(row = 1, column = 4)

for frame in(F1, F2, F3, F4):
    frame.grid(row = 0, column = 0, sticky = "NSEW")

F1.tkraise()

def get_data():
    #Initialization of Serial Comm
    ser = serial.Serial('/dev/ttyS0', 9600)
    while True:
        pulldata = ser.readline().decode('ascii')
        get_data = pulldata.split(',')
        F2.set(int(get_data[0]))
        F3.set(int(get_data[1]))
        F4.set(int(get_data[3]))

# start the thread that will poll the arduino
t = threading.Thread(target=get_data)
t.daemon = True
t.start()

my_window.mainloop()