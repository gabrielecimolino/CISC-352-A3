from tkinter import *
import math
import random

graph = None
frameGap = 0

WIDTH = 1500
HEIGHT = 800

boidSize = 5
obstacleSize = 20
bulletSize = 5
bulletSpeed = 2
shotAccuracy = 0.1
rateOfFire = 100
boidNumber = 100
boidSpeed = min(WIDTH, HEIGHT) / 100
separationDistance = 20
obstacleDistance = 70
perceptionDistance = 50
lineOfSight = 150
boundMargin = max(WIDTH, HEIGHT) / 10
boids = []
obstacles = []
bullets = []

#Effects
applyWind = False
windSpeed = None
windHeading = None
obstacleNumber = int(min(WIDTH, HEIGHT) / 100)
dogfight = False

centroidX = 0
centroidY = 0

def main():
    initialise()
    mainloop()


def initialise():
    build_graph()
    createBoids()
    #createObstacles()

def toggleWind():
    global applyWind
    applyWind = not(applyWind)

def toggleDogfight():
    global dogfight
    if(not(dogfight)):
        if(len(obstacles) == 0):
            createObstacles()

    dogfight = not(dogfight)


def build_graph():
    global graph
    global WIDTH
    global HEIGHT
    global boundMargin
    global windSpeed
    global windHeading

    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT,
                  (root.winfo_screenwidth() - WIDTH) / 2,
                  (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())

    frame = Frame(root, width = WIDTH, height = boundMargin)
    frame.pack()

    l = Label(frame, text="Wind speed: ")
    l.pack(side=LEFT)

    windSpeed = Scale(frame, from_=0, to=50, orient=HORIZONTAL)
    windSpeed.pack(side=LEFT)

    l = Label(frame, text="Wind heading: ")
    l.pack(side=LEFT)

    windHeading = Scale(frame, from_=0, to=360, orient=HORIZONTAL)
    windHeading.pack(side=LEFT)

    windButton = Button(frame, text="Wind", command=toggleWind)
    windButton.pack(side=LEFT)

    obstacleButton = Button(frame, text="Asteroids", command=createObstacles)
    obstacleButton.pack(side=LEFT)

    obstacleButton = Button(frame, text="Dogfight", command=toggleDogfight)
    obstacleButton.pack(side=LEFT)

    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(40, update)
    graph.pack()
    
def createBoids():
    global WIDTH
    global HEIGHT
    global boidSpeed
    global boids

    for i in range(boidNumber):
        boid = Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT), boidSpeed, (i > boidNumber / 2))
        boids.append(boid)

def createObstacles():
    global WIDTH
    global HEIGHT
    global separationDistance
    global boidSpeed
    global obstacles
    global obstacleNumber

    # posX = 0

    # while(posX < WIDTH):
    #     obstacle = Boid(posX, 0, boidSpeed)
    #     obstacles.append(obstacle)
    #     posX += separationDistance

    # posX = 0

    # while(posX < WIDTH):
    #     obstacle = Boid(posX, HEIGHT, boidSpeed)
    #     obstacles.append(obstacle)
    #     posX += separationDistance

    # posY = 0

    # while(posY < HEIGHT):
    #     obstacle = Boid(0, posY, boidSpeed)
    #     obstacles.append(obstacle)
    #     posY += separationDistance

    # posY = 0

    # while(posY < HEIGHT):
    #     obstacle = Boid(WIDTH, posY, boidSpeed)
    #     obstacles.append(obstacle)
    #     posY += separationDistance
    if(len(obstacles) == 0):
        for i in range(obstacleNumber):
            obstacle = Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT), boidSpeed, False)
            obstacles.append(obstacle)
    else:
        while(len(obstacles) > 0):
            del obstacles[len(obstacles) - 1]
        obstacles = []

def wind(velocities):
    global graph
    global WIDTH
    global HEIGHT
    global windSpeed
    global windHeading

    s = windSpeed.get()
    h = windHeading.get()
    h = h / 57.2958

    #graph.create_line(WIDTH / 2, HEIGHT / 2, WIDTH / 2 + s * math.sin(h), HEIGHT / 2 + s * math.cos(h))

    for i in range(len(velocities)):
        velocities[i][0] += s * math.sin(h)
        velocities[i][1] += s * math.cos(h)

    return velocities


def move():
    global boids
    global boidSpeed

    velocities = []

    #print("Moving boids")
    cohesionVelocities = cohesion()
    separationVelocities = separation()

    for i in range(len(boids)):
        velocities.append([cohesionVelocities[i][0] + separationVelocities[i][0], cohesionVelocities[i][1] + separationVelocities[i][1]])

    alignedVelocities = alignment()
    boundVelocities = bound()

    if(applyWind):
        velocities = wind(velocities)

    for i in range(len(boids)):
        vX = velocities[i][0] + alignedVelocities[i][0] + boundVelocities[i][0]
        vY = velocities[i][1] + alignedVelocities[i][1] + boundVelocities[i][1]
        magnitude = mag(vX, vY)
        if(magnitude > 0):
            vX = vX / magnitude
            vY = vY / magnitude
        else:
            vX = 0
            vY = 0
        boids[i].updatePosition(vX, vY, boidSpeed)

def shoot():
    global boids
    global bullets
    global bulletSize
    global boidSize
    global shotAccuracy
    global bulletSpeed
    global rateOfFire
    global lineOfSight

    for boid in boids:
        if(boid.framesSinceShot > rateOfFire):
            for otherBoid in boids:
                if(boid != otherBoid):
                    if(boid.red != otherBoid.red):
                        difX = otherBoid.posX - boid.posX
                        difY = otherBoid.posY - boid.posY
                        magnitude = mag(difX, difY)
                            
                        if(magnitude < lineOfSight):    
                            if(magnitude > 0):
                                difX = difX / magnitude
                                difY = difY / magnitude
                            else:
                                difX = 0
                                difY = 0

                            headingX = boid.headingX
                            headingY = boid.headingY
                            magnitude = mag(headingX, headingY)
                            if(magnitude > 0):
                                headingX = headingX / magnitude
                                headingY = headingY / magnitude
                            else:
                                headingX = 0
                                headingY = 0

                            if(abs(headingX - difX) < shotAccuracy and abs(headingY - difY) < shotAccuracy):
                                boid.framesSinceShot = 0
                                bullet = Bullet(boid.posX, boid.posY, boid.headingX * bulletSpeed, boid.headingY * bulletSpeed, boid.red)
                                bullets.append(bullet)
        else:
            boid.framesSinceShot += 1

def cleanUpBullets():
    global bullets
    global WIDTH
    global HEIGHT

    i = 0

    while(i < len(bullets)):
        delete = False

        if(bullets[i].posX < 0):
            delete = True
        if(bullets[i].posX > WIDTH):
            delete = True
        if(bullets[i].posY < 0):
            delete = True
        if(bullets[i].posY > HEIGHT):
            delete = True

        if(delete):
            del bullets[i]
        else:    
            i += 1

def resolveCollisions():
    global boids
    global bullets

    i = 0

    while(i < len(boids)):
        hit = False
        boids[i]
        j = 0

        while(j < len(bullets)):
            if(boids[i].red != bullets[j].red):
                if(collision(boids[i].posX, boids[i].posY, bullets[j].posX, bullets[j].posY)):
                    hit = True
                    del bullets[j]
                else:
                    j += 1
            else:
                j += 1

        if(hit):
            del boids[i]
        else:
            i += 1

def collision(boidX, boidY, bulletX, bulletY):
    global boidSize
    global bulletSize

    left = bulletX < boidX + boidSize
    right = bulletX + bulletSize > boidX
    down = bulletY < boidY + boidSize
    up = bulletY + bulletSize > boidY

    if(left and right and down and up):
        return True

    return False

def bound():
    global boids
    global HEIGHT
    global WIDTH

    velocities = []

    for boid in boids:
        pX = 0
        pY = 0

        if(boid.posX < 0 + boundMargin):
            pX = boundMargin - boid.posX
        if(boid.posX > WIDTH - boundMargin):
            pX = (WIDTH - boundMargin) - boid.posX
        if(boid.posY < 0 + boundMargin):
            pY = boundMargin - boid.posY
        if(boid.posY > HEIGHT - boundMargin):
            pY = (HEIGHT - boundMargin) - boid.posY

        velocities.append([pX, pY])

    return velocities

def cohesion():
    global boids
    global boidSpeed
    global frameGap
    global perceptionDistance
    global centroidX
    global centroidY
    global dogfight

    frameSmoothing = frameGap / 1000

    velocities = []

    centroidX = 0
    centroidY = 0

    for boid in boids:
        centroidX += boid.posX
        centroidY += boid.posY

    centroidX = centroidX / len(boids)
    centroidY = centroidY / len(boids)

    for boid in boids:
        neighbours = 0
        pX = 0
        pY = 0

        for otherBoid in boids:
            if( (dogfight and boid.red == otherBoid.red) or not(dogfight) ):
                difX = otherBoid.posX - boid.posX
                difY = otherBoid.posY - boid.posY
                difMagnitude = math.sqrt(math.pow(difX, 2) + math.pow(difY, 2))
                if(difMagnitude < perceptionDistance and difMagnitude > 0):
                    neighbours += 1
                    pX += otherBoid.posX
                    pY += otherBoid.posY

        difX = 0
        difY = 0
        
        if(neighbours > 0):
            difX = (pX / neighbours) - boid.posX
            difY = (pY / neighbours) - boid.posY
            difMagnitude = math.sqrt(math.pow(difX, 2) + math.pow(difY, 2))
            # if(difMagnitude != 0):
            #     difX = difX / difMagnitude
            #     difY = difY / difMagnitude

        velocities.append([difX, difY])

    # print("\nCohesion")
    # print(velocities)

    return velocities

def mag(x, y):
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

def separation():
    global boids 
    global obstacles
    global boidSpeed
    global frameGap
    global separationDistance

    frameSmoothing = frameGap / 1000

    velocities = []

    for boid in boids:
        vX = 0
        vY = 0

        for otherBoid in boids:
            difX = otherBoid.posX - boid.posX
            difY = otherBoid.posY - boid.posY
            difMagnitude = mag(difX, difY)

            if(difMagnitude < separationDistance and difMagnitude != 0):
                vX -= difX#(difX / difMagnitude)# * (separationDistance - difMagnitude)
                vY -= difY#(difY / difMagnitude)# * (separationDistance - difMagnitude)

        for obstacle in obstacles:
            difX = obstacle.posX - boid.posX
            difY = obstacle.posY - boid.posY
            difMagnitude = mag(difX, difY)

            if(difMagnitude < obstacleDistance and difMagnitude > 0):
                vX -= difX * math.pow((obstacleDistance - difMagnitude), 2)
                vY -= difY * math.pow((obstacleDistance - difMagnitude), 2)

        # if(touching > 0):
        #     vX = vX / touching
        #     vY = vY / touching

        # if(touching > 0):
        #     magnitude = mag(vX, vY)
        # else:
        #     magnitude = 1

        velocities.append([vX, vY])

    # print("\nSeparation")
    # print(velocities)

    return velocities

def alignment():
    # global boids

    # alignedVelocities = []

    # averageX = 0
    # averageY = 0

    # for i in range(len(velocities)):
    #     averageX += velocities[i][0]
    #     averageY += velocities[i][1]

    # for i in range(len(boids)):
    #     pX = (averageX - velocities[i][0]) / (len(boids) - 1)
    #     pY = (averageY - velocities[i][1]) / (len(boids) - 1)
    #     alignedVelocities.append([pX/8, pY/8])

    # print("\nAlignment")
    # print(alignedVelocities)

    # return alignedVelocities

    global boids
    global perceptionDistance
    global dogfight

    alignedVelocities = []

    for boid in boids:
        neighbours = 0
        pX = 0
        pY = 0

        for otherBoid in boids:
            if(boid != otherBoid):
                if( (dogfight and boid.red == boid.red) or not(dogfight) ):
                    if(mag((otherBoid.posX - boid.posX), (otherBoid.posY - boid.posY)) < perceptionDistance):
                        neighbours += 1   
                        pX += otherBoid.headingX
                        pY += otherBoid.headingY

        if(neighbours > 0):
            pX = pX / neighbours #(len(boids) - 1)
            pY = pY / neighbours #(len(boids) - 1)

        alignedVelocities.append([pX, pY])

    # print("\nAlignment")
    # print(alignedVelocities)

    return alignedVelocities

def update():
    global frameGap
    global dogfight

    move()
    if(dogfight):
        resolveCollisions()
        shoot()
    cleanUpBullets()
    draw()
    graph.after(frameGap, update)

def draw():
    global graph
    global boidSize
    global obstacleSize
    global bulletSize
    global centroidX
    global centroidY
    global boids
    global obstacles
    global bullets
    global dogfight

    graph.delete(ALL)

    positions = []

    for boid in boids:
        boid.drawBoid(graph, boidSize, dogfight)
        positions.append([boid.posX, boid.posY])

    for obstacle in obstacles:
        obstacle.drawObstacle(graph, obstacleSize)

    for bullet in bullets:
        bullet.updatePosition(graph, bulletSize)

    # print("\nPositions")
    # print(positions)

    graph.create_oval(centroidX - boidSize / 2, centroidY - boidSize / 2, centroidX + boidSize / 2, centroidY + boidSize / 2)


    if(applyWind):
        s = windSpeed.get()
        h = windHeading.get()
        h = h / 57.2958

        graph.create_line(WIDTH / 2, HEIGHT / 2, WIDTH / 2 + s * math.sin(h), HEIGHT / 2 + s * math.cos(h))

    graph.update()

class Boid:
    def __init__(self, posX, posY, boidSpeed, red):
        self.posX = posX
        self.posY = posY
        self.headingX = random.randint(0, boidSpeed)
        self.headingY = random.randint(0, boidSpeed)
        self.red = red
        self.framesSinceShot = 0

    def updatePosition(self, headingX, headingY, boidSpeed):

        self.headingX += headingX
        self.headingY += headingY

        if(self.headingX > boidSpeed):
            self.headingX = boidSpeed
        if(self.headingX < -boidSpeed):
            self.headingX = -boidSpeed
        if(self.headingY > boidSpeed):
            self.headingY = boidSpeed
        if(self.headingY < -boidSpeed):
            self.headingY = -boidSpeed

        # if(headingX != 0 and headingY != 0):
        #     self.headingX = headingX
        #     self.headingY = headingY

        self.posX += self.headingX
        self.posY += self.headingY

    def drawObstacle(self, graph, obstacleSize):
        graph.create_oval(self.posX - (obstacleSize / 2), self.posY - (obstacleSize / 2), self.posX + (obstacleSize / 2) , self.posY + (obstacleSize / 2), fill='#000')


    def drawBoid(self, graph, boidSize, dogfight):
        if(self.headingX == 0):
            heading = 0
        else:
            heading = math.atan(self.headingY/self.headingX)

        #print("Boid rotation is %s degrees" % (57.2958 * heading))

        cosHeading = math.cos(heading)
        sinHeading = math.sin(heading)

        # #Initialize pointing down
        # point1X = 0
        # point1Y = -boidSize

        # point2X = boidSize
        # point2Y = boidSize

        # point3X = -boidSize
        # point3Y = boidSize

        # #Initialize pointing right
        # point1X = boidSize
        # point1Y = 0

        # point2X = -boidSize
        # point2Y = boidSize

        # point3X = -boidSize
        # point3Y = -boidSize

        #Initialize pointing left
        point1X = -boidSize
        point1Y = 0

        point2X = boidSize
        point2Y = boidSize

        point3X = boidSize
        point3Y = -boidSize

        #Rotate to match heading
        tempX = point1X * cosHeading + point1Y * -sinHeading
        tempY = point1X * sinHeading + point1Y * cosHeading

        point1X = tempX + self.posX
        point1Y = tempY + self.posY

        tempX = point2X * cosHeading + point2Y * -sinHeading
        tempY = point2X * sinHeading + point2Y * cosHeading

        point2X = tempX + self.posX
        point2Y = tempY + self.posY

        tempX = point3X * cosHeading + point3Y * -sinHeading
        tempY = point3X * sinHeading + point3Y * cosHeading

        point3X = tempX + self.posX
        point3Y = tempY + self.posY

        if(not(self.red) and dogfight):
            graph.create_polygon(point1X, point1Y, point2X, point2Y, point3X, point3Y, fill="blue")
        else:
            graph.create_polygon(point1X, point1Y, point2X, point2Y, point3X, point3Y, fill="red")
        graph.create_line(point1X, point1Y, point1X + self.headingX, point1Y + self.headingY)
        #graph.create_polygon(startX, endY, (startX + (endX - startX) / 2, startY, endX, endY), fill="red")

class Bullet:
    def __init__(self, posX, posY, headingX, headingY, red):
        self.posX = posX
        self.posY = posY
        self.headingX = headingX
        self.headingY = headingY
        self.red = red

    def updatePosition(self, graph, bulletSize):
        self.posX += self.headingX
        self.posY += self.headingY

        if(self.red):
            graph.create_oval(self.posX - (bulletSize / 2), self.posY - (bulletSize / 2), self.posX + (bulletSize / 2) , self.posY + (bulletSize / 2), fill="red")
        else:
            graph.create_oval(self.posX - (bulletSize / 2), self.posY - (bulletSize / 2), self.posX + (bulletSize / 2) , self.posY + (bulletSize / 2), fill="blue")

main()

