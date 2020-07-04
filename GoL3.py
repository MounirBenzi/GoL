import random
import pygame
import pickle


#   Initilising pygame
pygame.init()
clock = pygame.time.Clock()
windowWidth = 700
windowHeight = 700
screen = pygame.display.set_mode((windowWidth + 150, windowHeight))
pygame.display.set_caption("Game of Life")
screen.fill((20, 20, 25))


class cellElement:
    def __init__(self, x, y, state=None, previous=None, colour=(0, 0, 0)):
        self.x = x  # x pos
        self.y = y  # y pos
        self.colour = colour
        self.alive = 0
        self.dead = 0
        self.died = 0
        self.born = 0
        self.value = random.randint(0, 1)   # Giving the state a random number 0 or 1
        self.previous = self.value  # Setting the previous state equal to the current state.

    def __getitem__(self, x, y):
         return self.x[x], self.y[y]

    def save(self): # Saves the previous state of the cell
        self.previous = self.value

    def newValue(self, state):  # Used to give cells a new state value
        self.value = state

    # The display function is what gives the cells their colours depending on their current and preivous states.
    # This allows us to easily tell which cells have been born and which cells have died. This was very helpful
    # during testing as it allowed me to check for patterns common in Conway's Game of Life

    def colourDisplay(self):  #print(self.previous, self.value)
        if self.previous == 0 and self.value == 1:  # If  a new cell is born, the cell is given a colour of green. Birth
            self.colour = (0, 255, 0)
        elif self.value == 1:   # If the cell is alive and was alive in the previous state then it will be given the colour black
            self.colour = (0, 0, 0)
        elif self.previous == 1 and self.value == 0:    # If the cell was alive and now is dead, the cell is given a colour of red
            self.colour = (255, 0, 0)
        else:
            self.colour = (255, 255, 255)   #   If the cell was dead before and is still dead, it is given a colour of white
        return self.colour



class GoL:
    def __init__(self,  rows, cols,  grid=[], nextGrid=[], colour=(0, 0, 0), stroke=1):  # Initialising all the variables we require for the cells
        self.colour = colour
        self.rows = rows    # Assigning the number of rows in the grid
        self.cols = cols    # Assigning the number of colums in the grid
        self.height = (windowHeight // rows)-1  #   Here I am calculating the width and heigh of each cell to ensure that we can fit all the rows and columns in with the stroke
        self.width = (windowWidth // cols)-1
        self.stroke = stroke    # Stroke between the cells.
        #self.value = random.randint(0, 1)   # Assinging the initial value of the states
        self.grid = grid
        self.changedState = 0
        #elf.previous = self.value

        # Here I am creating a 2D array which is populated by class objects. I have chosen to do this because it
        # allows me to easily obtain various statistics on each cell as well as gives me the ability to easily colour
        # and edit cells depending on certain outcomes.

        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(cellElement(i, j))  # Making each cell in the grid a class object

        self.grid = grid

    #   This function is used to reinitialise the grid. This is useful when resetting the grid.
    def initialState(self): # Function to randomise the states of the class objects in the array
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].alive = 0   # Resetting the stats for each cell
                self.grid[i][j].dead = 0
                x = random.randint(0,1)
                self.grid[i][j].value = x   # Giving all the class objects a random new class state. i.e whether the cell is dead or alive
                if x == 1:
                    self.grid[i][j].alive += 1  # If the cell is alive, I will add a counter to each cell. This allows me to track the number of times the cell is alive.
                else:
                    self.grid[i][j].dead += 1   # If the cell is dead, I will add a counter to each cell. This allows me to track the number of times the cell has died.

    #   This function is used to draw the grid using pygame rectangles. I also record all of the previous states of the
    # cells using the save function in the cellElement class
    def DrawGrid(self):  # creating myf grid
        global pause, nextIter
        self.changedState = 0   # Reintialising the number of cells that have changed states. This is because I want to display the states changed per frame.

        for i in range(self.rows):  # Doing the same as above, however this is to create the grid in pygame.
            for j in range(self.cols):
                x = self.grid[i][j].colourDisplay()  # getting the colours based on previous states
                rect = pygame.Rect(i*(self.width + self.stroke), j*(self.height + self.stroke), self.height, self.width)    # Listing all of the rectangles that are to be created, giving their position and their size
                pygame.draw.rect(screen, x, rect)  # Drawing all of the rectangles with the appropriate colour, corresponding to the cell's state.
        pygame.display.update() # Updating the screen

        # Saving the old states of the cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].save() # For each cell set the previous state equal to the current state

        if pause is False:  # Checking whether or not the program is paused. If not run the neighbour functino
            self.neighbours()

        #   To iterate by a single frame I had to pause the program then calculate the next state (using the neighbour function)
        #   To ensure that this is only run once i created a for loop that ends after one iteration.
        if nextIter is True:
            for i in range(1):
                self.neighbours()
                nextIter = False

    # The game of life works based on 3 main rules which below. This function calculates the number of live neighbouring
    # cells around each and every cell. I ran into a small problem here with the cells on the edges. A nice solution
    # was to wrap around the grid using the modulus function. This way the cells from one edge can interact with the cells
    # on the opposite edge, resolving the issue problem.

    def neighbours(self):
        self.changedState = 0
        for i in range(self.rows):
            for j in range(self.cols):
                state = int(self.grid[i][j].value)  # Here I am looping though each cell and finding the state of its neighbours
                neighbourSum = 0    # initialising the sum as

                # Each cell is surrounded by 8 other cells, the GoL calculates the state of our current cell depending
                # on the states of the surrounding cells. So by adding up all the states of the cells
                # going from top left corner to bottom right corner, we can calculate how many neighbours our cell has.
                # From here we can then apply the rules for the game of life
                neighbourSum += int(self.grid[(i-1 + self.rows) % self.rows][(j+1 + self.cols) % self.cols].previous)  # Top left. I used the % to make the matrix wrap around. This is so the edges are able to interact with eachother.
                neighbourSum += int(self.grid[(i + self.rows) % self.rows][(j + 1 + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i + 1 + self.rows) % self.rows][(j + 1 + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i - 1 + self.rows) % self.rows][(j + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i + 1 + self.rows) % self.rows][(j + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i - 1 + self.rows) % self.rows][(j - 1 + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i + self.rows) % self.rows][(j - 1 + self.cols) % self.cols].previous)
                neighbourSum += int(self.grid[(i + 1 + self.rows) % self.rows][(j - 1 + self.cols) % self.cols].previous)

                # Implementing rules for Game of Life.
                # The game of life has 4 main rules:
                # 1. If a cell has 3 neighbours, the cell is alive. (i.e. A cell is given birth to)
                # 2. If a cell has more than 3 neighbours, the cell dies due to overpopulation
                # 3. If a cell has less than 2 neighbours, the cell dies due to underpopulation
                # 4. If a cell has 2 neighbours, it remains in the same state
                if state == 0 and neighbourSum == 3:  # Birth
                    self.grid[i][j].newValue(1) # Setting the new state
                    self.grid[i][j].alive += 1  # Capturing every time a cell is born
                    self.changedState += 1  # Capturing every time a cell changes state
                elif state == 1 and (neighbourSum < 2 or neighbourSum > 3):  # Death
                    self.grid[i][j].newValue(0)  # Setting the new state
                    self.grid[i][j].dead += 1  # Capturing every time a cell dies
                    self.changedState += 1  # Capturing every time a cell changes state

    # The function below is used to allow the user to edit turn cells on and off.
    # I collect the x and y position of the mouse and alter the position so that i can have them as coord
    # with respect to my grid. From here I am then easily able to change the state of the cells

    def editGrid(self, xPos, yPos):
        xPos = xPos // (self.width + self.stroke)   # Takes the x position of the mouse and divides by the width of the cell (with the stroke) This give use the xcoord on my grid
        yPos = yPos // (self.height + self.stroke)  # Takes the y position of the mouse and divides by the width of the cell (with the stroke) This give use the ycoord on my grid
        if self.grid[xPos][yPos].value == 0:    # main the grid to see if the cell is alive or not
            self.grid[xPos][yPos].newValue(1)   # If dead, set the cells state to alive
            self.grid[xPos][yPos].alive += 1
            self.changedState += 1
        elif self.grid[xPos][yPos].value == 1:
            self.grid[xPos][yPos].newValue(0)   # If alive, set the state to dead
            self.grid[xPos][yPos].dead += 1
            self.changedState += 1

    # This is the function that is responsible for displaying all of the statistics as well as hiding them.
    # I was unable to find away to delete the drawn objects so i resorted to painting over them. This allowed the program
    # to update the statistics in realtime to the user.
    def statistics(self):
        global stats
        x, y = pygame.mouse.get_pos()  # Collects the x and y coordinates of the mouse with respect to the screen
        font = pygame.font.SysFont('sans', 15)
        if stats is True:
            xPos = x // (self.width + self.stroke)  # Takes the x position of the mouse and divides by the width of the cell (with the stroke) This give use the xcoord on my grid
            yPos = y // (self.height + self.stroke)  # Takes the y position of the mouse and divides by the width of the cell (with the stroke) This give use the ycoord on my grid
            if x < windowWidth:    # Ensuring code only runs when mouse is over the grid, as grid doesnt exist where the menu
                pygame.draw.rect(screen, (20, 20, 25), (710, 150, 170, 20), 0)  # Creating a black square to hide the old value, then writing over it to display the new one
                aliveText = font.render('Times cell has lived: %s ' % (self.grid[xPos][yPos].alive), 1, (255, 255, 255))   # Displaying the text showing the statistics
                screen.blit(aliveText, [710, 150])  # Displaying the statistics to screen
                pygame.draw.rect(screen, (20, 20, 25), (710, 180, 170, 20), 0)  # Creating a black square to hide the old value, then writing over it to display the new one
                deadText = font.render('Times cell has died: %s ' % (self.grid[xPos][yPos].dead), 1, (255, 255, 255))   # Displaying the text showing the statistics
                screen.blit(deadText, [710, 180])   # Displaying the statistics to screen
            pygame.draw.rect(screen, (20, 20, 25), (710, 210, 170, 20), 0)
            changedText = font.render('Cells that changed : %s' % (self.changedState), 1, (255, 255, 255))
            screen.blit(changedText, [710, 210])
        else:
            pygame.draw.rect(screen, (20, 20, 25), (700, 150, 150, 80))    # Drawing a rectangle to cover the statistics

        # Controls text
        pygame.draw.rect(screen, (20, 20, 25), (760, 235, 50, 20), 0)
        changedText = font.render('Controls:', 1, (255, 255, 255))
        screen.blit(changedText, [760, 235])

        # Presets text
        pygame.draw.rect(screen, (20, 20, 25), (760, 385, 50, 20), 0)
        changedText = font.render('Presets:', 1, (255, 255, 255))
        screen.blit(changedText, [760, 385])

    #   Function below is used to clear the Grid. This can be used to draw a pattern of your own.
    def clearGrid(self):
        self.changedState = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].newValue(0)     # Setting each value in the grid to 0
                self.grid[i][j].alive = 0   # Setting all states back to 0
                self.grid[i][j].dead = 0

    #   This function saves a copy of all the current states of the grid using pickle.
    # The grid array is first copied over then saved.
    def saveGrid(self):    # This function is used save presets
        arrayCopy = []  # Creating an Array to save the current array to
        for i in range(self.rows):
            arrayCopy.append([])
            for j in range(self.cols):
                arrayCopy[i].append(self.grid[i][j].value)  # Copying cell states to my newly created array

        arraySave = open('SavedCopy.obj', 'wb')   # Saving the array. Had to use 'wb' instead of 'w' as we are dealing with arrays not strings
        pickle.dump(arrayCopy, arraySave)

    # The function below allow us to reimport the state of the grid that was saved using pickle
    def printPresets(self, x):
        presets = ['Hammerhead.obj', 'Glider.obj', 'Oscillator.obj', 'Crawler.obj', 'Pulsar.obj', 'SavedCopy.obj']    # preset pattern names
        filehandler = open(presets[x], 'rb')    # Using pickle to load the file we saved
        presetArray = pickle.load(filehandler)  # Setting the array to equal to the loaded preset
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].value = presetArray[i][j]  # Setting the grid cell states to be equal to those loaded in the array
                self.grid[i][j].alive = 0  # Setting all states back to 0
                self.grid[i][j].dead = 0

# This function is what is used to create the buttons that allow the user to control and alter the GoL.
class buttonCreation:
    def __init__(self, x, y, text, function, rect = None):
        self.x = x
        self.y = y
        self.width = 105
        self.height = 25
        self.text = text
        self.rect = rect
        self.function = function
        self.textcol = (0,0,0)
        self.buttoncol = (128,128,128)
        self.buttonhov = (211,211,211)

    # This function is what draws the buttons, just like we drew the grid using pygame rectangles.

    def drawButtons(self):
        self.rect = pygame.draw.rect(screen, self.buttoncol, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('sans', 15)  # Initialising the font
        text = font.render(self.text, 1, self.textcol)  # rendering the font
        screen.blit(text, [self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)])   #   Drawing the text on to the screen. I also positioned the text to be in the centre of the button
        if mouseInArea(self.x, self.y,self.width,self.height):  # main to see if the mouse is over the button
            if mousePressed is True:
                self.callFunction() # If the button is pressed then the buttons's function is called

    def callFunction(self):
        self.function() # Calling the button's function

#   The function below is where i initialised all of the buttons i needed for the gui.
# I then return the buttons as an array so that I can easily display them all.
def guiInit():  # Initialising the gui
    global stats
    #Main buttons
    pauseButton = buttonCreation(730, 20, 'Pause', pauseBut)
    resetButton = buttonCreation(730, 50, 'Reset', reset)
    displayStatistics = buttonCreation(730, 110, 'Statistics', statButton)
    clearButton = buttonCreation(730, 80, 'Clear', clearBut)
    # Control buttons
    iterationsPerFrame = buttonCreation(730, 260, 'Iteration/Frame: 1', iterateFrame) # Iterations per frame using the variable
    nextIteration = buttonCreation(730, 290, 'Next Iteration', nextIterationButton)
    savePat = buttonCreation(730, 320, 'Save Pattern', saveArray)
    loadLastPat = buttonCreation(730, 350, 'Load Pattern', loadArray)
    # Preset buttons
    oscillator = buttonCreation(730, 410, 'Oscillator', pattPre)
    hammer = buttonCreation(730, 440, 'Hammer', hammerPre)
    glider = buttonCreation(730, 470, 'Glider', gliderPre)
    space = buttonCreation(730, 500, 'Crawler', spacePre)
    symmetry = buttonCreation(730, 530, 'Pulsar', symPre)

    quit = buttonCreation(730, 650, 'Quit', quitBut)
    return[pauseButton, resetButton, displayStatistics, clearButton, iterationsPerFrame, nextIteration, savePat, loadLastPat, oscillator, hammer, glider, space, symmetry, quit]


def reset():    # When reset is pressed, the grid is set back to its initial state
    global main
    main.initialState()

#   This function allows the user to chose how many iterations per frame the GoL will out put.
def iterateFrame():
    global valofIterationFrame, iteration, pause
    pause = False   #   This ensures that the program is running
    valofIterationFrame += 1    # everytime the user clicks the button, the number of iterations changes
    iterationsArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]   # This is the list of iterations the user can use. At interations of >20, the code slows down a fair bit due to the computational demands
    iteration = iterationsArray[valofIterationFrame % len(iterationsArray)]   # By using the modulus function we are allowing the user to cycle through the list options.
    gui[4].text = 'Iteration/Frame: ' + str(iteration)

#When the Next Iteration button is pressed, GoL is paused and i then use a for loop to run through the neighbour algorithm once

def nextIterationButton():
    global main, pause, nextIter
    pause = True
    gui[0].text = "Start"
    nextIter = True
    main.DrawGrid()
    #pygame.display.update()

# The functions below are what happens when the user selects the preset. I have already created and saved the presets using the same method
# The user will use to save and load their own.
# The functions below simply just tell pygame which preset to load from the preset pattern names
def loadPre(presetLoad):
    global main
    pause = False
    main.printPresets(presetLoad)


def hammerPre():
    global main
    main.printPresets(0)


def gliderPre():
    global main
    main.printPresets(1)


def pattPre():
    global main
    main.printPresets(2)


def spacePre():
    global main
    main.printPresets(3)


def symPre():
    global main
    main.printPresets(4)


# When the pause button is pressed the button's text is set to pause and the pause variable is changed.
# This prevents the neighbour algorthim from running which causes the prgram to halt

def pauseBut():
    global pause
    if pause is False:
        pause = True    # This stops the self.neighbour function from being run in the GoL class
        gui[0].text = "Start"
    else:
        pause = False
        gui[0].text = "Pause"

# When the stat button is pressed. It simply changes a variable which then causes the statistics to either
# be shown or hidden

def statButton():
    global stats, main
    if stats is False:
        stats = True
    else:
        stats = False

#Clears the grid
def clearBut():
    global main
    main.clearGrid()
    pause = True
    pauseBut()

#Causes program to close
def quitBut():
    exit()

# Checking if the mouse is on top of my buttons
def mouseInArea(x,y, width, height):
    mousePos = pygame.mouse.get_pos()
    if (x <= mousePos[0] <= x + width) and (y <= mousePos[1] <= y + height):
        return True

#   Function that calls the program to save an array
def saveArray():
    global main
    main.saveGrid()

# Function that calls the program to load an array
def loadArray():
    global main
    main.printPresets(5)

# This function is what displays the gui elements and is the reason why i returned an array
def guiDisplay(gui):
    for i in gui:
        i.drawButtons()
    pygame.display.update()

# The code below is what executes out program

main = GoL(70, 70)
gui = guiInit()     # initialising the gui
done = False
mousePressed = False
restart = False
pause = False
stats = False
nextIter = False
valofIterationFrame = 0
iteration = 1



while not done:
    mousePressed = False
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # main to see if the mouse button is pressed
            x, y = pygame.mouse.get_pos()  # Collects the x and y coordinates of the mouse with respect to the screen
            if x >= windowWidth:    # Ensuring that the button is only looking at events where the mouse is in the gui area
                mousePressed = True
            else:
                main.editGrid(x, y)   # Calls function to allow user to change the state of cells

    for i in range(iteration):  # This is where the program is iterated depending on how many iterations per frame the user wanted.
        main.DrawGrid()

    main.statistics()
    guiDisplay(gui)
    clock.tick(8)   # Sets the GoL fps. It is low to allow the user to see the difference when increasing the iteraions per frame
                    # would be too fast otherwise

