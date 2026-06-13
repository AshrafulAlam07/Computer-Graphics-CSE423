from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0.1, 0.1, 0.2)

class GameState:
    def __init__(self):
        self.player_score = 0
        self.is_game_over = False
        self.is_paused = False
        self.basket_position_x = SCREEN_WIDTH // 2
        self.basket_movement_speed = 30
        self.falling_diamond_x = random.randint(50, SCREEN_WIDTH - 50)
        self.falling_diamond_y = SCREEN_HEIGHT - 50
        self.diamond_fall_speed = 2
        self.available_diamond_colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
        self.current_diamond_color = random.choice(self.available_diamond_colors)
        self.previous_frame_time = time.time()

    def restart_game(self):
        self.player_score = 0
        self.is_game_over = False
        self.is_paused = False
        self.basket_position_x = SCREEN_WIDTH // 2
        self.diamond_fall_speed = 2
        self.create_new_diamond()
        print("Starting Over")

    def create_new_diamond(self):
        self.falling_diamond_x = random.randint(50, SCREEN_WIDTH - 50)
        self.falling_diamond_y = SCREEN_HEIGHT - 50
        self.current_diamond_color = random.choice(self.available_diamond_colors)

game_instance = GameState()

def determine_line_zone(start_x, start_y, end_x, end_y):
    delta_x = end_x - start_x
    delta_y = end_y - start_y

    if abs(delta_x) >= abs(delta_y):
        if delta_x > 0 and delta_y >= 0:
            return 0
        elif delta_x <= 0 and delta_y >= 0:
            return 3
        elif delta_x <= 0 and delta_y < 0:
            return 4
        else:  
            return 7
    else:
        if delta_x >= 0 and delta_y > 0:
            return 1
        elif delta_x <= 0 and delta_y > 0:
            return 2
        elif delta_x <= 0 and delta_y <= 0:
            return 5
        else:  
            return 6

def transform_to_zone_zero(coord_x, coord_y, zone_number):
    if zone_number == 0:
        return coord_x, coord_y
    elif zone_number == 1:
        return coord_y, coord_x
    elif zone_number == 2:
        return coord_y, -coord_x
    elif zone_number == 3:
        return -coord_x, coord_y
    elif zone_number == 4:
        return -coord_x, -coord_y
    elif zone_number == 5:
        return -coord_y, -coord_x
    elif zone_number == 6:
        return -coord_y, coord_x
    elif zone_number == 7:
        return coord_x, -coord_y

def transform_from_zone_zero(coord_x, coord_y, zone_number):
    if zone_number == 0:
        return coord_x, coord_y
    elif zone_number == 1:
        return coord_y, coord_x
    elif zone_number == 2:
        return -coord_y, coord_x
    elif zone_number == 3:
        return -coord_x, coord_y
    elif zone_number == 4:
        return -coord_x, -coord_y
    elif zone_number == 5:
        return -coord_y, -coord_x
    elif zone_number == 6:
        return coord_y, -coord_x
    elif zone_number == 7:
        return coord_x, -coord_y

def calculate_midpoint_line(start_x, start_y, end_x, end_y):
    line_points = []

    # Ensure we draw from left to right for zone 0
    if start_x > end_x:
        start_x, start_y, end_x, end_y = end_x, end_y, start_x, start_y

    line_zone = determine_line_zone(start_x, start_y, end_x, end_y)

    # Convert to zone 0
    start_x_zone0, start_y_zone0 = transform_to_zone_zero(start_x, start_y, line_zone)
    end_x_zone0, end_y_zone0 = transform_to_zone_zero(end_x, end_y, line_zone)

    # Ensure zone 0 ordering
    if start_x_zone0 > end_x_zone0:
        start_x_zone0, start_y_zone0, end_x_zone0, end_y_zone0 = end_x_zone0, end_y_zone0, start_x_zone0, start_y_zone0

    delta_x = end_x_zone0 - start_x_zone0
    delta_y = end_y_zone0 - start_y_zone0

    decision_parameter = 2 * delta_y - delta_x
    increment_east = 2 * delta_y
    increment_northeast = 2 * (delta_y - delta_x)

    current_x, current_y = start_x_zone0, start_y_zone0

    while current_x <= end_x_zone0:
        # Convert back to original zone
        original_x, original_y = transform_from_zone_zero(current_x, current_y, line_zone)
        line_points.append((original_x, original_y))

        if decision_parameter > 0:
            decision_parameter += increment_northeast
            current_y += 1
        else:
            decision_parameter += increment_east
        
        current_x += 1

    return line_points

def render_line(start_x, start_y, end_x, end_y, line_color=(1, 1, 1)):
    glColor3f(*line_color)
    pixel_points = calculate_midpoint_line(int(start_x), int(start_y), int(end_x), int(end_y))

    glBegin(GL_POINTS)
    point_index = 0
    while point_index < len(pixel_points):
        pixel_x, pixel_y = pixel_points[point_index]
        glVertex2f(pixel_x, pixel_y)
        point_index += 1
    glEnd()

def render_diamond_shape(center_x, center_y, diamond_size=10, diamond_color=(1, 1, 1)):
    # Diamond shape with 4 lines
    render_line(center_x, center_y + diamond_size, center_x + diamond_size, center_y, diamond_color)  # Top-right
    render_line(center_x + diamond_size, center_y, center_x, center_y - diamond_size, diamond_color)  # Bottom-right
    render_line(center_x, center_y - diamond_size, center_x - diamond_size, center_y, diamond_color)  # Bottom-left
    render_line(center_x - diamond_size, center_y, center_x, center_y + diamond_size, diamond_color)  # Top-left

def render_catcher_basket(center_x, center_y, basket_width=100, basket_height=10, basket_color=(1, 1, 1)):
    # Catcher shape (bowl-like)
    half_basket_width = basket_width // 2
    render_line(center_x - half_basket_width, center_y, center_x - half_basket_width + 10, center_y - basket_height, basket_color)  # Left side
    render_line(center_x - half_basket_width + 10, center_y - basket_height, center_x + half_basket_width - 10, center_y - basket_height, basket_color)  # Bottom
    render_line(center_x + half_basket_width - 10, center_y - basket_height, center_x + half_basket_width, center_y, basket_color)  # Right side
    render_line(center_x - half_basket_width, center_y, center_x + half_basket_width, center_y, basket_color)  # Top

def render_ui_button(button_x, button_y, button_width, button_height, button_color, button_type):
    # Draw button border
    render_line(button_x, button_y, button_x + button_width, button_y, button_color)  # Top
    render_line(button_x + button_width, button_y, button_x + button_width, button_y + button_height, button_color)  # Right
    render_line(button_x + button_width, button_y + button_height, button_x, button_y + button_height, button_color)  # Bottom
    render_line(button_x, button_y + button_height, button_x, button_y, button_color)  # Left

    # Draw button icon
    button_center_x = button_x + button_width // 2
    button_center_y = button_y + button_height // 2

    if button_type == "restart":  # Left arrow
        render_line(button_center_x + 5, button_center_y - 8, button_center_x - 5, button_center_y, button_color)
        render_line(button_center_x - 5, button_center_y, button_center_x + 5, button_center_y + 8, button_color)
        render_line(button_center_x - 5, button_center_y, button_center_x + 8, button_center_y, button_color)

    elif button_type == "play":  # Play triangle
        render_line(button_center_x - 5, button_center_y - 8, button_center_x - 5, button_center_y + 8, button_color)
        render_line(button_center_x - 5, button_center_y - 8, button_center_x + 8, button_center_y, button_color)
        render_line(button_center_x - 5, button_center_y + 8, button_center_x + 8, button_center_y, button_color)

    elif button_type == "pause":  # Pause bars
        render_line(button_center_x - 5, button_center_y - 8, button_center_x - 5, button_center_y + 8, button_color)
        render_line(button_center_x - 2, button_center_y - 8, button_center_x - 2, button_center_y + 8, button_color)
        render_line(button_center_x + 2, button_center_y - 8, button_center_x + 2, button_center_y + 8, button_color)
        render_line(button_center_x + 5, button_center_y - 8, button_center_x + 5, button_center_y + 8, button_color)

    elif button_type == "exit":  # Cross
        render_line(button_center_x - 6, button_center_y - 6, button_center_x + 6, button_center_y + 6, button_color)
        render_line(button_center_x - 6, button_center_y + 6, button_center_x + 6, button_center_y - 6, button_color)

def detect_collision(diamond_x, diamond_y, basket_x, basket_y):
    # Simple AABB collision detection
    diamond_size = 20
    basket_width = 60
    basket_height = 20

    # Diamond bounding box
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top = diamond_y + diamond_size
    diamond_bottom = diamond_y - diamond_size

    # Catcher bounding box
    basket_left = basket_x - basket_width // 2
    basket_right = basket_x + basket_width // 2
    basket_top = basket_y
    basket_bottom = basket_y - basket_height

    return (diamond_left < basket_right and diamond_right > basket_left and
            diamond_bottom < basket_top and diamond_top > basket_bottom)

def update_game_state():
    if game_instance.is_game_over or game_instance.is_paused:
        return

    current_frame_time = time.time()
    time_since_last_frame = current_frame_time - game_instance.previous_frame_time
    game_instance.previous_frame_time = current_frame_time

    # Move diamond down
    game_instance.falling_diamond_y -= game_instance.diamond_fall_speed * (time_since_last_frame * 60)  # 60 FPS normalization

    # Check collision
    if detect_collision(game_instance.falling_diamond_x, game_instance.falling_diamond_y, game_instance.basket_position_x, 50):
        game_instance.player_score += 1
        print(f"Score: {game_instance.player_score}")
        game_instance.create_new_diamond()
        # Increase difficulty
        game_instance.diamond_fall_speed += 0.1

    # Check if diamond hits ground
    elif game_instance.falling_diamond_y < 0:
        game_instance.is_game_over = True
        print(f"Game Over! Final Score: {game_instance.player_score}")

def render_display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw buttons
    render_ui_button(50, SCREEN_HEIGHT - 80, 60, 40, (0, 0.8, 0.8), "restart")  # Teal restart

    if game_instance.is_paused:
        render_ui_button(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT - 80, 60, 40, (1, 0.6, 0), "play")  # Amber play
    else:
        render_ui_button(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT - 80, 60, 40, (1, 0.6, 0), "pause")  # Amber pause

    render_ui_button(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 80, 60, 40, (1, 0, 0), "exit")  # Red exit

    # Draw catcher
    basket_color = (1, 0, 0) if game_instance.is_game_over else (1, 1, 1)
    render_catcher_basket(game_instance.basket_position_x, 50, basket_color=basket_color)

    # Draw diamond if not game over
    if not game_instance.is_game_over:
        render_diamond_shape(game_instance.falling_diamond_x, game_instance.falling_diamond_y, diamond_color=game_instance.current_diamond_color)

    glutSwapBuffers()

def handle_keyboard_input(key, mouse_x, mouse_y):
    if game_instance.is_game_over or game_instance.is_paused:
        return

    if key == b'\x1b':  # ESC key
        glutLeaveMainLoop()

def handle_special_keys(key, mouse_x, mouse_y):
    if game_instance.is_game_over or game_instance.is_paused:
        return

    if key == GLUT_KEY_LEFT:
        game_instance.basket_position_x = max(30, game_instance.basket_position_x - game_instance.basket_movement_speed)
    elif key == GLUT_KEY_RIGHT:
        game_instance.basket_position_x = min(SCREEN_WIDTH - 30, game_instance.basket_position_x + game_instance.basket_movement_speed)

def handle_mouse_click(button, state, click_x, click_y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        opengl_click_y = SCREEN_HEIGHT - click_y  # Convert to OpenGL coordinates

        # Check restart button
        if 50 <= click_x <= 110 and SCREEN_HEIGHT - 80 <= opengl_click_y <= SCREEN_HEIGHT - 40:
            game_instance.restart_game()

        # Check play/pause button
        elif SCREEN_WIDTH//2 - 30 <= click_x <= SCREEN_WIDTH//2 + 30 and SCREEN_HEIGHT - 80 <= opengl_click_y <= SCREEN_HEIGHT - 40:
            game_instance.is_paused = not game_instance.is_paused
            if game_instance.is_paused:
                print("Game Paused")
            else:
                print("Game Resumed")
                game_instance.previous_frame_time = time.time()  # Reset delta time

        # Check exit button
        elif SCREEN_WIDTH - 110 <= click_x <= SCREEN_WIDTH - 50 and SCREEN_HEIGHT - 80 <= opengl_click_y <= SCREEN_HEIGHT - 40:
            print(f"Goodbye! Final Score: {game_instance.player_score}")
            #glutLeaveMainLoop()
            glutDestroyWindow(glutGetWindow())

def idle_callback():
    update_game_state()
    glutPostRedisplay()

def initialize_opengl():
    glClearColor(*BACKGROUND_COLOR, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")

    initialize_opengl()

    glutDisplayFunc(render_display)
    glutKeyboardFunc(handle_keyboard_input)
    glutSpecialFunc(handle_special_keys)
    glutMouseFunc(handle_mouse_click)
    glutIdleFunc(idle_callback)

    print("Game Started! Use arrow keys to move the catcher.")
    print("Click the buttons to restart, pause/play, or exit the game.")

    glutMainLoop()

if __name__ == "__main__":
    main()