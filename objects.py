from cmu_112_graphics import *
import basic_graphics, time, random
from dataclasses import make_dataclass
import play, astar

Human = make_dataclass('Human', ['startRow', 'startCol', 'endRow', 'endCol', 'path'])

'''
class River(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def displace(self, startRow, endRow):
        maxDisp = 4

        widths = [0] * self.cols
        segments = []
        segments.append((startRow, endRow, maxDisp))

        while len(segments) > 0:
            topRow, bottomRow, randomness = segments.pop(0)

            center = (topRow + bottomRow + 1) // 2

            widths[center] = (widths[topRow] + widths[bottomRow])
            disp = random.randint(-randomness, randomness)
            widths[center] += disp

            
            if bottomRow - topRow > 2:
                segments.append((topRow, center, math.floor(randomness//2)))
                segments.append((center, bottomRow, math.floor(randomness//2)))

        # widths is a list of horizontal displacements, 
        # matching up with the index which is the col
        return widths

    def getRiverPath(self, startRow=0, startCol=50, 
                     endRow=152-1, endCol=50):

        path = astar.AStar.findPath(self, self.grid, (startRow, startCol), (endRow, endCol))
        newPath = []
        widths = displace(self, startRow, endRow)
        for row, col in path:
            colDisp = widths[row]
            newCol = col + colDisp
            while newCol < 0:
                newCol += 1
            newPath.append((row, newCol))
        return newPath
'''

class Lake(object):
    lake = (-100, -100)

    def draw(self, canvas):
        if Lake.lake != None:
            (x,y) = Lake.lake
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.lakeIMG))

class Mountain(object):
    mountains = []

    def __init__(self, canvas, mountains):
        self.canvas = canvas
         # list of tuples
        
    def draw(self, canvas):
        for (x, y) in Mountain.mountains:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.mountainIMG))
        
class Tipi(object):
    tipis = []

    def __init__(self, canvas, tipis):
        self.canvas = canvas
        
    def draw(self, canvas):
        for (x, y) in Tipi.tipis:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.tipiIMG))

class House(object):
    houses = []
    def draw(self, canvas):
        for (x, y) in House.houses:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.houseIMG))

class Skyscraper(object):
    skyscrapers = []
    def draw(self, canvas):
        for (x, y) in Skyscraper.skyscrapers:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.skyscraperIMG))

class Tree(object):
    trees = []
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        for (x, y) in Tree.trees:  
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.treeIMG))

class WelcomeSign(object):
    def draw(self, canvas):
        canvas.create_rectangle(self.signX-30, self.signY-15, 
                                self.signX+30, self.signY+15,
                                fill='tan', outline='black', width=1)
        canvas.create_line(self.signX, self.signY+15, self.signX, self.signY + 30, 
                           fill='black', width=2)
        canvas.create_text(self.signX, self.signY - 5, text='Welcome', font='Verdana 10')
        canvas.create_text(self.signX, self.signY + 5, text=f'to {self.townName}!', 
                           font='Verdana 10')

class Human(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        if self.humans != [[None, None, None, None] for i in range(5)]:
            for human in self.humans:
                row, col = human.startRow, human.startCol
                x, y = Human.getCellCenter(self, row, col)
                canvas.create_oval(x-self.objectR, y-self.objectR,
                                x+self.objectR, y+self.objectR,
                                fill='black')

    def getCellCenter(self, row, col):
        gridWidth  = 1095
        gridHeight = 760
        x = self.margin + gridWidth * (col+0.5) / self.cols
        y = self.margin + gridHeight * (row+0.5) / self.rows
        return (x, y)


class RandomMap(Mode):

    def appStarted(mode):

        mode.margin = 20
        mode.frameRightbound = 3*(mode.width/4)

        mode.lakeRX = 120
        mode.lakeRY = 80
        mode.mountainR = 70
        mode.tipiR = 25
        mode.treeR = 20
        mode.objectR = 4

    def getMap(mode):
        
        # lake
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)

            if play.Play.isValid(mode, x, y, mode.lakeRX):
                Lake.lake = x, y
                break
    
            # mountains
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)
            if play.Play.isValid(mode, x, y, mode.mountainR):
                Mountain.mountains.append((x,y))
                if len(Mountain.mountains) == 2:
                    break
        # tipis
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)
            if play.Play.isValid(mode, x, y, mode.tipiR):
                Tipi.tipis.append((x,y))
                if len(Tipi.tipis) == 10:
                    break
        
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)
            if play.Play.isValid(mode, x, y, mode.treeR): 
                Tree.trees.append((x,y))
                if len(Tree.trees) == 10:
                    break
                




'''
    def draw(self, canvas):
        for human in self.humans:
            x = human[0]
            y = human[1]
            canvas.create_oval(x-self.objectR, y-self.objectR,
                               x+self.objectR, y+self.objectR,
                               fill='black')
'''
