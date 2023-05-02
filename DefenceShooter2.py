# Import required library
import turtle
import keyboard
import serial
import re


#gareths vars
#over is the light intensity at which we have 2 lights
OVER = 900
UNDER = 25
dev = serial.Serial("COM4", baudrate=9600)

#these are coords passed to game code. -1.0 to 1.0. Percentage
#placement along our xy plane
x = 0.0
y = 0.0


#get the percentage across the axis it should be
def makeAxis(orig, ax):
    toRet = 0.0
    if ax == 0:
         return -1.0
    if orig == 0:
         return 1.0
    if orig > ax:
        toRet = -1.0 + ax / orig
    else:
        toRet = 1.0 - orig / ax

    return toRet

#given light values, make our correct x-y point
def makePoint(vals): 
    global x, y
    #make each point with the origin intensity and axis intensity
    x = makeAxis(vals[0], vals[1])
    y = makeAxis(vals[0], vals[2])

    if x > 1.0:
        x = 1.0
    if y > 1.0: 
        y = 1.0
    if x < -1.0:
        x = 1.0
    if y < -1.0: 
        y = 1.0

# while True:
def getCoord():
    global x, y
    lightVals = dev.readline()
    lightVals = lightVals.decode('ascii')
    lightVals = lightVals.strip()

    values = [0, 0, 0]

    x = 0
    for s in lightVals.split():
        s = int(s)

        #check to see if the light hasn't moved 
        if abs(s - values[x]) < 10:
          #   print("Gareth is dumb")
            return None
            
        values[x] = s
        x += 1
        
#     print(values)

    thresh = 0
    for s in values:
        thresh += s
    #see if 2 lights are detected by looking at total light detected 
    #also see if stuff is turning off 
    if thresh > OVER or thresh < UNDER:
     #    print("2 LIGHTS DETECTED\n")
        return None

    makePoint(values)
    
    return (x, y)






# Create screen
sc = turtle.Screen()
sc.title("Defence Shooter 2.0")
sc.bgcolor("black")
sc.colormode(255)
sc.setup(width = 1.0, height = 1.0)

currentShooterAmmo, shooterAmmo = 1, 1
shooterAmmoArray = [turtle.Turtle() for x in range(shooterAmmo)]
currentDefenderAmmo, defenderAmmo = 3, 3
shooterCooldown = 4
defenderCooldown = 5
gameTime = 120
remainingBases = 3
font = ('Arial', 15, 'normal')
gameOverBool = False
bulletSpeed = 6
bulletMoveDistance = 10

shooterAmmoTracker = turtle.Turtle()
blockAmmoTracker = turtle.Turtle()
timeTracker = turtle.Turtle()
timeTracker.hideturtle()
timeTracker.penup()
timeTracker.goto(260,350)
timeTracker.color(255,255,255)
timeTracker.pendown()
timeTracker.write("Please Wait...", align='left', font=font)


gameOverFont = ('Arial', 30, 'normal')
gameOver = turtle.Turtle()
gameOver.hideturtle()
gameOver.penup()
gameOver.goto(0,0)
gameOver.color(255,255,255)
gameOver.pendown()

#maybe make it just a 3x3 matrix for blocking

#outline for arena
wall_outline = ((376,250), (-376,250), (-376, -250), (376,-250))
turtle.register_shape("wall", wall_outline)
wall = turtle.Turtle()
wall.pencolor((255,255,255))
wall.shape("wall")
wall.penup()

#line showing middle of arena and seperating the two sides
middle_outline = ((0,250), (0,-250))
turtle.register_shape("middle_line", middle_outline)
middle_line = turtle.Turtle()
middle_line.pencolor(255,255,0)
middle_line.shape("middle_line")
middle_line.penup()

#custom shape for defence blocks
#has 50 length and 25 height 
defence_block = ((0,50),(0,-50),(-50,-50),(-50,50))
turtle.register_shape("defence_block", defence_block)

#shield defender character
defender_shape = ((0,15),(-5,0),(0,-15),(10,-15),(25,0),(10,15))
turtle.register_shape("defender", defender_shape)
defender = turtle.Turtle()
defender.speed(0)
defender.shape("defender")
defender.color((0,0,255))
defender.penup()
defender.goto(0, 345)

#array of defender block locations
#3 positions reservered for base targets
#current size is 10 wide and 15 height
#python matrix is weird, first [] is height second is width
#so im making the matrix inversed to make first [] width
width = 3
height = 4
defenderMatrix = [[turtle.Turtle() for x in range(height)] for y in range (width)]

#Generates the base images
defenderMatrix[0][3].shape("triangle")
defenderMatrix[0][3].hideturtle()
defenderMatrix[0][3].speed(0)
defenderMatrix[0][3].color((255,215,0))
defenderMatrix[0][3].left(90)
defenderMatrix[0][3].penup()
defenderMatrix[0][3].goto(-175,360)
defenderMatrix[0][3].showturtle()

defenderMatrix[1][3].shape("triangle")
defenderMatrix[1][3].hideturtle()
defenderMatrix[1][3].speed(0)
defenderMatrix[1][3].color((255,215,0))
defenderMatrix[1][3].left(90)
defenderMatrix[1][3].penup()
defenderMatrix[1][3].goto(-9,360)
defenderMatrix[1][3].showturtle()

defenderMatrix[2][3].shape("triangle")
defenderMatrix[2][3].hideturtle()
defenderMatrix[2][3].speed(0)
defenderMatrix[2][3].color((255,215,0))
defenderMatrix[2][3].left(90)
defenderMatrix[2][3].penup()
defenderMatrix[2][3].goto(157,360)
defenderMatrix[2][3].showturtle()

#turret attacker character
#shooting ORB will be a simple circle at .5 scale
shooter_shape = ((0,15),(0,-15),(15,-15),(15,-5),(25,-5),(25,5),(15,5),(15,15))
turtle.register_shape("shooter",shooter_shape)
shooter = turtle.Turtle()
shooter.speed(0)
shooter.shape("shooter")
shooter.color((255,0,255))
shooter.right(180)
shooter.penup()
shooter.goto(0, -350)

#sets up the defence matrix to be full of turtle objects
def initDefenceMatrix():
    for x in range(width):
        for y in range(height-1):
                xCord = 75 + 166 * x
                yCord = 25 + 115 * y
                defenderMatrix[x][y].shape("defence_block")
                if y != 1:
                    defenderMatrix[x][y].hideturtle()
                defenderMatrix[x][y].speed(0)
                defenderMatrix[x][y].color((102,204,255))
                defenderMatrix[x][y].penup()
                defenderMatrix[x][y].goto(-250 + xCord,yCord)
                

#returns index values of given coords
def mapCordToMatrix(xCord, yCord):
    xIndex = 0
    yIndex = yCord//94
    if xCord > -84 and xCord <= 82:
         xIndex = 1
    if xCord > 82 and xCord <= 250:
         xIndex = 2
    
    return (xIndex,yIndex)

#turns block visible at given index   
def placeBlock(xIndex, yIndex):
    global currentDefenderAmmo
    if currentDefenderAmmo <= 0:
         return
    if defenderMatrix[xIndex][yIndex].isvisible() is False:
        defenderMatrix[xIndex][yIndex].showturtle()
        currentDefenderAmmo -= 1

#checks if a bullet hit a block
# if yes turn block invisible and return true        
def checkForCollison(xIndex,yIndex):
     global remainingBases
     if defenderMatrix[xIndex][yIndex].isvisible():
          defenderMatrix[xIndex][yIndex].hideturtle()
          if yIndex == 3:
               remainingBases = remainingBases - 1
          return True
     return False


def moveDefender(xCord,yCord):
     if xCord <= 250 and xCord >= -250:
          if yCord >= 0 and yCord <= 375:
               defender.goto(xCord,yCord)

def moveShooter(xCord,yCord):
     if xCord <= 250 and xCord >= -250:
          if yCord <= 0 and yCord >= -375:
               shooter.goto(xCord,yCord)
               

#for ammo just have like a queue of bullet objects
#check if non empty to see if i can shoot, then pop and bang

def initShooterAmmo():
     for x in range(shooterAmmo):
          shooterAmmoArray[x]
          shooterAmmoArray[x].shape("circle")
          shooterAmmoArray[x].hideturtle()
          shooterAmmoArray[x].shapesize(stretch_wid=0.5,stretch_len=0.5)
          shooterAmmoArray[x].color((255,0,0))
          shooterAmmoArray[x].penup()
          shooterAmmoArray[x].goto(0,-340)
          shooterAmmoArray[x].left(90)

def shootBullet(xCord,yCord):
     global currentShooterAmmo
     if currentShooterAmmo <= 0:
          return
     shooterAmmoArray[0].goto(xCord,yCord + 15)
     shooterAmmoArray[0].showturtle()
     shooterAmmoArray[0].speed(bulletSpeed)
     currentShooterAmmo = 0
     # for x in range(shooterAmmo):
     #      if not shooterAmmoArray[x].isvisible():
     #           shooterAmmoArray[x].goto(xCord,yCord + 15)
     #           shooterAmmoArray[x].showturtle()
     #           shooterAmmoArray[x].speed(bulletSpeed)
     #           currentShooterAmmo = currentShooterAmmo - 1
     #           break
          
def moveBullets():
     for x in range(1):
          if shooterAmmoArray[x].isvisible():
               shooterAmmoArray[x].forward(bulletMoveDistance)
               xcord, ycord = shooterAmmoArray[x].pos()
               if ycord > 0 and ycord < 375:
                    bulletLocation = mapCordToMatrix(int(xcord),int(ycord))
                    if checkForCollison(bulletLocation[0],bulletLocation[1]):
                         shooterAmmoArray[x].hideturtle()
                         shooterAmmoArray[x].speed(0)
                         shooterAmmoArray[x].goto(0,-340)
               if ycord >=375:
                    shooterAmmoArray[x].hideturtle()
                    shooterAmmoArray[x].speed(0)
                    shooterAmmoArray[x].goto(0,-340)
               
def regenBulletAmmo():
     global shooterCooldown
     global currentShooterAmmo
     shooterCooldown = 2
     if currentShooterAmmo < 1 and shooterAmmoArray[0].isvisible() is False:
          currentShooterAmmo = 1

def regenBlockAmmo():
     global defenderCooldown
     global currentDefenderAmmo
     defenderCooldown = 3
     if currentDefenderAmmo < 3:
          currentDefenderAmmo =  currentDefenderAmmo + 1

ammoHolder = turtle.Turtle()
ammoHolder.hideturtle()
ammoHolder.goto(-270,-350)
ammoHolder.color(255,255,255)
ammoHolder.write("Ammo Remaining: ", align='right', font=font)

blockHolder = turtle.Turtle()
blockHolder.hideturtle()
blockHolder.goto(-273, 350)
blockHolder.color(255,255,255)
blockHolder.write("Blocks Remaining: ", align='right', font=font)

def initTrackers():
     shootText = "Ammo Remaining: "
     blockText = "Blocks Remaining: "
     shooterAmmoTracker.hideturtle()
     blockAmmoTracker.hideturtle()

     shooterAmmoTracker.penup()
     shooterAmmoTracker.goto(-260,-350)
     shooterAmmoTracker.pencolor(255,255,255)
     shooterAmmoTracker.pendown()
     shooterAmmoTracker.write(str(currentShooterAmmo), align='right', font=font)

     blockAmmoTracker.penup()
     blockAmmoTracker.goto(-260,350)
     blockAmmoTracker.pencolor(255,255,255)
     blockAmmoTracker.pendown()
     blockAmmoTracker.write(str(currentDefenderAmmo), align='right', font=font)

def updateTrackers():
     shootText = "Ammo Remaining: "
     blockText = "Blocks Remaining: "
     shooterAmmoTracker.clear()
     shooterAmmoTracker.write(str(currentShooterAmmo), align='right', font=font)
     blockAmmoTracker.clear()
     blockAmmoTracker.write(str(currentDefenderAmmo), align='right', font=font)

def displayGameOver():
     gameOver.write("Game Over!", align='center', font=gameOverFont)

def convertNormToCord(xVal,yVal):
     x = int(xVal * 250)
     y = int(yVal * 375)
     return (x,y)


def countdown(time):
     global shooterCooldown
     global defenderCooldown
     global gameOverBool
     if time > 0:

          shooterCooldown = shooterCooldown - 1
          defenderCooldown = defenderCooldown - 1 

          if shooterCooldown <= 0:
               regenBulletAmmo()
          if defenderCooldown <= 0:
               regenBlockAmmo()
          
          updateTrackers()
          timeText = "Time Remaining: " + str(time)
          timeTracker.clear()
          timeTracker.write(timeText, align='left', font=font)
          sc.ontimer(lambda: countdown(time - 1), 1000)
     else:
          turtle.write("Defender Wins!", align='left', font=font)
          gameOverBool = True




initDefenceMatrix()
initShooterAmmo()
initTrackers()
# setBlockLocation = mapCordToMatrix(214,132)
# placeBlock(setBlockLocation[0],setBlockLocation[1])
# bulletLocation = mapCordToMatrix(-123,231)
#bulletHit = checkForCollison(1,0)

gameOver.write("Hit 'space' to Start!", align='center', font=gameOverFont)

while True:
     try:
          if keyboard.is_pressed('space'):
               break
     except:
          pass


gameOver.clear()
countdown(gameTime)

while gameOverBool is False:
     #get light coordinates from sensors
     normVals = getCoord()
     #if light is present
     if normVals is not None:
          #map light coordinates to game arena coordinates
          cords = convertNormToCord(normVals[0],normVals[1])
          
          #if Y coord is less than 0, let shooter go
          if cords[1] < 0:
               #move shooter character
               #shoot bullet, only activates if there is ammo
               moveShooter(cords[0],cords[1])
               shootBullet(cords[0],cords[1])
          else:
               #map our arena coordinates to matrix indecies
               #place a block at the index locations and move defender
               blockLocation = mapCordToMatrix(cords[0], cords[1])
               placeBlock(blockLocation[0],blockLocation[1])
               moveDefender(cords[0],cords[1])
     #update any bullets currently moving
     moveBullets()
     #end game is all bases are destroyed
     if remainingBases <= 0:
          gameOverBool = True
     #update game screen
     sc.update()

displayGameOver()
    



sc.mainloop()