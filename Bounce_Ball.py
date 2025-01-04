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
def update_game(value):
    global ball_position, ball_speed, obstacles, roof_obstacles, long_obstacles, tall_obstacles, diamonds
    global coins, score, is_game_over, frame_count, lives

    if is_paused or is_game_over:
        glutTimerFunc(30, update_game, 0)
        return

    ball_speed[1] += gravity
    ball_position[1] += ball_speed[1]

    if ball_position[1] - ball_radius <= GROUND_HEIGHT:
        ball_position[1] = GROUND_HEIGHT + ball_radius
        ball_speed[1] = 0


    if ball_position[1] + ball_radius >= ROOF_HEIGHT:
        ball_position[1] = ROOF_HEIGHT - ball_radius
        ball_speed[1] = 0

    for obs in obstacles[:]:
        obs[0] -= 5
        if obs[0] + obs[2] < 0:
            obstacles.remove(obs)
        if check_collision_circle_rect((ball_position[0], ball_position[1], ball_radius), obs):
            if lives > 0:
                lives -= 1
                obstacles.remove(obs)  
            else:
                is_game_over = True

    for obs in roof_obstacles[:]:
        obs[0] -= 5
        if obs[0] + obs[2] < 0:
            roof_obstacles.remove(obs)
        if check_collision_circle_rect((ball_position[0], ball_position[1], ball_radius), obs):
            if lives > 0:
                lives -= 1
                roof_obstacles.remove(obs) 
            else:
                is_game_over = True

    for obs in long_obstacles[:]:
        obs[0] -= 5
        if obs[0] + obs[2] < 0:
            long_obstacles.remove(obs)
        if check_collision_circle_rect((ball_position[0], ball_position[1], ball_radius), obs):
            if lives > 0:
                lives -= 1
                long_obstacles.remove(obs)  
            else:
                is_game_over = True

    for obs in tall_obstacles[:]:
        obs[0] -= 5
        if obs[0] + obs[2] < 0:
            tall_obstacles.remove(obs)
        if check_collision_circle_rect((ball_position[0], ball_position[1], ball_radius), obs):
            if lives > 0:
                lives -= 1
                tall_obstacles.remove(obs) 
            else:
                is_game_over = True

    for coin in coins[:]:
        coin[0] -= 5
        if ((ball_position[0] - coin[0]) ** 2 + (ball_position[1] - coin[1]) ** 2) ** 0.5 < ball_radius + 8:
            coins.remove(coin)
            score += 1

    for diamond in diamonds[:]:
        diamond[0] -= 5
        if ((ball_position[0] - diamond[0]) ** 2 + (ball_position[1] - diamond[1]) ** 2) ** 0.5 < ball_radius + 10:
            diamonds.remove(diamond)
            lives += 1  

    
    frame_count += 1
    if frame_count % 250 == 0:
        long_obstacles.append([WIN_WIDTH, GROUND_HEIGHT + 10, 150, 20])
    if frame_count % 100 == 0:
        obstacles.append([WIN_WIDTH, GROUND_HEIGHT, 20, 50])
    if frame_count % 450 == 0:
        tall_obstacles.append([WIN_WIDTH, GROUND_HEIGHT + 100, 30, 100])
    if frame_count % 180 == 0:
        roof_obstacles.append([WIN_WIDTH, ROOF_HEIGHT - 140, 140, 35])
        
    diamond_y_positions = [GROUND_HEIGHT + 140, GROUND_HEIGHT + 200, GROUND_HEIGHT + 260, GROUND_HEIGHT + 320]
    current_y_index = 0

    if frame_count % 100 == 0:
        diamonds.append([WIN_WIDTH, diamond_y_positions[current_y_index]])
        current_y_index = (current_y_index + 1) % len(diamond_y_positions)

    if frame_count % 150 == 0:
        coins.append([WIN_WIDTH + 140, GROUND_HEIGHT + 140])

    if score >= 2:
        is_game_over = True
        render_text("YOU WIN!", WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2)

    glutPostRedisplay()
    glutTimerFunc(30, update_game, 0)

    
def check_collision_circle_rect(circle, rect):
    cx, cy, r = circle
    rx, ry, rw, rh = rect

    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))

    distance = ((cx - closest_x) ** 2 + (cy - closest_y) ** 2) ** 0.5

    return distance < r



def render_text(text, x, y):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    global score, lives
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_ground()
    draw_roof()
    draw_ball()
    draw_obstacles()
    draw_coins()
    draw_tall_obstacles()
    draw_roof_obstacles()
    draw_diamonds()
    draw_buttons()
    glColor3f(1, 1, 1)
    render_text(f"Score: {score}", 10, WIN_HEIGHT - 20)
    render_text(f"Lives: {lives}", 10, WIN_HEIGHT - 40)

    if is_game_over:
        glColor3f(1, 0, 0)
        if score >= 2:
            render_text("YOU WIN!", WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2)
        else:
            render_text("GAME OVER", WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2)

    glutSwapBuffers()

def keyboard(key, x, y):
    global ball_position, ball_speed
    if key == b' ' and ball_position[1] - ball_radius == GROUND_HEIGHT:
        ball_speed[1] = jump_speed
    elif key == b'd':  
        ball_position[0] += ball_horizontal_speed
    elif key == b'a':  
        ball_position[0] -= ball_horizontal_speed

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
