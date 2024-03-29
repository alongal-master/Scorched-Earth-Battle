from enum import Enum
from math import pi

# set up global variables
display_width = 1600
display_height = 900

# color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
good_health_color = green
normal_health_color = (0xff, 0x91, 0x00)
low_health_color = red
blue = (0, 0, 255)
nice_color = (0xfd, 0x30, 0xd5)
dark_green = (0x13, 0x70, 0x2c)
orange = (0xDC, 0x64, 0x0F)
dark_gray = (0x54, 0x4C, 0x46)
player_colors = [red, green, blue, nice_color, orange, dark_gray]

# tank constants
tank_width = 40
tank_height = 12
turret_width = 3
turret_length = int(tank_width/2) + 5
wheel_width = 5
full_tank_height = tank_height + wheel_width
move_step = 3
angle_step = pi/64
initial_turret_angle = -pi/2
initial_tank_health = 100
tank_explosion_power = 40
tank_explosion_radius = 100

# simple shell constants
min_shell_speed = 12
max_shell_speed = 22
shell_speed_step = (max_shell_speed-min_shell_speed)/100
simple_shell_power = 80
simple_shell_radius = 50

# temporary simple ground
ground_height_min = 500
ground_height_max = 800

# player settings
health_bar_init_positions = [(10, 10), (1390, 10), (10, 65), (1390, 65), (10, 120), (1390, 120)]
health_bar_length = 200
players_number = 3
max_players_number = 6
tanks_number = 1
max_tanks_number = 1


# PyGame fonts
class FontSize(Enum):
    XSMALL = 0.5
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Sounds
sound_explosion1 = "assets/music/Explosion1.wav"
sound_explosion2 = "assets/music/Explosion2.wav"
sound_explosion3 = "assets/music/Explosion3.wav"
sound_cannon1 = "assets/music/Cannon1.wav"


# No Sounds
sound_explosion1 = "assets/music/empty.wav"
sound_explosion2 = "assets/music/empty.wav"
sound_explosion3 = "assets/music/empty.wav"
sound_cannon1 = "assets/music/empty.wav"