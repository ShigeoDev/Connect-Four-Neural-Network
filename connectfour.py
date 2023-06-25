import turtle
import time
import math

screenwidth = 7
screenheight = 6
bordersize = 20

screen = turtle.Screen()
screen.setup((screenwidth) * 100 + 2 * bordersize, (screenheight) * 100 + 2 * bordersize)
screen.setworldcoordinates(0, 0, (screenwidth) * 100 + 2 * bordersize, (screenheight) * 100 + 5 * bordersize)
screen.bgcolor("blue")

turtle.tracer(0)

height = 6
width = 7

board = []
spaces = []
arrow = []
playable = []

turn = 1

def main():

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

    for x in range(0, width):

        playable.append(1)
    
    place(-1, 0, board)
    place(-1, 0, board)
    place(-1, 0, board)

    place(1, 1, board)
    place(-1, 1, board)
    place(1, 1, board)

    place(-1, 2, board)
    place(1, 2, board)
    place(1, 2, board)

    connections(1, 1, board)


    while True:
        for i in range(0, len(arrow)):
            arrow[i].onclick(click)
        updateBoard(board, spaces)
        turtle.update()

    turtle.update()

    time.sleep(3)

def place(color, col, board):
    y = 0
    while board[col][y] != 0:
        if y == 5:
            break
        elif y == 4:
            playable[col] = 0
        y += 1
    board[col][y] = color

def updateBoard(board, spaces):
    for x in range(0, width):
        for y in range(0, height):
            if board[x][y] == 1:
                spaces[x][y].color("black", "red")
            elif board[x][y] == -1:
                spaces[x][y].color("black", "yellow")

def click(x, y):
    global turn

    if playable[math.floor((x - bordersize)/100)]:
        place(turn, math.floor((x - bordersize)/100), board)
        turn *= -1

def connections(col, row, board):

    color = board[col][row]
    connections = []
    adjacent = []
    count = 0
    xdir = 0
    ydir = 0

    for y in range(-1, 2):
        if row + y >= 0 and row + y < height:
            for x in range(-1, 2):
                if x != 0 or y != 0:
                    if col + x >= 0 and col + x < width:
                        if board[col + x + xdir][row + y + ydir] == color:
                            while board[col + x + xdir][row + y + ydir] == color:
                                count += 1
                                xdir += x
                                ydir += y
                                if col + x + xdir < 0 or col + x + xdir >= width or row + y + ydir < 0 or row + y + ydir >= height:
                                    break
                            adjacent.append(count)
                            xdir = 0
                            ydir = 0
                            count = 0 
                        else:
                                adjacent.append(0)
                    else:
                        adjacent.append(0)
        else:
            for i in range(0, 3):
                adjacent.append(0)

    for i in range(0, 4):
        connections.append(adjacent[i] + adjacent[len(adjacent) - 1 - i] + 1) 
    
    print(connections)


if __name__ == "__main__":
    main()








