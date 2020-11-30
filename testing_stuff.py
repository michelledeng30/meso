import random
from cmu_112_graphics import *


def yup(humans):
    for human in humans:
        destX, destY = random.choice(houses)
        human.append(destX)
        human.append(destY)
    return humans

houses = [(1,1),(2,2),(4,4)]
# print(yup([[10,10],[50,50]]))

# x = 300, y = 300

def appStarted(app):
    app.x = 200
    app.y = 200
    app.r = 30

def redrawAll(app, canvas):
    canvas.create_polygon(app.x, app.y-app.r,
                          app.x+app.r, app.y+app.r,
                          app.x-app.r, app.y+app.r,
                          fill='saddlebrown', outline='black', width=3)
    canvas.create_line(app.x, app.y-app.r, app.x+8, app.y-app.r-15, 
                       fill='black', width=3)
    canvas.create_line(app.x, app.y-app.r, app.x-8, app.y-app.r-15,
                       fill='black', width=3)

# runApp(width=400, height=400)

openList = ['a', 23432, None]
#print(enumerate(openList))

def tryna():
    lst = [(1,1),(2,2),(3,3)]
    for item in lst:
        human[0], human[1] = random.choice(lst)
        destX, destY = random.choice(lst)
        




tryna()

