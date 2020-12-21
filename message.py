from cmu_112_graphics import *
import basic_graphics, time, random
import disaster, objects

# message creates all the popup instructions for the game

# the instructions for placing objects
class Message(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        text, color = None, None
        if self.startMessage:
            font='Verdana 14'
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawWelcome))
                            
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                               text='welcome to your new town! watch as civilians interact with each other and',
                               font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                               text='explore their surroundings. new townspeople are created when two collide',
                               font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                               text='so keep an eye out!',
                               font=font)

            canvas.create_text(self.windowX, self.windowY + self.windowYR - 20,
                           text='press ENTER to continue',
                           font='Verdana 12')

        else:
            if self.lakeMessage:
                text, color = 'click to place a lake.', 'dodgerblue'
            elif self.mountainMessage:
                text, color = 'click to place two mountains.', 'darkgrey'
            elif self.houseMessage:
                text, color = 'click to place 10 houses.', 'burlywood'
            elif self.treeMessage:
                text, color = 'click to place 10 trees.', 'darkgreen'

            elif (text, color) == (None, None):
                return
            canvas.create_rectangle(self.messageMidX - 150, 
                                    self.messageMidY - 20,
                                    self.messageMidX + 150, 
                                    self.messageMidY + 20,
                                    fill=color)    
            canvas.create_text(self.messageMidX, self.messageMidY,
                            text=text, font='Arial 14 bold')

# the popups that occur during the game
class Progress(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, canvas):
        
        font='Verdana 14'        
        
        # unlocked tipis
        if self.version == 1:

            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawTipi))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text=f'people have immigrated to town, so you\'ve unlocked the tipi upgrade to support', 
                            font=font)

            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text='your growing population! use the item bar on the right and click to select the tipi.',
                            font=font)                
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='then, click on the map to place your structure',
                            font=font)

        # unlocked houses
        elif self.version == 2:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawHouse))

            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='nice progress! you just unlocked stone cottage house. you can click to select the',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text='house feature and then click again to place it on the map. also, to spice things up,',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='you can place them on existing tipis to upgrade it into a cottage! and here\'s a', 
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 100,
                            text='hint: see what happens when you finish upgrading every single tipi on the map...', 
                            font=font)

        # unlocked skyscrapers
        elif self.version == 10:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawSkyscraper))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='we\'re moving into a new era! you\'ve successfully upgraded all the tipis to',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text='houses, and now you\'re free to create skyscrapers! however, these impressive',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='buildings come with a price: for each skyscraper placed, a tree will disappear.', 
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 110,
                            text='don\'t forsake the importance of the environment...', 
                            font=font)
        
        # unlocked trees
        elif self.version == 15:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawEnd))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='the environmental destruction is coming to light, and civilians are calling',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text='for change! you\'ve unlocked the ability to plant trees around town. so, pick',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='up a shovel and let\'s get our hands dirty!',
                            font=font)
            
        # epidemic
        elif self.version == 3:
            sick = int((len(self.humans)*4) * 0.40)
            dead = int((len(self.humans)*4) * 0.30)
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawPandemic))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='oh no! one if the new residents has the elusive COVID-20 virus. the town has',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text=f'suffered a huge epidemic. without quick action, {sick} civilians contracted the',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text=f'highly contagious sickness, leading to {dead} deaths before the vaccine was found.',
                            font=font)

        # famine
        elif self.version == 4:
            dead = int((len(self.humans)*4) * 0.20)
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawFamine))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text=f'it\'s spring {self.year}, and there\'s just been another bad harvest. the famine is',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text=f'reaching its peak, and people are struggling to get by. over the past few winters,',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text=f'you\'ve tragically lost {dead} residents to hunger.',
                            font=font)

        # wildfire
        elif self.version == 5:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawFire))
            dead = int((len(self.humans)*4) * 0.15)
            structures = objects.Tipi.tipis + objects.House.houses
            destruct = int(len(structures) * 0.10) + 1
            if destruct == 1: word = 'structure'
            else: word = 'structures'

            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='after a forest bonfire party gone wrong, a wildfire raged through the town! unfortunately',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text=f'{destruct} {word} burned down and {dead} perished in the flames. learn your fire safety',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='and always be careful!',
                            font=font)
        
        # earthquake
        elif self.version == 6:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawEarthquake))
            dead = int((len(self.humans)*4) * 0.10)
            structures = objects.Tipi.tipis + objects.House.houses
            destruct = int(len(structures) * 0.15) + 1
            if destruct == 1: word = 'structure'
            else: word = 'structures'

            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text='we didn\'t realize that the town was built on a faultline, and a terrifying 6.9 magnitude',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text=f'earthquake occurred late last night. {destruct} {word} were wholly demolished, taking the',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text=f'lives of {dead} in the process.',
                            font=font)

        # end of game
        elif self.version == 100:
            canvas.create_image(self.windowX, self.windowY, 
                                image=ImageTk.PhotoImage(self.drawEnd))
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 40,
                            text=f'alas, all good things must come to an end. this town has been thriving for ages, but ',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 60,
                            text=f'on the year {self.year} A112, it all comes crashing down. overpopulation, destruction of the',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 80,
                            text='environment, and lack of space and structure has caused increasing conflict until war',
                            font=font)
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 100,
                            text='inevitably broke out. only 25 people survived the brutal conflict.',
                            font=font)

            canvas.create_text(self.windowX, self.windowY - self.windowYR + 130,
                            text='but have no fear. civilization will grow again, and life will prosper.',
                            font=font)
                        
            canvas.create_text(self.windowX, self.windowY - self.windowYR + 200,
                            text='THANK YOU FOR PLAYING.',
                            font='Verdana 20 bold')
            return

        canvas.create_text(self.windowX, self.windowY + self.windowYR - 20,
                           text='press ENTER to continue',
                           font='Verdana 12')