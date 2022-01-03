from tkinter import *
from PIL import ImageTk, Image #import for drop downs
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


root = Tk()
root.title('Predictive Code')
root.geometry('70x50')

#single button that references all the button commands
#units
#error messages--string/float--out of range
#colors????


Density = 0
NozzleD = 0
AbrasiveD = 0
Pressures = 0
Angle = 0
Distance = 0

def myClick1():
	#check range
	#assign entered value to variable
	Density = float(e1.get())
	
	
def myClick2():
	#check range
	#assign entered value to variable
	NozzleD = float(e2.get())
	

def myClick3():
	#check range
	#assign entered value to variable
	AbrasiveD = float(e3.get())
	
	
def myClick4():
	#check range
	#assign entered value to variable
	Pressures = float(e4.get())
	
	
def myClick5():
	#check range
	#assign entered value to variable
	Angle = float(e5.get())
	
	
def myClick6():
	#check range
	#assign entered value to variable
	Distance = float(e6.get())
	#[Density, AbrasiveD, Pressures, Angles, Distances, NozzleD]
	#This SVDx is imported from the suggestive code. This will be decided at the end after all of our data is in as this changes slightly every time

	SVDx = [-2.10028933e-03, -1.58641015e+04, 1.06153955e-01, -1.02978351e-02, 2.26485204e+00, 6.00670165e+01]

	CurrRA = SVDx[0]*Density

	CurrRA += SVDx[5]*NozzleD

	CurrRA += SVDx[1]*AbrasiveD

	CurrRA += SVDx[2]*Pressures
	
	CurrRA += SVDx[3]*Angle

	CurrRA += SVDx[4]*Distance

	myLabel1 = Label(root, text = 'The predicted Ra value is')
	myLabel1.pack()
	myLabel2 = Label(root, text = CurrRA)
	myLabel2.pack()
	

	
#prompt for density
e1 = Entry(root)
e1.pack()
e1.insert(0,'Enter Density []')

#prompt for nozzleD
e2 = Entry(root)
e2.pack()
e2.insert(0,'Enter Nozzle Diameter [in]')

#prompt for AbrasiveD
e3 = Entry(root)
e3.pack()
e3.insert(0,'Enter Abrasive Diameter [in]')


#prompt for pressure
e4 = Entry(root)
e4.pack()
e4.insert(0,'Enter Pressure [PSI]')


#prompt for angle
e5 = Entry(root)
e5.pack()
e5.insert(0,'Enter Angle [deg]')


#prompt for distance
e6 = Entry(root)
e6.pack()
e6.insert(0,'Enter distance [in]')



#button to initialize density
myButton1 = Button(root, text= 'Ok', command=myClick1)

#button to initialize NozzleD
myButton1 = Button(root, text= 'Ok', command=myClick2)

#button to initialize abrasiveD
myButton1 = Button(root, text= 'Ok', command=myClick3)

#button to initialize pressure
myButton1 = Button(root, text= 'Ok', command=myClick4)

#button to initialize angle
myButton1 = Button(root, text= 'Ok', command=myClick5)

#button to initialize distance
myButton1 = Button(root, text= 'Ok', command=myClick6)
myButton1.pack()
	
root.mainloop()