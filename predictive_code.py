import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#This will come from the GUI as for what materials the user selects
User_Metal = 5083
User_Abrasive = "Garnet SMALL"

#reads the data from the excel file, the very last slot is the sheet name so this can easily be changed.
DFdata = pd.read_excel('Exp_Data.xlsx', 'Data3')

#Grabs the first row and reads the names
DFdata.head()

#This block makes vectors for each variable
Pressure = DFdata['Pressure (PSI)'].to_numpy()
Distance = DFdata['Distance (in)'].to_numpy()
Angle = DFdata['Angle (Deg)'].to_numpy()
NozzleD = DFdata['Nozzle ID (in)'].to_numpy()
Abrasive = DFdata['Abrasive'].to_numpy()
Metal = DFdata['Plate Material'].to_numpy()

Ra = DFdata['Ra'].to_numpy()
R3z = DFdata['R3z'].to_numpy()
Rv = DFdata['Rv'].to_numpy()
Rp = DFdata['R3z'].to_numpy()
Rt = DFdata['Rp'].to_numpy()
Rz = DFdata['Rz'].to_numpy()
RS = DFdata['RS'].to_numpy()
Rsk = DFdata['Rsk'].to_numpy()
RSm = DFdata['RSm'].to_numpy()
RzJIS = DFdata['RzJIS'].to_numpy()
R3y = DFdata['R3y'].to_numpy()
Rku = DFdata['Rku'].to_numpy()
Rmax = DFdata['Rmax'].to_numpy()
Rpc = DFdata['Rpc'].to_numpy()
Rk = DFdata['Rk'].to_numpy()
Rpk = DFdata['Rpk'].to_numpy()
Rvk = DFdata['Rvk'].to_numpy()
mr1 = DFdata['mr1'].to_numpy()
mr2 = DFdata['mr2'].to_numpy()

#This will be what variable is predicated, will be assigned from GUI
profile_variable = Rmax

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
min_val = 0
rpv_train = []
rpv_test = []
temp_test = []
temp_train = []
for k in range(10000):

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

    test_difference = np.average(abs(testtemp - profile_variable_test_sorted))
    test_max_difference = np.max(abs(testtemp - profile_variable_test_sorted))

    if min_max > test_max_difference:
        min_max = test_max_difference
        min_val = test_max_difference
        temp_test = all_test
        temp_train = all_train
        rpv_test = profile_variable_test
        rpv_train = profile_variable_train

#related_profile_var = related_profile_var[p]
#profile_variable_train = related_profile_var[1:n]
#all_train = all_vars[1:n]
#profile_variable_test = related_profile_var[n:]
#all_test = all_vars[n:]


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

print("")
print("This is the correlation vector")
print(x)

#fig = plt.figure()
#ax1 = fig.add_subplot(121)                                 #uncomment this for side by side graphs

#plt.plot(profile_variable_train, color='k', linewidth=2, label='RA Value')
#plt.plot(all_train@x, '-o', color ='r', linewidth=0.5, label='All Vars')
#plt.xlabel('Test Number In Set')
#plt.ylabel('um/s')
#plt.title('Training Set')

#fig3 = plt.figure()                                         #comment this for side by side graphs
#plt.plot(profile_variable_test, color='k', linewidth=2, label='RA Value')
#plt.plot(all_test@x, '-o', color ='r', linewidth=0.5, label='All Vars')
#plt.xlabel('Test Number In Set', fontsize=18)
#plt.ylabel('RA in um', fontsize=18)
#plt.title('SVD Predication using experimental data', fontsize=18)

#ax2 = fig.add_subplot(122)                                 #uncomment this for side by side graphs
fig2 = plt.figure()                                         #comment this for side by side graphs
plt.plot(profile_variable_test_sorted, color='k', linewidth=2, label='RA Value')
plt.plot(predicted_rpv, '-o', color ='r', linewidth=0.5, label='All Vars')
plt.xlabel('Test Number In Set', fontsize=18)
plt.ylabel('Rmax in um', fontsize=18)
plt.title('SVD Predication using experimental data sorted', fontsize=18)


plt.show()
