from cmu_112_graphics import *
import basic_graphics, time, random

def appStarted(app):
    app.first = True
    app.name = app.getUserInput("What is the name of your town?")


def mousePressed(app, event):
    pass

def keyPressed(app, event):
    if event.key == 'Enter':
        app.first = False
    elif event.key == 'p':
        drawP(app, canvas)

def drawP(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text='P')

def drawSplash(app, canvas):
    canvas.create_text(app.width//2, app.height//4, 
                       text='civilization simulator', 
                       font='Arial 26 bold', 
                       fill='blue')
    canvas.create_text(app.width//2, app.height//2,
                       text=f'Welcome to the town of \'{app.name}\'!',
                       font='Arial 20 bold')

def drawMessage(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
                       text='THE GAME!!!!', font='Arial 26 bold', 
                       fill='green')

def redrawAll(app, canvas):
    if app.first == True:
        drawSplash(app, canvas)
    else:
        drawMessage(app, canvas)
    

runApp(width=500, height=500)