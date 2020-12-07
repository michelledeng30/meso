from cmu_112_graphics import *
import basic_graphics, time, random
from dataclasses import make_dataclass
import play

Human = make_dataclass('Human', ['startRow', 'startCol', 'endRow', 'endCol', 'path'])

class Lake(object):
    lake = (-100, -100)

    def draw(self, canvas):
        if Lake.lake != None:
            (x,y) = Lake.lake
            canvas.create_oval(x - self.lakeR, y - self.lakeR + 10, 
                               x + self.lakeR, y + self.lakeR - 10, 
                               fill='dodgerblue', width=2, 
                               outline='blue')

class Mountain(object):
    mountains = []

    def __init__(self, canvas, mountains):
        self.canvas = canvas
         # list of tuples
        
    def draw(self, canvas):
        for (x, y) in Mountain.mountains:
            canvas.create_polygon(x,                     y - self.mountainR2,
                                  x + 2*self.mountainR1, y + self.mountainR1,
                                  x + 3*self.mountainR1, y + self.mountainR1,
                                  x + self.mountainR2,   y + self.mountainR2,
                                  x - self.mountainR2,   y + self.mountainR2,
                                  x - 3*self.mountainR1, y - self.mountainR1,
                                  x - 2*self.mountainR1, y - self.mountainR1,
                                  fill='darkgrey')
        
class Tipi(object):
    tipis = []

    def __init__(self, canvas, tipis):
        self.canvas = canvas
        
    def draw(self, canvas):
        for (x, y) in Tipi.tipis:
            canvas.create_polygon(x,            y-self.tipiR,
                                  x+self.tipiR, y+self.tipiR,
                                  x-self.tipiR, y+self.tipiR,
                                  fill='burlywood', width=3, 
                                  outline='sienna')

            canvas.create_line(x, y-self.tipiR, x+8, y-self.tipiR-15, 
                               fill='sienna', width=3)
            canvas.create_line(x, y-self.tipiR, x-8, y-self.tipiR-15,
                               fill='sienna', width=3)

class House(object):
    houses = []
    def draw(self, canvas):
        for (x, y) in House.houses:
            canvas.create_polygon(x-self.houseR,   y-self.houseR,
                                    x-self.houseR, y+self.houseR,
                                    x+self.houseR, y+self.houseR,
                                    x+self.houseR, y-self.houseR,
                                    x,             y-(2*self.houseR),
                                    fill='silver', outline='black', width=2)

class Tree(object):
    trees = []
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        for (x, y) in Tree.trees:    
            canvas.create_polygon(x - self.treeR//1.5, y,
                                  x,                y - (3/2)*(self.treeR//1.5),
                                  x + self.treeR//1.5, y,
                                  fill='darkgreen')
            canvas.create_polygon(x - self.treeR, y + self.treeR,
                                  x,              y - ((1/2)*self.treeR),
                                  x + self.treeR, y + self.treeR,
                                  fill='darkgreen')
            canvas.create_polygon(x - (self.treeR*1.2), y + 2*(self.treeR),
                                  x,                    y + ((1/4)*(self.treeR)),
                                  x + (self.treeR*1.2), y + 2*(self.treeR),
                                  fill='darkgreen')
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

        mode.lakeR = 80
        mode.mountainR1 = 10
        mode.mountainR2 = 60
        mode.tipiR = 20
        mode.treeR = 15
        mode.objectR = 5

    def getMap(mode):
        
        # lake
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)

            if play.Play.isValid(mode, x, y, mode.lakeR):
                Lake.lake = x, y
                break
    
            # mountains
        while True:
            x = random.randint(0, mode.frameRightbound-mode.margin/2)
            y = random.randint(0, mode.height - mode.margin)
            if play.Play.isValid(mode, x, y, mode.mountainR2):
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
