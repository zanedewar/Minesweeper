import random
import os
import pygame
import datetime
BOARD_SIZE = 9
NUM_MINES = BOARD_SIZE + int(BOARD_SIZE * .25)
HIT_MINE = False
REAL_HIT_MINE = False
FLAG = "\u2691"
BOMB = u"\U0001F4A3"
flagFlag = False
RED_FLAG = "\u001b[31m["+FLAG+"]\033[0m"
RAND_GUESS = (random.randint(-999, 0),random.randint(-999,0))
BLACK = (0,0,0)
LGRAY = (50,50,50)
SCREEN_X = 600
SCREEN_Y = 600
SQUARE_SIZE = SCREEN_X/BOARD_SIZE
TIMES = []
MAKE_GUESS_TIMES = []
fill_unchecked, print_board_screen, print_green_flags, print_flag, print_nums, get_points, print_squares, print_lines, get_cell, get_coord, get_pos = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
game_loop, sWap, clear, guEss, fill_list, get_mines, get_cells, make_guess, get_front_board, get_count, get_value_color, show_mines, build_value_string = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
FUNC_LIST = ["fillUnchecked", "printBoardScreen", "printGreenFlags", "printFlag", "printNums", "getPoints", "printSquares", "printLines", "getCell", "getCoord", "getPos",
"gameLoop", "swap", "clear", "guess", "fillList", "getMines", "getCells", "makeGuess", "getFrontBoard", "getCount", "getValueColor", "showMines", "buildValueString"]



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
                    start_time = datetime.datetime.now()
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
                    time = datetime.datetime.now() - start_time
                    TIMES.append(time)
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
            consoleClear()
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
    timeSum = 0
    for time in TIMES:
        print(time)
        timeSum += time.total_seconds()
    print("Average: " + str((timeSum / len(TIMES))))
    timeSum = 0
    timeZeros = 0
    timeNonZeros = 0
    print("Make Guess Times:")
    for time in MAKE_GUESS_TIMES:
        if(time >= datetime.timedelta(milliseconds=1)):
            timeSum += time.total_seconds()
            timeNonZeros += 1
            print(time)
        else:
            timeZeros += 1
    if(timeNonZeros != 0):        
        print("Average: " + str((timeSum / timeNonZeros)))
    print("Total zeroes: " + str(timeZeros))
    print("final:")
    printFuncs()
    

    
    
"""
Main loop for game
"""
def fillUnchecked():
    global fill_unchecked
    fill_unchecked += 1
    unChecked = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            unChecked.append((i,j))
    return unChecked

def printBoardScreen(screen, frontBoard, unChecked,backBoard):
    global print_board_screen
    print_board_screen += 1
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
    global print_green_flags
    print_green_flags += 1
    for (x,y) in mines:
        printFlag(screen,(x,y), (0,255,0))
def printFlag(screen, curr, color):
    global print_flag
    print_flag += 1
    currPos = swap(getPos(curr))
    x = currPos[0]
    y = currPos[1]
    r1 = pygame.Rect(getPoints(x, 1, 4), getPoints(y, 1, 6), SQUARE_SIZE * .5, SQUARE_SIZE * .4)
    pygame.draw.rect(screen, color, r1)
    pygame.draw.line(screen, color, (getPoints(x, 3, 4), getPoints(y, 1, 6)), (getPoints(x, 3, 4), getPoints(y, 5, 6)), 3)

def printNums(screen, currCell, backBoard):
    global print_nums
    print_nums += 1
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
    global get_points
    get_points += 1
    return (cellPos + (SQUARE_SIZE * (num/den)))

def printSquares(screen, squarePos):
    global print_squares
    print_squares += 1
    pygame.draw.rect(screen, (255,255,255), [squarePos[1],squarePos[0], SQUARE_SIZE+1,SQUARE_SIZE+1])

def printLines(screen):
    global print_lines
    print_lines += 1
    x,y = screen.get_size()
    
    for i in range(BOARD_SIZE-1):
        pygame.draw.line(screen, BLACK, ((i+1)*SQUARE_SIZE, 0), ((i+1)*SQUARE_SIZE,y))
    for i in range(BOARD_SIZE-1):
        pygame.draw.line(screen,BLACK,(0,(i+1)*SQUARE_SIZE),(x,(i+1)*SQUARE_SIZE))

def getCellFromMouse(x,y):
    global get_cell
    get_cell += 1
    cellX = getCoord(x)
    cellY = getCoord(y)
    return swap((cellX,cellY))

def getCoord(x):
    global get_coord
    get_coord += 1
    out = -1
    while(x > 0):
        x-=SQUARE_SIZE
        out+=1
    return out

def getPos(coords):
    global get_pos
    get_pos += 1
    x = SQUARE_SIZE * coords[0]
    y = SQUARE_SIZE * coords[1]
    return (x,y)

def gameLoop(frontBoard, backBoard, gameRunning, mines, gameWon):
    global game_loop
    game_loop += 1
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
    global sWap
    #print("Swap: " + str(sWap))
    sWap += 1
    #print("Swap after increment: " + str(sWap))
    #print("WE ARE SWAPPING")
    return (x[1], x[0])

def consoleClear():
    #os.system('cls')
    print()

#get user guess or change modes
def guess():
    global guEss
    guEss += 1
    global flagFlag
    userGuess = input("Enter space-seperated x,y values: ")
    if(userGuess.lower() == "f"):
        flagFlag = not flagFlag
        return RAND_GUESS
    return tuple(int(item)-1 for item in userGuess.split())

def invalidGuess(guess):
    return (guess[0] < 0 or guess[0] > BOARD_SIZE - 1) or (guess[1] < 0 or guess[1] > BOARD_SIZE - 1)

def fillList(char):
    global fill_list
    fill_list += 1
    retBoard = []
    for i in range(BOARD_SIZE):
        fillList = []
        for j in range(BOARD_SIZE):
            fillList.append(char)
        retBoard.append(fillList)
    return retBoard

def getMines(num):
    global get_mines
    get_mines += 1
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
    global get_cells
    get_cells += 1
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
    global make_guess
    make_guess += 1
    global HIT_MINE
    start_time = datetime.datetime.now()
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
    time = datetime.datetime.now() - start_time
    MAKE_GUESS_TIMES.append(time)
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
    global show_mines
    show_mines += 1
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
    global build_value_string
    build_value_string += 1
    val = 9 if val == -1 else val
    return getValueColor(val)+"["+str(val)+"]\033[0m"

def printFuncs():
    func_var_list = [fill_unchecked, print_board_screen, print_green_flags, print_flag, print_nums, get_points, print_squares, print_lines, get_cell, get_coord, get_pos,
game_loop, sWap, clear, guEss, fill_list, get_mines, get_cells, make_guess, get_front_board, get_count, get_value_color, show_mines, build_value_string]
    for i in range(len(FUNC_LIST)):
        print(f"{FUNC_LIST[i]}: {func_var_list[i]}")

if __name__ == "__main__":
    main()