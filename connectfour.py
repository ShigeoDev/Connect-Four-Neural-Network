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

# Arrays to store data on color and objects
board = []
spaces = []
arrow = []
playable = []

# 1 is Red, -1 is Yellow
turn = 1

def main():

    # Creating board and spaces with turtles
    for x in range(0, width):

        boardcol = []
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
            boardcol.append(0)

        board.append(boardcol)
        spaces.append(spacecol)

    # Creating clickable triangles
    for x in range(0, width):

        triangle = turtle.Turtle()
        triangle.penup()
        triangle.shape("triangle")
        triangle.speed(0)
        triangle.color("black", "green")
        triangle.shapesize(4, 2, 2)
        triangle.setheading(270)
        triangle.setpos(x * 100 + 50 + bordersize - 5, 650)
        arrow.append(triangle)

    # Making all the columns playable
    for x in range(0, width):

        playable.append(1)
    


    place(1, 0, board)
    place(1, 1, board)
    place(1, 3, board)
    place(1, 5, board)
    place(1, 6, board)

    potentials(3, 0, board)

    # Constantly checking for clicks
    while True:
        for i in range(0, len(arrow)):
            arrow[i].onclick(click)
        updateBoard(board, spaces)
        turtle.update()
    


    turtle.update()

    time.sleep(3)

# Function to place piece in certain column
def place(color, col, board):
    y = 0
    while board[col][y] != 0:
        if y == 5:
            break
        elif y == 4:
            playable[col] = 0
        y += 1
    board[col][y] = color

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

    if playable[math.floor((x - bordersize)/100)]:
        place(turn, math.floor((x - bordersize)/100), board)
        turn *= -1

# Checking for how many connected pieces in all directions of one piece
def connections(col, row, board):

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
    
    print(connections)

# Checking for what potentials are available
def potentials(col, row, board):

    # Temp arrays to store info on what pieces are where
    potentiallines = []
    halflines = []
    xdir = 0
    ydir = 0
    color = board[col][row]

    # Double for loop to go through all directions away from piece
    for y in range(-1, 2):
        for x in range(-1, 2):
            temp = []
            # Making sure its not the piece itself
            if x != 0 or y != 0:
                # While it is in bounds
                while col + x + xdir >= 0 and col + x + xdir < width and row + y + ydir >= 0 and row + y + ydir < height:
                    # Add the color info to the array
                    temp.append(board[col + x + xdir][row + y + ydir])
                    xdir += x
                    ydir += y
                
                xdir = 0
                ydir = 0

                # Add array of colors to halflines
                halflines.append(temp)

    # Adding the halflines together to make for bidirectional lines from the piece
    for i in range(0, 4):
        inline = []
        # Reversing the order of the first array because it is collected in the opposite direction, then adding it the inline
        for j in range(0, len(halflines[i])):
            inline.append(halflines[i][len(halflines[i]) - 1 - j])
        # Adding the piece itself to the array
        inline.append(color)
        # Adding the other direction array into inline
        for k in range(0, len(halflines[len(halflines) - 1 - i])):
            inline.append(halflines[len(halflines) - 1 - i][k])

        # Collecting all the arrays together
        potentiallines.append(inline)

    # 3rd potential line is wrong direction because of where it is located, needs to go left to right to correspond to columns
    potentiallines[2].reverse()
         
    # Initializing new variables for next loops
    count = 0
    potentials = 0
    zeroused = 0

    # For loop to go through the potential lines array
    for i in range(0, 4):
        j = 0
        # While loops to go through the individual bidirectional arrays to count the pieces in a row
        while j < len(potentiallines[i]):
            # If it is the same color add to count
            if potentiallines[i][j] == color:
                count += 1
            # If it is empty and no other empty spaces have appeared 
            if potentiallines[i][j] == 0 and zeroused == 0:
                zeroused = 1
                count += 1
            # Once it reaches four
            if count == 4:
                # In rare case it makes two potentials have to double check spot
                j -= 1
                # Add one to potentials
                potentials += 1
                # Reset zeroused
                zeroused = 0
                # Reset Count
                count = 0
            # Go to next space
            j += 1
        # Reset for next array
        count = 0
        zeroused = 0

    return(potentials)

if __name__ == "__main__":
    main()
