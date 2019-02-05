#!/usr/bin/python
import time
import GUI_Menu as gm
import Test_Connectivity as tc
import Home_Motors as hm
import Measurement_Sweep as ms
import Process_Data as pd

#**main code**
#This Main displays the GUI_Menu by default. The GUI_Menu allows the user to choose what code
#they want to run.Once the user makes a selection with the GUI, the main closes the GUI and
#runs the selected program. Upon completion of the selected program, the menu_GUI is shown again.

#Boolean Variable to quit entire program
Done=False

while not(Done):
    #Use Menu gui to get user's choice
    Option_Chosen=gm.GUI_Menu()
    
    #run choice chosen
    #option 16 means the user clicked exit
    if Option_Chosen==16:
        Done=True
    elif Option_Chosen==0:
        try:
            tc.Test_Connectivity()
        except:
            print("Uncaught error within test connectivity")
    elif Option_Chosen==1:
        try:
            hm.Home_Motors()
        except:
            print("Uncaught error within Home Motors")
    elif Option_Chosen==2:
        try:
            ms.Measurement_Sweep()
        except:
            print("Uncaught error within Measurement Sweep")
    elif Option_Chosen==3:
        try:
            pd.Convert_IES()
        except:
            print("Uncaught error within Measurement Sweep")
     
    else:
        try:
            webbrowser.open('Proj_Docs.html')
        except:
            print("File not Found for documentation")