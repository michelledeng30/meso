from Queue import PriorityQueue

class State(object):
    def __init__(self, value, parent, start=0, goal=0, solver=0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def getDist(self):
        pass

    def createChildren(self):
        pass

class StateString(State):
    def __init__(self, value, parent, start=0, goal=0):
        super(StateString, self).__init__(value, parent, start, goal, solver)
        self.dist = self.getDist()

    def getDist(self):
        if self.value == self.goal:
            return 0
        dist = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            dist += abs(i - self.value.index(letter))
        return dist

    def createChildren(self):
        if not self.children:
            for i in xrange(len(self.goal)-1):
                val = self.value
                val = val[:i] + val[i+1] + val[i] + val[i+2:]
                child = StateString(val, self)
                self.children.append(child)

class AStar:
    def __init__(self, start, goal):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def solve(self):
        startState = StateString(self.start, 0, self.start, self.goal)
        count = 0
        self.priorityQueue.put((0, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            closestChild.createChildren()
            self.visitedQueue.append(closestChild.value)
            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count += 1
                    if not child.dist: # distance is 0, made it to goal
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, startState))
        if not self.path:
            print("Goal is not possible")
        return self.path

if __name__ == "__main__":
    start1 = "ecbda"
    goal1 = "dabcd"
    print('starting...')
    a = AStar(start1, goal1)
    a.solve()
    for i in xrange(len(a.path)):
        print("%d) " %i + a.path[i])
                

    


