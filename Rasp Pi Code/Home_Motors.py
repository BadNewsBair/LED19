#!/usr/bin/env python
import time
import smbus
import sys
import RPi.GPIO as GPIO
import pygame

#**Home_Motors**
#Allows the user to position the motors to the home position by pressing the arrow keys
#Has an explanatory GUI. Pressing exit or enter returns the user to menu_GUI

#set this to true to run module by itself (must be set to false for main program to work)
Run_2= False

def Home_Motors():
    #setup pygame screen
    x=pygame.init()

    #colors
    BLACK=(0,0,0);WHITE=(255,255,255);    RED= (255,  0,  0)
    BLUE =(0,  0,255);
    #constants
    screenSize=(700,200)
    QUIT_ALL= False
    Task_Selected=False
    #setup
    gameDisplay=pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Senior Design Light Measurement Program - SimplyLED Project')
    clock =pygame.time.Clock()
    gameDisplay.fill(WHITE)
    
    #Display Text
    title_Font = pygame.font.SysFont("monospace", 40)
    title_Font.set_bold(True)
    caption_Font= pygame.font.SysFont("monospace", 30)
    caption_Font.set_bold(True)
    Title = title_Font.render("Homing Motors", 1, BLUE)
    gameDisplay.blit(Title, (20, 0))
    cap_0 = caption_Font.render("Press Arrow Keys to Move Motors", 1, BLACK)
    gameDisplay.blit(cap_0, (20,40))
    cap_1 = caption_Font.render("Top Motor: Up/Down", 1, BLACK)
    gameDisplay.blit(cap_1, (20, 70))
    cap_2 = caption_Font.render("Bottom Motor: Left/Right", 1, BLACK)
    gameDisplay.blit(cap_2, (20, 100))
    cap_3 = caption_Font.render("Press enter to return", 1, BLACK)
    gameDisplay.blit(cap_3, (20, 130))
    
    #update screen with blits
    pygame.display.update()

    #setup motor driver
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    #Assign GPIO numbers.
    V_Limit= 22; HR_Limit=27 ;HL_Limit=17
    H_Pulse=6   ;GND_1=12
    H_Dir=13    ;GND_2=16
    V_Pulse=19  ;GND_3=20
    V_Dir=26    ;GND_4=21

    #Set up Driver outputs.
    GPIO.setup(H_Pulse,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(H_Dir,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(V_Pulse,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(V_Dir,GPIO.OUT,initial=GPIO.LOW)

    #Set up grounds(From Test_Connectivity)
    GPIO.setup(GND_1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(GND_4,GPIO.OUT,initial=GPIO.LOW)
    
    #Variables for motion
    top_Moves_Clk=False
    top_Moves_Cclk=False
    bot_Moves_Clk=False
    bot_Moves_Cclk=False
    #determines how fast motors move
    top_Speed=.15
    bottom_Speed=.3
    
    

    #main loop
    while not (QUIT_ALL or Task_Selected):
        
        #step motors in direction of what arrow key is pressed
        if top_Moves_Clk:
            GPIO.output(V_Dir,GPIO.HIGH)
            time.sleep(top_Speed)
            GPIO.output(V_Pulse,GPIO.HIGH)
            time.sleep(top_Speed)
            GPIO.output(V_Pulse,GPIO.LOW)
        elif top_Moves_Cclk:
            GPIO.output(V_Dir,GPIO.LOW)
            time.sleep(top_Speed)
            GPIO.output(V_Pulse,GPIO.HIGH)
            time.sleep(top_Speed)
            GPIO.output(V_Pulse,GPIO.LOW)
        elif bot_Moves_Clk:
            GPIO.output(H_Dir,GPIO.HIGH)
            time.sleep(bottom_Speed)
            GPIO.output(H_Pulse,GPIO.HIGH)
            time.sleep(bottom_Speed)
            GPIO.output(H_Pulse,GPIO.LOW)
        elif bot_Moves_Cclk:
            GPIO.output(H_Dir,GPIO.LOW)
            time.sleep(bottom_Speed)
            GPIO.output(H_Pulse,GPIO.HIGH)
            time.sleep(bottom_Speed)
            GPIO.output(H_Pulse,GPIO.LOW)       

        #read keyboard strokes
        for event in pygame.event.get():
            
            #user clicked exit in gui
            if event.type == pygame.QUIT:
                QUIT_ALL=True
            x=0
            
            #user pushed a key
            if event.type==pygame.KEYDOWN:
                
                #update move variables
                if event.key== pygame.K_DOWN:
                    top_Moves_Clk=False
                    top_Moves_Cclk=True
                    bot_Moves_Clk=False
                    bot_Moves_Cclk=False
                if event.key== pygame.K_UP:
                    top_Moves_Clk=True
                    top_Moves_Cclk=False
                    bot_Moves_Clk=False
                    bot_Moves_Cclk=False     
                if event.key== pygame.K_LEFT:
                    top_Moves_Clk=False
                    top_Moves_Cclk=False
                    bot_Moves_Clk=False
                    bot_Moves_Cclk=True
                if event.key==pygame.K_RIGHT:
                    top_Moves_Clk=False
                    top_Moves_Cclk=False
                    bot_Moves_Clk=True
                    bot_Moves_Cclk=False
                    
                #exit
                if event.key== pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                    QUIT_ALL=True
            #user released a key
            if event.type==pygame.KEYUP:
                top_Moves_Clk=False
                top_Moves_Cclk=False
                bot_Moves_Clk=False
                bot_Moves_Cclk=False

    pygame.quit()

        
    

#Run code by itself if boolean run2 is true
if Run_2:
    Home_Motors()

    
