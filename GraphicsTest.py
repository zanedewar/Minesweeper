import random
import os
import pygame
BOARD_SIZE = 8
NUM_MINES = BOARD_SIZE + int(BOARD_SIZE * .25)
HIT_MINE = False
FLAG = "\u2691"
BOMB = u"\U0001F4A3"
flagFlag = False
RED_FLAG = "\u001b[31m["+FLAG+"]\033[0m"
RAND_GUESS = (random.randint(-999, 0),random.randint(-999,0))
BLACK = (0,0,0)
LGRAY = (50,50,50)
SCREEN_X = 500
SCREEN_Y = 500
SQUARE_SIZE = SCREEN_X/BOARD_SIZE

def main():
    backBoard = fillList(0)
    frontBoard = fillList("[-]")
    unChecked = fillUnchecked()
    printBoardTest(unChecked)
    
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

        
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if(event.button == 1):
                    mouseX,mouseY = pygame.mouse.get_pos()
                    print(f"{mouseX},{mouseY}")
                    print(getCellFromMouse(mouseX,mouseY))
                    coords = getCellFromMouse(mouseX,mouseY)
                    frontBoard = makeGuess(backBoard, frontBoard, coords)
                    printBoardGame(frontBoard)
                    printBoardScreen(screen,frontBoard,unChecked)
                elif(event.button == 2):
                    print("Right click")
                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                print("Key")
                #right click
        # Fill the background with white
        
        #pygame.draw.line(screen, (0,0,0),())

        #gameRunning = gameLoop(frontBoard,backBoard,gameRunning,mines,gameWon)

        # Draw a solid blue circle in the center

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
    

    if(HIT_MINE):
        consoleClear()
        showMines(frontBoard,backBoard)
        printBoardGame(frontBoard)
        print("Better luck next time!")
    elif(not gameRunning and gameWon):
        print("Good job!")
    else:
        print("Goodbye")
    
"""
Main loop for game
"""
def fillUnchecked():
    unChecked = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            unChecked.append((i,j))
    return unChecked

def printBoardScreen(screen, frontBoard, unChecked):
    for x in unChecked:
        if(frontBoard[x[0]][x[1]] != "[-]"):
            printSquares(screen, getPos((x[0],x[1])))
            unChecked.remove(x)
    printBoardTest(unChecked)
def printSquares(screen, squarePos):
    pygame.draw.rect(screen, (255,255,255), [squarePos[1],squarePos[0], SQUARE_SIZE,SQUARE_SIZE])
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

def gameLoop(frontBoard, backBoard, gameRunning, mines, gameWon):
    while(gameRunning):
        if(HIT_MINE):
            break
        for row in frontBoard:
            gameRunning = False
            if("[-]" in row):
                gameRunning = True
                break
        for (x,y) in mines:
            if(frontBoard[x][y] != RED_FLAG):
                gameRunning = True
                break
        if(not gameRunning):
            gameWon = True
            break
            
        currGuess = guess()
        while(flagFlag):
            print("FLAG MODE (PUT IN CELL OR 'f' TO RETURN)")
            currGuess = guess()
            if(currGuess != RAND_GUESS):
                while(invalidGuess(currGuess)):
                    print("Invalid guess")
                    currGuess = guess()
                currGuess = swap(currGuess)
                frontBoard[currGuess[0]][currGuess[1]] = RED_FLAG
            printBoardGame(frontBoard)
        if(currGuess != RAND_GUESS):
            while(invalidGuess(currGuess)):
                print("Invalid guess")
                currGuess = guess()
            currGuess = swap(currGuess)
            frontBoard = makeGuess(backBoard, frontBoard, currGuess)
            printBoardGame(frontBoard)
    return gameRunning

#swap values in tuple to correspond with arrays
def swap(x):
    return (x[1], x[0])

def consoleClear():
    os.system('cls')

#get user guess or change modes
def guess():
    global flagFlag
    userGuess = input("Enter space-seperated x,y values: ")
    if(userGuess.lower() == "f"):
        flagFlag = not flagFlag
        return RAND_GUESS
    return tuple(int(item)-1 for item in userGuess.split())

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
    #consoleClear()
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
    ret = []
    #left[0], right[1], up[2], down[3]
    ret.append(j-1 > -1)
    ret.append(j+1 < BOARD_SIZE)
    ret.append(i-1 > -1)
    ret.append(i+1 < BOARD_SIZE)
    return ret

"""
Print value of guess on board
If mine is hit, end game
If value is any number other than 0 print it as normal
If value is 0, reveal all cells around it by calling makeGuess recursively
"""
def makeGuess(backBoard, frontBoard, guess):
    global HIT_MINE
    val = backBoard[guess[0]][guess[1]]
    if(val == -1):
        HIT_MINE = True
    elif(val == 0):
        cells = getCells(guess[0],guess[1])
        frontBoard[guess[0]][guess[1]] = ""
        if(cells[0]):
            y = guess[1]-1
            frontBoard = makeGuess(backBoard, frontBoard, (guess[0],y)) if frontBoard[guess[0]][y] != "" else frontBoard
            if(cells[2]):
                frontBoard = makeGuess(backBoard, frontBoard, (guess[0]-1,y)) if frontBoard[guess[0]-1][y] != "" else frontBoard
            if(cells[3]):
                frontBoard = makeGuess(backBoard, frontBoard, (guess[0]+1,y)) if frontBoard[guess[0]+1][y] != "" else frontBoard
        if(cells[1]):
            y = guess[1]+1
            frontBoard = makeGuess(backBoard, frontBoard, (guess[0],y)) if frontBoard[guess[0]][y] != "" else frontBoard
            if(cells[2]):
                frontBoard = makeGuess(backBoard, frontBoard, (guess[0]-1,y)) if frontBoard[guess[0]-1][y] != "" else frontBoard
            if(cells[3]):
                frontBoard = makeGuess(backBoard, frontBoard, (guess[0]+1,y)) if frontBoard[guess[0]+1][y] != "" else frontBoard
        if(cells[2]):
            frontBoard = makeGuess(backBoard, frontBoard, (guess[0]-1, guess[1])) if frontBoard[guess[0]-1][guess[1]] != "" else frontBoard
        if(cells[3]):
            frontBoard = makeGuess(backBoard, frontBoard, (guess[0]+1, guess[1])) if frontBoard[guess[0]+1][guess[1]] != "" else frontBoard
    frontBoard[guess[0]][guess[1]] = buildValueString(val)
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
    if val == 0:
        #white
        out += "37m"
    elif val == 1:
        #blue
        out += "34m"
    elif val == 2:
        #green
        out += "32m"
    elif val == 4:
        #purple
        out += "35m"
    elif val == 6:
        #black
        out += "30m"
    elif val == 7:
        #yellow
        out += "33m"
    elif val == 9:
        out += "31m"
    else:
        out += "36m"
    return out

def showMines(frontBoard, backBoard):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if(backBoard[i][j] == -1):
                if(frontBoard[i][j] != RED_FLAG):
                    frontBoard[i][j] = buildValueString(-1)
                else:
                    frontBoard[i][j] = "\u001b[32m["+FLAG+"]\033[0m"
    return frontBoard

def buildValueString(val):
    val = 9 if val == -1 else val
    return getValueColor(val)+"["+str(val)+"]\033[0m"

if __name__ == "__main__":
    main()