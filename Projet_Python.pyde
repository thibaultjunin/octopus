add_library('minim')

"""
 > Inspiration from "Game & Watch, Octopus"
 > By Panha TES & Thibault JUNIN
 > Link: https://github.com/thibaultjunin/octopus
 > Drop a star ;)
"""

# Global variables
backgroundImage = None
pl = None # Player
ms = None # Monster
diedAtClock = 0 # Clock when the player has died
gainAtClock = 0 # Clock when the player has earn a coin, for the last time
wonAtClock = 0 # Clock when the player has won against the game 
clock = 0 # Number of frame since the beginning
sprites = [] # Array of every images (sprites) used in the game
minim = None # Minim variable to play sound
ambiance = None # Ambiance sound

"""
  Permission obtenue auprès de M.Lezowski, d'utiliser les class (et la programation orientée objet)
"""

def setup(): # init
    global backgroundImage, pl, heart, sprites, ms, minim, ambiance
    size(720, 480) # Set window size
    frameRate(15) # Fix frame rate to 15, better animations due to the lack of sprites
    backgroundImage = loadImage("background.png") # Background image (the cave)
    pl = Player() # Init of the player
    ms = Monster() # Init of the monster
    
    # Loading every required sprites
    sprites.append(loadImage("mining_1.png")) # 0
    sprites.append(loadImage("mining_2.png")) # 1
    
    sprites.append(loadImage("still.png")) # 2
    sprites.append(loadImage("walking_1.png")) # 3
    sprites.append(loadImage("walking_2.png")) # 4
    
    sprites.append(loadImage("still_left.png")) # 5
    sprites.append(loadImage("walking_1_left.png")) # 6
    sprites.append(loadImage("walking_2_left.png")) # 7
    
    sprites.append(loadImage("coin.png")) # 8
    sprites.append(loadImage("heart.png")) # 9
    sprites.append(loadImage("barrel.png")) # 10
    sprites.append(loadImage("goddess.png")) # 11
    sprites.append(loadImage("monster_1.png")) # 12
    sprites.append(loadImage("monster_2.png")) # 13
    
    sprites.append(loadImage("died.png")) # 14
    
    # Init of minim (sound system)
    minim = Minim(this) # Yes "this" exists only in Processing ;)
    
    # init and play of ambiance sound
    ambiance = minim.loadFile("ambiance_1.mp3");
    ambiance.loop()

# Game clock
def draw():
    global clock,diedAtClock,gainAtClock,wonAtClock
    pos = pl.getPosition() # Get the current position of the player
    
    if pl.isDead() and diedAtClock+15*5 < clock: # If the player has lost, change his sprite and return
        image(sprites[14], pos[0], pos[1])
        return
    
    clock += 1 # Increasing the clock
    if clock > 15*10 and not ms.isAlive() and wonAtClock == 0 and not pl.isDead(): # If 10s have gone through, spawn the monster
        ms.spawn()
        sound = minim.loadFile("monster.mp3")
        sound.play()
    
    background(backgroundImage) # reset the background
    
    for i in range(pl.getLives()): # show the life bar
        image(sprites[9], i*30, 0)
        
    image(sprites[8], 0, 30) # show the coin icon
    textSize(22)
    text(pl.getCoins(), 35, 50) # show the coin amount
    
    winAt = 50 # Number at which the player will won
    if pl.getCoins() > winAt and wonAtClock == 0: # If the player has earn the required amount, he win
        wonAtClock = clock # Set the clock when he has won
        ambiance.pause() # Stop the ambiance sound
        sound = minim.loadFile("win.mp3") # Load and play the winning sound
        sound.play()
        ms.kill() # Kill the monster
    if pl.getCoins() > winAt: # Change the barrel sprite
        image(sprites[11], 600, 312)
    else:
        image(sprites[10], 650, 390)
        
    if not pl.isDead(): # If the player is alive
        if pl.isMining(): # If the player is mining the barrel
            
            if pos[0] > 539:
                if int(random(0, 10)) == 1 and gainAtClock + 15 < clock:
                    gainAtClock = clock
                    pl.addCoin()
                    s = minim.loadFile("coins.mp3") # Load and play the coin sound
                    s.play()
                    
            if frameCount%2 == 0: # Mining animation
                image(sprites[0], pos[0], pos[1])
            else:
                image(sprites[1], pos[0], pos[1])
                
        else:
            
            if pl.isWalking(): # If the player is walking
                
                if frameCount%2 == 0:
                    
                    if pl.getDirection() == "right":
                        image(sprites[3], pos[0], pos[1])
                    else:
                        image(sprites[6], pos[0], pos[1])
                        
                else:
                    
                    if pl.getDirection() == "right":
                        image(sprites[4], pos[0], pos[1])
                    else:
                        image(sprites[7], pos[0], pos[1])
                        
            else:
                
                if pl.getDirection() == "right":
                    image(sprites[2], pos[0], pos[1])  
                else:
                    image(sprites[5], pos[0], pos[1])
    else:
        image(sprites[14], pos[0], pos[1])
                
    """
    Monster
    """
    
    msPos = ms.getPosition()
    if ms.isAlive():
        ms.move() # Move the monster
        if frameCount%3 == 0:
            image(sprites[12], msPos[0], msPos[1])
        else:
            image(sprites[13], msPos[0], msPos[1])
            
    """
    Death detection
    """
    
    if ms.isAlive() and overlap(102-20, 144-20, 134-20, 111-20, pos[0], pos[1], msPos[0], msPos[1]) and diedAtClock + 15*5 < clock: # If the player loose a life
        diedAtClock = clock
        pl.die()
        sound = minim.loadFile("death.mp3")
        sound.play()
        
    if pl.isDead(): # If the player died
        ambiance.pause()
        ms.kill()

"""
h1: height img 1
w1: width img 1
h2: height img 2
w2: width img 2
x1: x img 1
y1: y img 1
x2: x img 2
y2: y img 2
"""
def overlap(h1, w1, h2, w2, x1, y1, x2, y2): # Check if coordinates overlap. Source: https://github.com/thibaultjunin/cargame
    if within(x2,x1, x1+w1) or within(x2+w2, x1, x1+w1):
        if within(y2, y1, y1+h1) or within(y2+h2, y1, y1+h1):
            return True
    return False

def within(a, b, c):
    return a>b and a<c

def keyPressed(): # When a key is pressed
    if key == CODED:
        if keyCode == LEFT:
            if not pl.isDead():
                pl.left()
            pl.setWalking(True)
        if keyCode == RIGHT:
            if not pl.isDead():
                pl.right()
            pl.setWalking(True)
    else:
        if key == 'm' or key == 'M':
            if not pl.isDead():
                pl.setMining(True)
            
def keyReleased(): # When a key is release (stop the animation)
    if key == CODED:
        if keyCode == LEFT:
            pl.setWalking(False)
        if keyCode == RIGHT:
            pl.setWalking(False)
    else:
        if key == 'm' or key == 'M':
            pl.setMining(False)
    

class Player: # Play class
    
    def __init__(self):
        self.walking = False
        self.mining = False
        self.lives = 3
        self.coins = 0
        self.position = [0, 370]
        self.direction = "right"
        
    def getCoins(self): # Get the amount of coins
        return self.coins
    
    def addCoin(self): # Add a coin
        self.coins += 1
    
    def setWalking(self, w): # Set the animation
        self.walking = w
        
    def isWalking(self): # If the player is walking
        return self.walking
    
    def setMining(self, m): # Set the animation
        self.mining = m

    def isMining(self): # if the player is mining
        return self.mining
    
    def getLives(self): # Get the remaining lives
        return self.lives
    
    def die(self): # remove one life
        self.lives -= 1
        
    def isDead(self): # If the player has no remaing lifes
        return self.lives < 1
        
    def right(self): # Move the player to the right
        if self.position[0] < 570:
            self.position[0] += 10
        self.direction = "right"
        
    def left(self): # Move the player to the left
        if self.position[0] > -40:
            self.position[0] -= 10
        self.direction = "left"
    
    def getPosition(self): # Get player position
        return self.position
    
    def getDirection(self): # Get player direction (right|left)
        return self.direction
    
    def setDirection(self, d): # Set the player direction
        self.direction = d
        
class Monster: # Monster class
    
    def __init__(self):
        self.alive = False
        self.speed = [6.0, 6.0]
        self.position = [0, 0] # x, y
    
    def isAlive(self): # If the monster is alive
        return self.alive
    
    def spawn(self): # Spawn the monster
        self.alive = True
    
    def kill(self): # kill the monster
        self.alive = False
        
    def getPosition(self): # get monster position
        return self.position
    
    def move(self): # move the monster
        if self.position[0] > width-111 or self.position[0] < 0:
             self.speed[0] = -self.speed[0]
             if self.speed[0] > 0:
                 self.speed[0] += 0.1
        if self.position[1] > height-132 or self.position[1] < 0:
             self.speed[1] = -self.speed[1]
             if self.speed[1] > 0:
                 self.speed[1] += 0.1
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
    
    
    
    
