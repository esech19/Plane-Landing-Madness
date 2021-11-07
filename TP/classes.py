import random
from cmu_112_graphics import *
import time
import math


class Airplane(object):
    def __init__(self, xspeed, yspeed, x , y , app):

        self.app = app

        # plane sprites (from https://dribbble.com/shots/147169-Turbulence-Sprites) #later: helicopter sprite + helipad??
        self.spriteSheet = 'turbulence-sprite-sheet.png'
        self.spriteStrip = app.loadImage(self.spriteSheet)
        self.plane1Sprites = [ ]
        for i in range(4):
            sprite = self.spriteStrip.crop((64*i, 0, 60+64*i, 64))
            self.plane1Sprites.append(sprite)
        self.plane1SpriteCounter = 0
        self.plane1Sprite = self.plane1Sprites[self.plane1SpriteCounter]
        self.plane2Sprite = self.spriteStrip.crop((0,130,64,190)) #4 jet plane
        self.plane3Sprite = self.spriteStrip.crop((0,182,60,270))
        self.plane4Sprite = self.spriteStrip.crop((123,120,193,190))
        self.plane5Sprite = self.spriteStrip.crop((256,0,316,65))


        # generate list of plane sprites
        self.planeSprites=[self.plane1Sprite,self.plane2Sprite,self.plane3Sprite,self.plane4Sprite,self.plane5Sprite]

        self.path = []
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.isSelected = False
        self.state = 'air'
        self.selectedCount = 0
        self.rotationAngle=0
        self.width = 40
        self.height = 40

        #variables for callsign
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.numbers = '0123456789'
        self.callSign = str(self.letters[random.randint(0,len(self.letters)-1)])+str(self.letters[random.randint(0,len(self.letters)-1)])+str(self.letters[random.randint(0,len(self.letters)-1)])+str(self.numbers[random.randint(0,len(self.numbers)-1)])+str(self.numbers[random.randint(0,len(self.numbers)-1)])+str(self.numbers[random.randint(0,len(self.numbers)-1)])

        self.isRerouting = False

        #path generation
        self.pathChange = False

        self.maxSpeed = 7
        self.minSpeed = 1
        self.pathSpeed = 0.5
        self.taxiSpeed = 1

        #speeds
        if app.level == 'easy':
            self.maxSpeed = 7
            self.minSpeed = 1
            self.pathSpeed = 5
            self.taxiSpeed = 1
        
        #elif app

        #boolean to check for taxi availability (right after land right before taxi)
        self.landed = False

        self.sprite = self.planeSprites[random.randint(0,len(self.planeSprites)-1)]

    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)


    def getRotation(self):

        # calculate rotation for airplanes

        if self.xspeed == 0 and self.yspeed == 0:
            return 0
        elif self.xspeed == 0 and self.yspeed < 0:
            return 0
        elif self.xspeed == 0 and self.yspeed > 0:
            return 180
        elif self.yspeed == 0 and self.xspeed < 0:
            return 90
        elif self.yspeed == 0 and self.xspeed > 0:
            return 270 
        elif self.xspeed <0 and self.yspeed < 0:
            return 45
        elif self.xspeed <0 and self.yspeed > 0:
            return 135
        elif self.xspeed >0 and self.yspeed > 0:
            return 225
        elif self.xspeed > 0 and self.yspeed <0:
            return 315


    def speedUp(self,increase):
        if abs(self.pathSpeed) < self.maxSpeed:
            self.pathSpeed += increase

        if self.xspeed<self.maxSpeed and self.yspeed == 0:
            self.xspeed += increase
        elif abs(self.yspeed)<self.maxSpeed and self.xspeed == 0:
            self.yspeed += increase #changed from - to +
        elif abs(self.xspeed) == abs(self.yspeed):
                self.xspeed += increase
                self.yspeed -= increase

    def slowDown(self,decrease):
        if (self.pathSpeed)  > self.minSpeed:
            self.pathSpeed -= decrease

        if self.xspeed>self.minSpeed and self.yspeed == 0:
            self.xspeed -=decrease
        elif abs(self.yspeed)>self.minSpeed and self.xspeed == 0:
            self.yspeed -=decrease
        elif abs(self.xspeed) == abs(self.yspeed):
                self.xspeed -= decrease
                self.yspeed += decrease

    def isLanding(self,runway):
        if self.path != [] and self.state == 'air':
            for coord in runway.landingInfo:
                if (coord[0]-25<self.x<coord[0]+25) and (coord[1]-5<self.y<coord[1]+5):
                    newPath  = copy.copy(runway.landingInfo[coord])
                    self.path = newPath #runway.landingInfo[coord]
                    self.state = 'runway'
    
    def isLanded(self):
        if self.path == [] and self.state == 'runway':
            self.landed = True
            self.xspeed = 0
            self.yspeed = 0

    def isCompleted(self):
        if self.path == [ ] and self.state == 'taxi': 
            return True 


    def changePath(self):

        if self.path == []:
            self.x += self.xspeed
            self.y += self.yspeed
        else:  
            if(self.x < self.path[0][0]):
                self.xspeed = self.pathSpeed
            elif(self.x > self.path[0][0]):
                self.xspeed = -self.pathSpeed
            
            if(self.y < self.path[0][1]):
                self.yspeed = self.pathSpeed
            elif(self.y > self.path[0][1]):
                self.yspeed = -self.pathSpeed

            #jiggle fixer
            if(self.x == self.path[0][0]):
                self.xspeed = 0
            
            if(self.y == self.path[0][1]):
                self.yspeed = 0


            if(abs(self.x - self.path[0][0]) < self.pathSpeed):
                self.x += self.path[0][0] - self.x
            else:
                self.x += self.xspeed

            if(abs(self.y - self.path[0][1]) < self.pathSpeed):
                self.y += self.path[0][1] - self.y
            else:
                self.y += self.yspeed

            if(abs(self.x - self.path[0][0]) < self.pathSpeed and abs(self.y - self.path[0][1]) < self.pathSpeed):
                self.path.pop(0)
    #draws path 

    def drawPath(self,canvas):
        if self.path != []:
            fill='black'
            for coordIndex in range(len(self.path)):
                coordX=self.path[coordIndex][0]
                coordY=self.path[coordIndex][1]

                if self.isSelected:
                    fill='red'
                else:
                    fill='black'
                if self.state == 'air':
                    canvas.create_text(coordX,coordY,text='X',font='Arial 12 bold',fill=fill)

    def drawPlane(self,canvas): 
        if self.isSelected:
            canvas.create_oval(self.x-35,self.y-35,self.x+35,self.y+35, fill = 'yellow')                                                
        canvas.create_image(self.x,self.y, image=ImageTk.PhotoImage(self.sprite.rotate(self.getRotation(),expand = True)))
        canvas.create_text(self.x,self.y, text= self.callSign, font= 'Arial 8 bold')



    
        
    

