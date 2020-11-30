from cmu_112_graphics import *
import basic_graphics, time, random


# game dimensions: (20, 20, 1115, 780)
# grid size: 1095 * 760

'''
right now:
    tipis are in pixels
    humans are in grids


'''

class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # distance to start node, distance travelled
        self.h = 0 # estimated distance to end node
        self.f = 0 # total distance from start to end node

    # compare nodes
    def __eq__(self, other):
        return self.position == other.position


def astar(grid, start, end): # returns a list of tuples as the path
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    #initialize open & closed list
    openList = []
    closedList = []

    # add start node to open list
    openList.append(startNode)

    # loops until you find a path
    while len(openList) > 0:
        
        # get current node
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index
        
        # remove current from open, add to closed
        openList.pop(currentIndex)
        closedList.append(currentNode)

        # found the end
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # generate children
        children = []
        dirs = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
        for newPosition in dirs:
            # get node position
            nodePosition = (currentNode.position[0] + newPosition[0], 
                            currentNode.position[1] + newPosition[1])
            
            # check its in range
            if (nodePosition[0] > (len(grid)-1) or nodePosition[0] < 0 or
                nodePosition[1] > (len(grid[0])-1) or nodePosition[1] < 0):
                continue

            # check it's not an obstacle
            if grid[nodePosition[0]][nodePosition[1]] != 0:
                continue

            # create a new node
            newNode = Node(currentNode, nodePosition)

            # add to children list
            children.append(newNode)

        # loop through children
        for child in children:

            # check that the child is not on closed list
            for closedChild in closedList:
                if child == closedChild:
                    continue
            
            # create f, g, and h values
            child.g = currentNode.g + 1
            child.h = (((child.position[0] - endNode.position[0]) ** 2) +
                       ((child.position[1] - endNode.position[1]) ** 2))
            child.f = child.g + child.h

            # child is already in open list
            for openNode in openList:
                if child == openNode and child.g > openNode.g:
                    continue

            # add child to open list
            openList.append(child)

def appStarted(app):
    app.margin = 20
    app.cellSize = 5
    app.frameRightbound = 3*(app.width/4)
    app.rows = 152
    app.cols = 219

    app.lake = (500, 300)
    app.lakeR = 80
    app.mountains = [(300,200), (500,500)]
    app.mountainR1 = 10
    app.mountainR2 = 60



    app.grid = [([0] * app.cols) for row in range(app.rows)]
    app.grid = obstacles(app)

    app.tipis = [(100,200), (400, 400), (600, 200), (500, 100), 
                 (700,400), (300, 700), (900, 500)]
    
    app.tipiR = 20
    app.humanR = 5

    app.humans = [[None, None, None, None, None] for i in range(6)]
    #[startX, startY, endX, endY, path]
    app.humans = getHumans(app)

    app.paused = True

def obstacles(app):
    lakeX, lakeY = app.lake
    lakeRow, lakeCol = getCell(app, lakeX, lakeY)

    mountainX1, mountainY1 = app.mountains[0]
    mountainX2, mountainY2 = app.mountains[1]
    mountainRow1, mountainCol1 = getCell(app, mountainX1, mountainY1)
    mountainRow2, mountainCol2 = getCell(app, mountainX2, mountainY2)

    lakeRadius = int(app.lakeR / app.cellSize) # 80/5 = 16
    mountainRadius = int(app.mountainR2 / app.cellSize) # 60/5 = 12

    for x in range(app.cols):
        for y in range(app.rows):
            if distance(lakeRow, lakeCol, x, y) <= lakeRadius:
                app.grid[x][y] = 1
            if distance(mountainRow1, mountainCol1, x, y) <= mountainRadius:
                app.grid[x][y] = 1
            if distance(mountainRow2, mountainCol2, x, y) <= mountainRadius:
                app.grid[x][y] = 1
    return app.grid

def timerFired(app):
    if app.paused == False:
        moveHuman(app)

def keyPressed(app, event):
    if event.key == 'Space':
        app.paused = not app.paused

def moveHuman(app):
    for human in app.humans:
        path = human[4]

        # check if destination is reached
        if (path == None) or (len(path) == 0):
            findNewDest(app, human)
        else:
            (human[0], human[1]) = path[0]
            path.pop(0)


def findNewDest(app, human): # and path
    x, y = random.choice(list(app.tipis))
    destX, destY = getCell(app, x, y)
    human[2], human[3] = destX, destY
    path = astar(app.grid, (human[0], human[1]), (human[2], human[3]))
    human[4] = path

def getHumans(app):
    newList = []
    for human in app.humans:
        x, y = random.choice(list(app.tipis))
        human[0], human[1] = getCell(app, x, y)
        destX, destY = random.choice(list(app.tipis))
        human[2], human[3] = getCell(app, x, y)
        #if (destX, destY) == (human[0], human[1]):
        #    newX, newY = random.choice(list(app.tipis))
        #    destX, destY = getCell(app, x, y)
        path = astar(app.grid, (human[0], human[1]), (human[2], human[3]))
        human[4] = path
        newList.append(human)
    return newList


def drawHumans(app, canvas):

    for human in app.humans:
        row = human[0]
        col = human[1]
        x = col*5 + app.margin
        y = row*5 + app.margin
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


def drawFrame(app, canvas):
    # game
    canvas.create_rectangle(app.margin, app.margin, 
                            app.frameRightbound-app.margin/2, 
                            app.height - app.margin,
                            fill='palegreen', width=2)
    # info
    canvas.create_rectangle(app.frameRightbound+app.margin/2, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            fill='mistyrose', width=2)

def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = 1095
    gridHeight = 760
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)
    
def getCell(app, x, y):
    row = int((y - app.margin) / app.cellSize)
    col = int((x - app.margin) / app.cellSize)

    return row, col


def redrawAll(app, canvas):
    drawFrame(app, canvas)
    drawLake(app, canvas)
    drawMountains(app, canvas)
    drawTipis(app, canvas)
    drawHumans(app, canvas)


runApp(width=1500, height=800)

