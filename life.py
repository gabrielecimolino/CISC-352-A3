from tkinter import *

graph = None
line = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
pulsar = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
grid = pulsar
m = 25
generation = 0
maxGenerations = 9001


def main():
    readIt()
    initialise()
    mainloop()

def readIt():
    global grid
    global maxGenerations
    inputFile = open("inLife.txt","r")
    firstLine = True
    tempGrid = []

    for line in inputFile:
        if firstLine:
            firstLine = False
            maxGenerations = int(line)
        else:
            gridLine = []

            for char in line:
                if char == '0':
                    gridLine.append(0)
                if char == '1':
                    gridLine.append(1)

            tempGrid.append(gridLine)

    grid = tempGrid


def initialise():
    build_graph()


def build_graph():
    global graph
    global m
    WIDTH = m * len(grid[0])
    HEIGHT = m * len(grid)
    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT,
                  (root.winfo_screenwidth() - WIDTH) / 2,
                  (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(40, update)
    graph.pack()


def update():
    global generation
    global maxGenerations
    if generation < maxGenerations:
        draw()
        graph.after(500, update)


def draw():
    global graph
    global m
    global grid
    next_gen()
    newGrid = grid

    graph.delete(ALL)
    row = 0

    while row < len(newGrid):
        col = 0

        while col < len(newGrid[0]):
            cell = newGrid[row][col]

            startX = m * col
            endX = startX + m
            startY = m * row
            endY = startY + m
            if cell == 1:
                graph.create_rectangle(startX, startY, endX, endY,
                        fill='red')
            else:
                graph.create_rectangle(startX, startY, endX, endY,
                        fill='black')
            col = col + 1
        row = row + 1
    graph.update()

def next_gen():
    global generation
    global grid
    newGrid = [[0 for y in grid[0]] for x in grid]

    #print("\nNext gen")
    #print("Initial grid\n", grid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            newGrid[i][j] = fate(i, j)

    #print("Final grid\n", newGrid)
    grid = newGrid
    generation += 1

def fate(i, j):
    global grid
    living = grid[i][j] == 1
    numberOfNeighbours = neighbours(i, j)

    if living:
        if numberOfNeighbours == 2 or numberOfNeighbours == 3:
            return 1
        else:
            return 0
    else:
        if numberOfNeighbours == 3:
            return 1
        else:
            return 0

def neighbours(i, j):
    global grid
    count = 0
    cellName = "cell [%s" % i + ", %s]" % j

    #print("\nChecking neighbours of " + cellName)
    up = i - 1 >= 0
    down = i + 1 < len(grid)
    left = j - 1 >= 0
    right = j + 1 < len(grid[0])

    #Left
    if left:
        if(grid[i][j - 1] == 1):
            #print("There is a neighbour to the left of " +  cellName)
            count += 1
        if up:
            if(grid[i - 1][j - 1] == 1):
                #print("There is a neighbour to the left and up of " + cellName)
                count += 1
        if down:
            if(grid[i + 1][j - 1] == 1):
                #print("There is a neighbour to the left and down of " + cellName)
                count += 1

    #Right
    if right:
        if(grid[i][j + 1] == 1):
            #print("There is a neighbour to the right of " + cellName)
            count += 1
        if up:
            if(grid[i - 1][j + 1] == 1):
                #print("There is a neighbour to the right and up of " + cellName)
                count += 1
        if down:
            if(grid[i + 1][j + 1] == 1):
                #print("There is a neighbour to the right and down of " + cellName)
                count += 1

    #Middle
    if up:
        if(grid[i - 1][j] == 1):
            #print("There is a neighbour above " + cellName)
            count += 1
    if down:
        if(grid[i + 1][j] == 1):
            #print("There is a neighbour below " + cellName)
            count += 1

    #print("Cell [%s" % i + ", %s]" % j + " has %s neighbours" % count)
    return count

main()
