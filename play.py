from cmu_112_graphics import *
import basic_graphics, time, random
import objects, frames, message, astar
from dataclasses import make_dataclass

Human = make_dataclass('Human', ['startRow', 'startCol', 'endRow', 'endCol', 'path'])

class Play(object):

    buffer1 = 50
    buffer2 = 20
    rows = 152
    cols = 219


    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

    def getCell(self, x, y):
        row = int((y - self.margin) / self.cellSize)
        col = int((x - self.margin) / self.cellSize)

        return row, col

    def isValid(self, x, y, r):

        # check boundary
        if ((x <= self.margin + r + Play.buffer1) or 
            (x >= self.frameRightbound - r - Play.buffer1) or 
            (y <= self.margin + Play.buffer1) or 
            (y >= self.height - self.margin - Play.buffer1)):
            self.toastTime = time.time()
            return False

        # first case: lake
        if (x, y) == (-100, 100): return True

        # check lake
        lakeX, lakeY = objects.Lake.lake
        if Play.distance(x, y, lakeX, lakeY) <= self.lakeR + r + Play.buffer2:
            self.toastTime = time.time()
            return False

        # check mountain
        for cx, cy in objects.Mountain.mountains:
            if Play.distance(x, y, cx, cy) <= self.mountainR2 + r + Play.buffer2:
                self.toastTime = time.time()
                return False
        
        # check objects
        objectList = objects.Tipi.tipis + objects.Tree.trees + objects.House.houses
        for cx, cy in objectList:
            if Play.distance(x, y, cx, cy) <= self.tipiR + r + Play.buffer2:
                self.toastTime = time.time()
                return False
        return True

        # check welcome sign
        signX, signY = self.signX, self.signY
        if Play.distance(x, y, signX, signY) <= 30 + r + Play.buffer2:
            self.toastTime = time.time()
            return False

    def getHumans(self):
        humanList = []
        structures = objects.Tipi.tipis + objects.House.houses

        
        for human in self.humans:
            startX, startY = random.choice(structures)
            startRow, startCol = Play.getCell(self, startX, startY)
            endX, endY = random.choice(structures)
            endRow, endCol = Play.getCell(self, endX, endY)
            path = astar.AStar.findPath(self, self.grid, (startRow, startCol), (endRow, endCol))
            newHuman = Human(startRow=startRow, startCol=startCol,
                             endRow=endRow, endCol=endCol, 
                             path=path)
            humanList.append(newHuman)
        return humanList
    
    def findNewDest(self, human):
        structures = objects.Tipi.tipis + objects.House.houses
        endX, endY = random.choice(structures)
        endRow, endCol = Play.getCell(self, endX, endY)
        human.endRow, human.endCol = endRow, endCol
        human.path = astar.AStar.findPath(self, self.grid,
                                         (human.startRow, human.startCol),
                                         (human.endRow, human.endCol))

    def moveHuman(self):
        for human in self.humans:
            

            # check if destination is reached
            if (human.path == None) or (len(human.path) == 0):
                Play.findNewDest(self, human)
            else:
                (human.startRow, human.startCol) = human.path[0]
                human.path.pop(0)
            
            Play.checkCollision(self, human)
    
    def getNewHuman(self, row, col):
        structures = objects.Tipi.tipis + objects.House.houses
        (startRow, startCol) = (row, col)
        endX, endY = random.choice(structures)
        endRow, endCol = Play.getCell(self, endX, endY)
        path = astar.AStar.findPath(self, self.grid, (startRow, startCol), (endRow, endCol))
        newHuman = Human(startRow=startRow, startCol=startCol,
                         endRow=endRow, endCol=endCol, 
                         path=path)
        self.humans.append(newHuman)


    def checkCollision(self, current):
        structures = objects.Tipi.tipis + objects.House.houses
        humanList = copy.copy(self.humans)
        humanList.remove(current)
        for human in humanList:
            if (len(current.path) >= 2) and (len(human.path) >= 2):
                if ((current.path[0] == human.path[0]) and 
                (current.path[1] != human.path[1])):
                    x, y = random.choice(structures)
                    row, col = Play.getCell(self, x, y)
                    Play.getNewHuman(self, row, col)
                


    

    