from cmu_112_graphics import *
import basic_graphics, time, random
import objects

# disaster causes some kind of 'disaster' in the game and then changes the population
# and sometimes the list of structures. it also causes the end of the game.

class Disaster(object):

    def death(self):
        self.deathCount = int(len(self.humans) * self.deathRate)
        for i in range(self.deathCount):
            victim = random.choice(self.humans)
            self.humans.remove(victim)
    
    def destruction(self):
        self.structures = objects.Tipi.tipis + objects.House.houses
        self.destructionCount = int(len(self.structures) * self.destructionRate)
        for i in range(self.destructionCount):
            structure = random.choice(self.structures)
            if structure in objects.Tipi.tipis:
                objects.Tipi.tipis.remove(structure)
            else:
                objects.House.houses.remove(structure)

    def pandemic(self):
        self.deathRate = 0.30
        Disaster.death(self)
    
    def famine(self):
        self.deathRate = 0.20
        Disaster.death(self)
    
    def wildfire(self):
        self.deathRate = 0.15
        self.destructionRate = 0.10
        Disaster.death(self)
        Disaster.destruction(self)

    def earthquake(self):
        self.deathRate = 0.10
        self.destructionRate = 0.15
        Disaster.death(self)
        Disaster.destruction(self)

    def end(self):
        population = len(self.humans)
        for i in range(population-3):
            self.humans.pop()
        
    







