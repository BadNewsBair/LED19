#!/usr/bin/env python
import webbrowser
import time
import smbus
import sys
import RPi.GPIO as GPIO
from decimal import Decimal

#**Measurment_Sweep**
#Must be homed and setup first to get accurate measurements.
#Gets unique file name from user. Stores data every 10 degrees. Rotates by 360 degrees 12 times
#with top motor and 110 degrees with bottom motor.
#will not run if it can't read sensor.

#application note: ocassionally get invalid data point. Had to alter get average data point
#application note: stepper motors alternate between 15 steps and 16 steps to rotate 10 degrees 
#                  with little error
#application note:process takes less than 10 minutes to run
#application note:file does not save data until process is complete

#change to true to run this module by itself
Run_3=False

def Measurement_Sweep():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    #delay time
    delay=30

    #Assign GPIO numbers.
    V_Limit= 22; HR_Limit=27 ;HL_Limit=17
    H_Pulse=6   ;GND_1=12
    H_Dir=13    ;GND_2=16
    V_Pulse=19  ;GND_3=20
    V_Dir=26    ;GND_4=21

    #Set as outputs.
    GPIO.setup(H_Pulse,GPIO.OUT)
    GPIO.setup(H_Dir,GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(V_Pulse,GPIO.OUT)
    GPIO.setup(V_Dir,GPIO.OUT)

    #Set as inputs pulled down.
    GPIO.setup(V_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HR_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HL_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    #Set up grounds(From Test_Connectivity)
    GPIO.setup(GND_1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_4,GPIO.OUT,initial=GPIO.LOW)

    #Set Motor positions and counts.
    V_Pos = 0
    H_Pos = 0
    V_Count = 0
    H_Count = 0
    #Direction flag
    Dir = False
    Count = 0
    pulseV = 15   #for alternating pulse counts
    pulseH = 15  
    
    
    
    #******************************LIGHT SENSOR / File SETUP******************************************
    #this can change with different sensors
    DEVICE = 0x23
    READ = 0x20
    bus = smbus.SMBus(1)

    #Function that returns light sensor measurement.
    def readLight(addr=DEVICE):
        data = bus.read_i2c_block_data(addr,READ)
        return ((data[1] + (256 * data[0])) / 1.2)
    try:
        readLight()
        readLight()
    except:
        print("I2C sensor not connected")
        print("Connect first then try again")
        return
    #Function that prints light sensor measurement
    def writeAverageLight(H_Pos,V_Pos):
        working=False
        while not working:
            try:
                lux=1.00*int(readLight())
                time.sleep(0.15)
                working=True
                #if lux>350:
                   # print("lux too high")
                #working=False
            except:
                working=False
         #Save light and motor position data to file.
        f.write(str(lux)+"\n") #print >> f, lux
        f.write(str(H_Pos)+"\n") #print >> f, H_Pos
        f.write(str(V_Pos)+"\n")#print >> f, V_Pos
        #show current position in terminal
        print ("Light Level :           " + str(lux) + " lux")
        print ("Horizontal Position:    " + str(H_Pos) + " degrees")
        print ("Vertical Position:      " + str(V_Pos) + " degrees\n") 
    
    #User input for data file name.
    fileNameValid=False
    #filename = raw_input("Enter file name: ")
    while not(fileNameValid):
        filename =input("Enter unique file name: ")
        try:
            f= open("/home/pi/Desktop/LightProgram/Raw_Measurements/"+filename,"a")
            fileNameValid=True
        except:
            print("File name invalid,try again\n")  
    
    #*******************************MOTOR MOTION CODE************************************* 
    print ("\nMeasurements Starting in %d seconds.\nIf your going to leave, do it now\n", delay)
    #11 ten degree rotations (Horizontal loop)
    while H_Count <= 11:
        #direction of top motor's rotation flips each time
        Dir = not Dir
        #11 360 degree rotations (vertical loop)
        while V_Count < (36):
            #use Dir to set motor direction
            if Dir==False:
                GPIO.output(V_Dir,GPIO.LOW)
            else:
                GPIO.output(V_Dir,GPIO.HIGH)
            #read light intensity
            writeAverageLight(H_Pos,V_Pos)

            #step 10 degrees
            i=0
            while i < pulseV:
                GPIO.output(V_Pulse,GPIO.HIGH)
                time.sleep(.02)
                GPIO.output(V_Pulse,GPIO.LOW)
                time.sleep(.02)
                i = i + 1
                
            #alternate betwen 15 steps and 16 steps to reduce error
            if pulseV ==15:
                pulseV=16
            else:
                pulseV=15
            
            #Increment vertical step count and position.
            V_Count = V_Count + 1
            if Dir== True:
                V_Pos = V_Pos + 10
            else:
                V_Pos=V_Pos-10
            Count = Count + 1
            #pulseV = pulseV - 1
                    
        #(Out of Vertical loop)
        #Reset vertical motor step count
        V_Count = 0
        #read light intensity at 360 degrees or zero degrees
        writeAverageLight(H_Pos,V_Pos)

        #Pulse horizontal motor.
        i=0
        while i < pulseH:
            GPIO.output(H_Pulse,GPIO.HIGH)
            time.sleep(.02)
            GPIO.output(H_Pulse,GPIO.LOW)
            time.sleep(1)
            i = i + 1
        
        #alternate betwen 15 steps and 16 steps to reduce error   
        if pulseH == 15:
            pulseH=16
        else:
            pulseH=15
        #Increment vertical step count and position.
        H_Count = H_Count + 1
        H_Pos = H_Pos + 10
        Count = Count + 1
        
    #closing file (it is at this point where the contents actually save)
    f.close()
    #try:
    GPIO.Cleanup()
    print ("Lux Count: " + str(Count))

#runs the function outside of main if value for Run_3 set to true above
if Run_3:
    Measurement_Sweep()