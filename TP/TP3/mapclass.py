import random
from cmu_112_graphics import *
import math
import decimal

def roundHalfUp(d): # from https://www.cs.cmu.edu/~112/notes
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class Map(object):
    def __init__(self,app,level):

        #initializing level variable
        self.level=level

        self.app=app #initialize app
    
        # runways & terminal images ( made by me :) )

        self.rw1Unscaled = app.loadImage('Runway Drawing 27.png') 
        self.rw1 = app.scaleImage(self.rw1Unscaled,5.5/10)
        self.rw2Unscaled = app.loadImage('runway32.png')
        self.rw2 = app.scaleImage(self.rw2Unscaled,5.5/10)
        self.rw3Unscaled = app.loadImage('rw drawing 64.png')
        self.rw3 = app.scaleImage(self.rw3Unscaled,5.5/10)
        self.rw4Unscaled = app.loadImage('rw drawing 81.png')
        self.rw4 = app.scaleImage(self.rw4Unscaled,5.5/10)
        self.terminalUnscaled=app.loadImage('Terminal .png')
        self.terminal=app.scaleImage(self.terminalUnscaled, 6/10)
        self.parkingSpotUnscaled=app.loadImage('parking spots.png')
        self.parkingSpot=app.scaleImage(self.parkingSpotUnscaled, 3/10)

        #list of backgrounds and runways

        #self.backgrounds=[self.background1scaled,self.background2scaled,self.background3scaled,self.background4scaled]
        self.runwayImages=[self.rw1,self.rw2,self.rw3,self.rw4]
        self.runwayFlatImages=[self.rw1.rotate(90, expand=True),self.rw2.rotate(90, expand=True),self.rw3.rotate(90, expand = True),self.rw4.rotate(90, expand = True)]
        self.runways =[ ] #list of runways (initially 0)
        self.taxiways = [ ] #list of taxiways

        #list to check if runway corners are on top of each other 
        self.cornerSets = [ ]

        #sizes
        self.terminalWidth=self.terminal.size[0]
        self.terminalHeight=self.terminal.size[1]

        #coordinates of terminal (for runway generation purposes)
        self.terminalCoords = (app.width/2,app.height/2)
        self.terminalX=self.terminalCoords[0]
        self.terminalY=self.terminalCoords[1]
        self.r=225

        #number of runways
        self.runwayCount = 0

        #parking spot coords
        self.parkingSpotCoords = [ ]
        
        #chosen background for map generation

        self.colors = ['brown','blue','magenta','orange','maroon','green','yellow green','light grey','purple','cyan','lemon chiffon','khaki2','steel blue']
        self.color = self.colors[random.randint(0,len(self.colors)-1)]

        # variables that change based on difficulty of the level
        self.numParkingSpots = 0
        if self.level == 'Hard':
            self.numParkingSpots = 8
        elif self.level == 'Medium':
            self.numParkingSpots = 6
        elif self.level == 'Easy':
            self.numParkingSpots = 4

    #calculate runway corners 

    def getRunwayCorners(self,runwayImage,runwayCoords,angle):

        offsetAngle=(math.pi/2)+angle
        runwayWidth=runwayImage.size[0]
        runwayHeight=runwayImage.size[1]

        rX1CosTheta =  (runwayWidth/2)*math.cos((math.pi/2)+offsetAngle)
        rX1SinTheta =  (runwayHeight/2)*math.sin((math.pi/2)+offsetAngle)
        rX2CosTheta =  (runwayWidth/2)*math.cos(offsetAngle-(math.pi/2))
        rX2SinTheta =  (runwayHeight/2)*math.sin(offsetAngle-(math.pi/2))

        rYCosTheta = (runwayWidth/2)*math.cos(offsetAngle)
        rYSinTheta = (runwayHeight/2)*math.sin(offsetAngle)

        runwaycorners= [
        ((((runwayCoords[0])+rX1CosTheta)+rYCosTheta),(((runwayCoords[1])-rX1SinTheta)-rYSinTheta)),
        ((((runwayCoords[0])+rX2CosTheta)+rYCosTheta),(((runwayCoords[1]-rX2SinTheta)-rYSinTheta))),
        ((((runwayCoords[0])+rX1CosTheta)-rYCosTheta),(((runwayCoords[1]-rX1SinTheta)+rYSinTheta))),
        ((((runwayCoords[0])+rX2CosTheta)-rYCosTheta),(((runwayCoords[1]-rX2SinTheta)+rYSinTheta)))
                ]
        return runwaycorners

    def getRunwayEdges(self,runwayCorners):
        edge1Slope = (runwayCorners[1][1]-runwayCorners[0][1])/(runwayCorners[1][0]-runwayCorners[0][0])
        edge2Slope = (runwayCorners[2][1]-runwayCorners[0][1])/(runwayCorners[2][0]-runwayCorners[0][0])
        edge3Slope = (runwayCorners[3][1]-runwayCorners[1][1])/(runwayCorners[3][0]-runwayCorners[1][0])
        edge4Slope = (runwayCorners[3][1]-runwayCorners[2][1])/(runwayCorners[3][0]-runwayCorners[2][0])

    
    def areLegalCorners(self,corners,app):
        for corner in corners:
            cornerX=corner[0]
            cornerY=corner[1]

            if (((0<cornerX<app.width) == False) or ((0<cornerY<app.height) == False)):
                return False
            
            elif (((self.terminalX-(self.terminalWidth/2)-20)<cornerX<(20+(self.terminalWidth/2)+self.terminalX)) or ((self.terminalY+(self.terminalHeight/2)+20)<cornerY<(self.terminalY-(self.terminalHeight/2)-20)))==True:
                return False
        return True

    def generateRunway(self,runwayImage,app):  #for now, also use this function to make objects and parking spots
        
        if self.parkingSpotCoords == []:
            for i in range(self.numParkingSpots//2): #generate parking spot coordinates
                self.parkingSpotCoords.append((app.width/2+((1/4)*self.terminalWidth),(app.height//2-self.terminalHeight//2)+(700//self.numParkingSpots//2)+((self.terminalHeight//(self.numParkingSpots//2))*i)))
            for i in range(self.numParkingSpots//2):
                self.parkingSpotCoords.append((app.width/2-((1/4)*self.terminalWidth),(app.height//2-self.terminalHeight//2)+(700//self.numParkingSpots//2)+((self.terminalHeight//(self.numParkingSpots//2))*i)))

        runwayWidth = runwayImage.size[0]
        runwayHeight = runwayImage.size[1]
        isLegalRunway = False

        if app.level == 'Easy':

            while isLegalRunway == False:
                if self.runwayCount == 0:
                    xCoord = (random.randint(app.width/2, app.width))
                else:
                    xCoord = (random.randint(0, app.width/2))
                
                yCoord = (random.randint(100, app.height-100))
                runwayCoords=(xCoord,yCoord)

                runwayCorners1 = self.getRunwayCorners(runwayImage,runwayCoords,0)
                runwayCorners2 = self.getRunwayCorners(runwayImage,runwayCoords,(math.pi)/2)

                if self.areLegalCorners(runwayCorners1,app):
                    isLegalRunway = True
                    self.runwayCount+=1
                    self.cornerSets += [runwayCorners1]
                    return (Runway(runwayImage,runwayCoords,runwayCorners1,0))
                elif self.areLegalCorners(runwayCorners2,app):
                    isLegalRunway = True
                    self.runwayCount+=1
                    self.cornerSets += [runwayCorners2]
                    return (Runway(runwayImage,runwayCoords,runwayCorners2,(math.pi/2)))
            return None

        elif app.level == 'Medium':


            while isLegalRunway == False:

                if self.runwayCount == 0:
                    xCoord = (random.randint(0, app.width/2))
                else:
                    xCoord = (random.randint(app.width/2, app.width))
                
                xCoord = (random.randint(0, app.width))
                yCoord = (random.randint(50, app.height-50))
                runwayCoords=(xCoord,yCoord)

                runwayCorners1 = self.getRunwayCorners(runwayImage,runwayCoords,0)
                runwayCorners2 = self.getRunwayCorners(runwayImage,runwayCoords,(math.pi)/2)
                if self.areLegalCorners(runwayCorners1,app):
                    isLegalRunway = True
                    self.cornerSets += [runwayCorners1]
                    return (Runway(runwayImage,runwayCoords,runwayCorners1,0))
                elif self.areLegalCorners(runwayCorners2,app):
                    isLegalRunway = True
                    self.cornerSets += [runwayCorners2]
                    return (Runway(runwayImage,runwayCoords,runwayCorners2,(math.pi/2)))
            return None

        elif app.level == 'Hard':
            if self.runwayCount %2 == 0:
                xCoord = (random.randint(0, app.width/2))
            else:
                xCoord = (random.randint(app.width/2, app.width))

            while isLegalRunway == False:
                xCoord = (random.randint(0, app.width))
                yCoord = (random.randint(20, app.height-20))
                runwayCoords=(xCoord,yCoord)

                runwayCorners1 = self.getRunwayCorners(runwayImage,runwayCoords,0)
                runwayCorners2 = self.getRunwayCorners(runwayImage,runwayCoords,(math.pi)/2)
                if self.areLegalCorners(runwayCorners1,app):
                    isLegalRunway = True
                    self.cornerSets += [runwayCorners1]
                    return (Runway(runwayImage,runwayCoords,runwayCorners1,0))
                elif self.areLegalCorners(runwayCorners2,app):
                    isLegalRunway = True
                    self.cornerSets += [runwayCorners2]
                    return (Runway(runwayImage,runwayCoords,runwayCorners2,(math.pi/2)))
            return None




    def isLegalMove(self,coord,start,end):
        coordX = coord[0]
        coordY = coord[1]
        
        if start[0]<end[0] and start[1]<end[1]:
            #print('entering the right clauses')
            if coordX>=end[0] or coordY>=end[1]:
                
                return False
        elif start[0]<end[0] and start[1]>end[1]:
            if coordX>=end[0] or coordY<=end[1]:
                return False
        elif start[0]>end[0] and start[1]>end[1]:
            if coordX<=end[0] or coordY<=end[1]:
                return False
        elif start[0]>end[0] and start[1]<end[1]:
            if coordX<=end[0] or coordY>=end[1]:
                return False

        return True

        

    def generateTaxiway(self,start,end): #start and end are variables in form of (x,y)
        path = [(start[0],start[1])]
        newX = start[0]
        newY = start[1]
        while (end[0]-20<newX<end[0]+20 and end[1]-20<newY<end[1]+20) == False:
            if (start[0]<end[0] and start[1]<end[1]):
                potentialMoves = [(newX+5,newY),(newX,newY+5)]
            elif (start[0]>end[0] and start[1]<end[1]):
                #print('entering wrong clause')
                potentialMoves = [(newX-5,newY),(newX,newY+5)]
            elif (start[0]>end[0] and start[1]>end[1]):
                #print('entering wrong clause')
                potentialMoves = [(newX-5,newY),(newX,newY-5)]
            elif (start[0]<end[0] and start[1]>end[1]):
                #print('entering wrong clause')
                potentialMoves = [(newX+5,newY),(newX,newY-5)]

            option1 = potentialMoves[0] 
            option2 = potentialMoves[1]  

            move = random.choice((option1,option2))

            newX = move[0]
            newY = move[1]

            if self.isLegalMove((newX,newY),start,end):
                path.append((newX,newY))

            else:
                if move == option1: 
                    move = option2 

                elif move == option2: 
                    move = option1 

                newX = move[0]
                newY = move[1]
                if self.isLegalMove((newX,newY),start,end):
                    path.append((newX,newY))
            

        path.append((end[0],end[1]))
        return Taxiway(start,end,path)
            

    #def drawParkingSpots(self, app, canvas):

    def drawMap(self, app, canvas): 
        
        #drawing background
        canvas.create_rectangle(0,0,app.width,app.height,fill=self.color)

        #draw taxiways
        for taxiway in self.taxiways:
            for coordnum in range(0,len(taxiway.path),5):
                canvas.create_oval(taxiway.path[coordnum][0]-5,taxiway.path[coordnum][1]-5,taxiway.path[coordnum][0]+5,taxiway.path[coordnum][1]+5  ,fill='black')

        #draw terminal
        canvas.create_image(app.width/2,app.height/2,image=ImageTk.PhotoImage(self.terminal)) #terminal
    

        #draw parking spots
        for i in range(self.numParkingSpots//2):
            canvas.create_image(app.width/2+((1/4)*self.terminalWidth),(app.height//2-self.terminalHeight//2)+(700//self.numParkingSpots//2)+((self.terminalHeight//(self.numParkingSpots//2))*i),
            image=ImageTk.PhotoImage(self.parkingSpot.rotate(90)))
            canvas.create_image(app.width/2-((1/4)*self.terminalWidth),(app.height//2-self.terminalHeight//2)+(700//self.numParkingSpots//2)+((self.terminalHeight//(self.numParkingSpots//2))*i),
            image=ImageTk.PhotoImage(self.parkingSpot.rotate(270)))
        
        # draw runway
        for runway in self.runways:
            canvas.create_image(runway.coords[0],runway.coords[1], image=ImageTk.PhotoImage(runway.image.rotate((runway.angle), expand = True)))

        

    
class Runway(object):
    def __init__(self, image, coords, corners, angle):
        self.image = image
        self.coords = coords
        self.angle = angle
        self.corners = corners
        self.width = image.size[0]
        self.height = image.size[1]
        self.landingInfo = {
                        (coords[0],coords[1]-(self.height/2)): [(coords[0],coords[1]-(self.height/2)),(coords[0],coords[1]),(coords[0],coords[1]+(self.height/2)-(self.height/10))],
                        (coords[0],coords[1]+(self.height/2)): [(coords[0],coords[1]+(self.height/2)),(coords[0],coords[1]),(coords[0],coords[1]-(self.height/2)+(self.height/10))]
                            }

class Taxiway(object):
    def __init__(self,start,end,path):
        self.start = start
        self.end = end
        self.path = path





