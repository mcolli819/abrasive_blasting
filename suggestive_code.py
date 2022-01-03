import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root = tk.Tk()
root.title('Suggestive Code')
root.geometry('800x800')

#def variable and store based on selection
def comboclick(event):
    global RPVSelection # Setting select_sheet to global, so it can be modified
    global MetalSelection
    global AbrasiveSelection
    RPVSelection = myComboRPV.get()
    MetalSelection = myComboMetal.get()
    AbrasiveSelection = myComboAbrasive.get()


RPVSelection = 'Ra'
MetalSelection = '1018 Steel'
AbrasiveSelection = 'Steel Grit'

optionsRPV = [
'Ra',
'Rq',
'Rz',
'Rt',
'Rsm'] #list of drop down selections

optionsMetal = [
'1018 Steel',
'316 Stainless Steel',
'5083 Aluminium'] #list of drop down selections

optionsAbrasive = [
'Steel Grit',
'Silicon Carbide',
'Glass Grit',
'Coal Slag',
'Garnet (60 Grit)',
'Garnet (80 Grit)',
'Garnet (100 Grit)'] #list of drop down selections

#create combobox
myComboRPV = ttk.Combobox(root, value=optionsRPV)
myComboRPV.current(0)
myComboRPV.bind('<<ComboboxSelected>>', comboclick)
myComboRPV.pack()

myComboMetal = ttk.Combobox(root, value = optionsMetal)
myComboMetal.current(0)
myComboMetal.bind('<<ComboboxSelected>>', comboclick)
myComboMetal.pack()

myComboAbrasive = ttk.Combobox(root, value = optionsAbrasive)
myComboAbrasive.current(0)
myComboAbrasive.bind('<<ComboboxSelected>>', comboclick)
myComboAbrasive.pack()

#set close window button
button_close = tk.Button(root, width=35, text='Confirm Selection', command=root.quit, borderwidth=1).pack()



root.mainloop()

print(RPVSelection)
print(MetalSelection)
print(AbrasiveSelection)

T = tk.Text(root, height=5, width=80)
T.pack()
T.insert(tk.END, "Your Surface Roughness Parameter Selection: " + RPVSelection +
         '\nYour Metal Selection: ' + MetalSelection + '\nYour Abrasive Selection: ' + AbrasiveSelection +'\n\nPlease Enter your desried ' + RPVSelection + ' value below in microns')



def switch_Metal(argument):
    switcher = {
        '1018 Steel': 1018,
        '316 Stainless Steel': 316,
        '5083 Aluminium': 5083,
    }
    return switcher.get(argument, "error")

User_Metal = '1018'

def switch_Abrasive(argument):
    switcher = {
        'Steel Grit' : 'STEEL',
        'Silicon Carbide': 'Si Carbide',
        'Garnet (80 Grit)' : 'Garnet MEDIUM',
        'Glass Grit' : 'Glass',
        'Coal Slag' : 'Coal',
        'Garnet (60 Grit)': 'Garnet LARGE',
        'Garnet (100 Grit)': 'Garnet SMALL'

    }
    return switcher.get(argument, "error")


User_RPV = RPVSelection
User_Metal = switch_Metal(MetalSelection)
User_Abrasive = switch_Abrasive(AbrasiveSelection)

#reads the data from the excel file, the very last slot is the sheet name so this can easily be changed.
DFdata = pd.read_excel('Exp_Data.xlsx', 'Real Data')

#Grabs the first row and reads the names
DFdata.head()

profile_variable =DFdata[User_RPV].to_numpy()

Pressure = DFdata['Pressure (PSI)'].to_numpy()
Distance = DFdata['Distance (in)'].to_numpy()
Angle = DFdata['Angle (Deg)'].to_numpy()
NozzleD = DFdata['Nozzle ID (in)'].to_numpy()
Abrasive = DFdata['Abrasive'].to_numpy()
Metal = DFdata['Plate Material'].to_numpy()

#This takes all of the important variables, and takes them from a vector for each variable, to a vector for each test number by transposing
all_data = [Metal, Abrasive, Distance, Angle,  Pressure, NozzleD, profile_variable]
tempnumpy = np.array(all_data)
transpose_numpy = tempnumpy.T
all_data_vert = transpose_numpy.tolist()

#This takes all of the test numbers that have the same metal and abrasive and stores them
true_all_vars = []
related_profile_var = []
for i in range(len(all_data_vert)):
    if all_data_vert[i][0] == User_Metal and all_data_vert[i][1] == User_Abrasive:# and all_data_vert[i][2] == User_Distance:
        true_all_vars.append(all_data_vert[i][2:-1])
        related_profile_var.append(all_data_vert[i][-1])

all_vars = np.array(true_all_vars)
related_profile_var = np.array(related_profile_var)

#padding to add non-zero offset
all_vars = np.pad(all_vars,[(0,0),(0,1)], mode = 'constant', constant_values=1)

min_max = 1000
min_avg = 1000
min_val = 0
rpv_train = []
rpv_test = []
temp_test = []
temp_train = []
for l in range(40):
    for k in range(500):

        #Taking half of the data points as training data
        n = int(len(related_profile_var)*0.8)
        p = np.random.permutation(len(related_profile_var))
        all_vars = all_vars[p,:]
        related_profile_var = related_profile_var[p]
        profile_variable_train = related_profile_var[1:n]
        all_train = all_vars[1:n]
        profile_variable_test = related_profile_var[n:]
        all_test = all_vars[n:]

        sorted_ind = np.argsort(profile_variable_test)
        profile_variable_test_sorted = profile_variable_test[sorted_ind]

        U, S, VT = np.linalg.svd(all_train, full_matrices=0)
        x = VT.T @ np.linalg.inv(np.diag(S)) @ U.T @ profile_variable_train

        testtemp = all_test@x
        testtemp = testtemp[sorted_ind]

        test_avg_difference = np.average(abs(testtemp - profile_variable_test_sorted))
        test_max_difference = np.max(abs(testtemp - profile_variable_test_sorted))

        if min_max > test_avg_difference:
            min_max = test_avg_difference
            temp_test_2 = all_test
            temp_train_2 = all_train
            rpv_test_2 = profile_variable_test
            rpv_train_2 = profile_variable_train
            best_avg_difference = test_avg_difference
            best_max_difference = test_max_difference

    if min_avg > best_max_difference:
        min_avg = best_max_difference
        temp_test = temp_test_2
        temp_train = temp_train_2
        rpv_test = rpv_test_2
        rpv_train = rpv_train_2

all_train = temp_train
all_test = temp_test
profile_variable_train = rpv_train
profile_variable_test = rpv_test

sorted_ind = np.argsort(profile_variable_test)
profile_variable_test_sorted = profile_variable_test[sorted_ind]

U, S, VT = np.linalg.svd(all_train, full_matrices=0)
x = VT.T @ np.linalg.inv(np.diag(S)) @ U.T @ profile_variable_train

predicted_rpv = all_test @ x
predicted_rpv = predicted_rpv[sorted_ind]

test_difference = np.average(abs(predicted_rpv - profile_variable_test_sorted))
test_max_difference = np.max(abs(predicted_rpv - profile_variable_test_sorted))

print("Average error")
print(test_difference)
print("")
print("Max error")
print(test_max_difference)

#print("")
print("This is the correlation vector")
print(x)

SVDx = x

#print(SVDx) #This is taken from the Prediction code

desRA1 =1

e = tk.Entry(root)
e.pack()

def DesRaClick():
    global desRA1
    myLabel = tk.Label(root, text = 'Your desired Ra value is ' + e.get())
    myLabel.pack()
    desRA1 = e.get()
    root.quit()

myButton = tk.Button(root, text = 'Confirm Ra value', command = DesRaClick)
myButton.pack()

root.mainloop()

temp_bool = True
#while temp_bool:
#
#    try:
#        desRA = float(input("Please enter your desired RA value in microns: "))
#        temp_bool = False
#    except ValueError:
#        print("Oops, that was not a number. Please only enter a number.")


#density = float(input("Enter the density of your metal: "))
#abrasiveD = float(input("Enter the diameter of your abrasive: "))
print(desRA1)
mat_abrasive_effect =  SVDx[4]
desRA1 = float(desRA1)
desRA = desRA1 - mat_abrasive_effect

names = ["NozzleD", "Pressure", "Distance", "Angle"]
x_vars = np.array([0.0, 0.0, 0.0, 0.0])
x_min = np.array([0.2031, 50, 1, 15])
x_max = np.array([0.3125, 135, 8, 90])
a_vars = np.array([SVDx[3], SVDx[2], SVDx[0], SVDx[1]])
print(names)
print(a_vars)
#print("Nozzle D, Pressure, Distance, Angle")

x_vars_j = np.array([0.0])

for j in range(len(x_vars)):
    #This generates a temp vector for the max and min values for the parameters
    temp_min_x = np.zeros(len(x_vars))
    temp_max_x = np.zeros(len(x_vars))

    for i in range(len(x_vars)):

        if i > j:

            #This if and else detect if the correlation is positive or negative, then sets the temp x to max or min depending

            if a_vars[i] > 0:
                temp_min_x[i] = x_max[i]
                temp_max_x[i] = x_min[i]
            else:
                temp_min_x[i] = x_min[i]
                temp_max_x[i] = x_max[i]


    #print("this is temp max") #These are for testing
    #print(temp_max_x)

    #print("this is temp min")
    #print(temp_min_x)

    #This transposes the temp vector to they can be matrix Multiplied
    temp_max_x = temp_max_x.T
    temp_min_x = temp_min_x.T

    #Calculates the relative RA from the temp x values
    min_DesRA = np.matmul(a_vars, temp_min_x)
    max_DesRA = np.matmul(a_vars, temp_max_x)

    print(desRA)
    print("min desRA") #These are for testing
    print(min_DesRA)

    print("Max desRA")
    print(max_DesRA)




    #Calculates the max and min bounds from subtracting desRA by the relative RA, then dividing
    max_x_j = (desRA - max_DesRA)/a_vars[j]
    min_x_j = (desRA - min_DesRA)/a_vars[j]

    print("These are max then min values for the parameter")
    print(max_x_j)
    print(min_x_j)

    #if (min_x_j > x_max[j] or max_x_j < x_min[j]) and j!= len(x_vars):
     #   print("The desired RA can not be met with the current conditions")
      #  print(min_x_j)
       # print(max_x_j)
        #print(j)
        #print(len(x_vars))
        #exit()

    if min_x_j > x_max[j]:
        min_print = x_min[j]
    else:
        min_print = max(min_x_j, x_min[j])

    if max_x_j < x_min[j]:
        max_print = x_max[j]
    else:
        max_print = min(max_x_j, x_max[j])



    if j == 0:
        min_print = round(min_print, 4)
        max_print = round(max_print, 4)
    else:
        min_print = round(min_print, 1)
        max_print = round(max_print, 1)

    #print("The maximum value for " + names[j] +" is")
    #print(max_print)

    #print("The minimum value for " + names[j] +" is")
    #print(min_print)

    #temp_bool = True
    #while temp_bool:
    #    try:
    #        print("What " + names[j] + " value would you like to choose?")
    #        x_vars[j] = float(input())
    #        temp_bool = False
    #    except ValueError:
    #        print("Oops, that was not a number. Please only enter a number.")

    T = tk.Text(root, height=2, width=80)
    T.pack()
    T.insert(tk.END, 'The maximum ' + names[j] +' value you may choose is: ' + str(max_print) +'\nThe minimum ' + names[j] +' value you may choose is: ' + str(min_print))

    e = tk.Entry(root)
    e.pack()

    x_var = 0
    def DesRaClick():
        global x_var
        myLabel = tk.Label(root, text='Your desired ' +names[j] +' value is ' + e.get())
        myLabel.pack()
        x_var = e.get()
        root.quit()


    myButton = tk.Button(root, text='Confirm ' + names[j] + ' value', command=DesRaClick)
    myButton.pack()



    root.mainloop()
    x_vars[j] = float(x_var)
    print(x_vars[j])
    desRA = desRA - x_vars[j] * a_vars[j]



pred_RA = np.matmul(a_vars, x_vars.T)
pred_RA = pred_RA + mat_abrasive_effect
pred_RA = round(pred_RA, 3)

print("These are your inputs for Nozzle Diameter, Pressure, Distance, Angle")
print(x_vars)
print("This is the predicated parameter from your inputs")
print(pred_RA)

T = tk.Text(root, height=2, width=80)
T.pack()
T.insert(tk.END, 'The '+RPVSelection+' value that is predicted to come from your inputs is ' + str(pred_RA))

button_close = tk.Button(root, width=35, text='Confirm Selection', command=root.quit, borderwidth=1).pack()
root.mainloop()
