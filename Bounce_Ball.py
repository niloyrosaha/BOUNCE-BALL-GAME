from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math



#rahat











































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