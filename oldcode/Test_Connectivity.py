#Tests the limit switches to ensure that they are connected properly
import time
import smbus
import sys
import RPi.GPIO as GPIO
from decimal import Decimal
#Make this true to run module by itself (No Main)
Run_1=False
#Make this true to test connectivity of limit switches
Test_LS=False

def Test_Connectivity():
    #clear the pins
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    #Assign GPIO numbers.
    V_Limit= 22 ;HR_Limit=27 ;HL_Limit=17
    H_Pulse=6   ;H_Pulse_Check=12
    H_Dir=13    ;H_Dir_Check=16
    V_Pulse=19  ;V_Pulse_Check=20
    V_Dir=26    ;V_Dir_Check=21

    #Set limit switch pins as inputs pulled down.
    GPIO.setup(V_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HR_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HL_Limit,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    #Set Driver pins as outputs, initialize as gnd
    GPIO.setup(H_Pulse,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(H_Dir,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(V_Pulse,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(V_Dir,GPIO.OUT,initial=GPIO.LOW)
    
    #Set Driver checking pins as inputs pulled down
    GPIO.setup(H_Pulse_Check,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(H_Dir_Check,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(V_Pulse_Check,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(V_Dir_Check,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    #Booleans
    I2C_Works=False
    V_Hit=False ;HR_Hit=False ;HL_Hit=False
    H_Pulse_Works=False  ;H_Dir_Works=False
    V_Pulse_Works=False  ;V_Dir_Works=False
    
    #setup light sensor
    DEVICE = 0x23
    READ = 0x20
    bus = smbus.SMBus(1)
    def readLight(addr=DEVICE):
        data = bus.read_i2c_block_data(addr,READ)
        return ((data[1] + (256 * data[0])) / 1.2)

    #test i2c connection
    print("Testing Light Sensor Connection")
    
    try:
        print("Sensor Lux is: "+ str(int(readLight())))
        print("I2C communicating sucessfully \n")
        I2C_Works=True
    except:
        print("Light sensor connection faulty")
        print("Please Check Pins \n")
        
    
    #Test Motor Driver Connections
    print("Testing motor driver connections")
    print("Power off motor driver if you don't want it")
    print("to move. Then type anything and press enter")
    print("to continue\n")
    #raw_input("Press Enter")
    input("Press Enter")
    #Test H pulse
    GPIO.output(H_Pulse,GPIO.HIGH)
    time.sleep(.05)
    H_Pulse_Works=GPIO.input(H_Pulse_Check)
    time.sleep(.05)
    GPIO.output(H_Pulse,GPIO.LOW)
    time.sleep(.05)
    #Test H dir
    GPIO.output(H_Dir,GPIO.HIGH)
    time.sleep(.1)
    H_Dir_Works=GPIO.input(H_Dir_Check)
    time.sleep(.05)
    GPIO.output(H_Dir,GPIO.LOW)
    time.sleep(.05)
    #Test V Pulse
    GPIO.output(V_Pulse,GPIO.HIGH)
    time.sleep(.05)
    V_Pulse_Works=GPIO.input(V_Pulse_Check)
    time.sleep(.05)
    GPIO.output(V_Pulse,GPIO.LOW)
    time.sleep(.05)
    #Test V Dir
    GPIO.output(V_Dir,GPIO.HIGH)
    time.sleep(.05)
    V_Dir_Works=GPIO.input(V_Dir_Check)
    time.sleep(.05)
    GPIO.output(V_Dir,GPIO.LOW)
    time.sleep(.05)
    
    
    #print results so far
    print("So far we've found that...")
    print("I2C Works?     "+str(I2C_Works))
    print("H Pulse Works? "+str(H_Pulse_Works))
    print("H Dir Works?   "+str(H_Dir_Works))
    print("V Pulse Works? "+str(V_Pulse_Works))
    print("V Dir Works?   "+str(V_Dir_Works)+"\n")
    
    if(Test_LS): 
        #test limit switches
        print("Testing limit switches")
        print("Push limit switches sequentially or"
              +" push crtl c to cancel")
        while not(V_Hit and HR_Hit and HL_Hit):
            if GPIO.input(HR_Limit):
                HR_Hit=True
                print("Horizontal home LS hit...so its connected")
                time.sleep(1)
            if GPIO.input(HL_Limit):
                HL_Hit=True
                print("Horizontal end LS hit...so its connected")
                time.sleep(1)
            if GPIO.input(V_Limit):
                V_Hit=True
                print("Vertical LS hit...so its connected")
                time.sleep(1)
                
                
        #print off final results
        print("\n\nFinal Results...")
        print("I2C Works?       "+str(I2C_Works))
        print("H Pulse Works?   "+str(H_Pulse_Works))
        print("H Dir Works?     "+str(H_Dir_Works))
        print("V Pulse Works?   "+str(V_Pulse_Works))
        print("V Dir Works?     "+str(V_Dir_Works))
        print("H Home LS Works? "+str(HR_Hit))
        print("H End LS Works?  "+str(HL_Hit))
        print("V LS Works?      "+str(V_Hit))
        
        
        if (I2C_Works and H_Pulse_Works and H_Dir_Works and
            V_Pulse_Works and V_Dir_Works and HR_Hit and
            HL_Hit and V_Hit):
            print("\n\nEveything's connected... we think")
            print("Clear for measurement sweep")
        
    #clear the pins
    GPIO.cleanup()
    
#program runs by itself
if Run_1:
    Test_Connectivity()