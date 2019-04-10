from bh1750 import BH1750
import math
import numpy as np
# will be able to get rid of this later 
import pandas as pd
import warnings
import datetime
import smbus2
import time

# --------------------------------------------------------
class Data():
    test_csv =  'Lumen Calculator IES.xlsx'
    am_i_using_a_csv = False
    date = datetime.datetime.now()

    delay = .05
    
    def __init__(self):
        None
        #self.am_i_using_a_csv = True
        #self.test_csv = 'Lumen Calculator IES.xlsx'
        # will this work for every csv??
    def read_rho_theta_csv(self,csv_file = test_csv):
        rho_theta = pd.read_excel(csv_file,header= None,skiprows= 15)
        #deletes the last 2 columns since they are nans.....probably dont need this when creating our own
        rho_theta = rho_theta.drop(rho_theta.columns[[-2,-1]], axis =1)
        rho_theta = rho_theta.head(2)

        return rho_theta


    def data_csv(self,csv_file = test_csv, last_measured_angle=0):
        #need to change this to make more universal
        data_rows = int(last_measured_angle / 5 + 1)
        data = pd.read_excel('Lumen Calculator IES.xlsx',header= None,skiprows= 17)
        data = data.drop(data.columns[[-2,-1]], axis =1)
        data = data.head(data_rows)
        return data


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
        return(data_frame.round(3))

    def create_file(self, file_name = 'some_file_name.IES'):
        
        try:
            file = open(file_name,'x')
        except:
            #probably need a pop up window to prompt user about overwritting 
            print('Writing overtop previous saved data in file ....')
            file = open(file_name,'w')

        #header for the .ies file
        file.write('IESNA: LM-63-2002\n') 
        file.write('[TEST] L101803601\n') # allow for a user to input a test number
        file.write('[TESTLAB] SIMPLY LEDS, LLC (www.simplyleds.com) \n') 
        file.write('[ISSUEDATE] ' +str(self.date.strftime("%x"))+ ' \n')
        file.write('[MANUFAC] SIMPLY LEDS,LLC \n')
        file.write('[LUMCAT] FLDRS-110W-XV-40K-T5-CL \n')# allow for a user to input a partnumber
        file.write('[LUMINAIRE] ROADWAY AND AREA LUMINAIRE W/ CLEAR LENS \n')
        file.write('[BALLASTCAT] INVENTRONICS EUD-150S350DTA \n') #allow for a user to input the number
        file.write('[OTHER] INDICATING THE CANDELA VALUES ARE ABSOLUTE AND \n')
        file.write('[MORE] SHOULD NOT BE FACTORED FOR DIFFERENT LAMP RATINGS \n')
        file.write('[INPUT] 119.97 VAC 108.31W \n') 
        file.write('[TEST PROCEDURE] IESNA:LM-79-08 \n') #can be test angle range 
        file.write('TILT = NONE\n')
#        file.write("1 -1 "+ str(lux_candela_ratio)+" 19 37 1 1 1 0 0\n")
#        file.write("1 1 "+str(wattage)+"\n")
        file_name = file_name.split('.')[0]
        return(file_name)

    
    def theta_rotation(self, test=None):
        if test == str('Type_5'):
            rho_line = np.arange(-5,95,5,dtype='int')
            print('0-90 5 degree incremenets')
        elif test == str('Type_3') or test == str('Type_4'):
            rho_line = np.arange(-5,185,5,dtype='int')
            print('0-180 5 degree increments')
        else:
            rho_line = np.arange(-5,360,5,dtype='int')
            print('0-355 5 degree increments')

        #convert to list to add Rho and back to numpy array   
        rho_line = list(rho_line)
        rho_line[0] = 'Rho'
        rho_line = np.asarray(rho_line)
        
        #second row of theta/rho
        theta_line = np.zeros(rho_line.shape[0])
        theta_line = theta_line.astype('float')
        theta_line[theta_line == 0] = np.nan
        
        theta_line = list(theta_line)
        theta_line[0]='Theta'
        theta_line= np.asarray(theta_line)

        #combines the two
        theta_header = np.stack((rho_line, theta_line))
        
        # turn into panda data frame 
        theta_header = pd.DataFrame(data= theta_header)

        return(theta_header)

    def data_collect(self, header_length):
        #column 0, 0-90 by 5s
        column_degrees = np.arange(0,95,5,dtype='int')
        column_degrees = np.array([column_degrees])
        column_degrees = column_degrees.T
        #create empty array
        #data_array = np.zeros((column_degrees.size,header_length))
        data_array = np.zeros(column_degrees.size*header_length)
        # collect/store data
        bus = smbus2.SMBus(1)
        sensor = BH1750(bus)
        
        i=0
        while data_array[i] < data_array.size:
            print(sensor.measure_high_res2())
            data_array[i] = float(sensor.measure_high_res2())
            #data_array[i]=self.read_light()
            i = i + 1
            time.sleep(self.delay)
            if (i == data_array.size):
                break
        #go from 1d array to 2d array 
        data_array = np.resize(data_array,(column_degrees.size,header_length))
        #combine column array and data array
        data_array = np.concatenate((column_degrees, data_array), axis =1)
        #turn numpy array to data_frame
        data_array = pd.DataFrame(data= data_array)  
        return(data_array)

# This is for testing purposes only at the moment
def main():
    #supresses warning mainly from pandas 
    warnings.filterwarnings('ignore')
    test_data = Data()

    
    file_name = test_data.create_file()
    
    if Data.am_i_using_a_csv == True:
        try:
            #rho_theta_data, data_df = test_data.get_data_from_csv(Data.test_csv)
            rho_theta_df = test_data.read_rho_theta_csv(Data.test_csv)
            data_df = test_data.data_csv(Data.test_csv, last_measured_angle=90)
            
        except:
            print('Something is wrong with the csv file')
            exit()
    else:
        rho_theta_df = test_data.theta_rotation('Type_5')
        data_df = test_data.data_collect(rho_theta_df.shape[1]-1)
        print(data_df)
        print('Rho_theta_df size',rho_theta_df.shape)
        print('data_df size', data_df.shape)
        data_df = pd.concat([rho_theta_df,data_df], ignore_index = True)
        
   
    #rho_theta_data = rho_theta_data.fillna(' ')
    print(data_df)
    data_array = test_data.all_calculations(data_df, rho_theta_df)
    data_array = data_array.fillna(0)

    # appends the data to the file
    with open(file_name +'.IES', 'ab') as f:
        np.savetxt(f, rho_theta_data.values, fmt = '%s')
        np.savetxt(f, data_array.values, fmt = '%s')

    exit()
    

main()
