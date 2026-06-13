from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import time

# Global variables
width, height = 1200, 800
rain_drops = []
rain_angle = 0                                     # Angle rain direction
background_brightness = 0.2                        # 0.0 = night, 1.0 = day
day_night_speed = 0.02

# Key states for continuous input
keys = {
    'left': False,
    'right': False,
    'd': False,
    'n': False
}

# Rain drop class
class RainDrop:
    def __init__(self):
        self.x = random.uniform(0, width)
        self.y = random.uniform(height, height + 100)
        self.speed = random.uniform(3, 8)
        self.length = random.uniform(10, 25)
    
    def update(self):
        # Apply wind effect based on rain_angle
        wind_effect = math.sin(math.radians(rain_angle)) * 2
        self.x += wind_effect
        self.y -= self.speed
        
        # Reset rain drop when it goes off screen
        if self.y < -50:
            self.y = random.uniform(height, height + 100)
            self.x = random.uniform(-50, width + 50)

def init_rain():
    global rain_drops
    rain_drops = []
    for _ in range(150):
        rain_drops.append(RainDrop())

def draw_house():
    # House base color (adjusted for day/night)
    house_r = 0.6 + background_brightness * 0.3
    house_g = 0.4 + background_brightness * 0.4
    house_b = 0.2 + background_brightness * 0.2
    
    # Draw house base (rectangle using triangles)
    glColor3f(house_r, house_g, house_b)
    glBegin(GL_TRIANGLES)
    # Rectangle as two triangles
    # Triangle 1
    glVertex2f(400, 200)  # bottom left
    glVertex2f(800, 200)  # bottom right
    glVertex2f(400, 450)  # top left
    # Triangle 2
    glVertex2f(800, 200)  # bottom right
    glVertex2f(800, 450)  # top right
    glVertex2f(400, 450)  # top left
    glEnd()
    
    # Draw roof (triangle)
    roof_r = 0.8 + background_brightness * 0.2
    roof_g = 0.2 + background_brightness * 0.3
    roof_b = 0.1 + background_brightness * 0.2
    glColor3f(roof_r, roof_g, roof_b)
    glBegin(GL_TRIANGLES)
    glVertex2f(350, 450)  # left
    glVertex2f(850, 450)  # right
    glVertex2f(600, 600)  # top
    glEnd()
    
    # Draw door (rectangle using triangles)
    door_r = 0.4 + background_brightness * 0.2
    door_g = 0.2 + background_brightness * 0.2
    door_b = 0.1 + background_brightness * 0.1
    glColor3f(door_r, door_g, door_b)
    glBegin(GL_TRIANGLES)
    # Triangle 1
    glVertex2f(520, 200)
    glVertex2f(580, 200)
    glVertex2f(520, 350)
    # Triangle 2
    glVertex2f(580, 200)
    glVertex2f(580, 350)
    glVertex2f(520, 350)
    glEnd()
    
    # Draw door knob (point)
    glColor3f(1.0, 1.0, 0.8)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2f(565, 275)
    glEnd()
    
    # Draw windows (rectangles using triangles)
    window_r = 0.6 + background_brightness * 0.4
    window_g = 0.8 + background_brightness * 0.2
    window_b = 1.0
    glColor3f(window_r, window_g, window_b)
    
    # Left window
    glBegin(GL_TRIANGLES)
    # Triangle 1
    glVertex2f(450, 320)
    glVertex2f(500, 320)
    glVertex2f(450, 380)
    # Triangle 2
    glVertex2f(500, 320)
    glVertex2f(500, 380)
    glVertex2f(450, 380)
    glEnd()
    
    # Right window
    glBegin(GL_TRIANGLES)
    # Triangle 1
    glVertex2f(700, 320)
    glVertex2f(750, 320)
    glVertex2f(700, 380)
    # Triangle 2
    glVertex2f(750, 320)
    glVertex2f(750, 380)
    glVertex2f(700, 380)
    glEnd()
    
    # Window frames (lines)
    frame_brightness = 0.3 + background_brightness * 0.4
    glColor3f(frame_brightness, frame_brightness, frame_brightness)
    glLineWidth(2)
    
    # Left window frame
    glBegin(GL_LINES)
    # Vertical line
    glVertex2f(475, 320)
    glVertex2f(475, 380)
    # Horizontal line
    glVertex2f(450, 350)
    glVertex2f(500, 350)
    glEnd()
    
    # Right window frame
    glBegin(GL_LINES)
    # Vertical line
    glVertex2f(725, 320)
    glVertex2f(725, 380)
    # Horizontal line
    glVertex2f(700, 350)
    glVertex2f(750, 350)
    glEnd()
    
    # Draw chimney (rectangle using triangles)
    chimney_r = 0.5 + background_brightness * 0.2
    chimney_g = 0.3 + background_brightness * 0.2
    chimney_b = 0.2 + background_brightness * 0.1
    glColor3f(chimney_r, chimney_g, chimney_b)
    glBegin(GL_TRIANGLES)
    # Triangle 1
    glVertex2f(720, 500)
    glVertex2f(760, 500)
    glVertex2f(720, 580)
    # Triangle 2
    glVertex2f(760, 500)
    glVertex2f(760, 580)
    glVertex2f(720, 580)
    glEnd()

def draw_rain():
    # Rain color (more visible against different backgrounds)
    if background_brightness < 0.5:
        glColor3f(0.7, 0.9, 1.0)                              # Light blue night
    else:
        glColor3f(0.3, 0.5, 0.8)                               # Darker blue day
    
    glLineWidth(2)
    glBegin(GL_LINES)
    
    for drop in rain_drops:
        # Calculate wind-affected position
        wind_offset = math.sin(math.radians(rain_angle)) * drop.length * 0.3
        
        # Draw rain drop as a line
        glVertex2f(drop.x, drop.y)
        glVertex2f(drop.x + wind_offset, drop.y - drop.length)
    
    glEnd()

def draw_ground():
    ground_r = 0.1 + background_brightness * 0.3
    ground_g = 0.4 + background_brightness * 0.4
    ground_b = 0.1 + background_brightness * 0.2
    glColor3f(ground_r, ground_g, ground_b)
    glBegin(GL_TRIANGLES)
    # Ground as a large triangle strip
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(0, 200)
    glVertex2f(width, 0)
    glVertex2f(width, 200)
    glVertex2f(0, 200)
    glEnd()
def display():
    global background_brightness, rain_angle
    # Handle continuous key presses
    if keys['left']:
        rain_angle = max(rain_angle - 1, -30)  # Limit to -30 degrees
    if keys['right']:
        rain_angle = min(rain_angle + 1, 30)   # Limit to 30 degrees
    if keys['d']:
        background_brightness = min(background_brightness + day_night_speed, 1.0)
    if keys['n']:
        background_brightness = max(background_brightness - day_night_speed, 0.0)
    
    # Update rain drops
    for drop in rain_drops:
        drop.update()
    
    # Clear screen with background color
    glClearColor(background_brightness * 0.6, 
                background_brightness * 0.8, 
                background_brightness + 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw scene
    draw_ground()
    draw_house()
    draw_rain()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    key = key.decode('utf-8').lower()
    if key == 'd':
        keys['d'] = True
    elif key == 'n':
        keys['n'] = True
    elif key == '\x1b':  # ESC key
        glutLeaveMainLoop()

def keyboard_up(key, x, y):
    key = key.decode('utf-8').lower()
    if key == 'd':
        keys['d'] = False
    elif key == 'n':
        keys['n'] = False

def special_keys(key, x, y):
    if key == GLUT_KEY_LEFT:
        keys['left'] = True
    elif key == GLUT_KEY_RIGHT:
        keys['right'] = True

def special_keys_up(key, x, y):
    if key == GLUT_KEY_LEFT:
        keys['left'] = False
    elif key == GLUT_KEY_RIGHT:
        keys['right'] = False

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS
def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)

def init_opengl():
    glClearColor(0.2, 0.3, 0.4, 1.0)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    # Set up 2D orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    print("Controls:")
    print("Left Arrow: Bend rain to the left")
    print("Right Arrow: Bend rain to the right")
    print("D Key: Transition to day (lighter)")
    print("N Key: Transition to night (darker)")
    print("ESC: Exit")
    
    # Initialize GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"House with Animated Rainfall")
    
    # Initialize OpenGL
    init_opengl()
    
    # Initialize rain
    init_rain()
    
    # Register callback functions
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_keys)
    glutSpecialUpFunc(special_keys_up)
    glutTimerFunc(16, timer, 0)
    
    # Start main loop
    glutMainLoop()

if __name__ == "__main__":
    main()

# #task2

# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# import random
# import time

# # Global variables
# width, height = 800, 600
# box_margin = 50
# points = []
# base_speed = 2.0
# speed_multiplier = 1.0
# is_blinking = False
# is_frozen = False
# start_time = time.time()

# # Box boundaries
# box_left = box_margin
# box_right = width - box_margin
# box_top = height - box_margin
# box_bottom = box_margin

# # Point class
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.dx, self.dy = random.choice([(-1,-1), (-1,1), (1,-1), (1,1)])
#         self.r, self.g, self.b = [random.uniform(0.2, 1.0) for _ in range(3)]
#         self.original_color = (self.r, self.g, self.b)
#         self.is_visible = True

#     def update(self):
#         if is_frozen:
#             return

#         speed = base_speed * speed_multiplier
#         self.x += self.dx * speed
#         self.y += self.dy * speed

#         if self.x <= box_left or self.x >= box_right:
#             self.dx *= -1
#             self.x = max(box_left, min(box_right, self.x))

#         if self.y <= box_bottom or self.y >= box_top:
#             self.dy *= -1
#             self.y = max(box_bottom, min(box_top, self.y))

#     def update_blink(self):
#         if not is_blinking:
#             self.r, self.g, self.b = self.original_color
#             self.is_visible = True
#             return

#         current_time = time.time() - start_time
#         if current_time % 1.0 < 0.5:
#             self.r, self.g, self.b = self.original_color
#             self.is_visible = True
#         else:
#             self.r, self.g, self.b = 0.0, 0.0, 0.0
#             self.is_visible = False

# def draw_box():
#     glColor3f(1, 1, 1)
#     glLineWidth(3)
#     glBegin(GL_LINE_LOOP)
#     glVertex2f(box_left, box_bottom)
#     glVertex2f(box_right, box_bottom)
#     glVertex2f(box_right, box_top)
#     glVertex2f(box_left, box_top)
#     glEnd()

# def draw_points():
#     glPointSize(8)
#     glBegin(GL_POINTS)
#     for point in points:
#         point.update_blink()
#         if point.is_visible or not is_blinking:
#             glColor3f(point.r, point.g, point.b)
#             glVertex2f(point.x, point.y)
#     glEnd()

# def draw_instructions():
#     info = [
#         "Right Click: Add moving point",
#         "Left Click: Toggle blinking",
#         "Up Arrow: Increase speed",
#         "Down Arrow: Decrease speed",
#         "Spacebar: Freeze/Unfreeze",
#         f"Points: {len(points)}",
#         f"Speed: {speed_multiplier:.1f}x",
#         f"Status: {'FROZEN' if is_frozen else 'ACTIVE'}",
#         f"Blinking: {'ON' if is_blinking else 'OFF'}"
#     ]
#     glColor3f(0.8, 0.8, 0.8)
#     y = height - 20
#     for line in info:
#         glRasterPos2f(10, y)
#         for ch in line:
#             glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
#         y -= 18

# def display():
#     glClearColor(0, 0, 0, 1)
#     glClear(GL_COLOR_BUFFER_BIT)
#     for point in points:
#         point.update()
#     draw_box()
#     draw_points()
#     draw_instructions()
#     glutSwapBuffers()

# def mouse(button, state, x, y):
#     global is_blinking, start_time
#     if is_frozen or state != GLUT_DOWN:
#         return
#     gl_x, gl_y = x, height - y
#     if button == GLUT_RIGHT_BUTTON:
#         if box_left <= gl_x <= box_right and box_bottom <= gl_y <= box_top:
#             points.append(Point(gl_x, gl_y))
#             print(f"Added point at ({gl_x}, {gl_y})")
#     elif button == GLUT_LEFT_BUTTON:
#         is_blinking = not is_blinking
#         start_time = time.time()
#         print(f"Blinking: {'ON' if is_blinking else 'OFF'}")

# def keyboard(key, x, y):
#     global is_frozen
#     if key == b' ':
#         is_frozen = not is_frozen
#         print(f"Status: {'FROZEN' if is_frozen else 'ACTIVE'}")
#     elif key == b'\x1b':  # ESC key
#         glutLeaveMainLoop()

# def special_keys(key, x, y):
#     global speed_multiplier
#     if is_frozen:
#         return
#     if key == GLUT_KEY_UP:
#         speed_multiplier = min(speed_multiplier + 0.2, 5.0)
#         print(f"Speed increased to {speed_multiplier:.1f}x")
#     elif key == GLUT_KEY_DOWN:
#         speed_multiplier = max(speed_multiplier - 0.2, 0.1)
#         print(f"Speed decreased to {speed_multiplier:.1f}x")

# def timer(value):
#     glutPostRedisplay()
#     glutTimerFunc(16, timer, 0)

# def reshape(w, h):
#     global width, height, box_left, box_right, box_top, box_bottom
#     width, height = w, h
#     box_left = box_margin
#     box_right = width - box_margin
#     box_top = height - box_margin
#     box_bottom = box_margin
#     glViewport(0, 0, w, h)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluOrtho2D(0, w, 0, h)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# def init_opengl():
#     glEnable(GL_POINT_SMOOTH)
#     glEnable(GL_LINE_SMOOTH)
#     glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
#     glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
#     glClearColor(0, 0, 0, 1)

# def main():
#     print("=== Amazing Box Controls ===")
#     print("Right Click: Add moving point at cursor location")
#     print("Left Click: Toggle blinking on/off")
#     print("Up Arrow: Increase speed of all points")
#     print("Down Arrow: Decrease speed of all points")
#     print("Spacebar: Freeze/Unfreeze all functionality")
#     print("ESC: Exit")
#     print("============================")

#     glutInit()
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#     glutInitWindowSize(width, height)
#     glutInitWindowPosition(100, 100)
#     glutCreateWindow(b"Amazing Box - OpenGL Task")

#     init_opengl()

#     glutDisplayFunc(display)
#     glutReshapeFunc(reshape)
#     glutMouseFunc(mouse)
#     glutKeyboardFunc(keyboard)
#     glutSpecialFunc(special_keys)
#     glutTimerFunc(16, timer, 0)

#     glutMainLoop()

# if __name__ == "__main__":
#     main()
