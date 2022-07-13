import pygame as pg
import numpy as np
import random
import matplotlib.pyplot as plt

pg.init()
w = 750
h = 750
screen = pg.display.set_mode((w, h))

pg.font.init()
my_font = pg.font.SysFont('Times New Roman', 50)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 153, 0)
screen.fill(green)

initialNumInfected = 100
infectionRate = 0.3
daysToRecover = 7
daysToSuseptible = 10
recoveryRate = 0.4
suseptibleRate = 0.2
daysRunning = 500
simsRunning = 15

def initialInfect(initialNumInfected):
    i = 0
    while i < initialNumInfected:
        xNum, yNum = random.randint(0, 149), random.randint(0, 149)
        if cellGrid[yNum][xNum][0] == 0:
            cellGrid[yNum][xNum][0] = 2
            i += 1

def gatherData(num):
    numSus = 0
    numInf = 0
    numRec = 0
    for y in range(150):
        for x in range(150):
            if cellGrid[y][x][0] == 0:
                numSus += 1
            elif cellGrid[y][x][0] == 1 or cellGrid[y][x][0] == 2:
                numInf += 1
            elif cellGrid[y][x][0] == 3:
                numRec += 1
    stats[num][0].append(numSus)
    stats[num][1].append(numInf)
    stats[num][2].append(numRec)

def showCellsStatus():
    for y in range(150):
        for x in range(150):
            if cellGrid[y][x][0] == 0:
                pg.draw.rect(screen, green, pg.Rect(x * 5, y * 5, 5, 5))
            elif cellGrid[y][x][0] == 1:
                pg.draw.rect(screen, red, pg.Rect(x * 5, y * 5, 5, 5))
            elif cellGrid[y][x][0] == 2:
                pg.draw.rect(screen, red, pg.Rect(x * 5, y * 5, 5, 5))
            elif cellGrid[y][x][0] == 3:
                pg.draw.rect(screen, blue, pg.Rect(x * 5, y * 5, 5, 5))

def spreadInfection():
    for y in range(150):
        for x in range(150):
            if cellGrid[y][x][0] == 3 and cellGrid[y][x][1] >= daysToSuseptible and random.uniform(0, 1) < suseptibleRate:
                cellGrid[y][x][0] = 0
                cellGrid[y][x][1] = 0
                
            elif cellGrid[y][x][0] == 3:
                cellGrid[y][x][1] += 1

    for y in range(150):
        for x in range(150):
            if cellGrid[y][x][0] == 1:
                cellGrid[y][x][0] = 2

    for y in range(150):
        for x in range(150):
            if cellGrid[y][x][0] == 2 and cellGrid[y][x][1] >= daysToRecover and random.uniform(0,1) < recoveryRate:
                cellGrid[y][x][0] = 3
                cellGrid[y][x][1] = 0

            elif cellGrid[y][x][0] == 2:
                cellGrid[y][x][1] += 1
                try:
                    if cellGrid[y-1][x-1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y-1][x-1][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y-1][x][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y-1][x][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y-1][x+1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y-1][x+1][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y][x+1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y][x+1][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y+1][x+1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y+1][x+1][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y+1][x][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y+1][x][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y+1][x-1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y+1][x-1][0] = 1
                except:
                    pass
                try:
                    if cellGrid[y][x-1][0] == 0 and random.uniform(0, 1) < infectionRate:
                        cellGrid[y][x-1][0] = 1
                except:
                    pass

stats = {}
for i in range(daysRunning):
        stats[i] = [[], [], []]

x= 0
while x < simsRunning:
    cellGrid = []
    for y in range(150):
        cellGrid.append([[0, 0] for x in range(150)])
    
    initialInfect(initialNumInfected)

    i = 0
    while i < daysRunning:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        spreadInfection()
        showCellsStatus()
        simCounter = my_font.render(f'Simulation: {x + 1}/{simsRunning}', False, white)
        dayCounter = my_font.render(f'Day: {i + 1}/{daysRunning}', False, white)
        screen.blit(simCounter, (0, 0))
        screen.blit(dayCounter, (475, 0))
        gatherData(i)
        pg.display.update()
        i += 1

    x += 1


susData = []
infData = []
recData = []

for i in range(len(stats)):
    susData.append(np.average(stats[i][0]))
    infData.append(np.average(stats[i][1]))
    recData.append(np.average(stats[i][2]))

dataTimes = []
for i in stats.keys():
    i += 1
    dataTimes.append(i)



plt.plot(dataTimes, susData, label = "Suseptible", color='green' )
plt.plot(dataTimes, infData, label = "Infected", color = 'red')
plt.plot(dataTimes, recData, label = "Recovered", color='blue')
plt.legend()
plt.show()