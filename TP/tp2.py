from cmu_112_graphics import *
from classes import *
from mapclass import *
import random
import time
import decimal
import math
import copy

def roundHalfUp(d): # from https://www.cs.cmu.edu/~112/notes
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#beginning mode #based on code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

def startMode_redrawAll(app, canvas):
    font = 'Times 60 bold'
    canvas.create_rectangle(0,0,app.width,app.height,fill='Black')
    canvas.create_text(app.width/2, 200, text='Plane Landing Madness', font=font, fill = 'lightblue')
    canvas.create_text(app.width/2, 400, text='Press N for Novice Difficulty', font='Arial 30 bold italic',fill='white')
    canvas.create_text(app.width/2, 500, text= 'Press M for Intermediate Difficulty', font='Arial 30 bold italic', fill='white')
    canvas.create_text(app.width/2, 600, text='Press E for Expert Difficulty', font='Arial 30 bold italic',fill='white')
    canvas.create_text(app.width/2, 700, text='In Game, Press H for Instructions on How to Play', font='Arial 20',fill='yellow')
    

def startMode_keyPressed(app, event):
    if event.key == 'n':
        app.level = 'Easy'
    
    elif event.key == 'm':
        app.level = 'Medium'
        
    elif event.key == 'e':
        app.level = 'Hard'
        
    #make map

    app.map = Map(app,app.level)

    #initialize runwaylist

    if app.level == 'Easy':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]
        

    elif app.level == 'Medium':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]
        
    elif app.level == 'Hard':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]

    #generate taxiways:
    
    parkingSpotCount = 0
    while parkingSpotCount < len(app.map.parkingSpotCoords):
        for runway in app.map.runways:
            for landingCoord in runway.landingInfo:
                app.map.taxiways.append(app.map.generateTaxiway(runway.landingInfo[landingCoord][2],app.map.parkingSpotCoords[parkingSpotCount]))
                parkingSpotCount +=1

    #change mode to gamemode 
    app.mode = 'gameMode'

#help mode #based on code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

def helpMode_redrawAll(app, canvas):
    font = 'Times 60 bold'
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    canvas.create_text(app.width/2, 150, text='How to Play', font=font, fill='white')
    canvas.create_text(app.width/2, 300, text='Earn points by landing as many planes as possible. To land a plane, select it, select the "change path" option, and select the plane again to drag it to a runway.', font='Arial 15', fill='white')
    canvas.create_text(app.width/2, 350, text='Once landed, select the taxi option to taxi the plane to its gate.', font='Arial 15', fill='white')
    canvas.create_text(app.width/2, 400, text="Don't let any planes crash or get away! ", font='Arial 15', fill='white')
    canvas.create_text(app.width/2, 550, text='Press any key to return to the game', font='Arial 20 bold', fill='yellow')

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

def appStarted(app):
    #pygame.init()
    #app.mainTheme = Sound("song.mp3") #song from https://www.youtube.com/watch?v=YHEifuLCSIY
    # Ducktales Remastered Theme Song
    #app.landingSound = Sound('landsound.mp3')

    #initialize level
    app.level = 'Easy'
    #start screen
    app.map = Map(app,app.level)

    #runways to generate
    app.map.taxiways = []
    app.map.runways = []

    app.mode = 'startMode'
   
    #playsound('airplane-landing-01.mp3')

    #timedelay
    app.timerDelay = 1
  
    app.userInterface = False

    #plane list
    app.planes = [ ]

    #in case of crash
    app.plane1Crash = ''
    app.plane2Crash = ''

    app.planeLost = ''


    #score
    app.score = 0

    #gameover, collisions
    app.collision = False
    app.collisionCoords = (0,0)
    app.collisionSpriteUnscaled = app.loadImage('collision .png')
    app.collisionSprite = app.scaleImage(app.collisionSpriteUnscaled, 5/10)
    app.isGameOver = False

    #time check
    app.time = 0
    app.timeInitial = time.time()

def addPlane(app):
    y =  random.choice((-10,random.randint(int(app.height/3),int(2*(app.height/3)))))
    if y < 0: 
        x = random.randint(int(app.width/4),int(3*app.width/4))
        xspeed = 0
        if app.map.level == 'Easy':
            yspeed = 0.5

        elif app.map.level == 'Medium':
            yspeed = 0.75

        elif app.map.level == 'Hard':
            yspeed = 1
    else: 
        x = -10
        yspeed=0
        if app.map.level == 'Easy':
            xspeed = 0.5

        elif app.map.level == 'Medium':
            xspeed = 0.75

        elif app.map.level == 'Hard':
            xspeed = 1

    app.planes.append(Airplane(xspeed,yspeed,x,y,app))

def gameMode_keyPressed(app,event):
    #trigger help mode
    if event.key == 'h':
        app.mode = 'helpMode'
    if app.isGameOver or app.collision:
        if event.key == 'r':
            appStarted(app)

def changeState(app,x,y,plane):

    if plane.state == 'air':
        #change path btn bound box
        if ((((8.14*app.width)/10)<x<(9.9*app.width)/10) and ((3*app.height/30) < y < (4*app.height/30))):
            
            plane.path = [ ] 
            plane.pathChange = True                    

        elif (((((8.14*app.width)/10)<x<9.9*app.width)/10) and ((5*app.height/30) < y < (6*app.height/30))):
            
            plane.speedUp(0.5)

        elif ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (7*app.height/30) < y < (8*app.height/30):

            plane.slowDown(0.5)
        
        else:
            plane.pathChange = False
            plane.isSelected = False
    
    elif plane.state == 'runway' and plane.landed == True:

        if ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (3*app.height/30) < y < (4*app.height/30):
            print('taxi selected')
            for taxiway in app.map.taxiways:
                if  (taxiway.path[0][0]-10<plane.x<taxiway.path[0][0]+10 and taxiway.path[0][1]-10<plane.y<taxiway.path[0][1]+10):
                    print('changing taxipath')
                    newPath = copy.copy(taxiway.path)
                    plane.path = newPath
                    plane.pathChange = True
            plane.state = 'taxi'

        elif ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (5*app.height/30) < y < (6*app.height/30):
            plane.speedUp(0.5)

        elif ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (7*app.height/30) < y < (8*app.height/30):
            plane.slowDown(0.5)

        else:
            plane.pathChange = False
            plane.isSelected = False

    elif plane.state == 'runway' and plane.landed == False:

        if ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (5*app.height/30) < y < (6*app.height/30):
            plane.speedUp(0.5)

        elif ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (7*app.height/30) < y < (8*app.height/30):
            plane.slowDown(0.5)

        else:
            plane.pathChange = False
            plane.isSelected = False

    elif plane.state == 'taxi':

        if ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (5*app.height/30) < y < (6*app.height/30):
            plane.speedUp(0.5)

        elif ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (7*app.height/30) < y < (8*app.height/30):
            plane.slowDown(0.5)

        else:
            plane.pathChange = False
            plane.isSelected = False


def gameMode_mousePressed(app,event):

    for plane in app.planes:

        if plane.isSelected and plane.pathChange and (abs(plane.x - event.x) < 20 and (abs(plane.y - event.y)) < 30):
            
            plane.isRerouting = True

        elif plane.isSelected and plane.pathChange == False:
            
            changeState(app, event.x, event.y, plane)
        
        elif (abs(plane.x - event.x) < 20 and (abs(plane.y - event.y)) < 30):
            
            plane.isSelected = True

        elif plane.isSelected and (abs(plane.x - event.x) > 20 and (abs(plane.y - event.y)) > 30):
            changeState(app, event.x, event.y, plane)
        

     
def gameMode_mouseDragged(app, event):
    for plane in app.planes:
        if plane.isSelected and plane.pathChange and plane.isRerouting:
            plane.path.append((event.x, event.y))

          #path is done being changed


def gameMode_timerFired(app):

    # check for collision    #used algorithm idea/general structure from https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
    for plane in app.planes:
        for plane2 in app.planes:
            if plane != plane2:
                if (plane.x < plane2.x + plane2.width and 
                plane.x + plane.width > plane2.x and 
                plane.y < plane2.height + plane2.y and 
                plane.y + plane.height > plane2.y
                and (plane.state == plane2.state)):
                    app.collisionCoords = ((plane.x+plane2.x)//2,(plane.y+plane2.y)//2)
                    app.plane1Crash = plane.callSign
                    app.plane2Crash = plane2.callSign
                    app.collision = True
                    app.isGameOver = True
                    for plane in app.planes:
                        plane.xspeed = 0
                        plane.yspeed = 0
                        plane.pathSpeed = 0 

    
    #for plane 1 sprite
    for plane in app.planes:
        plane.plane1SpriteCounter = (1 + plane.plane1SpriteCounter) % len(plane.plane1Sprites)


    if app.map.level == 'Easy':
        if app.time % 350  == 0:
            addPlane(app)
    
    elif app.map.level == 'Medium':
        if app.time % 300 == 0:
            addPlane(app)

    elif app.map.level == 'Hard':
        if app.time % 250 == 0:
            addPlane(app)
    app.time += 1

    for plane in app.planes:
        for runway in app.map.runways:
            plane.isLanding(runway)
            plane.isLanded()
        
        if plane.isCompleted():
            plane.xspeed = 0
            plane.yspeed = 0
            app.planes.pop(app.planes.index(plane))
            app.score+=100
        
    #initial movement of planes and check for gameover


    
    for plane in app.planes:
        if ((plane.state == 'air') and (plane.x>app.width or plane.y>app.height)):
            app.planeLost = plane.callSign
            app.isGameOver = True
        elif ((plane.state == 'air') and (plane.x>app.width or plane.y>app.height) and (plane.path!=[])):
            app.planeLost = plane.callSign
            app.isGameOver = True
        elif (plane.state == 'air') and (plane.x<0 and (plane.xspeed<0)):
            app.planeLost = plane.callSign
            app.isGameOver = True
        elif (plane.state == 'air') and (plane.y<0 and (plane.yspeed<0)):
            app.planeLost = plane.callSign
            app.isGameOver = True

        ## moving after path is generated
        plane.changePath()
    

def drawUserInterface(app,canvas):
    for plane in app.planes:
        if plane.isSelected:
            canvas.create_rectangle(app.width-(2*app.width/10),0,app.width,(3*app.height/10),fill='lightblue',width = 5)
            if plane.state == 'air':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (3*app.height/30), ((9.9*app.width)/10), (4*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(3.5*app.height/30), text='Change Path', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.landed == False and plane.state  == 'runway':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text='Landing ... ', font = 'Arial 18 bold')
                canvas.create_text((2*app.width-(2*app.width/10))/2,((3.5)*app.height/30), text= plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.landed == True and plane.state == 'runway':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (3*app.height/30), ((9.9*app.width)/10), (4*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(3.5*app.height/30), text='Taxi', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.state == 'taxi':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text='Taxiing ... ', font = 'Arial 18 bold')
                canvas.create_text((2*app.width-(2*app.width/10))/2,((3.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill=app.map.color,width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
                


def drawPlanes(app, canvas):
    #plane sprites
    if app.planes!=[]:
        for plane in app.planes:
            if plane.sprite in plane.plane1Sprites:
                plane.sprite = plane.plane1Sprites[plane.plane1SpriteCounter] 
            plane.drawPlane(canvas)
            plane.drawPath(canvas)
            

def drawScore(app,canvas):
    canvas.create_rectangle(0,0,app.width/10,app.height/20,fill='lightblue',outline='black',width='3')
    canvas.create_text(app.width/20,app.height/40,text=f'Score = {app.score}', font='Arial 14 bold', fill='black')


def drawGameOver(app,canvas):
    if app.isGameOver:
        canvas.create_rectangle(0,0,app.width,app.height, fill='black')
        canvas.create_text(app.width/2,app.height/4,text='GAME OVER!', font='Arial 60 bold', fill='white')
        canvas.create_text(app.width/2,3*app.height/4,text=f'Your Score = {app.score}', font='Times 30 bold', fill='blue')

        if app.collision:
            canvas.create_image(app.collisionCoords[0],app.collisionCoords[1],image=ImageTk.PhotoImage(app.collisionSprite))
            canvas.create_text(app.width/2,2*app.height/4,text=f'{app.plane1Crash} and {app.plane2Crash} Crashed!', font='Arial 40 bold italic', fill='white')
        else:
            canvas.create_text(app.width/2,2*app.height/4,text=f'{app.planeLost} never landed.', font='Arial 30 bold italic', fill='white')
        canvas.create_text(app.width/2,3.7*app.height/4,text="Press the 'R' Key to Restart", font='Arial 20', fill='white')

    
def gameMode_redrawAll(app, canvas):
    app.map.drawMap(app, canvas)
    drawScore(app,canvas)
    drawPlanes(app,canvas)
    drawUserInterface(app,canvas)
    drawGameOver(app,canvas)



runApp(width=1600, height=800)