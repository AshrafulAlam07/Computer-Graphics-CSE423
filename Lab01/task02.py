from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

# Global variables
width, height = 800, 600
box_margin = 50
points = []
base_speed = 2.0
speed_multiplier = 1.0
is_blinking = False
is_frozen = False
start_time = time.time()

# Box boundaries
box_left = box_margin
box_right = width - box_margin
box_top = height - box_margin
box_bottom = box_margin

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx, self.dy = random.choice([(-1,-1), (-1,1), (1,-1), (1,1)])
        self.r, self.g, self.b = [random.uniform(0.2, 1.0) for _ in range(3)]
        self.original_color = (self.r, self.g, self.b)
        self.is_visible = True

    def update(self):
        if is_frozen:
            return

        speed = base_speed * speed_multiplier
        self.x += self.dx * speed
        self.y += self.dy * speed

        if self.x <= box_left or self.x >= box_right:
            self.dx *= -1
            self.x = max(box_left, min(box_right, self.x))

        if self.y <= box_bottom or self.y >= box_top:
            self.dy *= -1
            self.y = max(box_bottom, min(box_top, self.y))

    def update_blink(self):
        if not is_blinking:
            self.r, self.g, self.b = self.original_color
            self.is_visible = True
            return

        current_time = time.time() - start_time
        if current_time % 1.0 < 0.5:
            self.r, self.g, self.b = self.original_color
            self.is_visible = True
        else:
            self.r, self.g, self.b = 0.0, 0.0, 0.0
            self.is_visible = False

def draw_box():
    glColor3f(1, 1, 1)
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box_left, box_bottom)
    glVertex2f(box_right, box_bottom)
    glVertex2f(box_right, box_top)
    glVertex2f(box_left, box_top)
    glEnd()

def draw_points():
    glPointSize(8)
    glBegin(GL_POINTS)
    for point in points:
        point.update_blink()
        if point.is_visible or not is_blinking:
            glColor3f(point.r, point.g, point.b)
            glVertex2f(point.x, point.y)
    glEnd()

def draw_instructions():
    # info = [
    #     "Right Click: Add moving point",
    #     "Left Click: Toggle blinking",
    #     "Up Arrow: Increase speed",
    #     "Down Arrow: Decrease speed",
    #     "Spacebar: Freeze/Unfreeze",
    #     f"Points: {len(points)}",
    #     f"Speed: {speed_multiplier:.1f}x",
    #     f"Status: {'FROZEN' if is_frozen else 'ACTIVE'}",
    #     f"Blinking: {'ON' if is_blinking else 'OFF'}"
    # ]
    glColor3f(0.8, 0.8, 0.8)
    y = height - 20
    for line in info:
        glRasterPos2f(10, y)
        for ch in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
        y -= 18

def display():
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    for point in points:
        point.update()
    draw_box()
    draw_points()
    draw_instructions()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global is_blinking, start_time
    if is_frozen or state != GLUT_DOWN:
        return
    gl_x, gl_y = x, height - y
    if button == GLUT_RIGHT_BUTTON:
        if box_left <= gl_x <= box_right and box_bottom <= gl_y <= box_top:
            points.append(Point(gl_x, gl_y))
            print(f"Added point at ({gl_x}, {gl_y})")
    elif button == GLUT_LEFT_BUTTON:
        is_blinking = not is_blinking
        start_time = time.time()
        print(f"Blinking: {'ON' if is_blinking else 'OFF'}")

def keyboard(key, x, y):
    global is_frozen
    if key == b' ':
        is_frozen = not is_frozen
        print(f"Status: {'FROZEN' if is_frozen else 'ACTIVE'}")
    elif key == b'\x1b':  # ESC key
        glutLeaveMainLoop()

def special_keys(key, x, y):
    global speed_multiplier
    if is_frozen:
        return
    if key == GLUT_KEY_UP:
        speed_multiplier = min(speed_multiplier + 0.2, 5.0)
        print(f"Speed increased to {speed_multiplier:.1f}x")
    elif key == GLUT_KEY_DOWN:
        speed_multiplier = max(speed_multiplier - 0.2, 0.1)
        print(f"Speed decreased to {speed_multiplier:.1f}x")

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def reshape(w, h):
    global width, height, box_left, box_right, box_top, box_bottom
    width, height = w, h
    box_left = box_margin
    box_right = width - box_margin
    box_top = height - box_margin
    box_bottom = box_margin
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_opengl():
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glClearColor(0, 0, 0, 1)

def main():
    print("=== Amazing Box Controls ===")
    print("Right Click: Add moving point at cursor location")
    print("Left Click: Toggle blinking on/off")
    print("Up Arrow: Increase speed of all points")
    print("Down Arrow: Decrease speed of all points")
    print("Spacebar: Freeze/Unfreeze all functionality")
    print("ESC: Exit")
    print("============================")

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Amazing Box - OpenGL Task")

    init_opengl()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(16, timer, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
