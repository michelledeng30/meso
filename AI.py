

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

def main():

    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = (2, 2)
    end = (8, 8)

    path = astar(grid, start, end)
    print(path)

if __name__ == '__main__':
    main()

    
    
    
    
    
    


