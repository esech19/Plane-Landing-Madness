from cmu_112_graphics import *
from playsound import playsound
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
    font = 'Hevletica 26 bold'
    canvas.create_rectangle(0,0,app.width,app.height,fill='red')
    canvas.create_text(app.width/2, 200, text='ATC Simulator', font=font)
    canvas.create_text(app.width/2, 400, text='Choose a Difficulty', font=font)
    canvas.create_text(app.width/2, 500, text='Press E for Easy', font=font)
    canvas.create_text(app.width/2, 600, text= 'Press M for Intermediate', font=font)
    canvas.create_text(app.width/2, 700, text='Press H for Expert', font=font)

def startMode_keyPressed(app, event):
    if event.key == 'e':
        app.level = 'Easy'
    elif event.key == 'm':
        app.level = 'Medium'
    elif event.key == 'h':
        app.level = 'Hard'

    #make map

    app.map = Map(app,app.level)

    #initialize runwaylist

    if app.level == 'Easy':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]

    elif app.level == 'Medium':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]
        
    elif app.level == 'Hard':
        app.map.runways = [app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
        app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]



    '''
    print(app.map.parkingSpotCoords)
    if app.map.parkingSpotCoords == [ ]:
        print('empty')
    '''

    app.map.taxiways.append(app.map.generateTaxiway((100,200),(200,300)))

    #generate taxiways:
    '''
    parkingSpotCount = 0
    while parkingSpotCount < len(app.map.parkingSpotCoords):
        for runway in app.map.runways:
            for landingCoord in runway.landingInfo:
                parkingSpotCount +=1
                app.map.taxiways.append(app.map.generateTaxiway(runway.landingInfo[landingCoord][2],app.map.parkingSpotCoords[parkingSpotCount]))
    '''

    


    #change mode to gamemode 
    app.mode = 'gameMode'

#help mode #based on code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

def helpMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_rectangle(0,0,app.width,app.height,fill='yellow')
    canvas.create_text(app.width/2, 150, text='HELP', font=font)
    canvas.create_text(app.width/2, 250, text='click and drag to make planes land', font=font)
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game', font=font)

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

def appStarted(app):
    #initialize level
    app.level = 'Easy'
    #start screen
    app.map = Map(app,app.level)

    #runways to generate
    app.map.runways = []
    #[app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app),
    #app.map.generateRunway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],app)]
    #app.map.runways= [Runway(app.map.rw1,(200,500),0),Runway(app.map.runwayImages[random.randint(0,len(app.map.runwayImages)-1)],(1000,500),0)]

    app.mode = 'startMode'
    #initialize map object

    #playsound('airplane-landing-01.mp3')

    #timedelaykk 
    app.timerDelay = 10
    #sprite list
    '''
    app.planeSprites=[app.plane1Sprite,app.plane2Sprite,app.plane3Sprite,app.plane4Sprite]
    '''
    app.userInterface = False

    #plane listkhjj
    app.planes = [ ]

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

    #add planes over time   

def addPlane(app):
    y =  random.choice((-10,app.height/3,2*app.height/3))
    if y < 0: 
        x = random.choice((app.width/4,app.width/2,3*app.width/4))
        xspeed = 0
        if app.map.level == 'Easy':
            yspeed = 0.5

        elif app.map.level == 'Medium':
            yspeed = 1

        elif app.map.level == 'Hard':
            yspeed = 2
    else: 
        x = -10
        yspeed=0
        xspeed = random.randint(0,5)
        if app.map.level == 'Easy':
            xspeed = 0.5

        elif app.map.level == 'Medium':
            xspeed = 1

        elif app.map.level == 'Hard':
            xspeed = 2

    #add new generated planes to app.planes
    '''
    sprite = app.planeSprites[random.randint(0,len(app.planeSprites)-1)].rotate(50)
    '''
    app.planes.append(Airplane(xspeed,yspeed,x,y,app))

def gameMode_keyPressed(app,event):
    #trigger help mode
    if event.key == 'h':
        app.mode = 'helpMode'
    if event.key == 'p':
        app.planes.append(Airplane(0,-0.5,app.width/2,app.height/2,app))
    if app.isGameOver:
        if event.key == 'r':
            appStarted(app)
    '''
    if event.key == 'Enter':
        for plane in app.planes:
            if plane.isSelected:
                plane.isRerouting = False
                plane.isPathChange = False
                plane.isSelected = False
    '''       


def changeState(app,x,y,plane):
    #if plane.isSelected == True:
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
            print('deselecting plane')
            plane.pathChange = False
            plane.isSelected = False
    
    elif plane.state == 'runway' and plane.landed == True:

        if ((((8.14*app.width)/10)<x<9.9*app.width)/10) and (3*app.height/30) < y < (4*app.height/30):
           # plane.path =  taxipath
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
    print(event.x,event.y)
    #for runway in app.map.runways:
        #print(app.map.areLegalCorners(runway,app))
    for plane in app.planes:

        if plane.isSelected and plane.pathChange and (abs(plane.x - event.x) < 20 and (abs(plane.y - event.y)) < 30):
            print('entering right clause')
            plane.isRerouting = True

        elif plane.isSelected and plane.pathChange == False:
            print('clause 2')
            changeState(app, event.x, event.y, plane)
        
        elif (abs(plane.x - event.x) < 20 and (abs(plane.y - event.y)) < 30):
            print('clause 1')
            plane.isSelected = True

        elif plane.isSelected and (abs(plane.x - event.x) > 20 and (abs(plane.y - event.y)) > 30):
            changeState(app, event.x, event.y, plane)
        

     
def gameMode_mouseDragged(app, event):
    for plane in app.planes:
        if plane.isSelected and plane.pathChange and plane.isRerouting:
            print('changing path') #is path ready to be changed
            plane.path.append((event.x, event.y))
            print('path was changed')
          #path is done being changed


def gameMode_timerFired(app):

    # check for collision
    '''
    for plane in app.planes:
        planeList = copy.copy(app.planes)
        planeList.pop(planeList.index(plane))
        for plane2 in planeList:
            if (plane.x < plane2.x + plane2.width and 
            plane.x + plane.width > plane2.x and 
            plane.y < plane2.height + plane2.y and 
            plane.y + plane.height > plane2.y
            and (plane.state == plane2.state)):
                app.collisionCoords = ((plane.x+plane2.x)//2,(plane.y+plane2.y)//2)
                app.collision = True
                app.isGameOver = True
    '''


    #for plane sprites
    for plane in app.planes:
        plane.plane1SpriteCounter = (1 + plane.plane1SpriteCounter) % len(plane.plane1Sprites)
        plane.plane1Sprite = plane.plane1Sprites[plane.plane1SpriteCounter]

    #determines when planes come into existence
    #app.time = int((time.time()-app.timeInitial)//1)

    #print(app.time)

    if app.map.level == 'Easy':
        if app.time % 250  == 0:
            addPlane(app)
    elif app.map.level == 'Medium':
        if app.time % 125 == 0:
            addPlane(app)
    elif app.map.level == 'Hard':
        if app.time % 75 == 0:
            addPlane(app)
    app.time += 1

    for plane in app.planes:
        for runway in app.map.runways:
            plane.isLanding(runway)
            plane.isLanded()
        
        if plane.isCompleted():
            app.planes.pop(app.planes.index(plane))
            app.score+=100
    
    #initial movement of planes and check for gameover
    for plane in app.planes:
        if (plane.state == 'air') and (plane.x>app.width or plane.y>app.height):
            app.isGameOver = True


        ## moving after path is generated
        plane.changePath()
    

def drawUserInterface(app,canvas):
    for plane in app.planes:
        if plane.isSelected:
            canvas.create_rectangle(app.width-(2*app.width/10),0,app.width,(3*app.height/10),fill='lightblue',width = 5)
            if plane.state == 'air':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (3*app.height/30), ((9.9*app.width)/10), (4*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(3.5*app.height/30), text='Change Path', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.landed == False and plane.state  == 'runway':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((3.5)*app.height/30), text= plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.landed == True and plane.state == 'runway':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (3*app.height/30), ((9.9*app.width)/10), (4*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(3.5*app.height/30), text='Taxi', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
            elif plane.state == 'taxi':
                canvas.create_text((2*app.width-(2*app.width/10))/2,((1.5)*app.height/30), text=plane.callSign, font = 'Arial 18 bold')
                canvas.create_rectangle((8.14*app.width)/10, (5*app.height/30), ((9.9*app.width)/10), (6*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(5.5*app.height/30), text='Speed Up', font = 'Arial 15 bold')
                canvas.create_rectangle((8.14*app.width)/10, (7*app.height/30), ((9.9*app.width)/10), (8*app.height/30), fill='lightGreen',width=3)
                canvas.create_text((2*app.width-(2*app.width/10))/2,(7.5*app.height/30), text='Slow Down', font = 'Arial 15 bold')
                


def drawPlanes(app, canvas):
    #plane sprites
    if app.planes!=[]:
        for plane in app.planes:
            plane.drawPlane(canvas)
            plane.drawPath(canvas)
            if plane.isSelected:
                canvas.create_oval(plane.x-5,plane.y-5,plane.x+5,plane.y+5, fill='red')

def drawScore(app,canvas):
    canvas.create_rectangle(0,0,app.width/10,app.height/20,fill='white',outline='black',width='3')
    canvas.create_text(app.width/20,app.height/40,text=f'Score = {app.score}', font='Arial 14 bold', fill='red')

def drawGameOver(app,canvas):
    if app.isGameOver == True:
        if app.collision == True:
            canvas.create_image(app.collisionCoords[0],app.collisionCoords[1],image=ImageTk.PhotoImage(app.collisionSprite))
        canvas.create_rectangle(0,0,app.width,app.height, fill='orange')
        canvas.create_text(app.width/2,app.height/2,text='you lost, press R to restart', font='Arial 30 bold')
        
        

    
def gameMode_redrawAll(app, canvas):
    app.map.drawMap(app, canvas)
    drawScore(app,canvas)
    drawPlanes(app,canvas)
    drawUserInterface(app,canvas)
    drawGameOver(app,canvas)



runApp(width=1750, height=800)