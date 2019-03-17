import math
# will be able to get rid of this later 
import csv
import pandas as pd
# -------------------------------------

def steradians(rho_0= 0, rho_1=None):
    if rho_0 == 0 and rho_1 == None:
        return(0)
    else:
        left_equation = (2 * math.pi * (1 - math.cos(rho_1 * math.pi/180))) 
        right_equation = (2 * math.pi * (1 - math.cos(rho_0 * math.pi/180)))
        return(left_equation-right_equation)

def lumens(last_angle_measured):

    data_rows = last_angle_measured / 5 + 1

    Rho_Theta = pd.read_excel('Lumen Calculator IES.xlsx',header= None,skiprows= 15)
    #deletes the last 2 columns since they are nans.....probably dont need this when creating our own
    Rho_Theta = Rho_Theta.drop(Rho_Theta.columns[[-2,-1]], axis =1)
    Rho_Theta = Rho_Theta.head(2)
    _, cols = Rho_Theta.shape

    data = pd.read_excel('Lumen Calculator IES.xlsx',header= None,skiprows= 17)
    data = data.drop(data.columns[[-2,-1]], axis =1)
    data = data.head(int(data_rows))
    

    data = data.append(data.mean(axis=0),ignore_index=True)
    data[0][int(data_rows)] = 'Average'

    steradians_values = []
    steradians_values.append('Steradains')
    #this is only for the first value cna probably change my code to make prettier
    steradians_values.append(0)

    for i in range (1,cols-1):
        rho_0, _  = Rho_Theta[i]
        rho_1, _ = Rho_Theta[i+1]    
        steradians_values.append(steradians(rho_0=rho_0, rho_1 =rho_1))

    steradians_values = pd.Series(dict(zip(data.columns, steradians_values)))
    data = data.append(steradians_values, ignore_index = True)

    lumens_values = []
    lumens_values.append('Lumens')
    
    print(data.round(3))
    
    steradians_values = data.loc([0],[1])
    print(steradians_values)


    #this is for testing purposes only at the moment

def main():
    lumens(90)
    #print(steradians(0,5))

main()