from cmu_112_graphics import *
import basic_graphics, time, random
import objects, frames, message, play, astar, disaster
from dataclasses import make_dataclass


'''
CITATIONS
graphics: https://www.cs.cmu.edu/~112/notes/notes-graphics.html
astar algorithm (astar file): https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

'''

'''
THINGS TO DO
    get rid of dead code
    set up mountain obstacle
    mandatory instructions with next and with skip
    have graphics
        first instructions
        your town has been built! it's year 0, watch the people interact, etc
        look! upgrades & new structures!! add to keep up with your growing population
    figure out this toast message
'''

Human = make_dataclass('Human', ['startRow', 'startCol', 'endRow', 'endCol', 'path'])

class WelcomeMode(Mode):
    def appStarted(mode):
        mode.buttonColor1 = 'palegreen'
        #mode.textColor1 = 'darkgray'
        mode.buttonColor2 = 'pink'
        #mode.textColor1 = 'darkgray'
        mode.width1 = 0
        mode.width2 = 0

    def redrawAll(mode, canvas):
        frames.Welcome.draw(mode, canvas)
    
    def mouseMoved(mode, event):
        x, y = event.x, event.y
        
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.app.height//2 - 2*mode.app.boxY) and 
            (y <= mode.app.height//2 - mode.app.boxY)):
            mode.buttonColor1 = 'limegreen'
            mode.width1 = 2
            #mode.textColor = 'dimgray'
        else: 
            mode.buttonColor1 = 'palegreen'
            mode.width1 = 0
            #mode.textColor = 'darkgray'

        if ((x >= mode.app.width//2 - mode.app.boxX) and 
              (x <= mode.app.width//2 + mode.app.boxX) and 
              (y >= mode.app.height//2 + mode.app.boxY) and 
              (y <= mode.app.height//2 + 2*mode.app.boxY)):
            mode.buttonColor2 = 'lightcoral'
            mode.width2 = 2
            #mode.textColor = 'dimgrey'

        else:
            mode.buttonColor2 = 'pink'
            mode.width2 = 0
            # mode.textColor = 'darkgray'

    def mousePressed(mode, event):
        x, y = event.x, event.y
        # first time, needs to make a choice
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.app.height//2 - 2*mode.app.boxY) and 
            (y <= mode.app.height//2 - mode.app.boxY)):
            if (mode.app.create == None):
                mode.app.setActiveMode(mode.app.chooseMode)
            else:
                mode.app.setActiveMode(mode.app.gameMode)
            
        elif ((x >= mode.app.width//2 - mode.app.boxX) and 
              (x <= mode.app.width//2 + mode.app.boxX) and 
              (y >= mode.app.height//2 + mode.app.boxY) and 
              (y <= mode.app.height//2 + 2*mode.app.boxY)):
            mode.app.setActiveMode(mode.app.instructsMode)

class InstructsMode(Mode):
    def appStarted(mode):
        mode.margin = 20
        mode.buttonColor3 = 'paleturquoise'
        mode.width3 = 0
        mode.buttonColor5 = 'palegreen'
        mode.width5 = 0
        mode.boxHeight = mode.height - 6*mode.margin
    
    def redrawAll(mode, canvas):
        frames.Instructs.draw(mode, canvas)

    def mouseMoved(mode, event):
        x, y = event.x, event.y

        # hover on back button
        if ((x >= mode.app.width//2 - mode.app.backX) and 
            (x <= mode.app.width//2 + mode.app.backX) and 
            (y >= mode.app.backHeight - mode.app.backY) and 
            (y <= mode.app.backHeight + mode.app.backY)):
            mode.buttonColor3 = 'mediumturquoise'
            mode.width3 = 2
        else:
            mode.buttonColor3 = 'paleturquoise'
            mode.width3 = 0
        
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.boxHeight - mode.app.boxY) and 
            (y <= mode.boxHeight)):
            mode.buttonColor5 = 'limegreen'
            mode.width5 = 2
        else:
            mode.buttonColor5 = 'palegreen'
            mode.width5 = 0


    def mousePressed(mode, event):
        x, y = event.x, event.y

        # go back
        if ((x >= mode.app.width//2 - mode.app.backX) and 
            (x <= mode.app.width//2 + mode.app.backX) and 
            (y >= mode.app.backHeight - mode.app.backY) and 
            (y <= mode.app.backHeight + mode.app.backY)):
            mode.app.setActiveMode(mode.app.welcomeMode)

        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.boxHeight - mode.app.boxY) and 
            (y <= mode.boxHeight)):
            if (mode.app.create == None):
                mode.app.setActiveMode(mode.app.chooseMode)
            else:
                mode.app.setActiveMode(mode.app.gameMode)

class ChooseMode(Mode):
    def appStarted(mode):
        CreateMode.objectInfo(mode)

        #button info
        
        mode.buttonColor1 = 'palegreen'
        mode.buttonColor2 = 'pink'
        mode.buttonColor3 = 'paleturquoise'
        mode.width1 = 0
        mode.width2 = 0
        mode.width3 = 0

    def redrawAll(mode, canvas):
        frames.Choose.draw(mode, canvas)
    
    def mouseMoved(mode, event):
        x, y = event.x, event.y
        
        # hover on first button
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.app.height//2 - 2*mode.app.boxY) and 
            (y <= mode.app.height//2 - mode.app.boxY)):
            mode.buttonColor1 = 'limegreen'
            mode.width1 = 2
        else: 
            mode.buttonColor1 = 'palegreen'
            mode.width1 = 0

        # hover on second button
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
              (x <= mode.app.width//2 + mode.app.boxX) and 
              (y >= mode.app.height//2 + mode.app.boxY) and 
              (y <= mode.app.height//2 + 2*mode.app.boxY)):
            mode.buttonColor2 = 'lightcoral'
            mode.width2 = 2
        else:
            mode.buttonColor2 = 'pink'
            mode.width2 = 0

        # hover on back button
        if ((x >= mode.app.width//2 - mode.app.backX) and 
            (x <= mode.app.width//2 + mode.app.backX) and 
            (y >= mode.app.backHeight - mode.app.backY) and 
            (y <= mode.app.backHeight + mode.app.backY)):
            mode.buttonColor3 = 'mediumturquoise'
            mode.width3 = 2
        else:
            mode.buttonColor3 = 'paleturquoise'
            mode.width3 = 0
    
    def mousePressed(mode, event):
        x, y = event.x, event.y

        # self create
        if ((x >= mode.app.width//2 - mode.app.boxX) and 
            (x <= mode.app.width//2 + mode.app.boxX) and 
            (y >= mode.app.height//2 - 2*mode.app.boxY) and 
            (y <= mode.app.height//2 - mode.app.boxY)):
            mode.app.create = True
            mode.app.setActiveMode(mode.app.createMode)
        
        # auto create
        elif ((x >= mode.app.width//2 - mode.app.boxX) and 
              (x <= mode.app.width//2 + mode.app.boxX) and 
              (y >= mode.app.height//2 + mode.app.boxY) and 
              (y <= mode.app.height//2 + 2*mode.app.boxY)):
            mode.app.create = False
            objects.RandomMap.getMap(mode)
            mode.app.setActiveMode(mode.app.gameMode)

        # go back
        elif ((x >= mode.app.width//2 - mode.app.backX) and 
              (x <= mode.app.width//2 + mode.app.backX) and 
              (y >= mode.app.backHeight - mode.app.backY) and 
              (y <= mode.app.backHeight + mode.app.backY)):
            mode.app.setActiveMode(mode.app.welcomeMode)


class CreateMode(Mode):

    def appStarted(mode):

        mode.humans = []
        mode.objectInfo()
        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4) # 3*375 = 1125
        mode.infoWidth = mode.width - 2*mode.margin - mode.frameRightbound
        mode.infoMidX = mode.frameRightbound + mode.margin + mode.infoWidth/2
        mode.buttonR = 50


        mode.year = 0

        mode.population = 0

        # instruction bools

        mode.lakeMessage = True
        mode.mountainMessage = False
        mode.houseMessage = False
        mode.treeMessage = False
        mode.startMessage = False

        mode.placingLake = False
        mode.placingMountains = False
        mode.placingHomes = False
        mode.placingTrees = False

        mode.messageMidX = mode.margin + 160
        mode.messageMidY = mode.margin + 30

        # popup
        mode.toastTime = 0
        mode.toastMessage = False

        # button info
        mode.buttonColor4 = 'palegreen'
        mode.width4 = 0
        mode.outline1 = 'white'
        mode.outline2 = 'white'
    
    def objectInfo(mode):

        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4)
        mode.townName = mode.app.townName
        mode.signX = 3*mode.margin
        mode.signY = mode.height/2
        mode.lakeR = 80
        mode.mountainR1 = 10
        mode.mountainR2 = 60
        mode.tipiR = 20
        mode.houseR = 15

        mode.treeR = 15
        mode.objectR = 5
    
    def mouseMoved(mode, event):
        (x,y) = (event.x, event.y)
        # view instructions
        if ((x >= mode.infoMidX - 60) and 
            (x <= mode.infoMidX + 60) and 
            (y >= mode.height - 80) and 
            (y <= mode.height - 60)):
            mode.buttonColor4 = 'limegreen'
            mode.width4 = 2
        else:
            mode.buttonColor4 = 'palegreen'
            mode.width4 = 0

    def mousePressed(mode, event):

        (x,y) = (event.x, event.y)
        # view instructions
        if ((x >= mode.infoMidX - 60) and 
            (x <= mode.infoMidX + 60) and 
            (y >= mode.height - 80) and 
            (y <= mode.height - 60)):
            mode.app.setActiveMode(mode.app.instructsMode)

        # placing lake
        if mode.lakeMessage:
            mode.placingLake = True
        if mode.placingLake and play.Play.isValid(mode, x, y, mode.lakeR):
                objects.Lake.lake = (x,y)
                mode.placingLake = False
                mode.placingMountains = True
                mode.lakeMessage = False
                mode.mountainMessage = True
        
        # placing mountains
        elif mode.placingMountains and play.Play.isValid(mode, x, y, mode.mountainR2):
                objects.Mountain.mountains.append((x, y))
                if len(objects.Mountain.mountains) == 2:
                    mode.mountainMessage = False
                    mode.houseMessage = True
                    mode.placingMountains = not mode.placingMountains
                    mode.placingHomes = not mode.placingHomes

        # placing homes
        elif mode.placingHomes and play.Play.isValid(mode, x, y, mode.tipiR):
                objects.Tipi.tipis.append((x, y))
                if len(objects.Tipi.tipis) == 10:
                    mode.houseMessage = False
                    mode.treeMessage = True
                    mode.placingHomes = False
                    mode.placingTrees = True

        # placing trees
        elif mode.placingTrees and play.Play.isValid(mode, x, y, mode.treeR):
                objects.Tree.trees.append((x, y))
                if len(objects.Tree.trees) >= 10:
                    mode.treeMessage = False
                    mode.placingTrees = False
                    mode.move = True
                    mode.startMessage = True
                    # start game
                    mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        frames.Frame.draw(mode, canvas)
        frames.Info.draw(mode, canvas, mode.year, mode.population)

        objects.WelcomeSign.draw(mode, canvas)
        objects.Lake.draw(mode, canvas)
        objects.Mountain.draw(mode, canvas)
        objects.Tipi.draw(mode, canvas)
        objects.Tree.draw(mode, canvas)
        if mode.toastMessage:
            message.Toast.draw(mode, canvas)
        if mode.app.createMode:
            message.Message.draw(mode, canvas)

class GameMode(Mode):
    def appStarted(mode):

        #bools
        mode.paused = True
        mode.move = False
        
        # info
        mode.year = 0
        mode.population = 0

        # button info
        mode.buttonColor4 = 'palegreen'
        mode.width4 = 0
        mode.outline1 = 'white'
        mode.outline2 = 'white'
    
        # new objects
        mode.addTipi = False
        mode.addHouse = False

        # frame info
        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4) # 3*375 = 1125
        mode.infoWidth = mode.width - 2*mode.margin - mode.frameRightbound
        mode.infoMidX = mode.frameRightbound + mode.margin + mode.infoWidth/2
        mode.buttonR = 50

        mode.cellSize = 5
        mode.rows = 152
        mode.cols = 219
        mode.grid = [([0] * mode.cols) for row in range(mode.rows)]
        mode.humans = [[None, None, None, None] for i in range(5)]

        mode.toastTime = 0
        # messages
        mode.lakeMessage = mode.mountainMessage = mode.houseMessage = False
        mode.treeMessage = mode.toastMessage = False
        mode.startMessage = True
        mode.messageMidX = mode.app.margin + 160
        mode.messageMidY = mode.app.margin + 30


        # initialize game
        CreateMode.objectInfo(mode)
        mode.grid = astar.AStar.obstacles(mode)
        mode.humans = play.Play.getHumans(mode)


    def mouseMoved(mode, event):
        (x,y) = (event.x, event.y)
        
        # on tipi button
        if mode.addTipi == False:
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 200 - mode.buttonR) and
                (y <= 200 + mode.buttonR)):
                mode.outline1 = 'black'
            else:
                mode.outline1 = 'white'

        # on house button
        if mode.addHouse == False:
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 350 - mode.buttonR) and
                (y <= 350 + mode.buttonR)):
                mode.outline2 = 'black'
            else:
                mode.outline2 = 'white'

        # view instructions
        if ((x >= mode.infoMidX - 60) and 
            (x <= mode.infoMidX + 60) and 
            (y >= mode.height - 80) and 
            (y <= mode.height - 60)):
            mode.buttonColor4 = 'limegreen'
            mode.width4 = 2
        else:
            mode.buttonColor4 = 'palegreen'
            mode.width4 = 0
    
    # view instructions
    def mousePressed(mode, event):

        x, y = event.x, event.y

        # go to instructions
        if ((x >= mode.infoMidX - 60) and 
            (x <= mode.infoMidX + 60) and 
            (y >= mode.height - 80) and 
            (y <= mode.height - 60)):
            mode.app.setActiveMode(mode.app.instructsMode)

        # add new tipi
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 200 - mode.buttonR) and
              (y <= 200 + mode.buttonR)):
            mode.addTipi = True
            mode.outline1 = 'red'
        
        elif mode.addTipi == True:
            if play.Play.isValid(mode, x, y, mode.tipiR):
                objects.Tipi.tipis.append((x, y))
                mode.addTipi = False
                mode.outline1 = 'white'

        # add new house
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 350 - mode.buttonR) and
              (y <= 350 + mode.buttonR)):
            mode.addHouse = True
            mode.outline2 = 'red'

        elif mode.addHouse == True:
            if play.Play.isValid(mode, x, y, mode.houseR):
                objects.House.houses.append((x, y))
                mode.addHouse = False
                mode.outline2 = 'white'

    def keyPressed(mode, event):

        if event.key == 'p':
            mode.paused = not mode.paused
        elif event.key == 'Space':
            mode.paused = False
            mode.startMessage = False
            mode.move = True
        elif (event.key == 's') and (mode.paused == True):
            mode.takeStep()


    def takeStep(mode):
        mode.year += 1
        play.Play.moveHuman(mode)
        
        # humans immigrate to the town every 100 years
        if mode.year % 100 == 0 and mode.year != 0:
            newHumans = random.randint(1, 4)
            for i in range(newHumans):
                play.Play.getNewHuman(mode, mode.rows//2, 1)
        '''
        # at year 125, there's a global pandemic
        if mode.year == 125:
            disaster.Disaster.pandemic(mode)
            mode.paused = True
        
        # at year 125, there's a famine
        elif mode.year == 150:
            disaster.Disaster.famine(mode)
            mode.paused = True
        
        # at year 175, there's a wildfire
        elif mode.year == 175:
            disaster.Disaster.wildfire(mode)
            mode.paused = True

        # at year 210, there's an earthquake
        elif mode.year == 210:
            disaster.Disaster.earthquake(mode)
            mode.paused = True
        '''
    def timerFired(mode):
        if not mode.paused:
            mode.takeStep()

        # displaying a message
        if time.time() - mode.toastTime < 2.5:
            mode.toastMessage = True
        else:
            mode.toastMessage = False

    def redrawAll(mode, canvas):
        frames.Frame.draw(mode, canvas)
        frames.Info.draw(mode, canvas, mode.year, mode.population)

        objects.WelcomeSign.draw(mode, canvas)
        objects.Lake.draw(mode, canvas)
        objects.Mountain.draw(mode, canvas)
        objects.Tipi.draw(mode, canvas)
        objects.House.draw(mode, canvas)
        objects.Tree.draw(mode, canvas)

        message.Message.draw(mode, canvas)
        # message.Toast.draw(mode, canvas)
        if mode.move:
            objects.Human.draw(mode, canvas)


class MyModalApp(ModalApp):
    def appStarted(app):
        app.townName = app.getUserInput("What is the name of your town?")

        app.margin = 20
        app.boxX = 120
        app.boxY = 50
        app.backX = 50
        app.backY = 20
        app.backHeight = app.height - 3*app.margin
        app.buttonR = 50
        app.create = None

        app.welcomeMode = WelcomeMode()
        app.gameMode = GameMode()
        app.instructsMode = InstructsMode()
        app.chooseMode = ChooseMode()

        app.createMode = CreateMode()
        app.setActiveMode(app.welcomeMode)

app = MyModalApp(width=1500, height=800)


