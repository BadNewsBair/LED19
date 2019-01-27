#!/usr/bin/python
import pygame
#Gui that allows user to select which program they want to run. Uses pygame in order to be able to
#detect keyboard strokes. User navigates the different choices using the up and down arrow keys and
#makes a choice by pressing enter. The user can exit at any time

def GUI_Menu():
    #intialize pygame
    x=pygame.init()

    #colors
    BLACK=(0,0,0);  WHITE=(255,255,255);    RED= (255,0,0)
    BLUE =(0,0,255)
    
    #constants
    screenSize=(850,500) #width,height
    text_Start=170 #height at which the text starts
    Curs_H=60 #height of cursor
    D_Curs_H=text_Start #defualt height of cursor
    Menu_Options= ['1.Test Connectivity','2.Home Motors','3.Measurements Sweep','4.Convert to IES',
                    'EX.Documentation']
    #variables
    Cursor_Sel=0 #part of menu that is selected by cursor
    QUIT_ALL= False #exits entire program if true
    Task_Selected=False #program selected

    #**Setup GUI**
    gameDisplay=pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Senior Design Light Measurement Program - SimplyLED Project')
    clock =pygame.time.Clock()
    title_Font = pygame.font.SysFont("monospace", 80)
    title_Font.set_bold(True)
    options_Font = pygame.font.SysFont("monospace", 30)
    options_Font.set_bold(True)
    comments_Font= pygame.font.SysFont("calibri", 20)
    

    #Main Loop (quits only when exit pressed or selection made)
    while not (QUIT_ALL or Task_Selected):
        
        clock.tick(30)
        pygame.display.update()
        gameDisplay.fill(WHITE)
        
        #Draw Device
        #Device = pygame.image.load("h.jpg")
        #Device =pygame.transform.scale(Device, (650, 500))
        Device = pygame.image.load("Device_A.jpg")
        Device =pygame.transform.scale(Device, (400, 500))
        #Device = pygame.image.load("Device_B.jpg")
        #Device =pygame.transform.scale(Device, (400, 500))
        gameDisplay.blit(Device, (500,0))

        #Draw Title Text
        Title1= title_Font.render("IES File", 1, BLUE)
        gameDisplay.blit(Title1, (0, 20))
        Title2= title_Font.render("Generator", 1, BLUE)
        gameDisplay.blit(Title2, (0, 70))
        #Draw Options Text
        Opt_0 = options_Font.render(Menu_Options[0], 1, BLACK)
        gameDisplay.blit(Opt_0, (60, text_Start))
        Opt_1 = options_Font.render(Menu_Options[1], 1, BLACK)
        gameDisplay.blit(Opt_1, (60, text_Start+30))
        Opt_2 = options_Font.render(Menu_Options[2], 1, BLACK)
        gameDisplay.blit(Opt_2, (60, text_Start+60))
        Opt_3 = options_Font.render(Menu_Options[3], 1, BLACK)
        gameDisplay.blit(Opt_3, (60, text_Start+90))
        Opt_4 = options_Font.render(Menu_Options[4], 1, BLACK)
        gameDisplay.blit(Opt_4, (60, text_Start+120))
        #Draw comments text
        app_note0 = comments_Font.render("*Up and down keys are for navigation", 1, BLACK)
        gameDisplay.blit(app_note0, (60, text_Start+180))
        app_note1 = comments_Font.render("*Press enter to select process, then follow cmd prompts", 1, BLACK)
        gameDisplay.blit(app_note1, (60, text_Start+195))
        app_note2 = comments_Font.render("*Crtl then c will exit process once selected", 1, BLACK)
        gameDisplay.blit(app_note2, (60, text_Start+210))
        app_note3 = comments_Font.render("**Lower case c, no caps lock", 1, BLACK)
        gameDisplay.blit(app_note3, (60, text_Start+225))
        
        #Draw Cursor
        Curs_H=Cursor_Sel*30+ D_Curs_H
        pygame.draw.lines(gameDisplay, RED, False, [[30, 0+Curs_H], [45, 15+Curs_H], [30, 30+Curs_H]], 5)

        #check user input
        for event in pygame.event.get():
            
            #user clicked exit in gui
            if event.type == pygame.QUIT:
                QUIT_ALL=True
                
            #user pushed a key on keyboard
            if event.type==pygame.KEYDOWN:
                #up down arrow keys with wrap around
                if event.key== pygame.K_DOWN:
                    if Cursor_Sel== len(Menu_Options)-1:
                        Cursor_Sel=0
                    else:
                        Cursor_Sel=Cursor_Sel+1
                if event.key== pygame.K_UP:
                    if Cursor_Sel==0:
                        Cursor_Sel= len(Menu_Options)-1
                    else:
                        Cursor_Sel=Cursor_Sel-1
                #making a selection
                if event.key== pygame.K_RETURN:
                    print("\nRunning "+ Menu_Options[Cursor_Sel])
                    Task_Selected=True

    pygame.quit()
    
    if QUIT_ALL:
        Cursor_Sel=16
    #Value returned by function is the postion of the cursor
    #when selection is made
    return Cursor_Sel
