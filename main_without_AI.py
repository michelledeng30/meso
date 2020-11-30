from cmu_112_graphics import *
import basic_graphics, time, random

'''
resources
    every time a person intersects with a tree, gain resource
    use resources to "buy" new structures and upgrade current structures
        tipis -> stone houses -> skyscrapers
        boathouse
        hospital (affects disaster resilience)
        community center

immigration
    increment by years or number of houses?

disasters
    what is it based off of?

A*
AI algorithm

random map generator



'''



def appStarted(app):
    # frame
    app.margin = 20
    app.frameRightbound = 3*(app.width/4) # 3*375 = 1125
    app.frameWidth = app.frameRightbound - app.margin
    app.frameMidX = app.frameWidth/2 + app.margin
    app.frameMidY = app.height/2 + app.margin
    app.infoMidX = app.width-(app.width//8)-(2*app.margin)
    app.infoWidth = app.width - 2*app.margin - app.frameRightbound
    app.instructsMidX = app.margin + 160
    app.instructsMidY = app.margin + 30
    app.signX = app.frameMidX + 30

    # info
    app.year = 0

    # objects
    app.tipis = []
    app.houses = []
    app.trees = []
    app.mountains = []
    app.lake = (-100, -100)
    app.humans = [[None, None, None, None] for i in range(10)]

    # drawing radii
    app.objectR = 15
    app.lakeR = 80
    app.mountainR1 = 10
    app.mountainR2 = 60
    app.humanR = 5
    app.tipiR = 20

    # bools
    app.paused = True
    app.movingHumans = False

    app.text=''

    app.toastMessage = False
    app.displayMessage = True

    app.checkingCollisions = False

    # placing bools
    app.placingLake = False
    app.placingMountains = False
    app.placingHouses = False
    app.placingTrees = False

    # instructions bools
    app.lakeInstructs = True
    app.mountainInstructs = False
    app.houseInstructs = False
    app.treeInstructs = False
    app.startInstructs = False

    app.messageTime = 0
    app.toastTime = 0

    # splash screen
    app.homePage = True
    app.instructionsPage = False
    app.gamePage = False
    app.instructs = False
    app.townName = app.getUserInput("What is the name of your town?")

    # instructions screen

    # images
    app.lakeImage0 = app.loadImage('lake.png')
    app.lakeImage = app.scaleImage(app.lakeImage0, 3/10)
    app.mountainImage0 = app.loadImage('mountain.png')
    app.mountainImage = app.scaleImage(app.mountainImage0, 2/10)


def keyPressed(app, event):
    if event.key == 'Enter':
        app.homePage = False
        app.instructionsPage = False
    elif event.key == 'i' and app.homePage == True:
        app.instructionsPage = True
        app.homePage = False
    elif event.key == 'b' and app.instructionsPage == True:
        app.instructionsPage = False
        app.homePage = True
    elif event.key == 'Space' and app.gamePage == False:
        app.paused = not app.paused
        app.gamePage = True
        app.startInstructs = False
    elif event.key == 'p' and app.gamePage == True:
        app.paused = not app.paused
    elif event.key == 'c':
        app.checkingCollisions = not app.checkingCollisions
    else:
        pass

def mousePressed(app, event):
    (x, y) = (event.x, event.y)
    # placing the lake
    if app.homePage == False:
        if app.lakeInstructs:
            app.placingLake = True
        if app.placingLake:
            if objectIsValid(app, x, y, app.lakeR):
                app.lake = (x,y)
                app.placingLake = False
                app.placingMountains = True
                app.lakeInstructs = False
                app.mountainInstructs = True
        # placing mountains
        elif app.placingMountains:
            if objectIsValid(app, x, y, app.mountainR2):
                app.mountains.append((x, y))
                if len(app.mountains) == 2:
                    app.mountainInstructs = False
                    app.houseInstructs = True
                    app.placingMountains = not app.placingMountains
                    app.placingHouses = not app.placingHouses

        # placing homes
        elif app.placingHouses:
            if objectIsValid(app, x, y, app.objectR):
                app.tipis.append((x, y))
                if len(app.tipis) == 10:
                    app.houseInstructs = False
                    app.treeInstructs = True
                    app.placingHouses = False
                    app.placingTrees = True

        # placing trees
        elif app.placingTrees:
            if objectIsValid(app, x, y, app.objectR):
                app.trees.append((x, y))
                if len(app.trees) >= 10:
                    app.treeInstructs = False
                    app.placingTrees = False
                    app.movingHumans = True
                    app.startInstructs = True
                    getHumans(app)

def timerFired(app):
    if not app.paused:
        app.year += 1
        moveHuman(app)
    # add new humans every 50 years
    if app.year % 50 == 0 and app.year != 0:
        newHumans = random.randint(1, 4)
        for i in range(newHumans):
            createNewHuman(app)
    if app.displayMessage == True:
        app.displayMessage = False
    if time.time() - app.toastTime < 2.5:
        app.toastMessage = True
    else:
        app.toastMessage = False

def getHumans(app):
    for human in app.humans:
        human[0], human[1] = random.choice(list(app.tipis))
        findNewDest(app, human)

def findNewDest(app, human):
    destX, destY = random.choice(list(app.tipis))
    human[2], human[3] = destX, destY

def createNewHuman(app):
    destX, destY = random.choice(list(app.tipis))
    human = [app.frameMidX, app.margin+5, destX, destY]
    app.humans.append(human)

def checkCollision(app, human):
    checkList = copy.deepcopy(app.humans)
    curX, curY = human[0], human[1]
    curDestX, curDestY = human[2], human[3]
    for checkHuman in checkList:
        checkX, checkY = checkHuman[0], checkHuman[1]
        checkDestX, checkDestY = checkHuman[2], checkHuman[3]
        if (distance(checkX, checkY, curX, curY) <= 2*app.humanR and
            curDestX, curDestY != checkDestX, checkDestY):
            return True
    return False

def moveHuman(app):
    for human in app.humans:
        x = human[0]
        y = human[1]
        destX = human[2]
        destY = human[3]
        # add a new human if there's a collision
        if app.checkingCollisions:
            if checkCollision(app, human):
                createNewHuman(app)
                app.checkingCollisions = not app.checkingCollisions
        # if the human reaches their dest, set a new dest
        if distance(x, y, destX, destY) <= app.objectR:
            findNewDest(app, human)
        # check direction of human
        if x > destX: signX = -1
        else: signX = +1
        if y > destY: signY = -1
        else: signY = +1
        # set speed of human
        if abs(x - destX) > abs(y - destY):
            if distance(x, y, destX, destY) >= 400:
                dx = 4*signX
                dy = 3*signY
            else:
                dx = 3.5*signX
                dy = 2.5*signY
        else:
            if distance(x, y, destX, destY) >= 400:
                dx = 3*signX
                dy = 4*signY
            else:
                dx = 2.5*signX
                dy = 3.5*signY
        # if human is in line with dest, go straight
        if abs(x - destX) < 2:
            dx = 0
        if abs(y - destY) < 2:
            dy = 0
        # if object is gonna intersect with mountain
        #for mountainX, mountainY in app.mountains:
        #    if ((x + dx) - mountainX <= app.mountainR2 and 
        #        (y + dy) - mountainY <= app.mountainR2):
        #        dy = -dy
        #        dx = -dx
        human[0] += dx
        human[1] += dy

def objectIsValid(app, x, y, r):
    # check boundary
    if ((x <= app.margin + r) or (x >= app.frameRightbound - r) or 
       (y <= app.margin) or (y >= app.height - app.margin)):
       app.toastTime = time.time()
       return False
    # check sign
    signX, signY = app.signX, 45
    if distance(x, y, signX, signY) <= app.objectR + r:
        app.toastTime = time.time()
        return False
    # check lake
    lakeX, lakeY = app.lake
    if distance(x, y, lakeX, lakeY) <= app.lakeR + r:
        app.toastTime = time.time()
        return False
    # check mountain
    for cx, cy in app.mountains:
        if distance(x, y, cx, cy) <= app.mountainR2 + r:
            app.toastTime = time.time()
            return False
    # check objects
    objects = app.tipis + app.trees
    for cx, cy in objects:
        if distance(x, y, cx, cy) <= app.objectR + r:
            app.toastTime = time.time()
            return False
    return True


def drawToastMessage(app, canvas):
    canvas.create_text(app.width//3 + 50, app.height - 40, 
                       text='Object is not valid! Try placing again',
                       font='Arial 16 bold', fill='red')

def drawMessage(app, canvas):
    canvas.create_rectangle(app.frameMidX - 40, app.frameMidY - 20,
                            app.frameMidX + 40, app.frameMidY + 20,
                            fill='mistyrose', outline='black', width=2)
    canvas.create_text(app.frameMidX, app.frameMidY, 
                       text=app.text, font='Arial 30 bold')


def drawInfo(app, canvas):
    canvas.create_text(app.infoMidX, 40, 
                       text=f'Year: {app.year}')
    canvas.create_text(app.infoMidX, 60,
                       text=f'Population: {len(app.humans)}')
    canvas.create_text(app.infoMidX, 100,
                       text='Upgrades', font='Arial 20 bold')
    canvas.create_text(app.infoMidX, app.height - 40,
                       text='Press \'p\' to pause')

def drawNewHouse(app, canvas):
    canvas.create_text(app.infoMidX-60, 140, text='House')
    canvas.create_polygon(app.infoMidX-app.objectR-60, 190-app.objectR,
                              app.infoMidX-app.objectR-60, 190+app.objectR,
                              app.infoMidX+app.objectR-60, 190+app.objectR,
                              app.infoMidX+app.objectR-60, 190-app.objectR,
                              app.infoMidX-60, 190-(2*app.objectR),
                              fill='silver', outline='black', width=3)

def drawHumans(app, canvas):
    for human in app.humans:
        x = human[0]
        y = human[1]
        canvas.create_oval(x-app.humanR, y-app.humanR,
                           x+app.humanR, y+app.humanR,
                           fill='black')

def drawLake(app, canvas):
    if app.lake != None:
        (x,y) = app.lake
        #canvas.create_image(x, y, image=ImageTk.PhotoImage(app.lakeImage))
        canvas.create_oval(x - app.lakeR, y - app.lakeR + 10, 
                           x + app.lakeR, y + app.lakeR - 10, 
                           fill='dodgerblue', width=2, outline='blue')

def drawMountains(app, canvas):
    for (x, y) in app.mountains:
        #canvas.create_image(x, y, image=ImageTk.PhotoImage(app.mountainImage))
        canvas.create_polygon(x, y - app.mountainR2,
                              x + 2*app.mountainR1, y + app.mountainR1,
                              x + 3*app.mountainR1, y + app.mountainR1,
                              x + app.mountainR2, y + app.mountainR2,
                              x - app.mountainR2, y + app.mountainR2,
                              x - 3*app.mountainR1, y - app.mountainR1,
                              x - 2*app.mountainR1, y - app.mountainR1,
                              fill='darkgrey')

def drawTipis(app, canvas):
    for (x, y) in app.tipis:
        canvas.create_polygon(x, y-app.tipiR,
                            x+app.tipiR, y+app.tipiR,
                            x-app.tipiR, y+app.tipiR,
                            fill='burlywood', outline='sienna', width=3)
        canvas.create_line(x, y-app.tipiR, x+8, y-app.tipiR-15, 
                        fill='sienna', width=3)
        canvas.create_line(x, y-app.tipiR, x-8, y-app.tipiR-15,
                        fill='sienna', width=3)

def drawHouses(app, canvas):
    for (x, y) in app.houses:
        canvas.create_polygon(x-app.objectR, y-app.objectR,
                              x-app.objectR, y+app.objectR,
                              x+app.objectR, y+app.objectR,
                              x+app.objectR, y-app.objectR,
                              x, y-(2*app.objectR),
                              fill='silver', outline='black', width=3)

def drawTrees(app, canvas):
    for (x, y) in app.trees:    
        canvas.create_polygon(x - app.objectR//1.5, y,
                              x, y - (3/2)*(app.objectR//1.5),
                              x + app.objectR//1.5, y,
                              fill='darkgreen')
        canvas.create_polygon(x - app.objectR, y + app.objectR,
                              x, y - ((1/2)*app.objectR),
                              x + app.objectR, y + app.objectR,
                              fill='darkgreen')
        canvas.create_polygon(x - (app.objectR*1.2), y + 2*(app.objectR),
                              x, y + ((1/4)*(app.objectR)),
                              x + (app.objectR*1.2), y + 2*(app.objectR),
                              fill='darkgreen')

def drawInstructsWindow(app, canvas):
    text, color = None, None
    if app.lakeInstructs:
        text, color = 'Click to place a lake.', 'dodgerblue'
    elif app.mountainInstructs:
        text, color = 'Click to place two mountains.', 'darkgrey'
    elif app.houseInstructs:
        text, color = 'Click to place 10 houses.', 'burlywood'
    elif app.treeInstructs:
        text, color = 'Click to place 10 trees.', 'darkgreen'
    elif app.startInstructs:
        text, color = 'Press SPACE to begin!', 'bisque'
    elif (text, color) == (None, None):
        return
    canvas.create_rectangle(app.instructsMidX - 150, app.instructsMidY - 20,
                            app.instructsMidX + 150, app.instructsMidY + 20,
                            fill=color)    
    canvas.create_text(app.instructsMidX, app.instructsMidY,
                       text=text, font='Arial 14 bold')

def drawWelcomeSign(app, canvas):
    canvas.create_rectangle(app.signX-30, 30, app.signX+30, 60,
                            fill='tan', outline='black', width=1)
    canvas.create_line(app.signX, 60, app.signX, 70, 
                       fill='black', width=2)
    canvas.create_text(app.signX, 40, text='Welcome', font='Arial 10')
    canvas.create_text(app.signX, 50, text=f'to {app.townName}!', 
                       font='Arial 10')

def drawInstructionsPage(app, canvas):
    canvas.create_text(app.width//2, app.margin+50, 
                       text='instructions', 
                       font='Arial 22 bold', 
                       fill='blue')
    canvas.create_text(app.width//2, app.height - 60,
                       text='Press \'b\' to return to home page')
    canvas.create_text(app.width//2, app.height - 40,
                       text='Press ENTER to continue',
                       font='Arial 18 bold', fill='purple')
    # 1) initialize map by placing a lake, mountains, houses and trees
    # 2) start your civilization! watch as the villagers move and interact
    # 3) how does population increase? every time two villagers meet, a new one 
    # is generated. also, every 50 years, new people move to your town
    # 4) upgrade current buildings in the sidebar when they become available
    # 5) place down new buildings/structures to support the growing population
        # houses, community centers, boathouse, skyscrapers
    # 6) watch out for disasters...

def drawHomePage(app, canvas):
    canvas.create_text(app.width//2, app.height//4, 
                       text='civilization simulator', 
                       font='Arial 26 bold', 
                       fill='blue')
    canvas.create_text(app.width//2, app.height//2 + 40,
                       text='Press ENTER to continue',
                       font='Arial 18 bold', fill='purple')
    canvas.create_text(app.width//2, app.height//2 + 70,
                       text='Press \'i\' to see instructions',
                       font='Arial 18 bold', fill='magenta')

def drawFrame(app, canvas):
    # game
    canvas.create_rectangle(app.margin, app.margin, 
                            app.frameRightbound-app.margin/2, # 1125 - 10 
                            app.height - app.margin, # 800 - 20
                            fill='palegreen', width=2)
    # game size: (20, 20, 1115, 780)
    # info
    canvas.create_rectangle(app.frameRightbound+app.margin/2, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            fill='mistyrose', width=2)

def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

def redrawAll(app, canvas):
    # splash screen
    if app.homePage:
        drawHomePage(app, canvas)
        
    # instructions
    elif app.instructionsPage:
        drawInstructionsPage(app, canvas)
    else:
        drawFrame(app, canvas)
        drawInfo(app, canvas)
        if app.toastMessage:
            drawToastMessage(app, canvas)
        if app.displayMessage:
            drawMessage(app, canvas)
        
        drawInstructsWindow(app, canvas)

        drawWelcomeSign(app, canvas)
        drawLake(app, canvas)
        drawMountains(app, canvas)
        drawTipis(app, canvas)
        drawHouses(app, canvas)
        drawTrees(app, canvas)
        drawNewHouse(app, canvas)
        if app.movingHumans:
            drawHumans(app, canvas)


runApp(width=1500, height=800)
