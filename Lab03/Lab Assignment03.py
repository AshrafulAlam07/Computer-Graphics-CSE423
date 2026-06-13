from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import *

# Global game state management
class GameState:
    def __init__(self):
        self.is_over = False
        self.lives_left = 5
        self.current_score = 0
        self.missed_shots = 0
        self.elapsed_time = 0

    def reset(self):
        self.is_over = False
        self.lives_left = 5
        self.current_score = 0
        self.missed_shots = 0
        self.elapsed_time = 0

# Camera and view management
class CameraController:
    def __init__(self):
        self.previous_coords = None
        self.position = (0, 500, 500)
        self.first_person_active = False
        self.auto_follow_enabled = False
        self.field_of_view = 120

    def toggle_perspective(self):
        self.first_person_active = not self.first_person_active
        self.auto_follow_enabled = False

    def toggle_auto_follow(self):
        self.auto_follow_enabled = not self.auto_follow_enabled

# Player character management
class PlayerCharacter:
    def __init__(self):
        self.coordinates = [0, 0, 0]
        self.rotation_angle = 0
        self.collapse_angle = 0
        self.turn_speed = 10
        self.movement_speed = 30
        self.weapon_length = 80

    def move_forward(self, boundary_limit):
        new_x = self.coordinates[0] + 10 * cos(radians(self.rotation_angle))
        new_y = self.coordinates[1] + 10 * sin(radians(self.rotation_angle))

        if -boundary_limit + 50 <= new_x <= boundary_limit - 50:
            self.coordinates[0] = new_x
        if -boundary_limit + 50 <= new_y <= boundary_limit - 50:
            self.coordinates[1] = new_y

    def move_backward(self, boundary_limit):
        new_x = self.coordinates[0] - 10 * cos(radians(self.rotation_angle))
        new_y = self.coordinates[1] - 10 * sin(radians(self.rotation_angle))

        if -boundary_limit + 55 <= new_x <= boundary_limit - 55:
            self.coordinates[0] = new_x
        if -boundary_limit + 55 <= new_y <= boundary_limit - 55:
            self.coordinates[1] = new_y

    def rotate_left(self):
        self.rotation_angle = (self.rotation_angle + 10)

    def rotate_right(self):
        self.rotation_angle = (self.rotation_angle - 10)

    def collapse(self):
        self.collapse_angle = 90

# Cheat system management
class CheatSystem:
    def __init__(self):
        self.enabled = False
        self.weapon_tracking = False

    def toggle_main_cheat(self):
        self.enabled = not self.enabled
        if not self.enabled:
            self.weapon_tracking = False

    def toggle_weapon_tracking(self, camera_first_person):
        if self.enabled and camera_first_person:
            self.weapon_tracking = not self.weapon_tracking

# Global instances
game_state = GameState()
camera = CameraController()
player = PlayerCharacter()
cheat_system = CheatSystem()

# Game constants
WORLD_BOUNDARY = 600
random_variable = 423

# Game object collections
projectile_list = []
adversary_list = []

# Projectile and enemy parameters
projectile_velocity = 10
projectile_altitude = 100
adversary_radius = 50
adversary_velocity = 0.1

def spawn_adversaries():
    """Initialize enemy positions across the battlefield"""
    global adversary_list
    while len(adversary_list) < 5:
        x_coord = random.randint(-WORLD_BOUNDARY + 100, WORLD_BOUNDARY - 100)
        y_coord = random.randint(-WORLD_BOUNDARY + 100, WORLD_BOUNDARY - 100)
        z_coord = 50
        adversary_list.append({'pos': (x_coord, y_coord, z_coord)})

def render_screen_text(x_pos, y_pos, message, typeface=GLUT_BITMAP_HELVETICA_18):
    """Display text overlay on the game screen"""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x_pos, y_pos)
    for character in message:
        glutBitmapCharacter(typeface, ord(character))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def render_all_objects():
    """Main rendering dispatcher for game objects"""
    if not game_state.is_over:
        render_player_character()
    else:
        render_player_character()
        render_adversary_entities()
        render_projectiles()

def render_player_character():
    """Draw the player character with all components"""
    global player, game_state

    glPushMatrix()

    x_pos, y_pos, z_pos = player.coordinates
    glTranslatef(x_pos, y_pos, z_pos)
    glRotatef(180, 0, 0, 1)
    glRotatef(player.rotation_angle, 0, 0, 1)

    if game_state.is_over:
        glRotatef(player.collapse_angle, 0, 1, 0)

    # Character torso
    glColor3f(0, 0.4, 0)
    glTranslatef(0, 0, 100)
    glScalef(0.5, 1, 2)
    glutSolidCube(50)
    glScalef(2, 1, 0.5)
    glTranslatef(0, 0, -100)

    # Character legs - first leg
    glColor3f(0, 0, 1)
    glTranslatef(0, 10, 50)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)

    glRotatef(-180, 0, 1, 0)
    glTranslatef(0, -10, -50)

    # Character legs - second leg
    glTranslatef(0, -10, 50)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    glRotatef(-180, 0, 1, 0)
    glTranslatef(0, 10, -50)

    # Character head
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 165)
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glTranslatef(0, 0, -165)

    # Character arms - first arm
    glColor3f(1, 0.8, 0.6)
    glTranslatef(0, 30, 125)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)

    glRotatef(90, 0, 1, 0)
    glTranslatef(0, -30, -125)

    # Character arms - second arm
    glTranslatef(0, -30, 125)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 30, -125)

    # Weapon barrel
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 125)
    glRotatef(-90, 0, 1, 0)
    glScalef(1, 1, 2)
    gluCylinder(gluNewQuadric(), 10, 3, 40, 10, 10)
    glScalef(1, 1, 0.5)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, -125)

    glPopMatrix()

def render_adversary_entities():
    """Draw all enemy entities with animation"""
    global adversary_list, game_state, adversary_radius

    animation_scale = 1 + 0.2 * sin(game_state.elapsed_time)

    for adversary in adversary_list:
        glPushMatrix()

        x_pos, y_pos, z_pos = adversary['pos']
        glTranslatef(x_pos, y_pos, z_pos)
        glScalef(animation_scale, animation_scale, animation_scale)

        # Main body sphere
        glColor3f(1, 0, 0)
        glutSolidSphere(adversary_radius, 10, 10)

        # Head sphere
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, 75)
        glutSolidSphere(adversary_radius // 2, 10, 10)
        glTranslatef(0, 0, -75)

        glPopMatrix()

def render_projectiles():
    """Draw all active projectiles"""
    global projectile_list

    for projectile in projectile_list:
        glPushMatrix()
        glTranslatef(projectile['pos'][0], projectile['pos'][1], projectile['pos'][2])
        glRotatef(projectile['angle'], 0, 0, 1)
        glColor3f(1, 0, 0)
        glutSolidCube(10)
        glPopMatrix()

def initialize_fresh_game():
    """Reset all game parameters to starting values"""
    global cheat_system, player, camera, projectile_list, adversary_list

    game_state.reset()
    cheat_system.enabled = False
    cheat_system.weapon_tracking = False

    player.coordinates = [0, 0, 0]
    player.rotation_angle = 0
    player.collapse_angle = 0

    projectile_list = []
    adversary_list = []

    spawn_adversaries()
    print("Fresh game initialized!")

def handle_key_input(pressed_key, mouse_x, mouse_y):
    """Process keyboard input for player actions"""
    global player, cheat_system, game_state, camera

    if game_state.is_over:
        if pressed_key == b'r':
            initialize_fresh_game()
        return

    if pressed_key == b'r':
        initialize_fresh_game()

    if pressed_key == b'w':
        player.move_forward(WORLD_BOUNDARY)
    elif pressed_key == b's':
        player.move_backward(WORLD_BOUNDARY)
    elif pressed_key == b'a':
        player.rotate_left()
    elif pressed_key == b'd':
        player.rotate_right()
    elif pressed_key == b'c':
        cheat_system.toggle_main_cheat()
    elif pressed_key == b'v':
        cheat_system.toggle_weapon_tracking(camera.first_person_active)

    glutPostRedisplay()

def handle_special_keys(special_key, mouse_x, mouse_y):
    """Process special keyboard input for camera control"""
    global camera

    if not camera.first_person_active:
        cam_x, cam_y, cam_z = camera.position

        if special_key == GLUT_KEY_LEFT:
            rotation_angle = -5
            new_x = cam_x * cos(radians(rotation_angle)) - cam_y * sin(radians(rotation_angle))
            new_y = cam_x * sin(radians(rotation_angle)) + cam_y * cos(radians(rotation_angle))
            camera.position = (new_x, new_y, cam_z)

        elif special_key == GLUT_KEY_RIGHT:
            rotation_angle = 5
            new_x = cam_x * cos(radians(rotation_angle)) - cam_y * sin(radians(rotation_angle))
            new_y = cam_x * sin(radians(rotation_angle)) + cam_y * cos(radians(rotation_angle))
            camera.position = (new_x, new_y, cam_z)

        elif special_key == GLUT_KEY_UP:
            cam_z += 10
            camera.position = (cam_x, cam_y, cam_z)

        elif special_key == GLUT_KEY_DOWN:
            cam_z -= 10
            camera.position = (cam_x, cam_y, cam_z)

def handle_mouse_input(button_pressed, button_state, mouse_x, mouse_y):
    """Process mouse input for shooting and camera switching"""
    global projectile_list, camera, player, projectile_altitude

    if button_pressed == GLUT_LEFT_BUTTON and button_state == GLUT_DOWN:
        angle_in_radians = radians(player.rotation_angle)
        projectile_x = player.coordinates[0] + player.weapon_length * cos(angle_in_radians)
        projectile_y = player.coordinates[1] + player.weapon_length * sin(angle_in_radians)
        projectile_z = projectile_altitude

        new_projectile = {
            "pos": [projectile_x, projectile_y, projectile_z],
            "angle": player.rotation_angle
        }
        projectile_list.append(new_projectile)

    elif button_pressed == GLUT_RIGHT_BUTTON and button_state == GLUT_DOWN:
        camera.toggle_perspective()
        cheat_system.weapon_tracking = False
        perspective_mode = 'First-person' if camera.first_person_active else 'Third-person'
        print(f"Camera mode switched to: {perspective_mode}")

def configure_view_perspective():
    """Set up camera projection and view matrix"""
    global camera, player, cheat_system

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(camera.field_of_view, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera.first_person_active:
        head_elevation = 200
        shoulder_displacement = -25
        rear_offset = 75
        player_x, player_y, player_z = player.coordinates

        # Calculate perpendicular direction vectors
        right_direction_x = -sin(radians(player.rotation_angle)) * shoulder_displacement
        right_direction_y = cos(radians(player.rotation_angle)) * shoulder_displacement

        backward_direction_x = -cos(radians(player.rotation_angle)) * rear_offset
        backward_direction_y = -sin(radians(player.rotation_angle)) * rear_offset

        view_x = player_x + player.weapon_length * cos(radians(player.rotation_angle)) * 0.25 + right_direction_x + backward_direction_x
        view_y = player_y + player.weapon_length * sin(radians(player.rotation_angle)) * 0.25 + right_direction_y + backward_direction_y
        view_z = player_z + head_elevation

        if camera.first_person_active and cheat_system.weapon_tracking:
            gluLookAt(camera.previous_coords[0], camera.previous_coords[1], camera.previous_coords[2],
                     camera.previous_coords[3], camera.previous_coords[4], camera.previous_coords[5],
                     0, 0, 1)
        else:
            target_x = view_x + cos(radians(player.rotation_angle))
            target_y = view_y + sin(radians(player.rotation_angle))
            camera.previous_coords = (view_x, view_y, view_z, target_x, target_y, view_z)
            gluLookAt(view_x, view_y, view_z,
                     target_x, target_y, view_z,
                     0, 0, 1)
    else:
        cam_x, cam_y, cam_z = camera.position
        gluLookAt(cam_x, cam_y, cam_z,
                  0, 0, 0,
                  0, 0, 1)

def display_game_scene():
    """Main display function for rendering the complete scene"""
    global WORLD_BOUNDARY

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    configure_view_perspective()

    # Floor tile configuration
    tile_dimension = 80
    tile_count = WORLD_BOUNDARY // tile_dimension

    # Render checkered floor pattern
    for x_index in range(-tile_count, tile_count):
        for y_index in range(-tile_count, tile_count):
            if (x_index + y_index) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1.0, 1.0, 1.0)

            x_start = x_index * tile_dimension
            y_start = y_index * tile_dimension

            glBegin(GL_QUADS)
            glVertex3f(x_start, y_start, 0)
            glVertex3f(x_start + tile_dimension, y_start, 0)
            glVertex3f(x_start + tile_dimension, y_start + tile_dimension, 0)
            glVertex3f(x_start, y_start + tile_dimension, 0)
            glEnd()

    # Boundary wall configuration
    wall_minimum = -WORLD_BOUNDARY + 50
    wall_maximum = WORLD_BOUNDARY - 50
    wall_elevation = 100
    ground_level = 0

    # Render boundary walls with different colors
    wall_colors = [(0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (0.0, 0.0, 1.0), (1.0, 1.0, 1.0)]
    wall_configs = [
        # Left wall
        [(wall_minimum, wall_minimum, ground_level), (wall_minimum, wall_minimum, wall_elevation),
         (wall_minimum, wall_maximum, wall_elevation), (wall_minimum, wall_maximum, ground_level)],
        # Right wall
        [(wall_maximum, wall_minimum, ground_level), (wall_maximum, wall_minimum, wall_elevation),
         (wall_maximum, wall_maximum, wall_elevation), (wall_maximum, wall_maximum, ground_level)],
        # Bottom wall
        [(wall_minimum, wall_minimum, ground_level), (wall_maximum, wall_minimum, ground_level),
         (wall_maximum, wall_minimum, wall_elevation), (wall_minimum, wall_minimum, wall_elevation)],
        # Top wall
        [(wall_minimum, wall_maximum, ground_level), (wall_maximum, wall_maximum, ground_level),
         (wall_maximum, wall_maximum, wall_elevation), (wall_minimum, wall_maximum, wall_elevation)]
    ]

    for color, wall_vertices in zip(wall_colors, wall_configs):
        glColor3f(*color)
        glBegin(GL_QUADS)
        for vertex in wall_vertices:
            glVertex3f(*vertex)
        glEnd()

    # Render game entities based on current state
    if not game_state.is_over:
        render_all_objects()
        render_adversary_entities()
        render_projectiles()
    else:
        render_player_character()

    # Display game information overlay
    if game_state.is_over:
        render_screen_text(10, 710, f"GAME OVER. Your final score is {game_state.current_score}",
                          GLUT_BITMAP_TIMES_ROMAN_24)
        render_screen_text(10, 650, "Press 'R' to RESTART THE GAME",
                          GLUT_BITMAP_HELVETICA_18)
    else:
        render_screen_text(10, 710, f"Player Life Remaining: {game_state.lives_left}")
        render_screen_text(10, 650, f"Game Score: {game_state.current_score}")
        render_screen_text(10, 680, f"Player Bullet Missed: {game_state.missed_shots}")

    glutSwapBuffers()

def game_update_cycle():
    """Main game loop for updating all game mechanics"""
    global game_state, projectile_list, adversary_list, player, cheat_system

    if game_state.is_over:
        glutPostRedisplay()
        return

    game_state.elapsed_time += 0.1

    # Update projectile positions and remove out-of-bounds projectiles
    for projectile in projectile_list[:]:
        projectile['pos'][0] += projectile_velocity * cos(radians(projectile['angle']))
        projectile['pos'][1] += projectile_velocity * sin(radians(projectile['angle']))

        if abs(projectile['pos'][0]) > WORLD_BOUNDARY or abs(projectile['pos'][1]) > WORLD_BOUNDARY:
            is_cheat_projectile = 'cheat' in projectile
            projectile_list.remove(projectile)

            if not is_cheat_projectile:
                game_state.missed_shots += 1
                print(f"Missed! Bullets left before game over: {10 - game_state.missed_shots}")
                if game_state.missed_shots == 10:
                    game_state.is_over = True
                    player.collapse()

    # Update enemy movement towards player
    for adversary in adversary_list:
        delta_x = player.coordinates[0] - adversary['pos'][0]
        delta_y = player.coordinates[1] - adversary['pos'][1]
        distance_to_player = sqrt(delta_x**2 + delta_y**2)

        if distance_to_player > 1:
            adversary['pos'] = (
                adversary['pos'][0] + (delta_x / distance_to_player) * adversary_velocity,
                adversary['pos'][1] + (delta_y / distance_to_player) * adversary_velocity,
                adversary['pos'][2]
            )

    # Check for player-enemy collisions
    for adversary in adversary_list[:]:
        delta_x = player.coordinates[0] - adversary['pos'][0]
        delta_y = player.coordinates[1] - adversary['pos'][1]
        collision_distance = sqrt(delta_x**2 + delta_y**2)

        if collision_distance < adversary_radius:
            if not game_state.is_over:
                game_state.lives_left -= 1
                print(f"Life reduced! Remaining: {game_state.lives_left}")
                if game_state.lives_left <= 0:
                    game_state.is_over = True
                    player.collapse()
                adversary_list.remove(adversary)
                spawn_adversaries()

    # Check for projectile-enemy collisions
    for adversary in adversary_list[:]:
        for projectile in projectile_list[:]:
            distance_x = projectile['pos'][0] - adversary['pos'][0]
            distance_y = projectile['pos'][1] - adversary['pos'][1]
            collision_distance = sqrt(distance_x**2 + distance_y**2)

            if collision_distance < adversary_radius:
                adversary_list.remove(adversary)
                projectile_list.remove(projectile)
                game_state.current_score += 10
                spawn_adversaries()
                break

        # Handle cheat mode functionality
    if cheat_system.enabled and not game_state.is_over:
        player.rotation_angle = player.rotation_angle + 0.6

        nearest_target = None
        minimum_angle_difference = 360

        # Find enemy with smallest angle difference from player aim
        for adversary in adversary_list:
            delta_x = adversary['pos'][0] - player.coordinates[0]
            delta_y = adversary['pos'][1] - player.coordinates[1]
            target_angle = degrees(atan2(delta_y, delta_x)) % 360

            angle_difference = abs((target_angle - player.rotation_angle + 180) % 360 - 180)

            if angle_difference < minimum_angle_difference:
                minimum_angle_difference = angle_difference
                nearest_target = adversary

        # Auto-fire when enemy is in line of sight
        if nearest_target and minimum_angle_difference < 10:
            # Check if a bullet is already heading toward this enemy
            already_fired = False
            for projectile in projectile_list:
                if 'cheat' in projectile:
                    # Check if projectile is close to the enemy
                    px, py = projectile['pos'][0], projectile['pos'][1]
                    ax, ay = nearest_target['pos'][0], nearest_target['pos'][1]
                    if sqrt((px - ax)**2 + (py - ay)**2) < adversary_radius * 2:
                        already_fired = True
                        break
            if not already_fired:
                projectile_list.append({
                    "pos": [player.coordinates[0], player.coordinates[1], projectile_altitude],
                    "angle": player.rotation_angle,
                    "cheat": True
                })

    # Final game over check
    if game_state.lives_left <= 0 and not game_state.is_over:
        game_state.is_over = True
        player.collapse()
        projectile_list.clear()

    glutPostRedisplay()

def main():
    """Initialize and start the game"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Bullet Frenzy")

    glEnable(GL_DEPTH_TEST)

    spawn_adversaries()

    glutDisplayFunc(display_game_scene)
    glutIdleFunc(game_update_cycle)
    glutKeyboardFunc(handle_key_input)
    glutSpecialFunc(handle_special_keys)
    glutMouseFunc(handle_mouse_input)

    glutMainLoop()

if __name__ == "__main__":
    main()