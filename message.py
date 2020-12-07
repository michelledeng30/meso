from cmu_112_graphics import *
import basic_graphics, time, random

class Message(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        text, color = None, None
        if self.lakeMessage:
            text, color = 'Click to place a lake.', 'dodgerblue'
        elif self.mountainMessage:
            text, color = 'Click to place two mountains.', 'darkgrey'
        elif self.houseMessage:
            text, color = 'Click to place 10 houses.', 'burlywood'
        elif self.treeMessage:
            text, color = 'Click to place 10 trees.', 'darkgreen'
        elif self.startMessage:
            text, color = 'Press SPACE to begin!', 'bisque'
        elif (text, color) == (None, None):
            return
        canvas.create_rectangle(self.messageMidX - 150, 
                                self.messageMidY - 20,
                                self.messageMidX + 150, 
                                self.messageMidY + 20,
                                fill=color)    
        canvas.create_text(self.messageMidX, self.messageMidY,
                           text=text, font='Arial 14 bold')


class Toast(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        canvas.create_text(self.width//3 + 50, self.height - 40, 
                           text='Object is not valid! Try placing again',
                           font='Arial 16 bold', fill='red')
    
