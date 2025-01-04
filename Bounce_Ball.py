from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math



#rahat

# Game variables
WIN_WIDTH, WIN_HEIGHT = 600, 400
GROUND_HEIGHT = 25  # Height of the ground
ROOF_HEIGHT = WIN_HEIGHT - GROUND_HEIGHT

ball_position = [100, GROUND_HEIGHT + 15] 
ball_radius = 15
ball_speed = [0, 0] 
ball_horizontal_speed = 5
gravity = -0.5
jump_speed = 14
obstacles = []
roof_obstacles=[]
long_obstacles=[]
tall_obstacles=[]
coins = []
score = 0
is_game_over = False
frame_count = 0
lives = 0  
diamonds = []  
is_paused = False 
BUTTONS = {
    "Pause": (200, WIN_HEIGHT - 50, 80, 30),  
    "Restart": (400, WIN_HEIGHT - 50, 100, 30),
}



def draw_circle(cx, cy, r):
    x, y = 0, r
    d = 1 - r
    while x <= y:
        draw8way(cx, cy, x, y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

def draw_line(x1, y1, x2, y2):
    zone = findzone(x1, y1, x2, y2)  
    x1, y1 = zone0(zone, x1, y1)
    x2, y2 = zone0(zone, x2, y2)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    x = x1
    y = y1

    glPointSize(5)
    glBegin(GL_POINTS)
    while x <= x2:
        xo, yo = originalzone(zone, x, y)
        glVertex2f(xo, yo)
        x += 1
        if d < 0:
            d += 2 * dy
        else:
            d += 2 * (dy - dx)
            y += 1
    glEnd()

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy): 
        if dx >= 0 and dy >= 0:
            return 0  # Zone 0
        elif dx <= 0 and dy >= 0:
            return 3  # Zone 3
        elif dx <= 0 and dy <= 0:
            return 4  # Zone 4
        elif dx >= 0 and dy <= 0:
            return 7  # Zone 7
    else:  # Slope greater than 1
        if dx >= 0 and dy >= 0:
            return 1  # Zone 1
        elif dx <= 0 and dy >= 0:
            return 2  # Zone 2
        elif dx <= 0 and dy <= 0:
            return 5  # Zone 5
        elif dx >= 0 and dy <= 0:
            return 6  # Zone 6

    
def draw8way(center_x, center_y, x, y):
    glBegin(GL_POINTS)
    glVertex2f(center_x + x, center_y + y)
    glVertex2f(center_x + y, center_y + x)
    glVertex2f(center_x + x, center_y - y)
    glVertex2f(center_x + y, center_y - x)
    glVertex2f(center_x - x, center_y + y)
    glVertex2f(center_x - y, center_y + x)
    glVertex2f(center_x - x, center_y - y)
    glVertex2f(center_x - y, center_y - x)
    glEnd()

def zone0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def originalzone(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_rectangle(x1, y1, x2, y2):
    draw_line(x1, y1, x2, y1)
    draw_line(x2, y1, x2, y2)
    draw_line(x2, y2, x1, y2)
    draw_line(x1, y2, x1, y1)

def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)

def draw_ball():
    glColor3f(1, 0, 0)
    draw_circle(ball_position[0], ball_position[1], ball_radius)

def draw_ground():
    glColor3f(0, 0, 1)
    draw_rectangle(0, 0, WIN_WIDTH, GROUND_HEIGHT)

def draw_roof():
    glColor3f(0, 0, 1)  
    draw_rectangle(0, ROOF_HEIGHT-100, WIN_WIDTH, WIN_HEIGHT-100)









































#chisty

























































#niloy




































def init_window():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIN_WIDTH, WIN_HEIGHT)
    glutCreateWindow(b"Bounce Ball Game with Roof and Nails")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutTimerFunc(30, update_game, 0)

    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIN_WIDTH, 0, WIN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)

if __name__ == "__main__":
    init_window()
    glutMainLoop()