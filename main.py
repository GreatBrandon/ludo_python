import pygame
from pygame.locals import *
import random
import matplotlib.pyplot as plt
import time
import pandas as pd
import csv

# variables, constants, lists
WIDTH = 1000
HEIGHT = 820
FPS = 60
BLACK = (0,0,0)
BLACK2 = (50,50,50)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
RED2 = (191, 29, 17)

# track pos 0-15 is starting squares yellow green red black
# track pos 16 starts at yellow starting square!!! 26 green start 36 red start 46 black start 55 end track
# track pos 56-59 yellow 60-63 green 64-67 red 68-71 black
TRACKX = [103,178,103,178,632,707,632,707,635,710,635,710,102,178,102,178,     62,123,184,245,306,306,306,306,306,405,504,504,504,504,504,565,626,687,748,748,748,687,626,565,504,504,504,504,504,405,306,306,306,306,306,245,184,123,62,62,     119,174,229,285,405,405,405,405,693,637,581,525,405,405,405,405]
TRACKY = [105,105,180,180,105,105,180,180,639,639,715,715,640,640,717,717,     309,309,309,309,309,248,187,126,65,65,65,126,187,248,309,309,309,309,309,408,507,507,507,507,507,568,629,690,751,751,751,690,629,568,507,507,507,507,507,408,     408,408,408,408,120,174,230,286,408,408,408,408,697,641,585,529]

def reset(): # reset
    global POSITIONS, COLOURS, PLAYER, HUMANS, PRIORITY, DISTANCETRAVELLED, amountofrolls, amountofturns, timer, inputtext, turn
    POSITIONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    COLOURS = [YELLOW, YELLOW, YELLOW, YELLOW, GREEN, GREEN, GREEN, GREEN, RED, RED, RED, RED ,BLACK2, BLACK2, BLACK2, BLACK2]
    PLAYER = "Yellow"

    HUMANS = [True, True, True, True]
    DISTANCETRAVELLED = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # data analytics stuff
    amountofrolls = 0
    amountofturns = 1
    timer = time.time()
    inputtext = ""
    turn = 0
reset()

file = open("rolls.txt", "r") # open file and read values
ones = int(file.readline())
twos = int(file.readline())
threes = int(file.readline())
fours = int(file.readline())
fives = int(file.readline())
sixs = int(file.readline())
file.close()

# screen
pygame.init() # https://realpython.com/pygame-a-primer/ used for basic setup of script and basic knowledge of pygame
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("LUDO")

# images https://www.geeksforgeeks.org/python-display-images-with-pygame/
boardimage = pygame.image.load("img/ludo.png") 
one = pygame.image.load("img/1.png")
two = pygame.image.load("img/2.png")
three = pygame.image.load("img/3.png")
four = pygame.image.load("img/4.png")
five = pygame.image.load("img/5.png")
six = pygame.image.load("img/6.png")
rolls = [one,two,three,four,five,six]

pieces = [] # generate all pieces
for i in range(16):
    i = pygame.rect.Rect(TRACKX[i]-20,TRACKY[i]-20,40,40) # x y width height
    pieces.append(i)

# fonts
font = pygame.font.Font("freesansbold.ttf", 40)
font2 = pygame.font.Font("freesansbold.ttf", 100)
font3 = pygame.font.Font("freesansbold.ttf", 22)
font4 = pygame.font.Font("freesansbold.ttf", 32)

# other game objects
dice = pygame.rect.Rect(860,450,128,128)
roll = 1
dicerolled = False
rolling = 0
dragging = False
canskip = False
skip = pygame.rect.Rect(860,200,100,60)
skiptext = font3.render("Click to", True, WHITE)
skiptext2 = font3.render("skip", True, WHITE)
playertext2 = font.render("Player:", True, WHITE)
playertext = font.render(PLAYER, True, WHITE)
txt1 = font3.render("Click dice", True, WHITE)
txt2 = font3.render("to roll", True, WHITE)
# menu objects
backbutton = pygame.rect.Rect(400,700, 200,75)
backtext = font.render("BACK", True, BLACK)
wintext = font2.render("{} won!".format(PLAYER), True, BLACK)
wintext_rect = wintext.get_rect(center=(WIDTH/2, 200))

# functions
def nextplayer(): # next player
    global PLAYER, turn, playertext, dicerolled, rolling, amountofturns
    if PLAYER == "Yellow":
        PLAYER = "Green"
        turn = 1
    elif PLAYER == "Green":
        PLAYER = "Red"
        turn = 2
    elif PLAYER == "Red":
        PLAYER = "Black"
        turn = 3
    elif PLAYER == "Black":
        PLAYER = "Yellow"
        turn = 0
        amountofturns += 1
    playertext = font.render(PLAYER, True, WHITE)
    dicerolled = False
    rolling = 0

def calculatemove(): # function that checks and calculates moves, return True if legal, False if illegal
    global finalx, finaly, newposition
    if POSITIONS[pos] <= 15: # if piece is on start
        if roll == 6:
            if COLOURS[pos] == YELLOW and PLAYER == "Yellow": # move piece to correct spot on track
                finalx = TRACKX[16]
                finaly = TRACKY[16]
                newposition = 16
            elif COLOURS[pos] == GREEN and PLAYER == "Green": # duplicate of above
                finalx = TRACKX[26]
                finaly = TRACKY[26]
                newposition = 26
            elif COLOURS[pos] == RED and PLAYER == "Red": # duplicate of above
                finalx = TRACKX[36]
                finaly = TRACKY[36]
                newposition = 36
            elif COLOURS[pos] == BLACK2 and PLAYER == "Black": # duplicate of above
                finalx = TRACKX[46]
                finaly = TRACKY[46]
                newposition = 46
            else:
                selected.x = TRACKX[POSITIONS[pos]]-20 # if wrong colour chosen
                selected.y = TRACKY[POSITIONS[pos]]-20
                return False
        else: # duplicate of above
            selected.x = TRACKX[POSITIONS[pos]]-20 # if wrong colour chosen
            selected.y = TRACKY[POSITIONS[pos]]-20
            return False

    elif POSITIONS[pos] >= 16 and POSITIONS[pos] <= 55: # if piece is on track
        newposition = POSITIONS[pos]+roll
        if COLOURS[pos] == YELLOW and PLAYER == "Yellow": # calculate how far down the track it must go
            if newposition <=59:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == GREEN and PLAYER == "Green":
            if newposition > 55: # continue the lap / pass the yellow start square
                newposition -= 40
            elif newposition > 25 and POSITIONS[pos] < 26: # enter the base
                newposition += 34
            if newposition <= 63: # check is it actually your base and not opponents base
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == RED and PLAYER == "Red": # duplicate of above
            if newposition > 55:
                newposition -= 40
            elif newposition > 35 and POSITIONS[pos] < 36:
                newposition += 28
            if newposition <= 67:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == BLACK2 and PLAYER == "Black": # duplicate of above
            if newposition > 55:
                newposition -= 40
            elif newposition > 45 and POSITIONS[pos] < 46:
                newposition += 22
            if newposition <= 71:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        else: return False

    elif POSITIONS[pos] >= 56: # if piece in base
        newposition = POSITIONS[pos]+roll
        if COLOURS[pos] == YELLOW and PLAYER == "Yellow": # calculate how far it's still allowed to go
            if newposition <=59:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == GREEN and PLAYER == "Green": # duplicate of above
            if newposition <=63:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == RED and PLAYER == "Red": # duplicate of above
            if newposition <=67 and PLAYER == "Red":
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        elif COLOURS[pos] == BLACK2 and PLAYER == "Black": # duplicate of above
            if newposition <=71:
                finalx = TRACKX[newposition]
                finaly = TRACKY[newposition]
            else: return False
        else: return False
    else: return False
    return True

def check(): # checks can pieces be taken, winners
    global POSITIONS, playgame, DISTANCETRAVELLED, winmenu, wintext, wintext_rect, timetaken, winmenu2
    finishedpieces = 0
    for i in range(16): 
        if POSITIONS[i] == POSITIONS[pos] and not COLOURS[i] == COLOURS[pos]: # check can any opponents pieces be taken
            takenpiece = pieces[i]
            takenpiece.x = TRACKX[i]-20
            takenpiece.y = TRACKY[i]-20
            POSITIONS[i] = i
            DISTANCETRAVELLED[i] = 0
        if PLAYER == "Yellow" and POSITIONS[i] >=56 and POSITIONS[i] <=59: # check are all your pieces on the end and win game
            finishedpieces += 1
        elif PLAYER == "Green" and POSITIONS[i] >=60 and POSITIONS[i] <=63:
            finishedpieces += 1
        elif PLAYER == "Red" and POSITIONS[i] >=64 and POSITIONS[i] <=67:
            finishedpieces += 1
        elif PLAYER == "Black" and POSITIONS[i] >=68 and POSITIONS[i] <=71:
            finishedpieces += 1
    if finishedpieces == 4: # if player won game
        overwrite = open("rolls.txt", "w")
        overwrite.write("{}\n{}\n{}\n{}\n{}\n{}".format(ones,twos,threes,fours,fives,sixs)) # write rolls to file
        overwrite.close()
        timetaken = "{}s".format(round(time.time() - timer))
        playgame = False
        if HUMANS[turn]:
            wintext = font2.render("{} won!".format(PLAYER), True, BLACK)
            winmenu = True
        else:
            wintext = font.render("{} (Computer) won!".format(PLAYER), True, BLACK)
            adddata = ["Computer", amountofturns, amountofrolls, humanplayers, timetaken]
            with open('data.csv', 'a') as f: # write data to csv file
                w = csv.writer(f)
                w.writerow(adddata)
                f.close()
            winmenu2 = True
        wintext_rect = wintext.get_rect(center=(WIDTH/2, 200))

def addrolls(): # adds rolls for data collecting
    global ones, twos, threes, fours, fives, sixs, amountofrolls
    if roll == 1:
        ones +=1
    elif roll == 2:
        twos +=1
    elif roll == 3:
        threes +=1
    elif roll == 4:
        fours+=1
    elif roll ==5:
        fives+=1
    else: sixs+=1
    amountofrolls +=1

# main loop
clock = pygame.time.Clock()
run = True
mainmenu = True
playgame = False
rulesmenu = False
chooseplayersmenu = False
dataanalyticsmenu = False
winmenu = False
winmenu2 = False
while run:
    while playgame: # game loop
        for event in pygame.event.get(): # checks for any inputs
            if event.type == QUIT: # close the window
                run = False
                playgame = False
            elif event.type == MOUSEBUTTONDOWN and HUMANS[turn]: # drag the piece
                    if event.button == 1:
                        for i in range(16):
                            if pieces[i].collidepoint(event.pos) and dicerolled and legal: # select the piece to drag
                                dragging = True
                                selected = pieces[i] # the actual piece itself for dragging
                                pos = i # the piece from the list of 16 pieces for maths and calculations purposes

                                mouse_x, mouse_y = event.pos # https://stackoverflow.com/questions/41332861/click-and-drag-a-rectangle-with-pygame
                                offset_x = selected.x - mouse_x
                                offset_y = selected.y - mouse_y
                        if dice.collidepoint(event.pos) and not dicerolled: # roll the dice
                            roll = random.randint(1,6)
                            dicetext = font.render(str(roll), True, BLACK)
                            dicerolled = True
                            
                        elif skip.collidepoint(event.pos) and dicerolled and not legal: # skip button
                            nextplayer()

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:            
                    if dragging:
                        dragging = False
                        calculatemove()
                        if not canskip:
                            # snap the piece to the correct position or teleport piece back to previous position (anti cheat)
                            if selected.x < finalx+10 and selected.x > finalx-50 and selected.y < finaly+10 and selected.y > finaly-50:
                                selected.x = finalx-20
                                selected.y = finaly-20
                                POSITIONS[pos] = newposition
                                check()
                                if not roll == 6: # next player
                                    nextplayer()
                                dicerolled = False
                                rolling = 0
                            else:
                                selected.x = TRACKX[POSITIONS[pos]]-20
                                selected.y = TRACKY[POSITIONS[pos]]-20

            elif event.type == MOUSEMOTION: # drag the piece
                if dragging: # https://stackoverflow.com/questions/41332861/click-and-drag-a-rectangle-with-pygame
                    mouse_x, mouse_y = event.pos
                    selected.x = mouse_x + offset_x
                    selected.y = mouse_y + offset_y

        # computer AI
        if not HUMANS[turn]:
            dicerolled = True
            if rolling == 10:
                addrolls()
                PRIORITY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                for i in range(16): # calculate priority of each piece, higher is better
                    selected = pieces[i]
                    pos = i
                    legal = calculatemove()
                    if not legal: # if no legal moves
                        PRIORITY[i] = 0
                        continue
                    if newposition == 16 and COLOURS[i] == YELLOW: # check can piece be on starting square
                        PRIORITY[i] = 3
                    elif newposition == 26 and COLOURS[i] == GREEN:
                        PRIORITY[i] = 3
                    elif newposition == 36 and COLOURS[i] == RED:
                        PRIORITY[i] = 3
                    elif newposition == 46 and COLOURS[i] == BLACK2:
                        PRIORITY[i] = 3
                    elif newposition >= 56 and COLOURS[i] == YELLOW and POSITIONS[i] <= 55: # check can piece move to base
                        PRIORITY[i] = 5
                    elif newposition >= 60 and COLOURS[i] == GREEN and POSITIONS[i] <= 55:
                        PRIORITY[i] = 5
                    elif newposition >= 64 and COLOURS[i] == RED and POSITIONS[i] <= 55:
                        PRIORITY[i] = 5
                    elif newposition >= 68 and COLOURS[i] == BLACK2 and POSITIONS[i] <= 55:
                        PRIORITY[i] = 5
                    else:
                        PRIORITY[i] = 1
                    
                    for j in range(16):
                        if newposition == POSITIONS[j] and COLOURS[j] != COLOURS[i] and i != j: # check can piece be taken
                            PRIORITY[i] = 4
                        elif POSITIONS[i] == POSITIONS[j] and COLOURS[j] == COLOURS[i] and i != j: # check can a group of 2 or more pieces can be split apart
                            PRIORITY[i] = 2
                
                if PRIORITY != [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]: # if any legal moves
                    maximum = 0
                    for i in range(16):
                        if PRIORITY[i] > maximum: # if piece has higher priority than the current highest
                            maximum = PRIORITY[i]
                            selected = pieces[i]
                            pos = i
                        elif PRIORITY[i] == maximum and DISTANCETRAVELLED[i] > DISTANCETRAVELLED[pos] and DISTANCETRAVELLED[i] <= 40: # if pieces have same priority (both are on track) choose piece furthest on track
                            maximum = PRIORITY[i]
                            selected = pieces[i]
                            pos = i
                    calculatemove() # makes the move
                    selected.x = finalx-20
                    selected.y = finaly-20
                    POSITIONS[pos] = newposition
                    DISTANCETRAVELLED[pos] += roll
                    check()
                    if not roll == 6:
                        nextplayer()
                    dicerolled = False
                    rolling = 0
                else:
                    nextplayer()

        if rolling < 10 and dicerolled:
            roll = random.randint(1,6)
            rolling += 1
            if rolling == 10:
                if HUMANS[turn]:
                    addrolls()
                canskip = True
                for i in range(16): # check for legal moves
                    selected = pieces[i]
                    pos = i
                    legal = calculatemove()
                    if legal: 
                        canskip = False 
                        break

        # draw to screen
        screen.fill(BLACK)
        screen.blit(boardimage, (10,10))
        for i in range(16):
            pygame.draw.rect(screen, COLOURS[i], pieces[i], border_radius = 40)
        pygame.draw.rect(screen, BLACK, dice)
        if dicerolled and HUMANS[turn] and canskip and rolling == 10: # show skip button
            pygame.draw.rect(screen, RED, skip, border_radius=10)
            screen.blit(skiptext, (870,205))
            screen.blit(skiptext2, (885,230))
        screen.blit(playertext, (850,350))
        screen.blit(playertext2, (850,310))
        screen.blit(rolls[roll-1], (850, 450))
        screen.blit(txt1, (860,575))
        screen.blit(txt2, (860,600))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    while mainmenu: # main menu loop
        # menu objects
        ludotext = font2.render("LUDO", True, BLACK)
        playbutton = pygame.rect.Rect(750,300,200,75)
        playtext = font.render("PLAY", True, BLACK)
        rulesbutton = pygame.rect.Rect(750, 400, 200, 75)
        rulestext = font.render("RULES", True, BLACK)
        databutton = pygame.rect.Rect(750,500,200,75)
        datatext = font3.render("DATA ANALYTICS", True, BLACK)
        menupng = pygame.image.load("img/menu.png")
        for event in pygame.event.get(): # check for any inputs
            if event.type == QUIT: # close the window
                run = False
                mainmenu = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playbutton.collidepoint(event.pos): # play button pressed
                        mainmenu = False
                        chooseplayersmenu = True
                    elif rulesbutton.collidepoint(event.pos): # rules button presse
                        mainmenu = False
                        rulesmenu = True
                    elif databutton.collidepoint(event.pos): # data analytics button pressed
                        # read csv file and generate leaderboard into pygame
                        csvf = r"data.csv"
                        data = pd.read_csv(csvf)
                        newdata = data.sort_values("# Turns") # sorts csv file by least amount of turns https://www.geeksforgeeks.org/how-to-sort-data-by-column-in-a-csv-file-in-python/
                        newdata.to_csv("data.csv", index=False)
                        col1 = []
                        col2 = []
                        col3 = []
                        col4 = []
                        col5 = []
                        with open("data.csv", "r") as f:
                            reader = csv.reader(f)
                            for i in range(11):
                                row = next(reader)
                                i1 = font3.render(row[0],True,BLACK)
                                i2 = font3.render(row[1],True,BLACK)
                                i3 = font3.render(row[2],True,BLACK)
                                i4 = font3.render(row[3],True,BLACK)
                                i5 = font3.render(row[4],True,BLACK)
                                col1.append(i1)
                                col2.append(i2)
                                col3.append(i3)
                                col4.append(i4)
                                col5.append(i5)
                        mainmenu = False # switch menu
                        dataanalyticsmenu = True
        # draw to screen
        screen.fill(WHITE)
        screen.blit(menupng, (50,175))
        screen.blit(ludotext, (360, 25))
        pygame.draw.rect(screen, RED2, playbutton, border_radius=15)
        screen.blit(playtext, (795,320))
        pygame.draw.rect(screen, RED2, rulesbutton, border_radius = 15)
        screen.blit(rulestext, (785,420))
        pygame.draw.rect(screen, RED2, databutton, border_radius = 15)
        screen.blit(datatext, (755, 526))
        pygame.display.flip()
    
    while rulesmenu: # rules menu loop
        # menu objects
        rulestitle = font2.render("RULES", True, BLACK)
        rulespng = pygame.image.load("img/rules.png")
        for event in pygame.event.get(): # checks for any inputs
            if event.type == QUIT: # close the window
                run = False
                rulesmenu = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if backbutton.collidepoint(event.pos): # back button pressed
                        mainmenu = True
                        rulesmenu = False
        # draw to screen
        screen.fill(WHITE)
        screen.blit(rulespng, (15,150))
        screen.blit(rulestitle, (350,25))
        pygame.draw.rect(screen, RED2, backbutton, border_radius=15)
        screen.blit(backtext, (444,720))
        pygame.display.flip()
    
    while chooseplayersmenu: # choose players menu loop
        # menu objects
        choose0 = pygame.rect.Rect(750,200,200,75)
        choose1 = pygame.rect.Rect(750,300,200,75)
        choose2 = pygame.rect.Rect(750,400,200,75)
        choose3 = pygame.rect.Rect(750,500,200,75)
        choose4 = pygame.rect.Rect(750,600,200,75)
        choose0text = font3.render("COMPUTER ONLY", True, BLACK)
        choose1text = font4.render("1 PLAYER", True, BLACK)
        choose2text = font4.render("2 PLAYERS", True, BLACK)
        choose3text = font4.render("3 PLAYERS", True, BLACK)
        choose4text = font4.render("4 PLAYERS", True, BLACK)
        for event in pygame.event.get(): # checks for any inputs
            if event.type == QUIT: # close the window
                run = False
                chooseplayersmenu = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if backbutton.collidepoint(event.pos): # back button presses
                        mainmenu = True
                        chooseplayersmenu = False
                    elif choose0.collidepoint(event.pos): # computer only button pressed, start game
                        reset()
                        chooseplayersmenu = False
                        playgame = True
                        HUMANS = [False, False, False, False]
                        humanplayers = 0
                    elif choose1.collidepoint(event.pos): # 1 player button pressed, start game
                        reset()
                        chooseplayersmenu = False
                        playgame = True
                        HUMANS = [True, False, False, False]
                        humanplayers = 1
                    elif choose2.collidepoint(event.pos): # 2 player button pressed, start game
                        reset()
                        chooseplayersmenu = False
                        playgame = True
                        HUMANS = [True, True, False, False]
                        humanplayers = 2
                    elif choose3.collidepoint(event.pos): # 3 player button pressed, start game
                        reset()
                        chooseplayersmenu = False
                        playgame = True
                        HUMANS = [True, True, True, False]
                        humanplayers = 3
                    elif choose4.collidepoint(event.pos): # 4 player button pressed, start game
                        reset()
                        chooseplayersmenu = False
                        playgame = True
                        humanplayers = 4
        # draw to screen
        screen.fill(WHITE)
        screen.blit(menupng, (50,175))
        screen.blit(ludotext, (360,25))
        pygame.draw.rect(screen, RED2, backbutton, border_radius=15)
        screen.blit(backtext, (444,720))
        pygame.draw.rect(screen, RED2, choose0, border_radius=15)
        pygame.draw.rect(screen, RED2, choose1, border_radius=15)
        pygame.draw.rect(screen, RED2, choose2, border_radius=15)
        pygame.draw.rect(screen, RED2, choose3, border_radius=15)
        pygame.draw.rect(screen, RED2, choose4, border_radius=15)
        screen.blit(choose0text, (753, 226))
        screen.blit(choose1text, (770, 323))
        screen.blit(choose2text, (760, 423))
        screen.blit(choose3text, (760, 523))
        screen.blit(choose4text, (760, 623))
        pygame.display.flip()
    
    while dataanalyticsmenu: # data analytics menu
        # menu objects
        datatitle = font2.render("Data Analytics", True, BLACK)
        graphbutton = pygame.rect.Rect(380,285, 240,75)
        graphtext = font.render("View Graph", True, BLACK)
        mean = round(data["# Turns"].mean())
        median = round(data["# Turns"].median())
        average = round(data["# Dice rolls"].mean())
        modelist = str(data["Human Players"].mode()).split()
        mode = modelist[1]
        text1 = font3.render("The mean amount of turns per game is {}".format(mean), True, BLACK)
        text2 = font3.render("The median amount of turns per game is {}".format(median), True, BLACK)
        text3 = font3.render("The average amount of dice rolls is {} per game".format(average), True, BLACK)
        text4 = font3.render("The mode amount of human players is {}".format(mode), True, BLACK)
        text5 = font3.render("Press button below for a bar chart of all lifetime dice rolls", True, BLACK)
        text6 = font.render("TOP 10 LEADERBOARD", True, (0,128,0))
        for event in pygame.event.get(): # checks for any inputs
            if event.type == QUIT: # closes the window
                run = False
                dataanalyticsmenu = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if graphbutton.collidepoint(event.pos): # view graph button pressed
                        pygame.display.quit() # closes pygame window
                        chart = plt.bar(["One", "Two", "Three", "Four", "Five", "Six"], [ones,twos,threes,fours,fives,sixs], color="#ffbb66") # generates matplotlib graph 
                        plt.bar_label(chart, padding=-20) # https://stackoverflow.com/questions/28931224/how-to-add-value-labels-on-a-bar-chart
                        plt.show() # shows generated graph, waits until window closed to continue running code
                        screen = pygame.display.set_mode((WIDTH,HEIGHT)) # reopens pygame window
                        pygame.display.set_caption("LUDO")
                    elif backbutton.collidepoint(event.pos): # back button pressed
                        dataanalyticsmenu = False
                        mainmenu = True
        # draw to screen
        screen.fill(WHITE)
        screen.blit(datatitle, (150,25))
        screen.blit(text1, (150,150))
        screen.blit(text2, (150,175))
        screen.blit(text3, (150,200))
        screen.blit(text4, (150,225))
        screen.blit(text5, (150,250))
        screen.blit(text6, (250,380))
        for i in range(11): # draw leaderboard to screen
            screen.blit(col1[i], (150,425+(i*25)))
            screen.blit(col2[i], (350,425+(i*25)))
            screen.blit(col3[i], (450,425+(i*25)))
            screen.blit(col4[i], (600,425+(i*25)))
            screen.blit(col5[i], (800,425+(i*25)))
        pygame.draw.rect(screen, RED2, graphbutton, border_radius=15)
        screen.blit(graphtext, (390,305))
        pygame.draw.rect(screen, RED2, backbutton, border_radius=15)
        screen.blit(backtext, (444,720))
        pygame.display.flip()

    while winmenu: # human player winner menu
        # menu objects
        inputbox = pygame.rect.Rect(225,400,140,32)
        enterbutton = pygame.rect.Rect(400,700,200,75)
        entertext = font.render("ENTER", True, BLACK)
        info = font.render("Enter name of winner below", True, BLACK)
        for event in pygame.event.get(): # checks for any inputs
            if event.type == QUIT: # closes the window
                run = False
                winmenu = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if enterbutton.collidepoint(event.pos): # enters the text from the textbox
                        if inputtext == "": # if text box empty
                            inputtext = PLAYER
                        adddata = [inputtext, amountofturns, amountofrolls, humanplayers, timetaken]
                        with open('data.csv', 'a') as f: # adds data to csv file
                            w = csv.writer(f)
                            w.writerow(adddata)
                            f.close()
                        mainmenu = True # goes back to main menu
                        winmenu = False
            elif event.type == KEYDOWN: # adds characters to inputbox
                if event.key == K_BACKSPACE:
                    inputtext = inputtext[:-1]
                elif event.key == K_RETURN:
                    pass
                else:
                    inputtext += event.unicode
        # draw to screen
        screen.fill(WHITE)
        screen.blit(wintext, wintext_rect)
        screen.blit(info, (225,300))
        txt = font4.render(inputtext, True, BLACK)
        inputbox.w = max(200, txt.get_width()+10)
        screen.blit(txt, (inputbox.x+5, inputbox.y+5))
        pygame.draw.rect(screen, RED2, inputbox, 2)
        pygame.draw.rect(screen, RED2, enterbutton, border_radius=15)
        screen.blit(entertext, (430,720))
        pygame.display.flip()
    
    while winmenu2: # if computer won game
        for event in pygame.event.get(): # checks for any input
            if event.type == QUIT: # close the window
                run = False
                winmenu2 = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if backbutton.collidepoint(event.pos): # back button pressed
                        mainmenu = True
                        winmenu2 = False
        # draw to screen
        screen.fill(WHITE)
        screen.blit(wintext,wintext_rect)
        pygame.draw.rect(screen, RED2, backbutton, border_radius=15)
        screen.blit(backtext, (444,720))
        pygame.display.flip()

# add rolls data to file again
overwrite = open("rolls.txt", "w")
overwrite.write("{}\n{}\n{}\n{}\n{}\n{}".format(ones,twos,threes,fours,fives,sixs))
overwrite.close()
pygame.quit() # quit