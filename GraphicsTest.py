import random
import os
import pygame
import datetime
BOARD_SIZE = 20
NUM_MINES = BOARD_SIZE * 2
HIT_MINE = False
REAL_HIT_MINE = False
FLAG = "\u2691"
BOMB = u"\U0001F4A3"
flagFlag = False
RED_FLAG = "\u001b[31m["+FLAG+"]\033[0m"
RAND_GUESS = (random.randint(-999, 0),random.randint(-999,0))
BLACK = (0,0,0)
LGRAY = (50,50,50)
SCREEN_X = 800
SCREEN_Y = 800
SQUARE_SIZE = SCREEN_X/BOARD_SIZE


def main():
    global HIT_MINE
    global REAL_HIT_MINE
    backBoard = fillList(0)
    frontBoard = fillList("[-]")
    unChecked = fillUnchecked()
    
    gameRunning = True
    gameWon = False
    
    mines = []
    #Generate and place mines
    mines = getMines(NUM_MINES)
    for (x,y) in mines:
        backBoard[x][y] = -1

    #print(backBoard)
    printBoardGame(frontBoard)
    backBoard = getFrontBoard(backBoard)
    printBoardTest(backBoard)
    
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
    running = True
    screen.fill(LGRAY)
    printLines(screen)
    while running:
        while gameRunning:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not REAL_HIT_MINE:
                    #Get mouse pos
                    mouseX,mouseY = pygame.mouse.get_pos()
                    #Get coordinates from mouse pos
                    coords = getCellFromMouse(mouseX,mouseY)
                    #left click
                    if(event.button == 1):    
                        #Make guess and update board
                        frontBoard = makeGuess(backBoard, frontBoard, coords)
                        #printBoardGame(frontBoard)
                        print()
                    elif(event.button == 3):
                        print("Right click")
                        frontBoard[coords[0]][coords[1]] = RED_FLAG
                    #Update screen
                    printBoardScreen(screen,frontBoard,unChecked,backBoard)
                    pygame.display.flip()
                    #printFuncs()
                elif event.type == pygame.KEYDOWN:
                    print("Key")
                    #right click
            
            if(HIT_MINE):
                break
            for row in frontBoard:
                gameRunning = False
                if("[-]" in row):
                    gameRunning = True
                    break
            for (x,y) in mines:
                if(frontBoard[x][y] != RED_FLAG and frontBoard[x][y] != "\u001b[32m["+FLAG+"]\033[0m"):
                    gameRunning = True
                    break
            if(not gameRunning):
                gameWon = True
                break
            if(REAL_HIT_MINE):
                showMines(frontBoard,backBoard,screen,mines)
            #gameRunning = gameLoop(frontBoard,backBoard,gameRunning,mines,gameWon)
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        
        if(HIT_MINE):
            showMines(frontBoard,backBoard,screen,mines)
            printBoardScreen(screen,frontBoard,unChecked,backBoard)
            printBoardGame(frontBoard)
            print("Better luck next time!")
            HIT_MINE = False
            REAL_HIT_MINE = True
            #gameRunning = False
        elif(not gameRunning and gameWon):
            printGreenFlags(screen,mines)
            print("Good job!")
            REAL_HIT_MINE = True
            gameWon = False
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
"""
Main loop for game
"""
def fillUnchecked():
    unChecked = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            unChecked.append((i,j))
    return unChecked

def printBoardScreen(screen, frontBoard, unChecked,backBoard):
    i = 0
    while i < len(unChecked):
        curr = unChecked[i]
        if(frontBoard[curr[0]][curr[1]] != "[-]"):
            printSquares(screen, getPos((curr[0],curr[1])))
            printLines(screen)
            if(frontBoard[curr[0]][curr[1]] == RED_FLAG):
                printFlag(screen, curr, (255,0,0))
            else:
                printNums(screen,curr,backBoard)
                unChecked.remove(unChecked[i])
                i-=1
        i+=1

def printGreenFlags(screen, mines):
    for (x,y) in mines:
        printFlag(screen,(x,y), (0,255,0))
def printFlag(screen, curr, color):
    currPos = swap(getPos(curr))
    x = currPos[0]
    y = currPos[1]
    r1 = pygame.Rect(getPoints(x, 1, 4), getPoints(y, 1, 6), SQUARE_SIZE * .5, SQUARE_SIZE * .4)
    pygame.draw.rect(screen, color, r1)
    pygame.draw.line(screen, color, (getPoints(x, 3, 4), getPoints(y, 1, 6)), (getPoints(x, 3, 4), getPoints(y, 5, 6)), 3)

def printNums(screen, currCell, backBoard):
    val = backBoard[currCell[0]][currCell[1]]
    cellPos = getPos(currCell)
    cellPos = swap(cellPos)
    points = []
    x = cellPos[0]
    y = cellPos[1]
    
    
    oneSixthY = getPoints(y, 1, 6)
    fiveSixthY = getPoints(y, 5, 6)
    oneHalfX = getPoints(x, 1, 2)
    oneHalfY = getPoints(y, 1, 2)
    oneFourthX = getPoints(x, 1, 4)
    threeFourthsX = getPoints(x, 3, 4)
    
    #Segment points
    p1 = (oneFourthX, oneSixthY)
    p2 = (threeFourthsX,oneSixthY)
    p3 = (p2[0], oneHalfY)
    p4 = (p1[0], p3[1])
    p5 = (p4[0], fiveSixthY)
    p6 = (p2[0],p5[1])

    pointsList = [[], [], [p1,p2,p2,p3,p3,p4,p4,p5,p5,p6], [p1,p2,p2,p3,p3,p4,p3,p6,p5,p6], [p1,p4,p4,p3,p2,p6], [p1,p2,p1,p4,p4,p3,p3,p6,p6,p5], 
    [p1,p2,p1,p4,p4,p3,p3,p6,p6,p5,p5,p4], [p1,p2,p2,p6], [p1,p5,p5,p6,p6,p2,p2,p1,p1,p4,p3,p4], [p2,p1,p1,p4,p4,p3,p3,p2,p2,p6,p6,p5]]
    colorList = [(), (0,0,255), (0,247,239), (0,100,100), (255, 0, 255), (255, 128, 0), (0, 0, 0), (255,0,127), (255,102,178), (255,0,0)]

    if(val == 1):
        p1 = (oneFourthX, getPoints(y, 1, 3))
        p2 = (oneHalfX, oneSixthY)
        p3 = (p2[0],fiveSixthY)
        p4 = (oneFourthX,p3[1])
        p5 = (threeFourthsX,p3[1])
        points = [p1,p2,p2,p3,p4,p5]
    else:
        val = 9 if val == -1 else val
        points = pointsList[val]
    color = colorList[val]
    
    for i in range(len(points) - 1):
            pygame.draw.line(screen, color, points[i], points[i+1], 5)
            i+=1


def getPoints(cellPos, num, den):
    return (cellPos + (SQUARE_SIZE * (num/den)))

def printSquares(screen, squarePos):
    pygame.draw.rect(screen, (255,255,255), [squarePos[1],squarePos[0], SQUARE_SIZE+1,SQUARE_SIZE+1])

def printLines(screen):
    x,y = screen.get_size()
    
    for i in range(BOARD_SIZE-1):
        pygame.draw.line(screen, BLACK, ((i+1)*SQUARE_SIZE, 0), ((i+1)*SQUARE_SIZE,y))
    for i in range(BOARD_SIZE-1):
        pygame.draw.line(screen,BLACK,(0,(i+1)*SQUARE_SIZE),(x,(i+1)*SQUARE_SIZE))

def getCellFromMouse(x,y):
    cellX = getCoord(x)
    cellY = getCoord(y)
    return swap((cellX,cellY))

def getCoord(x):
    out = -1
    while(x > 0):
        x-=SQUARE_SIZE
        out+=1
    return out

def getPos(coords):
    x = SQUARE_SIZE * coords[0]
    y = SQUARE_SIZE * coords[1]
    return (x,y)


#swap values in tuple to correspond with arrays
def swap(x):
    return (x[1], x[0])

def invalidGuess(guess):
    return (guess[0] < 0 or guess[0] > BOARD_SIZE - 1) or (guess[1] < 0 or guess[1] > BOARD_SIZE - 1)

def fillList(char):
    retBoard = []
    for i in range(BOARD_SIZE):
        fillList = []
        for j in range(BOARD_SIZE):
            fillList.append(char)
        retBoard.append(fillList)
    return retBoard

def getMines(num):
    mines = []
    for i in range(num):
        x = random.randint(0,BOARD_SIZE-1)
        y = random.randint(0,BOARD_SIZE-1)
        mines.append([x,y])
    return mines

def printBoardGame(board):
    for i in range(BOARD_SIZE):
        out = ""
        for j in range(BOARD_SIZE):
            out += str(board[i][j]) + " "
        print(out)
        

def printBoardTest(board):
    for row in board:
        print(row)

#Check if cells exist to left, right, up, or down
def getCells(i,j):
    ret = [j-1 > -1, j+1 < BOARD_SIZE, i-1 > -1, i+1 < BOARD_SIZE]
    #left[0], right[1], up[2], down[3]
    return ret

"""
Print value of guess on board
If mine is hit, end game
If value is any number other than 0 print it as normal
If value is 0, reveal all cells around it by calling makeGuess recursively
"""
def makeGuess(backBoard, frontBoard, guess):
    global HIT_MINE
    x = guess[0]
    y0 = guess[1]
    val = backBoard[x][y0]

    if(val == -1):
        HIT_MINE = True
    elif(val == 0 and frontBoard[x][y0] != ""):
        cells = getCells(x,y0)
        frontBoard[x][y0] = ""

        if(cells[0] and frontBoard[x][y0-1] != ""):
            y = y0-1
            frontBoard = makeGuess(backBoard, frontBoard, (x,y)) 

            if(cells[2] and frontBoard[x-1][y] != ""):
                frontBoard = makeGuess(backBoard, frontBoard, (x-1,y))

            if(cells[3] and frontBoard[x+1][y] != ""):
                frontBoard = makeGuess(backBoard, frontBoard, (x+1,y))

        if(cells[1] and frontBoard[x][y0+1] != ""):
            y = y0+1
            frontBoard = makeGuess(backBoard, frontBoard, (x,y))

            if(cells[2] and frontBoard[x-1][y] != ""):
                frontBoard = makeGuess(backBoard, frontBoard, (x-1,y))

            if(cells[3] and frontBoard[x+1][y] != ""):
                frontBoard = makeGuess(backBoard, frontBoard, (x+1,y))

        if(cells[2] and frontBoard[x-1][y0] != ""):
            frontBoard = makeGuess(backBoard, frontBoard, (x-1, y0))
            return frontBoard

        if(cells[3] and frontBoard[x+1][y0] != ""):
            frontBoard = makeGuess(backBoard, frontBoard, (x+1, y0))
            return frontBoard

    frontBoard[x][y0] = buildValueString(val)
    return frontBoard


def getFrontBoard(board):
    retBoard = fillList(0)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cells = getCells(i,j)
            currCount = getCount(board, cells, i, j)
            retBoard[i][j] = currCount if board[i][j] != -1 else -1    
    return retBoard

def getCount(board, cells, i, j):
    currCount = 0
    if(cells[0]):
        y = j-1
        currCount = currCount+1 if board[i][y] == -1 else currCount
        if(cells[2]):
            currCount = currCount+1 if board[i-1][y] == -1 else currCount
        if(cells[3]):
            currCount = currCount+1 if board[i+1][y] == -1 else currCount
    if(cells[2]):
        currCount = currCount+1 if board[i-1][j] == -1 else currCount
    if(cells[3]):
        currCount = currCount+1 if board[i+1][j] == -1 else currCount
    if(cells[1]):
        y = j+1
        currCount = currCount+1 if board[i][y] == -1 else currCount
        if(cells[2]):
            currCount = currCount+1 if board[i-1][y] == -1 else currCount
        if(cells[3]):
            currCount = currCount+1 if board[i+1][y] == -1 else currCount
    return currCount

#Gets appropriate color code for given value
def getValueColor(val):
    out = "\u001b["
    colors = ["37", "34", "32", "36", "35", "36", "30", "33", "36", "31"]
    out += colors[val] + "m"
    return out

def showMines(frontBoard, backBoard, screen, mines):
    greenFlag = "\u001b[32m["+FLAG+"]\033[0m"
    for (i,j) in mines:
        printSquares(screen, getPos((i,j)))
        if(frontBoard[i][j] != RED_FLAG and frontBoard[i][j] != greenFlag):
            printNums(screen, (i,j), backBoard)
            frontBoard[i][j] = buildValueString(-1)
        else:
            printFlag(screen, (i,j), (0,255,0))
            frontBoard[i][j] = greenFlag
    printLines(screen)
    return frontBoard

def buildValueString(val):
    val = 9 if val == -1 else val
    return getValueColor(val)+"["+str(val)+"]\033[0m"

if __name__ == "__main__":
    main()