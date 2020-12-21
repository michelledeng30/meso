from cmu_112_graphics import *
import basic_graphics, time, random
import objects, frames, message, play
from dataclasses import make_dataclass

# astar runs the search algorithm for the humans by taking in a start and end position
# and generating a path. it also sets up the grid with the obstacles


# CITATION: for lines 13-24 and 76-171 the a* algorithm was adapted from 
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

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

        lakeCellRX = int(self.lakeRX / self.cellSize) 
        lakeCellRY = int(self.lakeRY / self.cellSize)

        for row in range(lakeRow - lakeCellRY, lakeRow + lakeCellRY):
            for col in range(lakeCol - lakeCellRX, lakeCol + lakeCellRX):
                self.grid[row][col] = 1
        
        # establish mountain as obstacle
        for x, y in objects.Mountain.mountains:
            (midRow, midCol) = play.Play.getCell(self, x, y)

            # first section
            for row in range(midRow-13, midRow-6):
                for col in range(midCol-4, midCol+4):
                    self.grid[row][col] = 1
            
            # second section
            for row in range(midRow-6, midRow):
                for col in range(midCol-7, midCol+7):
                    self.grid[row][col] = 1
            
            # third section
            for row in range(midRow, midRow+6):
                for col in range(midCol-10, midCol+10):
                    self.grid[row][col] = 1
            
            # fourth section
            for row in range(midRow+6, midRow+12):
                for col in range(midCol-15, midCol+16):
                    if (row < self.rows) and (col < self.cols):
                        self.grid[row][col] = 1
            
            # fifth section
            for row in range(midRow+12, midRow+15):
                for col in range(midCol-17, midCol+18):
                    if (row < self.rows) and (col < self.cols):
                        self.grid[row][col] = 1

        return self.grid

    def findPath(self, grid, start, end):

        # create start and end node
        startNode = Node(None, start)
        startNode.g = startNode.h = startNode.f = 0
        endNode = Node(None, end)
        endNode.g = endNode.h = endNode.f = 0

        # create the target list and the visited list
        newList = []
        visitedList = []

        # add start node to target list
        newList.append(startNode)

        # loop until a path is found
        while len(newList) > 0:

            # Get the current node
            currentNode = newList[0]
            currentIndex = 0
            for index, item in enumerate(newList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            # we don't want this node, pop off new list, add to visited list
            newList.pop(currentIndex)
            visitedList.append(currentNode)

            # found the end and path
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # return reversed path

            # generate children -> possible directions
            children = []
            dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for newPosition in dirs: 

                # get node position
                nodePosition = (currentNode.position[0] + newPosition[0], 
                                 currentNode.position[1] + newPosition[1])

                # make sure node is on the board
                if ((nodePosition[0] > (self.rows - 1)) or 
                    (nodePosition[0] < 0) or 
                    (nodePosition[1] > (self.cols - 1)) or 
                    (nodePosition[1] < 0)):
                    continue

                # make sure the cell is valid (0, not 1)
                if grid[nodePosition[0]][nodePosition[1]] != 0:
                    continue

                # create new node
                newNode = Node(currentNode, nodePosition)

                # add to children list
                children.append(newNode)

            # loop through children
            for child in children:

# CITATION: lines 148-154 and 162-168 for checking if we have already tried the child from 
# https://gist.github.com/MageWang/48a2626c8280a6b59c89cc4bff6b0e37

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

                # child is already in the new list
                check2 = False
                for newNode in newList:
                    if child == newNode and child.g > newNode.g:
                        check2 = True
                        continue
                if check2:
                    continue

                # child is valid, add the child to the new list
                newList.append(child)




