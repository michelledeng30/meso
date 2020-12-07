from cmu_112_graphics import *
import basic_graphics, time, random
import objects, frames, message, play
from dataclasses import make_dataclass

# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# lines 9 to 21 and 72 to 152

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class AStar(object):

    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

    def obstacles(self):
        # establish lake as obstacle

        lakeX, lakeY = objects.Lake.lake
        lakeRow, lakeCol = play.Play.getCell(self, lakeX, lakeY)

        lakeCellR = int(self.lakeR / self.cellSize) # 80/5 = 16

        for row in range(self.rows):
            for col in range(self.cols):
                if AStar.distance(lakeRow, lakeCol, row, col) <= lakeCellR:
                    self.grid[row][col] = 1
        
        # establish mountain as obstacle
        for x, y in objects.Mountain.mountains:
            (midRow, midCol) = play.Play.getCell(self, x, y)

            # first section
            for row in range(midRow-12, midRow-6):
                for col in range(midCol-3, midCol+3):
                    self.grid[row][col] = 1
            
            # second section
            for row in range(midRow-6, midRow):
                for col in range(midCol-6, midCol+6):
                    self.grid[row][col] = 1
            
            # third section
            for row in range(midRow, midRow+6):
                for col in range(midCol-9, midCol+9):
                    self.grid[row][col] = 1
            
            # fourth section
            for row in range(midRow+6, midRow+13):
                for col in range(midCol-12, midCol+13):
                    if (row < self.rows) and (col < self.cols):
                        self.grid[row][col] = 1

        return self.grid


    def findPath(self, grid, start, end):

        # Create start and end node
        startNode = Node(None, start)
        startNode.g = startNode.h = startNode.f = 0
        endNode = Node(None, end)
        endNode.g = endNode.h = endNode.f = 0

        # Initialize both open and closed list
        newList = []
        visitedList = []

        # Add the start node
        newList.append(startNode)

        # Loop until you find the end
        while len(newList) > 0:

            # Get the current node
            currentNode = newList[0]
            currentIndex = 0
            for index, item in enumerate(newList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            # Pop current off open list, add to closed list
            newList.pop(currentIndex)
            visitedList.append(currentNode)

            # Found the goal
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for newPosition in dirs: 

                # Get node position
                nodePosition = (currentNode.position[0] + newPosition[0], 
                                 currentNode.position[1] + newPosition[1])

                # Make sure within range
                if ((nodePosition[0] > (self.rows - 1)) or 
                    (nodePosition[0] < 0) or 
                    (nodePosition[1] > (self.cols - 1)) or 
                    (nodePosition[1] < 0)):
                    continue


                # Make sure not obstacle cell
                if grid[nodePosition[0]][nodePosition[1]] != 0:
                    continue

                # Create new node
                newNode = Node(currentNode, nodePosition)

                # Append
                children.append(newNode)

            # Loop through children
            for child in children:


                # Child is on the closed list
# https://gist.github.com/MageWang/48a2626c8280a6b59c89cc4bff6b0e37
# lines 142 to 148 and 157 to 163

                check1 = False
                for visitedChild in visitedList:
                    if child == visitedChild:
                        check1 = True
                        continue
                if check1:
                    continue

                # Create the f, g, and h values
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                
                check2 = False
                for newNode in newList:
                    if child == newNode and child.g > newNode.g:
                        check2 = True
                        continue
                if check2:
                    continue

                # Add the child to the open list
                newList.append(child)
            

    '''
    def findPath(self, grid, start, end): # returns a list of tuples as the path
        startNode = Node(None, start)
        startNode.g = startNode.h = startNode.f = 0
        endNode = Node(None, end)
        endNode.g = endNode.h = endNode.f = 0

        #initialize open & closed list
        pathList = []
        visitedList = []

        # add start node to open list
        pathList.append(startNode)

        # loops until you find a pathList
        while len(pathList) > 0:
            
            # get current node
            currentNode = pathList[0]
            currentIndex = 0
            for index, item in enumerate(pathList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index
            
            # remove current from open, add to closed
            pathList.pop(currentIndex)
            visitedList.append(currentNode)

            # found the end
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            # generate children -> possible directions to move in
            children = []
            dirs = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
            for newPosition in dirs:
                # get node position
                nodePosition = (currentNode.position[0] + newPosition[0], 
                                currentNode.position[1] + newPosition[1])
                
                # check its in range of grid
                if (nodePosition[0] > (len(grid)-1) or nodePosition[0] < 0 or
                    nodePosition[1] > (len(grid[0])-1) or nodePosition[1] < 0):
                    continue

                # check it's not an obstacle
                if grid[nodePosition[0]][nodePosition[1]] != 0:
                    continue

                # create a new node (position)
                newNode = Node(currentNode, nodePosition)

                # add to children list
                children.append(newNode)

            # loop through children
            for child in children:

                # check that the child is not on closed list
                for closedChild in visitedList:
                    if child == closedChild:
                        continue
                
                # create f, g, and h values
                child.g = currentNode.g + 1
                child.h = (((child.position[0] - endNode.position[0]) ** 2) +
                        ((child.position[1] - endNode.position[1]) ** 2))
                child.f = child.g + child.h

                # child is already in open list
                for openNode in pathList:
                    if child == openNode and child.g > openNode.g:
                        continue

                # add child to open list
                pathList.append(child)
        '''


