import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

# Game states
PREPLAY = 0
INPLAY = 1
POSTPLAY = 2
gameState = PREPLAY

# set up the window
wH = wW = 800
window = pyglet.window.Window(width = wW, height = wH)
framesPerSecond = 50.

# set up a point
# don't place it in the center so we can tell how
# the coordinate system works in pyglet
pX = wW // 4
pY = wH // 4

# give the point a constant speed
# in one direction
vX = 30 # pixels / second
vY = -30 # pixels / second

# setup a 'pong player': a tall rectangle
# first the position of the center of the pong
pongX = (wW * 3) // 4
pongY = wH // 2

# now the coordinates of the lines relative to the center
pongLines = [(-10,-50),(-10,50),(10,50),(10,-50)]

# combine the two to calculate where the lines should be on the screen
pongPos = [(pongX + x, pongY + y) for x, y in pongLines]

# the pong has vertical velocity when the right keys are pressed
pongSpeed = 50
pongV = 0

# Below are are helper functions for drawing points, lines, shapes
# and text using pyglet    

def drawPoint(x, y):
    "draws a point at x, y"
    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', (x, y)))

def drawPolygonLines(xys):
    "draws a shape outline using the given x, y points of the lines"

    l = len(xys)
    pts = []
    for x, y in xys:
        pts.append(x)
        pts.append(y)
    pyglet.graphics.draw(l, pyglet.gl.GL_LINE_LOOP, ('v2f', tuple(pts)))

def drawPolygon(xys):
    "draws a shape using the given x, y points of the sides"

    l = len(xys)
    pts = []
    for x, y in xys:
        pts.append(x)
        pts.append(y)
    pyglet.graphics.draw(l, pyglet.gl.GL_POLYGON, ('v2f', tuple(pts)))

def drawLabel(value, x, y):
    "draws the given text at the given x, y position"

    label = pyglet.text.Label(value,
                          font_name='Times New Roman',
                          font_size=10, x=x, y=y,
                          anchor_x='left', anchor_y='center')
    label.draw()

def pointInRectangle(x, y, rec):
    "is the given point inside the given lines of a rectangle?"
    # since we know these are the points for a rectangle, we know
    # we can simplyfy things
    x0 = rec[0][0]
    x1 = rec[3][0]
    y0 = rec[0][1]
    y1 = rec[1][1]
   
    # is the point within these coords?
    return x > x0 and x < x1 and y > y0 and y < y1

def update(dt):
    "This is called at regular intervals by the pyglet game"
    if gameState == INPLAY:
        updateInPlay(dt)

def updateInPlay(dt):
    "How the game is updated while in play."
    
    # update method needs to know about these variables
    global pX, vX
    global pY, vY
    global pongX, pongY, pongV, pongLines, pongPos
    
    # update the points position using it's velocity
    pX = pX + (vX * dt)
    pY = pY + (vY * dt)

    # update position of the pong
    pongY = pongY + (pongV * dt)
    # so now the pong's lines on the screen need to be updated
    pongPos = [(pongX + x, pongY + y) for x, y in pongLines]

    # bounce the ball off walls!
    if pX < 0 or pX > wW:
        vX = -1 * vX
    if pY < 0 or pY > wH:
        vY = -1 * vY

    # bounce the ball off the pong
    if pointInRectangle(pX, pY, pongPos):
        print "hit!!!"
        # if it's inside the pong
        vX = -1 * vX

@window.event
def on_key_press(symbol, modifiers):
    global pongV, gameState
    print "on_key_press: ", symbol
    if gameState == INPLAY:
        if symbol == key.UP:
            pongV = pongSpeed
        if symbol == key.DOWN:
            pongV = -pongSpeed
    elif gameState == PREPLAY and symbol == key.ENTER:
        # start playing!
        gameState = INPLAY
    
    

@window.event
def on_key_release(symbol, modifiers):
    global pongV
    print "on_key_release: ", symbol
    if gameState == INPLAY:
        if symbol == key.UP or symbol == key.DOWN:
            pongV = 0

@window.event
def on_draw():
    "Called by pyglet when it's time to draw the screen"

    # first we have to clear everything
    window.clear()

    # then redraw everything!

    if gameState == INPLAY:
        # draw the point
        drawPoint(pX, pY)
        # draw the pong
        drawPolygonLines(pongPos)
    elif gameState == PREPLAY:
        # draw the start message
        drawLabel("Press ENTER to start game.", wW//2, wH//2)
    elif gameState == POSTPLAY:
        # draw the game over message
        drawLabel("Game Over Dude.", wW//2, wH//2)
    

# How fast do we want to update our game?
pyglet.clock.schedule_interval(update, 1./framesPerSecond)

# Run the game!  This is where our program will be sitting.  The @window.event methods are callbacks
pyglet.app.run()

print "Exiting Game."
