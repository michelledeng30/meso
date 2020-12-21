from cmu_112_graphics import *
import basic_graphics, time, random
import objects, frames, message, play, astar, disaster
from dataclasses import make_dataclass

# meso is the main file for running the game

# GENERAL CITATIONS
# color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
# cmu 112 graphics from https://www.cs.cmu.edu/~112/notes/notes-graphics.html

Human = make_dataclass('Human', ['startRow', 'startCol', 'endRow', 'endCol', 'path'])

class WelcomeMode(Mode):
    def appStarted(mode):
        mode.townName = 'no'
        mode.buttonColor1 = 'palegreen'
        mode.buttonColor2 = 'pink'
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
        else: 
            mode.buttonColor1 = 'palegreen'
            mode.width1 = 0

        if ((x >= mode.app.width//2 - mode.app.boxX) and 
              (x <= mode.app.width//2 + mode.app.boxX) and 
              (y >= mode.app.height//2 + mode.app.boxY) and 
              (y <= mode.app.height//2 + 2*mode.app.boxY)):
            mode.buttonColor2 = 'lightcoral'
            mode.width2 = 2

        else:
            mode.buttonColor2 = 'pink'
            mode.width2 = 0

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

    # CITATION for mouseMoved: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
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
        mode.tipiUnlocked = mode.houseUnlocked = mode.skyscraperUnlocked = mode.treeUnlocked = False
        mode.humans = []
        mode.objectInfo()
        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4) # 3*375 = 1125
        mode.infoWidth = mode.width - 2*mode.margin - mode.frameRightbound
        mode.infoMidX = mode.frameRightbound + mode.margin + mode.infoWidth/2
        mode.buttonR = 50
        mode.townName = 'town'

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

        # button info
        mode.buttonColor4 = 'palegreen'
        mode.width4 = 0
        mode.tipiOutline = mode.houseOutline = mode.skyscraperOutline = mode.treeOutline = 'white'
    
    def objectInfo(mode):
        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4)
        mode.signX = 3*mode.margin
        mode.signY = mode.height/2
        mode.lakeRX = 120
        mode.lakeRY = 80
        mode.mountainR = 80
        mode.treeR = 20
        mode.objectR = 5
        mode.tipiR = 25
        mode.houseR = 15
        mode.skyscraperR = 25
        
        # CITATIONS
        # grass jpeg: https://depositphotos.com/128558532/stock-photo-green-grass-background-texture.html
        # lake png: https://www.seekpng.com/ipng/u2q8o0r5e6e6y3a9_lake-png-transparent-image-lake-clipart-transparent-background/
        # mountain png: https://www.cleanpng.com/png-sugarloaf-mountain-computer-icons-mountain-699724/
        # tree png: http://clipart-library.com/free/pine-tree-clipart-png.html
        # tipi png: https://www.pngwing.com/en/free-png-zopse
        # house png: https://www.flaticon.com/free-icon/medieval-house_509843#
        # skyscraper png: https://www.pngegg.com/en/png-bcubn

        # images
        mode.grassIMG = mode.loadImage('grass.jpg')
        mode.treeIMG = mode.loadImage('tree.png')
        mode.treeIMG = mode.scaleImage(mode.treeIMG, 1/4)
        mode.mountainIMG = mode.loadImage('mountain.png')
        mode.mountainIMG = mode.scaleImage(mode.mountainIMG, 1/6)
        mode.lakeIMG = mode.loadImage('lake.png')
        mode.lakeIMG = mode.scaleImage(mode.lakeIMG, 1/2)
        mode.tipiIMG = mode.loadImage('tipi.png')
        mode.houseIMG = mode.loadImage('house.png')
        mode.houseIMG = mode.scaleImage(mode.houseIMG, 1/2)
        mode.skyscraperIMG = mode.loadImage('skyscraper.png')

        # draw images (i drew these on my ipad!)
        mode.drawWelcome = mode.loadImage('drawWelcome.png')
        mode.drawWelcome = mode.scaleImage(mode.drawWelcome, 1/3)
        mode.drawTipi = mode.loadImage('drawtipi.png')
        mode.drawTipi = mode.scaleImage(mode.drawTipi, 1/3)
        mode.drawHouse = mode.loadImage('drawhouse.png')
        mode.drawHouse = mode.scaleImage(mode.drawHouse, 1/3)
        mode.drawSkyscraper = mode.loadImage('drawskyscraper.png')
        mode.drawSkyscraper = mode.scaleImage(mode.drawSkyscraper, 1/3)
        mode.drawPandemic = mode.loadImage('drawpandemic.png')
        mode.drawPandemic = mode.scaleImage(mode.drawPandemic, 1/3)
        mode.drawFamine = mode.loadImage('drawfamine.png')
        mode.drawFamine = mode.scaleImage(mode.drawFamine, 1/3)
        mode.drawFire = mode.loadImage('drawfire.png')
        mode.drawFire = mode.scaleImage(mode.drawFire, 1/3)
        mode.drawEarthquake = mode.loadImage('drawearthquake.png')
        mode.drawEarthquake = mode.scaleImage(mode.drawEarthquake, 1/3)
        mode.drawEnd = mode.loadImage('drawend.png')
        mode.drawEnd = mode.scaleImage(mode.drawEnd, 1/3)
    
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
        if mode.placingLake and play.Play.isValid(mode, x, y, mode.lakeRX):
                objects.Lake.lake = (x,y)
                mode.placingLake = False
                mode.placingMountains = True
                mode.lakeMessage = False
                mode.mountainMessage = True
        
        # placing mountains
        elif mode.placingMountains and play.Play.isValid(mode, x, y, mode.mountainR):
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
                    mode.version = 0
                    mode.startMessage = True
                    mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        frames.Frame.draw(mode, canvas)
        frames.Info.draw(mode, canvas, mode.year, mode.population)

        objects.WelcomeSign.draw(mode, canvas)
        objects.Lake.draw(mode, canvas)
        objects.Mountain.draw(mode, canvas)
        objects.Tipi.draw(mode, canvas)
        objects.Tree.draw(mode, canvas)

        if mode.app.createMode:
            message.Message.draw(mode, canvas)

class GameMode(Mode):
    def appStarted(mode):

        #bools
        mode.paused = True
        mode.move = False
        mode.townName = 'town'
        mode.gameEnd = False

        # info
        mode.year = 0
        mode.population = 0

        # button info
        mode.buttonColor4 = 'palegreen'
        mode.width4 = 0
        mode.tipiOutline = 'white'
        mode.houseOutline = 'white'
        mode.skyscraperOutline = 'white'
        mode.treeOutline = 'white'

        # new objects
        mode.addTipi = False
        mode.addHouse = False
        mode.addSkyscraper = False
        mode.addTree = False

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

        # messages
        mode.lakeMessage = mode.mountainMessage = mode.houseMessage = False
        mode.treeMessage = False
        mode.startMessage = True
        mode.messageMidX = mode.app.margin + 160
        mode.messageMidY = mode.app.margin + 30

        # progress window
        mode.game = mode.frameRightbound - mode.margin
        mode.windowX = (mode.frameRightbound - mode.margin) // 2
        mode.windowY = mode.height // 2
        mode.windowXR = 350
        mode.windowYR = 250
        mode.windowOn = True
        mode.message1 = False
        mode.message2 = False
        mode.version = 0

        # more bools for the interactive buttons
        mode.tipiUnlocked = False
        mode.houseUnlocked = False
        mode.skyscraperUnlocked = False
        mode.treeUnlocked = False

        # initialize game
        CreateMode.objectInfo(mode)
        mode.townName = mode.getUserInput("What is the name of your town?")
        mode.grid = astar.AStar.obstacles(mode)
        mode.humans = play.Play.getHumans(mode)
        mode.possibleDisasters = [None, 'pandemic', 'famine', 'wildfire', 'earthquake']

    def mouseMoved(mode, event):
        (x,y) = (event.x, event.y)
        
        # on tipi button
        if (mode.addTipi == False) and (mode.tipiUnlocked == True):
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 200 - mode.buttonR) and
                (y <= 200 + mode.buttonR)):
                mode.tipiOutline = 'black'
            else:
                mode.tipiOutline = 'white'

        # on house button
        if (mode.addHouse == False) and (mode.houseUnlocked == True):
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 350 - mode.buttonR) and
                (y <= 350 + mode.buttonR)):
                mode.houseOutline = 'black'
            else:
                mode.houseOutline = 'white'
        
        # on skyscraper button
        if (mode.addSkyscraper == False) and (mode.skyscraperUnlocked == True):
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 500 - mode.buttonR) and
                (y <= 500 + mode.buttonR)):
                mode.skyscraperOutline = 'black'
            else:
                mode.skyscraperOutline = 'white'

        # on tree button
        if (mode.addTree == False) and (mode.treeUnlocked == True):
            if ((x >= mode.infoMidX - mode.buttonR) and 
                (x <= mode.infoMidX + mode.buttonR) and
                (y >= 650 - mode.buttonR) and
                (y <= 650 + mode.buttonR)):
                mode.treeOutline = 'black'
            else:
                mode.treeOutline = 'white'
        
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

        # choose tipi option
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 200 - mode.buttonR) and
              (y <= 200 + mode.buttonR) and
              (mode.tipiUnlocked == True)):
            mode.addTipi = True
            mode.tipiOutline = 'red'

        # add new tipi
        elif mode.addTipi == True:
            if play.Play.isValid(mode, x, y, mode.tipiR):
                objects.Tipi.tipis.append((x, y))
                mode.addTipi = False
                mode.tipiOutline = 'white'

        # choose house option
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 350 - mode.buttonR) and
              (y <= 350 + mode.buttonR) and
              (mode.houseUnlocked == True)):
            mode.addHouse = True
            mode.houseOutline = 'red'

        # add new house
        elif mode.addHouse == True:
            # upgrade existing tipi
            new = play.Play.upgradeTipi(mode, x, y)
            if new != None:
                objects.Tipi.tipis.remove(new)
                objects.House.houses.append(new)
                mode.addHouse = False
                mode.houseOutline = 'white'
            # add newHouse
            elif play.Play.isValid(mode, x, y, mode.houseR):
                objects.House.houses.append((x, y))
                mode.addHouse = False
                mode.houseOutline = 'white'
        
        # choose skyscraper option
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 500 - mode.buttonR) and
              (y <= 500 + mode.buttonR) and
              (mode.skyscraperUnlocked == True)):
            mode.addSkyscraper = True
            mode.skyscraperOutline = 'red'

        # add new skyscraper
        elif mode.addSkyscraper == True:
            # upgrade existing house
            new = play.Play.upgradeHouse(mode, x, y)
            if new != None:
                objects.House.houses.remove(new)
                objects.Skyscraper.skyscrapers.append(new)
                mode.addSkyscraper = False
                mode.skyscraperOutline = 'white'
                deadTree = random.choice(objects.Tree.trees)
                objects.Tree.trees.remove(deadTree)
            # add new skyscraper
            elif play.Play.isValid(mode, x, y, mode.skyscraperR):
                objects.Skyscraper.skyscrapers.append((x, y))
                mode.addSkyscraper = False
                mode.skyscraperOutline = 'white'
                deadTree = random.choice(objects.Tree.trees)
                objects.Tree.trees.remove(deadTree)

        # choose tree option
        elif ((x >= mode.infoMidX - mode.buttonR) and 
              (x <= mode.infoMidX + mode.buttonR) and
              (y >= 650 - mode.buttonR) and
              (y <= 650 + mode.buttonR) and
              (mode.treeUnlocked == True)):
            mode.addTree = True
            mode.treeOutline = 'red'

        # add new tree
        elif mode.addTree == True:
            if play.Play.isValid(mode, x, y, mode.treeR):
                objects.Tree.trees.append((x, y))
                mode.addTree = False
                mode.TreeOutline = 'white'
        
    def keyPressed(mode, event):
        if event.key == 'p':
            mode.paused = not mode.paused
        elif (event.key == 'Enter') and (mode.windowOn == True):
            if mode.gameEnd != True:
                mode.windowOn = False
                mode.paused = False
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
        
        # progress 1: unlocked new tipis
        if mode.year == 100:
            mode.paused = True
            mode.addTipi = mode.addHouse = mode.addSkyscraper = mode.addTree = False
            mode.tipiUnlocked = True
            mode.version = 1
            mode.windowOn = True

        # progress 2: unlocked stone houses
        if mode.year == 225:
            mode.paused = True
            mode.addTipi = mode.addHouse = mode.addSkyscraper = mode.addTree = False
            mode.houseUnlocked = True
            mode.version = 2
            mode.windowOn = True
        
        # progress 10: unlocked skyscrapers by upgrading all tipis to houses
        if len(objects.Tipi.tipis) == 0 and mode.message1 == False:
            mode.paused = True
            mode.addTipi = mode.addHouse = mode.addSkyscraper = mode.addTree = False
            mode.skyscraperUnlocked = True
            mode.tipiUnlocked = False
            mode.version = 10
            mode.windowOn = True
            mode.message1 = True

        # after 3 skyscrapers are placed, unlock the option of planting trees
        if len(objects.Skyscraper.skyscrapers) == 5 and mode.message2 == False:
            mode.paused = True
            mode.addTipi = mode.addHouse = mode.addSkyscraper = mode.addTree = False
            mode.treeUnlocked = True
            mode.version = 15
            mode.windowOn = True
            mode.message2 = True
            print('sky unlocked', mode.skyscraperUnlocked) # True
            print('addSkyscraper', mode.addSkyscraper) # False

        # end game: overpopulation or lack of resources or no more disasters
        if (len(mode.humans) >= 75) or (len(objects.Tree.trees) == 0) or (len(mode.possibleDisasters) == 0):
            mode.paused = True
            mode.version = 100
            mode.windowOn = True
            disaster.Disaster.end(mode)
            mode.gameEnd = True

        # starting at year 250, every 200 years there's a chance of a disaster occurring
        if ((mode.year - 350) % 100 == 0) and (mode.year >= 350):
            current = random.choice(mode.possibleDisasters)
            mode.paused = True
            mode.addTipi = mode.addHouse = False
            if current == None:
                mode.paused = False
            if current == 'pandemic':
                mode.version = 3
                mode.windowOn = True
                disaster.Disaster.pandemic(mode)
                mode.possibleDisasters.remove('pandemic')
            elif current == 'famine':
                mode.version = 4
                mode.windowOn = True
                disaster.Disaster.famine(mode)
                mode.possibleDisasters.remove('famine')
            elif current == 'wildfire':
                mode.version = 5
                mode.windowOn = True
                disaster.Disaster.wildfire(mode)
                mode.possibleDisasters.remove('wildfire')
            elif current == 'earthquake':
                mode.version = 6
                mode.windowOn = True
                disaster.Disaster.earthquake(mode)
                mode.possibleDisasters.remove('earthquake')

        # end game: overpopulation, war, pollution
        if (len(mode.humans) >= 75) or (len(objects.Tree.trees) == 0):
            mode.paused = True
            mode.version = 100
            mode.windowOn = True
            disaster.Disaster.end(mode)
            mode.gameEnd = True
            
    def timerFired(mode):
        if not mode.paused:
            mode.takeStep()

    def redrawAll(mode, canvas):
        frames.Frame.draw(mode, canvas)
        frames.Info.draw(mode, canvas, mode.year, mode.population)

        objects.WelcomeSign.draw(mode, canvas)
        objects.Lake.draw(mode, canvas)
        objects.Mountain.draw(mode, canvas)
        objects.Tipi.draw(mode, canvas)
        objects.House.draw(mode, canvas)
        objects.Skyscraper.draw(mode, canvas)
        objects.Tree.draw(mode, canvas)
        if mode.windowOn:
            message.Message.draw(mode, canvas)
        
        if mode.move:
            objects.Human.draw(mode, canvas)
        if mode.windowOn:
            message.Progress.draw(mode, canvas)

# CITATION: the MyModalApp class framework from cmu 112 notes
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):

        app.margin = 20
        app.boxX = 120
        app.boxY = 50
        app.backX = 50
        app.backY = 20
        app.backHeight = app.height - 3*app.margin
        app.buttonR = 50
        app.create = None

        app.drawStart = app.loadImage('drawend.png')
        app.drawStart = app.scaleImage(app.drawStart, 1/1.35)

        app.welcomeMode = WelcomeMode()
        app.gameMode = GameMode()
        app.instructsMode = InstructsMode()
        app.chooseMode = ChooseMode()

        app.createMode = CreateMode()
        app.setActiveMode(app.welcomeMode)

app = MyModalApp(width=1500, height=800)