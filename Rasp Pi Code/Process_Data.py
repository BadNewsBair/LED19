#!/usr/bin/env python

#**Process_Data**
#Converts Raw Data from the measurment sweep into an IES file that can be run by photometric toolbox
#Can determine what information user needs to supply each time by changing provide defaults booleans

#Application note: This code only works for the current measurement sweep code.

#run process data without main
run_6=False

def Convert_IES():
    #variables
    lines=[]; Lux=[]; temp_Lux=[] ;F_Lux=[]
    HA=[];VA=[];steps_VA=[]; temp=0.0;i=0

    #defaults
    filename='trial2.txt' #defualt file
    wattage=150
    entry_file_path="/home/pi/Desktop/LightProgram/Raw_Measurements/"
    ies_file_path="/home/pi/Desktop/LightProgram/IES_Files/"
    distance=20
    unit=0.0
    lux_candela_ratio=37.161216 #20 ft conversion

    #booleans
    flipped=False
    userSelectsFile=True #determines whether to let user enter data
    userSelectsWattage=True #determines whether to let user enter data
    userSelectsDistance=True #allows user to enter the distance to the light

    #have user select the file
    fileNameValid=False
    if userSelectsFile:
        while not fileNameValid:
                filename=input("Enter file name: ")+".txt"
                try:
                    file=open(entry_file_path+filename,"r")
                    fileNameValid=True
                except:
                    print("File name is invalid, try again")
    else:
        file=open(filename,"r")

    #have user enter the wattage
    wattageValid=False
    if userSelectsWattage:
        while not wattageValid:
                try:
                    wattage= float(input("Enter wattage: "))
                    wattageValid=True
                except:
                    print("Wattage NaN, try again")
    
    #have user enter the distance, then convert to metric
    prob_second=False
    distanceValid=False
    if userSelectsDistance:
        while not distanceValid:
                try:
                    distance= float(input("Enter distance: "))
                    prob_second=True
                    unit=float(input("Feet (0) or Meters (1)?: "))
                    distanceValid=True
                    if(unit == 0.0):
                        lux_candela_ratio= 0.09290304*distance*distance
                    elif(unit == 1.0):
                        lux_candela_ratio=distance*distance
                    else:
                        print("Unit number is not a 1 or 0, try again")
                        distanceValid=False
                except:
                    if(not prob_second):
                        print("Distance NaN, try again")
                    elif(prob_second):
                        print("Unit not an int, try again")
                    else:
                        print("something is wrong with distance valid")

    #Take input file and seperate into parts
    with open(entry_file_path+filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

        for lux in range(0,len(lines),3):
            Lux.append(lines[lux])                   # Lux Values
        for ha in range(2,len(lines),3):
            HA.append(int(lines[ha]))                # Horizontal Angle Values
        for va in range(1,len(lines),3):
            try:
                VA.append(int(lines[va]))                # Vertical Angle Vales
                i=i+1
            except:
                i=i-1
               #print("Error is at "+str(i))

    file.close()
    lines.clear()

    print("File Output: ")
    print("Lux: " + str(Lux))
    print("VA : " + str(VA))
    print("HA : " + str(HA)+"\n")

    #Determine number of Lux values
    print("Calculations from file:")
    len_LUX=len(Lux)
    print("Num Lux Values: " + str(len(Lux)))

    #Determine When Vertical axis rotates 360
    len_HA=HA.index(360)+1
    print("Num vertival angles: " +str(len_HA))
    len_VA= int(len(VA)/len_HA)
    print("Num Horizontal angles: "+str(len_VA)+"\n")

    #find unique steps for horizontal and vertical axis
    print("Unique Horizontal and Vertical angles:")
    steps_HA= HA[0:len_HA]
    print("HA: "+str(steps_HA))
    z=0
    while z<len_VA:
        steps_VA.append(VA[z*len_HA])
        z += 1
    print("VA: "+str(steps_VA))

    #After this point, this code only works for the way the measuremnt sweep data is setup

    #reorders lux so it reads in order
    i=0
    j=0
    z=0
    dir=False
    while(i<len_VA):
        dir=not dir
        temp_Lux.clear()
        while (j<len_HA):
            if(dir):
                #F_Lux.append(Lux[i*len_HA+j])
                F_Lux.append(Lux[z+j])
            else:
                temp_Lux.append(Lux[z+j])
                #print(z+j)
            j +=1
        z+=37
        if len(temp_Lux)>0:
            temp_Lux.reverse()
            #temp=temp_Lux.pop(0)
            #temp_Lux.append(temp)
            F_Lux.extend(temp_Lux)
        j=0
        i +=1
    print(len(F_Lux))
    print("Lux: "+str(F_Lux))

    #creating ies file through bit banging
    filename_ies= filename[:-4]+".ies"
    try:
        file_ies=open(ies_file_path+filename_ies,"w")
    except:
        print("Whoops ies file won't open")
    file_ies.write("IESNA:LM-63-23232323232323232323232323232323\n")
    file_ies.write("[TEST] Senior Design Light Test 1\n")
    file_ies.write("[MANUFAC] SimplyLEDs\n")
    file_ies.write("TILT = NONE\n")
    #37.161216 is for the conversion from lux to candela at 20 ft
    #19=number of horizontal angles
    #37= number of vertical angles
    file_ies.write("1 -1 "+ str(lux_candela_ratio)+" 19 37 1 1 1 0 0\n")
    #150 is the wattage
    file_ies.write("1 1 "+str(wattage)+"\n")
    #set of vertical angles (ies viewpoint)
    file_ies.write("0.00 10.00 20.00 30.00 40.00 50.00 60.00 70.00 80.00")
    file_ies.write(" 90.00 100.00 110.00 120.00 130.00 140.00 150.00 160.00 170.00 180.00\n")
    #set of horizontal angles (ies viewpoint)
    file_ies.write("0.00 10.00 20.00 30.00 40.00 50.00 60.00 70.00 80.00 90.00 100.00 110.00 120.00 ")
    file_ies.write("130.00 140.00 150.00 160.00 170.00 180.00 190.00 200.00 210.00 220.00 230.00 240.00 ")
    file_ies.write("250.00 260.00 270.00 280.00 290.00 300.00 310.00 320.00 330.00 340.00 350.00 360.00\n")
      
    #averaging 1st column so it doesn't through an error
    #if first column is really off then you know that you have bad data
    i=0
    z=0
    while i<37:
        z= z+float(F_Lux[i])
        i=i+1
    z=round(z/37,1)
    print(z)
    i=0
    #writting actual lux values
    while i<37:
        #file_ies.write(str(F_Lux[i])+" "+str(F_Lux[i+37])+" "+str(F_Lux[i+74])+" "+str(F_Lux[i+111])+" ")
        file_ies.write(str(z)+" "+str(F_Lux[i+37])+" "+str(F_Lux[i+74])+" "+str(F_Lux[i+111])+" ")
        file_ies.write(str(F_Lux[i+148])+" "+str(F_Lux[i+185])+" "+str(F_Lux[i+222])+" "+str(F_Lux[i+259])+" ")
        file_ies.write(str(F_Lux[i+296])+" "+str(F_Lux[i+333])+" "+str(F_Lux[i+370])+" "+str(F_Lux[i+407])+" ")
        file_ies.write("0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")
        i=i+1
    file_ies.close()
    print(lux_candela_ratio)
#allows program to run by itself for debugging purposes if run_6 is true
if run_6:
    Convert_IES()