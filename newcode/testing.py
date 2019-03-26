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
            rho_theta = rho_theta.head(2)

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
            return data
        except :
            print('This didnt work idiot')

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

    # Creates the Steradians Row and appends to Data Frame
    def steradains_df(self, Rho_Theta_df, data_df):
        steradians_values = []
        steradians_values.append('Steradains')
        #this is only for for the first value can probably change my code to make prettier
        steradians_values.append(0)
        total_steradians = 0
        for i in range (1,Rho_Theta_df.shape[1]-1):
            rho_0, _  = Rho_Theta_df[i]
            rho_1, _ = Rho_Theta_df[i+1]    
            steradians_values.append(self.steradians_equation(rho_0=rho_0, rho_1 =rho_1))
            total_steradians += self.steradians_equation(rho_0=rho_0, rho_1 = rho_1)
        steradians_values = pd.Series(dict(zip(data_df.columns, steradians_values)))
        data = data_df.append(steradians_values, ignore_index = True)
        return(data , total_steradians)

    def lumens(self,data):           
        lumens_values = []
        lumens_values.append('Lumens')
        total_lumens =0
        for i in range (1, data.shape[1] -1):
            Average_Row = data[i][data.shape[0]-2]
            Steradains_Row = data[i][data.shape[0]-1]
            lumens_values.append(Average_Row*Steradains_Row)
            total_lumens += Average_Row * Steradains_Row
        lumens_values = pd.Series(dict(zip(data.columns, lumens_values)))
        data = data.append(lumens_values, ignore_index = True)
        return(data)
    
    def all_calculations(self, data_df, rho_theta_data):
        average = self.data_average(data_df)
        steradains_df, summed_total_steradains = self.steradains_df(Rho_Theta_df=rho_theta_data ,data_df=average)
        data_frame = self.lumens(steradains_df)
        print(data_frame)

    def get_data_from_csv(self,csv_file):
        print(csv_file)
        print('i made it here')
        rho_theta_data = self.read_rho_theta_csv(csv_file)
        #data_df, num_rows = self.data_csv(csv_file, last_measured_angle=90)
        #return(rho_theta_data, data_df)


# This is for testing purposes only at the moment
def main():
    test_data = Data()
    if Data.am_i_using_a_csv == True:
        try:
            #rho_theta_data, data_df = test_data.get_data_from_csv(Data.test_csv)
            rho_theta_data = test_data.read_rho_theta_csv(Data.test_csv)
            data_df = test_data.data_csv(Data.test_csv, last_measured_angle=90)
        except:
            print('Something is wrong with the csv')
            exit()

    test_data.all_calculations(data_df, rho_theta_data)
        

main()