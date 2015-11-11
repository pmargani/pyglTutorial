import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

# set up the window
wH = wW = 800
window = pyglet.window.Window(width = wW, height = wH)
framesPerSecond = 50.

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

def update(dt):
    "This is called at regular intervals by the pyglet game"
    pass


@window.event
def on_key_press(symbol, modifiers):
    print "on_key_press: ", symbol

@window.event
def on_key_release(symbol, modifiers):
    print "on_key_release: ", symbol

@window.event
def on_draw():
    "Called by pyglet when it's time to draw the screen"

    # first we have to clear everything
    window.clear()

    # then redraw everything!
    drawLabel("START", wW//2, wH//2)


# How fast do we want to update our game?
pyglet.clock.schedule_interval(update, 1./framesPerSecond)

# Run the game!  This is where our program will be sitting.  The @window.event methods are callbacks
pyglet.app.run()

print "Exiting Game."
