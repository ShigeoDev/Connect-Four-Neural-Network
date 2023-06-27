import turtle
import time
import math

# Basic screen measurements
screenwidth = 7
screenheight = 6
bordersize = 20

# Creating turtle display
screen = turtle.Screen()
screen.setup((screenwidth) * 100 + 2 * bordersize, (screenheight) * 100 + 2 * bordersize)
screen.setworldcoordinates(0, 0, (screenwidth) * 100 + 2 * bordersize, (screenheight) * 100 + 5 * bordersize)
screen.bgcolor("blue")

# Makes it not update constantly, much faster
turtle.tracer(0)

# Rows and columns on a board
height = 6
width = 7

# Multi game variables
amountOfGames = 1

# Arrays to store data on color and objects
games = []
spaces = []
arrow = []
playablecol = []
playablegame = []
wins = []
redpotentials = []
yellowpotentials = []
redconnections = []
yellowconnections = []

# Neural network components
nodes = 8
layers = 2

output = []
weights = []
neurons = []

# 1 is Red, -1 is Yellow
turn = 1

# If the game is played by person
clickable = 1

def main():

    # Creating multiple games
    for i in range(0, amountOfGames):
        board = []
        for x in range(0, width):
            boardcol = []
            for y in range(0, height):
                boardcol.append(0)
            board.append(boardcol)
        games.append(board)

    # Creating board and spaces with turtles
    for x in range(0, width):

        spacecol = []

        for y in range(0, height):

            circle = turtle.Turtle()
            circle.penup()
            circle.shape("circle")
            circle.speed(0)
            circle.color("black", "white")
            circle.shapesize(4, 4, 4)
            circle.setpos(x * 100 + 50 + bordersize - 5, y * 100 + 50 + bordersize - 5)
            spacecol.append(circle)

        spaces.append(spacecol)

    # Creating clickable triangles
    for x in range(0, width):

        triangle = turtle.Turtle()
        triangle.penup()
        triangle.shape("triangle")
        triangle.speed(0)
        triangle.color("black", "red")
        triangle.shapesize(4, 2, 2)
        triangle.setheading(270)
        triangle.setpos(x * 100 + 50 + bordersize - 5, 650)
        arrow.append(triangle)

    # Making all the columns and games playable & setting all wins to 0
    for i in range(0, amountOfGames):
        temp = []
        playablegame.append(1)
        wins.append(0)
        for x in range(0, width):
            temp.append(1)
        playablecol.append(temp)

    for i in range(0, amountOfGames):
        redtemp = []
        yellowtemp = []
        for i in range(0, width):
            redtempcolumns = []
            yellowtempcolumns = []
            for j in range(0, height):
                redtempcolumns.append(0)
                yellowtempcolumns.append(0)
            redtemp.append(redtempcolumns)
            yellowtemp.append(yellowtempcolumns)
        redpotentials.append(redtemp)
        yellowpotentials.append(yellowtemp)

    for i in range(0, amountOfGames):
        redtemp = []
        yellowtemp = []
        redconnections.append(redtemp)
        yellowconnections.append(yellowtemp)
    
    

    # Constantly checking for clicks
    if clickable:
        while True:
            for i in range(0, len(arrow)):
                arrow[i].onclick(click)
            updateBoard(games[0], spaces)
            turtle.update()
    
    turtle.update()

    time.sleep(3)

# Function to place piece in certain column
def place(color, col, boardnum):
    y = 0
    board = games[boardnum]
    if playablegame[boardnum]:
        while board[col][y] != 0 and playablecol[boardnum][col]:
            if y == 5:
                break
            elif y == 4:
                playablecol[boardnum][col] = 0
            y += 1
        board[col][y] = color

    connections(col, y, boardnum)
    findPotentials(col, y, boardnum)

# Updating the turtles colors
def updateBoard(board, spaces):
    for x in range(0, width):
        for y in range(0, height):
            if board[x][y] == 1:
                spaces[x][y].color("black", "red")
            elif board[x][y] == -1:
                spaces[x][y].color("black", "yellow")

# Function to read the click data
def click(x, y):
    global turn

    if playablecol[0][math.floor((x - bordersize)/100)] and playablegame[0]:
        place(turn, math.floor((x - bordersize)/100), 0)
        turn *= -1
    
    for i in range(0, width):
        if turn == 1:
            arrow[i].color("black", "red")
        if turn == -1:
            arrow[i].color("black", "yellow")

# Checking for how many connected pieces in all directions of one piece
def connections(col, row, boardnum):

    board = games[boardnum]
    color = board[col][row]
    connections = []
    adjacent = []
    count = 0
    xdir = 0
    ydir = 0

    # Two for loops to go through all adjacent spaces
    for y in range(-1, 2):
        # Checking if in bounds vertically
        if row + y >= 0 and row + y < height:
            # Second for loop for going through 2d array
            for x in range(-1, 2):
                # Checking to see if it isn't the actual space
                if x != 0 or y != 0:
                    # Checking if in bounds horizontally
                    if col + x >= 0 and col + x < width:
                        # While it is the same color
                        while board[col + x + xdir][row + y + ydir] == color:
                            count += 1
                            # Continuing vector in same direction
                            xdir += x
                            ydir += y
                            # If its out of bounds break the loop
                            if col + x + xdir < 0 or col + x + xdir >= width or row + y + ydir < 0 or row + y + ydir >= height:
                                break
                        # Adding value to the array
                        adjacent.append(count)
                        # Resetting values
                        xdir = 0
                        ydir = 0
                        count = 0 
                    else:
                        adjacent.append(0)
        else:
            # Adding 3 zeroes because whole row is skipped
            for i in range(0, 3):
                adjacent.append(0)

    # Combining opposite vectors together into four bidirectional ones
    for i in range(0, 4):
        connections.append(adjacent[i] + adjacent[len(adjacent) - 1 - i] + 1) 
    
    # If four in a row is detected, game is not playable anymore
    for i in range(0,4):
        if connections[i] == 4:
            playablegame[boardnum] = 0
            wins[boardnum] = 1
    
    if color == 1:
        redconnections[boardnum].append(connections)
    elif color == -1:
        yellowconnections[boardnum].append(connections)


# Checking for what potentials are available
def findPotentials(col, row, boardnum):

    # Temp arrays to store info on what pieces are where
    board = games[boardnum]
    potentiallines = []
    halflines = []
    halfy = []
    halfx = []
    spacey = []
    spacex = []
    xdir = 0
    ydir = 0
    color = board[col][row]

    # Double for loop to go through all directions away from piece
    for y in range(-1, 2):
        for x in range(-1, 2):
            temp = []
            temp2 = [] 
            temp3 = []
            # Making sure its not the piece itself
            if x != 0 or y != 0:
                # While it is in bounds
                while col + x + xdir >= 0 and col + x + xdir < width and row + y + ydir >= 0 and row + y + ydir < height:
                    # Add the color info to the array
                    temp.append(board[col + x + xdir][row + y + ydir])
                    # Storing data on what height the pieces are
                    temp2.append(row + y + ydir)
                    temp3.append(col + x + xdir)
                    xdir += x
                    ydir += y
                
                xdir = 0
                ydir = 0

                # Add array of colors to halflines
                halflines.append(temp)
                # Add the arrays to the halfx and halfy
                halfy.append(temp2)
                halfx.append(temp3)

    # Adding the halflines/halfy/halfx together to make for bidirectional lines from the piece
    for i in range(0, 4):
        inline = []
        connectedy = []
        connectedx = []
        # Reversing the order of the first array because it is collected in the opposite direction, then adding it the inline
        for j in range(0, len(halflines[i])):
            inline.append(halflines[i][len(halflines[i]) - 1 - j])
            connectedy.append(halfy[i][len(halfy[i]) - 1 - j])
            connectedx.append(halfx[i][len(halfx[i]) - 1 - j])
        # Adding the piece itself to the array
        inline.append(color)
        connectedy.append(row)
        connectedx.append(col)
        # Adding the other direction array into inline
        for k in range(0, len(halflines[len(halflines) - 1 - i])):
            inline.append(halflines[len(halflines) - 1 - i][k])
            connectedy.append(halfy[len(halfy) - 1 - i][k])
            connectedx.append(halfx[len(halfx) - 1 - i][k])

        # Collecting all the arrays together
        potentiallines.append(inline)
        spacey.append(connectedy)
        spacex.append(connectedx)
    

    # 3rd potential line is wrong direction because of where it is located, needs to go left to right to correspond to columns
    potentiallines[2].reverse()
    spacey[2].reverse()
    spacex[2].reverse()

    # Initializing new variables for next loops
    count = 0
    zeroused = 0
    zerox = 0
    zeroy = 0

    # For loop to go through the potential lines array
    for i in range(0, 4):
        j = 0
        # While loops to go through the individual bidirectional arrays to count the pieces in a row
        while j < len(potentiallines[i]):
            # If it is the same color add to count
            if potentiallines[i][j] == color:
                count += 1
            # If it reaches the opposite color reset the count
            elif potentiallines[i][j] == -color:
                count = 0
            # If it is empty and no other empty spaces have appeared 
            if potentiallines[i][j] == 0:
                if zeroused == 0:
                    zeroused = 1
                    zeroy = j
                    zerox = i
                    count += 1
                # If zero has been used and it reaches another zero, reset the count to one and set the zero location
                elif zeroused == 1:
                    zeroused == 0
                    zeroy = j
                    zerox = i
                    count == 1
            # Once it reaches four
            if count == 4:
                # Storing the potential to the potential array
                if color == 1:
                    redpotentials[boardnum][spacex[zerox][zeroy]][spacey[zerox][zeroy]] = 1
                elif color == -1:
                    yellowpotentials[boardnum][spacex[zerox][zeroy]][spacey[zerox][zeroy]] = -1
                # Go back 3 spaces to check for more potentials right after
                j -= 3
                # Reset zeroused
                zeroused = 0
                # Reset Count
                count = 0
            # Go to next space
            j += 1
        # Reset for next array
        count = 0
        zeroused = 0

def getPoints(color, boardnum, win):
    board = games[boardnum] 
    points = 0
    doubleconnection = 2
    tripleconnection = 10
    potentialpoints = 100
    if win:
        points += 10000
    if color:
        potentials = redpotentials[boardnum]
        connections = redconnections[boardnum]
    else:
        potentials = yellowpotentials[boardnum]
        connections = yellowconnections[boardnum]
    
    for i in connections:
        for j in range(0, 4):
            if connections[i][j] == 3:
                points += tripleconnection
            elif connections[i][j] == 2:
                points += doubleconnection
    
    for x in potentials:
        for y in potentials[0]:
            if potentials[x][y] == 1:
                points += potentialpoints
    
    return points

if __name__ == "__main__":
    main()
