from cmu_112_graphics import *
import basic_graphics, time, random

class MyApp(App):

    def appStarted(self):
        # frame
        self.margin = 20
        self.frameRightbound = 3*(self.width/4)
        self.frameWidth = self.frameRightbound - self.margin
        self.frameMidX = self.frameWidth/2 + self.margin
        self.frameMidY = self.height/2 + self.margin
        self.infoMidX = self.width-(self.width//8)-(2*self.margin)
        self.infoWidth = self.width - 2*self.margin - self.frameRightbound
        self.instructsMidX = self.margin + 160
        self.instructsMidY = self.margin + 30
        self.signX = self.frameMidX + 30

        # info
        self.year = 0

        # objects
        self.tipis = [(-100, -100)]
        self.houses = []
        self.trees = []
        self.mountains = []
        MyApp.lake = None
        self.humans = [[None, None, None, None] for i in range(10)]

        # drawing radii
        self.objectR = 15
        self.lakeR = 80
        self.mountainR1 = 10
        self.mountainR2 = 60
        self.humanR = 5
        self.tipiR = 20

        # bools
        self.paused = True
        self.movingHumans = False

        self.toastMessage = False
        self.displayMessage = True

        self.checkingCollisions = False

        # placing bools
        self.placingLake = True
        self.placingMountains = False
        self.placingHouses = False
        self.placingTrees = False

        # instructions bools
        self.lakeInstructs = True
        self.mountainInstructs = False
        self.houseInstructs = False
        self.treeInstructs = False
        self.startInstructs = False

        self.messageTime = 0
        self.toastTime = 0

        # splash screen
        self.homePage = True
        self.instructionsPage = False
        self.gamePage = False
        self.instructs = False
        self.townName = self.getUserInput("What is the name of your town?")

        # instructions screen

        # images
        self.lakeImage0 = self.loadImage('lake.png')
        self.lakeImage = self.scaleImage(self.lakeImage0, 3/10)
        self.mountainImage0 = self.loadImage('mountain.png')
        self.mountainImage = self.scaleImage(self.mountainImage0, 2/10)

    def keyPressed(self, event):
        if event.key == 'Enter':
            self.homePage = False
            self.instructionsPage = False
        elif event.key == 'i' and self.homePage == True:
            self.instructionsPage = True
            self.homePage = False
        elif event.key == 'b' and self.instructionsPage == True:
            self.instructionsPage = False
            self.homePage = True
        elif event.key == 'Space' and self.gamePage == False:
            self.paused = False
            self.gamePage = True
            self.startInstructs = False
        elif event.key == 'p' and self.gamePage == True:
            self.paused = not self.paused
        elif event.key == 'c':
            self.checkingCollisions = not self.checkingCollisions
        else:
            pass

    def mousePressed(self, event):
        (x, y) = (event.x, event.y)
        print('mouse', x, y)
        # placing the lake
        if self.homePage == False:
            if self.lakeInstructs:
                self.placingLake = True
            if self.placingLake:
                if self.objectIsValid(x, y, self.lakeR):
                    print('valid:', self.objectIsValid(x, y, self.lakeR))
                    MyApp.lake = (x, y)
                    self.placingLake = False
                    self.placingMountains = True
                    self.lakeInstructs = False
                    self.mountainInstructs = True
            # placing mountains
            elif self.placingMountains:
                if self.objectIsValid(x, y, self.mountainR2):
                    self.mountains.selfend((x, y))
                    if len(self.mountains) == 2:
                        self.mountainInstructs = False
                        self.houseInstructs = True
                        self.placingMountains = not self.placingMountains
                        self.placingHouses = not self.placingHouses

            # placing homes
            elif self.placingHouses:
                if self.objectIsValid(x, y, self.objectR):
                    self.tipis.selfend((x, y))
                    if len(self.tipis) == 10:
                        self.houseInstructs = False
                        self.treeInstructs = True
                        self.placingHouses = False
                        self.placingTrees = True

            # placing trees
            elif self.placingTrees:
                if self.objectIsValid(x, y, self.objectR):
                    self.trees.selfend((x, y))
                    if len(self.trees) >= 10:
                        self.treeInstructs = False
                        self.placingTrees = False
                        self.movingHumans = True
                        self.startInstructs = True
                        getHumans(self)

    def timerFired(self):
        if not self.paused:
            self.year += 1
            self.moveHuman()
        # add new humans every 50 years
        if self.year % 50 == 0 and self.year != 0:
            newHumans = random.randint(1, 4)
            for i in range(newHumans):
                self.createNewHuman()
        if self.displayMessage == True:
            self.displayMessage = False
        if time.time() - self.toastTime < 2.5:
            self.toastMessage = True
        else:
            self.toastMessage = False

    def getHumans(self):
        for human in self.humans:
            human[0], human[1] = random.choice(list(self.tipis))
            self.findNewDest(human)

    def findNewDest(self, human):
        destX, destY = random.choice(list(self.tipis))
        human[2], human[3] = destX, destY

    def createNewHuman(self):
        destX, destY = random.choice(list(self.tipis))
        human = [self.frameMidX, self.margin+5, destX, destY]
        self.humans.selfend(human)

    def checkCollision(self, human):
        checkList = copy.deepcopy(self.humans)
        curX, curY = human[0], human[1]
        curDestX, curDestY = human[2], human[3]
        for checkHuman in checkList:
            checkX, checkY = checkHuman[0], checkHuman[1]
            checkDestX, checkDestY = checkHuman[2], checkHuman[3]
            if (MyApp.distance(checkX, checkY, curX, curY) <= 2*self.humanR and
                curDestX, curDestY != checkDestX, checkDestY):
                return True
        return False

    def moveHuman(self):
        for human in self.humans:
            x = human[0]
            y = human[1]
            destX = human[2]
            destY = human[3]
            # add a new human if there's a collision
            if self.checkingCollisions:
                if checkCollision(self, human):
                    self.createNewHuman()
                    self.checkingCollisions = not self.checkingCollisions
            # if the human reaches their dest, set a new dest
            if MyApp.distance(x, y, destX, destY) <= self.objectR:
                self.findNewDest(human)
            # check direction of human
            if x > destX: signX = -1
            else: signX = +1
            if y > destY: signY = -1
            else: signY = +1
            # set speed of human
            if abs(x - destX) > abs(y - destY):
                if MyApp.distance(x, y, destX, destY) >= 400:
                    dx = 4*signX
                    dy = 3*signY
                else:
                    dx = 3.5*signX
                    dy = 2.5*signY
            else:
                if MyApp.distance(x, y, destX, destY) >= 400:
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
            #for mountainX, mountainY in self.mountains:
            #    if ((x + dx) - mountainX <= self.mountainR2 and 
            #        (y + dy) - mountainY <= self.mountainR2):
            #        dy = -dy
            #        dx = -dx
            human[0] += dx
            human[1] += dy

    def objectIsValid(self, x, y, r):
        # check boundary
        if ((x <= self.margin + r) or (x >= self.frameRightbound - r) or 
            (y <= self.margin) or (y >= self.height - self.margin)):
            self.toastTime = time.time()
        return False
        # check sign
        signX, signY = self.signX, 45
        if MyApp.distance(x, y, signX, signY) <= self.objectR + r:
            self.toastTime = time.time()
            return False
        # check lake
        lakeX, lakeY = self.lake
        if MyApp.distance(x, y, lakeX, lakeY) <= self.lakeR + r:
            self.toastTime = time.time()
            return False
        # check mountain
        for cx, cy in self.mountains:
            if MyApp.distance(x, y, cx, cy) <= self.mountainR2 + r:
                self.toastTime = time.time()
                return False
        # check objects
        objects = self.tipis + self.trees
        for cx, cy in objects:
            if MyApp.distance(x, y, cx, cy) <= self.objectR + r:
                self.toastTime = time.time()
                return False
        return True


    def drawToastMessage(self, canvas):
        canvas.create_text(self.width//3 + 50, self.height - 40, 
                        text='Object is not valid! Try placing again',
                        font='Arial 16 bold', fill='red')

    def drawMessage(self, canvas):
        canvas.create_rectangle(self.frameMidX - 40, self.frameMidY - 20,
                                self.frameMidX + 40, self.frameMidY + 20,
                                fill='mistyrose', outline='black', width=2)
        canvas.create_text(self.frameMidX, self.frameMidY, 
                        text=self.text, font='Arial 30 bold')


    def drawInfo(self, canvas):
        canvas.create_text(self.infoMidX, 40, 
                        text=f'Year: {self.year}')
        canvas.create_text(self.infoMidX, 60,
                        text=f'Population: {len(self.humans)}')
        canvas.create_text(self.infoMidX, 100,
                        text='Upgrades', font='Arial 20 bold')
        canvas.create_text(self.infoMidX, self.height - 40,
                        text='Press \'p\' to pause')

    def drawNewHouse(self, canvas):
        canvas.create_text(self.infoMidX-60, 140, text='House')
        canvas.create_polygon(self.infoMidX-self.objectR-60, 190-self.objectR,
                                self.infoMidX-self.objectR-60, 190+self.objectR,
                                self.infoMidX+self.objectR-60, 190+self.objectR,
                                self.infoMidX+self.objectR-60, 190-self.objectR,
                                self.infoMidX-60, 190-(2*self.objectR),
                                fill='silver', outline='black', width=3)

    def drawHumans(self, canvas):
        for human in self.humans:
            x = human[0]
            y = human[1]
            canvas.create_oval(x-self.humanR, y-self.humanR,
                            x+self.humanR, y+self.humanR,
                            fill='black')

    def drawLake(self, canvas):

        print(self.lake)
        if MyApp.lake != None:
            print('tryna draw lake')
            (x, y) = MyApp.lake
            #canvas.create_image(x, y, image=ImageTk.PhotoImage(self.lakeImage))
            canvas.create_oval(x - self.lakeR, y - self.lakeR + 10, 
                            x + self.lakeR, y + self.lakeR - 10, 
                            fill='dodgerblue', width=2, outline='blue')

    def drawMountains(self, canvas):
        for (x, y) in self.mountains:
            #canvas.create_image(x, y, image=ImageTk.PhotoImage(self.mountainImage))
            canvas.create_polygon(x, y - self.mountainR2,
                                x + 2*self.mountainR1, y + self.mountainR1,
                                x + 3*self.mountainR1, y + self.mountainR1,
                                x + self.mountainR2, y + self.mountainR2,
                                x - self.mountainR2, y + self.mountainR2,
                                x - 3*self.mountainR1, y - self.mountainR1,
                                x - 2*self.mountainR1, y - self.mountainR1,
                                fill='darkgrey')

    def drawTipis(self, canvas):
        for (x, y) in self.tipis:
            canvas.create_polygon(x, y-self.tipiR,
                                x+self.tipiR, y+self.tipiR,
                                x-self.tipiR, y+self.tipiR,
                                fill='burlywood', outline='sienna', width=3)
            canvas.create_line(x, y-self.tipiR, x+8, y-self.tipiR-15, 
                            fill='sienna', width=3)
            canvas.create_line(x, y-self.tipiR, x-8, y-self.tipiR-15,
                            fill='sienna', width=3)

    def drawHouses(self, canvas):
        for (x, y) in self.houses:
            canvas.create_polygon(x-self.objectR, y-self.objectR,
                                x-self.objectR, y+self.objectR,
                                x+self.objectR, y+self.objectR,
                                x+self.objectR, y-self.objectR,
                                x, y-(2*self.objectR),
                                fill='silver', outline='black', width=3)

    def drawTrees(self, canvas):
        for (x, y) in self.trees:    
            canvas.create_polygon(x - self.objectR//1.5, y,
                                x, y - (3/2)*(self.objectR//1.5),
                                x + self.objectR//1.5, y,
                                fill='darkgreen')
            canvas.create_polygon(x - self.objectR, y + self.objectR,
                                x, y - ((1/2)*self.objectR),
                                x + self.objectR, y + self.objectR,
                                fill='darkgreen')
            canvas.create_polygon(x - (self.objectR*1.2), y + 2*(self.objectR),
                                x, y + ((1/4)*(self.objectR)),
                                x + (self.objectR*1.2), y + 2*(self.objectR),
                                fill='darkgreen')

    def drawInstructsWindow(self, canvas):
        text, color = None, None
        if self.lakeInstructs:
            text, color = 'Click to place a lake.', 'dodgerblue'
        elif self.mountainInstructs:
            text, color = 'Click to place two mountains.', 'darkgrey'
        elif self.houseInstructs:
            text, color = 'Click to place 10 houses.', 'burlywood'
        elif self.treeInstructs:
            text, color = 'Click to place 10 trees.', 'darkgreen'
        elif self.startInstructs:
            text, color = 'Press SPACE to begin!', 'bisque'
        elif (text, color) == (None, None):
            return
        canvas.create_rectangle(self.instructsMidX - 150, self.instructsMidY - 20,
                                self.instructsMidX + 150, self.instructsMidY + 20,
                                fill=color)    
        canvas.create_text(self.instructsMidX, self.instructsMidY,
                        text=text, font='Arial 14 bold')

    def drawWelcomeSign(self, canvas):
        canvas.create_rectangle(self.signX-30, 30, self.signX+30, 60,
                                fill='tan', outline='black', width=1)
        canvas.create_line(self.signX, 60, self.signX, 70, 
                        fill='black', width=2)
        canvas.create_text(self.signX, 40, text='Welcome', font='Arial 10')
        canvas.create_text(self.signX, 50, text=f'to {self.townName}!', 
                        font='Arial 10')

    def drawInstructionsPage(self, canvas):
        canvas.create_text(self.width//2, self.margin+50, 
                        text='instructions', 
                        font='Arial 22 bold', 
                        fill='blue')
        canvas.create_text(self.width//2, self.height - 60,
                        text='Press \'b\' to return to home page')
        canvas.create_text(self.width//2, self.height - 40,
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

    def drawHomePage(self, canvas):
        canvas.create_text(self.width//2, self.height//4, 
                        text='civilization simulator', 
                        font='Arial 26 bold', 
                        fill='blue')
        canvas.create_text(self.width//2, self.height//2 + 40,
                        text='Press ENTER to continue',
                        font='Arial 18 bold', fill='purple')
        canvas.create_text(self.width//2, self.height//2 + 70,
                        text='Press \'i\' to see instructions',
                        font='Arial 18 bold', fill='magenta')

    def drawFrame(self, canvas):
        # game
        canvas.create_rectangle(self.margin, self.margin, 
                                self.frameRightbound-self.margin/2, 
                                self.height - self.margin,
                                fill='palegreen', width=2)
        # info
        canvas.create_rectangle(self.frameRightbound+self.margin/2, self.margin,
                                self.width-self.margin, self.height-self.margin,
                                fill='mistyrose', width=2)

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

    def redrawAll(self, canvas):
        # splash screen
        if self.homePage:
            self.drawHomePage(canvas)
            print("self.homePage")
        # instructions
        elif self.instructionsPage:
            self.drawInstructionsPage(canvas)
            print("self.instructionsPage")
        else:
            print('running game')
            self.drawFrame(canvas)
            self.drawInfo(canvas)
            if self.toastMessage:
                self.drawToastMessage(canvas)
            if self.displayMessage:
                self.drawMessage(canvas)
            
            self.drawInstructsWindow(canvas)

            self.drawWelcomeSign(canvas)
            self.drawLake(canvas)
            self.drawMountains(canvas)
            self.drawTipis(canvas)
            self.drawHouses(canvas)
            self.drawTrees(canvas)
            self.drawNewHouse(canvas)
            if self.movingHumans:
                self.drawHumans(canvas)


MyApp(width=1500, height=800)


