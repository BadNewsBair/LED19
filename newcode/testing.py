import math
import numpy as np
# will be able to get rid of this later 
import csv
import pandas as pd
# --------------------------------------------------------
class Data():
    test_csv =  'Lumen Calculator IES.xlsx'
    am_i_using_a_csv = True
    def __init__(self):
        None
        #self.am_i_using_a_csv = True
        #self.test_csv = 'Lumen Calculator IES.xlsx'
        # will this work for every csv??
    def read_rho_theta_csv(self,csv_file = test_csv):
        try:
            rho_theta = pd.read_excel(csv_file,header= None,skiprows= 15)
            #deletes the last 2 columns since they are nans.....probably dont need this when creating our own
            rho_theta = rho_theta.drop(rho_theta.columns[[-2,-1]], axis =1)
            rho_T=theta = rho_theta.head(2)
            #_, cols = Rho_Theta.shape

            return rho_theta
        except:
            print('This didnt work idiot')

    def data_csv(self,csv_file = test_csv, last_measured_angle=0):
        #need to change this to make more universal
        data_rows = int(last_measured_angle / 5 + 1)
        try:
            data = pd.read_excel('Lumen Calculator IES.xlsx',header= None,skiprows= 17)
            data = data.drop(data.columns[[-2,-1]], axis =1)
            data = data.head(data_rows)
            return data, data_rows
        except :
            print('This didnt work idiot')

    # need to make data rows more universal(espessially without the csv) 
    def data_average(self,data_frame=None):
        data_rows = data_frame.shape[0]
        data_average = data_frame.append(data_frame.mean(axis=0),ignore_index=True)
        data_average[0][int(data_rows)] = 'Average'
        return data_average

    #equation to calculate the Steradians
    def steradians_equation(self,rho_0= 0, rho_1=None):
        if rho_0 == 0 and rho_1 == None:
            return(0)
        else:
            left_equation = (2 * math.pi * (1 - math.cos(rho_1 * math.pi/180))) 
            right_equation = (2 * math.pi * (1 - math.cos(rho_0 * math.pi/180)))
            return(left_equation-right_equation)

    def Steradains(self, Rho_Theta_data_frame = self):
        steradians_values = []
        steradians_values.append('Steradains')
        #this is only for for the first value can probably change my code to make prettier
        steradians_values.append(0)



        def lumens(self,last_angle_measured):







            

            total_steradians = 0 
            for i in range (1,cols-1):
                rho_0, _  = Rho_Theta[i]
                rho_1, _ = Rho_Theta[i+1]    
                steradians_values.append(steradians(rho_0=rho_0, rho_1 =rho_1))
                total_steradians += steradians(rho_0=rho_0, rho_1 = rho_1)
            print(total_steradians)
            steradians_values = pd.Series(dict(zip(data.columns, steradians_values)))
            data = data.append(steradians_values, ignore_index = True)

            lumens_values = []
            lumens_values.append('Lumens')
            total_lumens =0

            for i in range (1, cols -1):
                Average_Row = data[i][data.shape[0]-2]
                Steradains_Row = data[i][data.shape[0]-1]
                lumens_values.append(Average_Row*Steradains_Row)
                total_lumens += Average_Row * Steradains_Row

            lumens_values = pd.Series(dict(zip(data.columns, lumens_values)))
            data = data.append(lumens_values, ignore_index = True)

            print(total_lumens)
            #print(data.round(3))
    
# This is for testing purposes only at the moment
def main():
    #Data.am_i_using_a_csv = True
    if Data.am_i_using_a_csv == True:
        try:
            test_data = Data()
            rho_theta_data,rho_theta_cols = test_data.read_rho_theta_csv(Data.test_csv)
            data_df, num_rows = test_data.data_csv(Data.test_csv, last_measured_angle=90)
            average = test_data.data_average(data_df)
            print(average)
        except:
            print('im DOING SOMETHING WRONG')
            exit()
    print('This might be working')
    
    #lumens(90)

main()