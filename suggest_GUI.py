from tkinter import *
from PIL import ImageTk, Image #import for drop downs
from tkinter import ttk


root = Tk()
root.title('dropdowns')
root.geometry('400x400') #
	
options1 = [
'Ra',
'Rq', 
'Rz', 
'Rt', 
'Rsm'] #list of drop down selections



def comboclick(event):

	myLabel = Label(root, text=myCombo.get()).pack()
	
	if myCombo.get() == options1[0]:
		entry_Ra = Entry(root, width = 20)
		entry_Ra.pack()
		entry_Ra.insert(0, '- - Enter Ra Value - -')
		#if entry_Ra.get() is within the desired range:
			#desRA = entry_Ra.get()
		#else: (not in desired range)
			#display error statement
			#{}
	if myCombo.get() == 'Rq':
		entry_Rq = Entry(root, width = 20)
		entry_Rq.pack()
		entry_Rq.insert(0, '- - Enter Rq Value - -')
	
	if myCombo.get() == 'Rz':
		entry_Rz = Entry(root, width = 20)
		entry_Rz.pack()
		entry_Rz.insert(0, '- - Enter Rz Value - -') 
	
	if myCombo.get() == 'Rt':
		entry_Rt = Entry(root, width = 20)
		entry_Rt.pack()
		entry_Rt.insert(0, '- - Enter Rt Value - -')
		
	if myCombo.get() == 'Rsm':
		entry_Rsm = Entry(root, width = 20)
		entry_Rsm.pack()
		entry_Rsm.insert(0, '- - Enter Rsm Value - -')
		
	entry_density = Entry(root, width = 20)
	entry_density.pack()
	entry_density.insert(0, '- - Enter Density [unit] - -')
		#if entry_density.get() is within the desired range:
			#density = entry_density.get()
		#else: (not in desired range)
			#display error statement
			#exit if statement
	density = entry_density.get()
			
			
		#entry_metal.get() will grab the entered value
	
clicked = StringVar()

myCombo = ttk.Combobox(root, value=options1)
myCombo.current(0)
myCombo.bind('<<ComboboxSelected>>', comboclick)
myCombo.pack()

	



root.mainloop()
	
