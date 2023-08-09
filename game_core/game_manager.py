import pygame
from shapely.geometry import LineString
from random import choice
from math import sin, cos, radians

import game_core.constants
from game_core.constants import *
from game_core.ground import Ground
from game_core.player import Player
from game_core.utils import animate_ground_sloughing, halt_whole_game, animate_explosion, message_to_screen
from bots import bots

class GameManager:
    """
    Class which represents game manager object in game
    """
    def __init__(self, tank_number, player_objects):
        """
        Init function
        :param player_number: number of players
        :param tank_number: number of tanks for each player
        """
        self.players = []
        self.active_player = None
        self.game_display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('ScorchedEarth')
        self.clock = pygame.time.Clock()
        self.strike_earth_sound = pygame.mixer.Sound(sound_explosion1)
        self.normal_strike_sound = pygame.mixer.Sound(sound_explosion2)
        self.ground = None
        self.players_number = len(player_objects)
        self.player_objects = player_objects
        self.taken_colors = []
        self.tank_number = tank_number
        self.free_colors = ['red', 'green', 'blue', 'purple', 'yellow', 'orange', 'cyan', 'magenta']
        self.player_color_dict = {}
    def reinitialize_players(self):
        """
        Reinitialize available tanks in the game
        :return: none
        """
        self.ground = Ground(self.game_display)
        self.players = []
        # Get the RGB values from Pygame's color dictionary
        for i, player in enumerate(self.player_objects):
            preferred_color = player.get_preferred_color()
            # Color is valid and not taken
            if preferred_color not in self.taken_colors and preferred_color in pygame.color.THECOLORS:
                color = preferred_color
                self.taken_colors.append(preferred_color)
            # Color already taken or invalid :(
            else:
                color = self.free_colors.pop()
            # Create player object
            self.players.append(Player(self.game_display, self.tank_number, pygame.color.THECOLORS[color], i, player))
        init_tanks_positions = []
        for player in self.players:
            player.initialize_tanks(init_tanks_positions, self.ground)
        self.active_player = self.players[0]

    def check_collision(self, prev_shell_position, current_shell_position):
        """
        Checks collision of shell with other objects and return coordinates of shell collision
        :param prev_shell_position: Coordinates of previous shell position
        :param current_shell_position: Coordinates of updated shell position
        :return: Coordinates of collision or None if no collision detected
        """
        line1 = LineString([prev_shell_position, current_shell_position])

        for player in self.players:
            intersection = player.check_collision_with_tanks(line1)
            if intersection:
                return intersection

        return self.ground.check_collision(line1)

    def correct_ground(self, point, explosion_radius):
        """
        Corrects ground after explosion
        :param point: point of explosion
        :param explosion_radius: radius of explosion
        :return: none
        """
        left_ground = self.ground.update_after_explosion(point, explosion_radius)
        if len(left_ground) > 0:
            self.draw_all()
            animate_ground_sloughing(self.game_display, left_ground, self.ground)
            self.ground.update_after_sloughing(left_ground)

    def apply_players_damages(self, collision_point, shell_power, shell_radius):
        """
        Applies damages for players tanks
        :param collision_point: point of collision
        :param shell_power: power of shell
        :param shell_radius: radius of shell
        :return: none
        """
        explosion_points = []
        for player in self.players:
            explosion_points.extend(player.apply_damage(collision_point, shell_power, shell_radius))
        if len(explosion_points) > 0:
            for point in explosion_points:
                self.correct_ground(point, tank_explosion_radius)
                self.apply_players_damages(point, tank_explosion_power, tank_explosion_radius)

    def correct_tanks_heights(self):
        """
        Corrects heights of all players' tanks
        :return: none
        """
        for player in self.players:
            player.correct_tanks_heights(self.ground)

    def fire_simple_shell(self, tank_object):
        """
        Show animation of shooting simple shell
        :param tank_object: tank object that shoots the shell
        :return: none
        """
        (power, gun_angle, fire_sound, color, gun_end_coord) = tank_object.get_init_data_for_shell()
        pygame.mixer.Sound.play(fire_sound)
        speed = min_shell_speed + shell_speed_step * power
        shell_position = list(gun_end_coord)
        elapsed_time = 0.1

        fire = True

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    halt_whole_game()

            prev_shell_position = list(shell_position)
            vertical_speed = -((speed * cos(gun_angle)) - 10 * elapsed_time / 2)
            horizontal_speed = (speed * sin(gun_angle))
            shell_position[0] += int(horizontal_speed * elapsed_time)
            shell_position[1] += int(vertical_speed * elapsed_time)
            elapsed_time += 0.1

            if shell_position[1] > 2 * display_height:
                break

            collision_point = self.check_collision(prev_shell_position, shell_position)

            if collision_point:
                animate_explosion(self.game_display, collision_point, self.strike_earth_sound, simple_shell_radius)
                self.correct_ground(collision_point, simple_shell_radius)
                self.apply_players_damages(collision_point, simple_shell_power, simple_shell_radius)
                self.correct_tanks_heights()
                fire = False
            else:
                pygame.draw.circle(self.game_display, color, (shell_position[0], shell_position[1]), 4)

            pygame.display.update()
            self.clock.tick(60)
        return shell_position[0], shell_position[1]

    def update_players(self):
        """
        Updates each player information
        :return: none
        """
        left_players = []
        for player in self.players:
            if player.is_in_game():
                left_players.append(player)

        if self.active_player in left_players:
            self.active_player = left_players[(left_players.index(self.active_player) + 1) % len(left_players)]
        else:
            if len(left_players) > 0:
                init_index = self.players.index(self.active_player)
                while True:
                    self.active_player = self.players[(init_index + 1) % len(self.players)]
                    if self.active_player in left_players:
                        break

        self.players = left_players

    def draw_all(self):
        """
        Draws all elements on display
        :return: none
        """
        self.game_display.fill(black)
        self.ground.draw()
        for player in self.players:
            player.draw_tanks_and_bars()

        self.active_tank.show_tanks_angle()
        self.active_tank.show_tanks_power()

    def generate_tank_list(self):
        """
        Generate a list of active tanks for the bots.
        :return: list of dictionaries of tanks
        """
        tank_list = []
        for player in self.players:
            tanks = player.active_tanks
            if not tanks:
                continue
            new_dict = {}
            new_dict["name"] = player.bot_object.get_name()
            new_dict["position"] = (tanks[0].position[0],game_core.constants.display_height - tanks[0].position[1])
            new_dict["health"] = tanks[0].tank_health
            tank_list.append(new_dict)

        return tank_list
    def run(self):
        """
        Run game
        :return: none
        """
        self.reinitialize_players()
        self.active_tank = self.players[0].next_active_tank()
        game_exit = False
        game_over = False
        fps = 15

        angle_change = 0
        power_change = 0

        while not game_exit:
            if game_over:
                message_to_screen(self.game_display, "Game over", red, -50, FontSize.LARGE, sys_font=False)
                message_to_screen(self.game_display, "S - play again", green, 50, sys_font=False)
                message_to_screen(self.game_display, "Q - quit", green, 80, sys_font=False)
                pygame.display.update()
                while game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_exit = True
                                game_over = False
                            if event.key == pygame.K_s:
                                self.reinitialize_players()
                                self.active_tank = self.players[0].next_active_tank()
                                game_exit = False
                                game_over = False
                                break
                        elif event.type == pygame.QUIT:
                            game_exit = True
                            game_over = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Play turn
                        # Get power and angle from the bot object

                        angle, power = self.active_player.get_angle_and_power_from_bot(self.generate_tank_list())
                        if angle and power:
                            # Animate the change of angle
                            rad_angle = radians(angle)
                            current_angle = self.active_tank.get_current_angle()
                            angle_delta = angle_step if current_angle < rad_angle else -angle_step # In which direction should we move the angle
                            num_of_changes = int((current_angle - rad_angle) / angle_step)
                            for i in range(abs(num_of_changes)):
                                self.active_tank.update_turret_angle(angle_delta)
                                pygame.time.wait(100)
                                self.draw_all()
                                pygame.display.update()

                            # Animate the change of power
                            current_power = self.active_tank.get_current_power()
                            power_delta = 1 if current_power < power else -1
                            power_changes = abs(current_power - power)
                            for i in range(power_changes):
                                self.active_tank.update_tank_power(power_delta)
                                pygame.time.wait(20)
                                self.draw_all()
                                pygame.display.update()
                            pygame.time.wait(1000) # Wait before shooting
                            print(f"Team {self.active_player.name} attacked with angle={angle}, power={power}")
                            shell_position = self.fire_simple_shell(self.active_tank)
                            self.update_players()
                            # Update bot with their hit position
                            self.active_player.update_last_hit_position((shell_position[0], display_height-shell_position[1]))
                        self.active_tank = self.active_player.next_active_tank()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        angle_change = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        power_change = 0

            self.draw_all()

            if len(self.players) <= 1:
                game_over = True

            if self.active_tank:
                self.active_tank.show_tank_special()

            pygame.display.update()
            self.clock.tick(fps)
