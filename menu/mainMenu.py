import pygame

import bots.bots
from game_core import constants
from menu.option import GroupedOptions
from game_core.game_manager import GameManager

MUSIC = False

effect_length = 1200
effectTimeTable = (
    (3030, 3030 + effect_length),
    (7230, 7230 + effect_length),
    (11150, 11150 + effect_length),
    (15250, 15250 + effect_length),
    (19250, 19250 + effect_length - 200)
)
effectTimeMin = effectTimeTable[0][0]
effectTimeMax = effectTimeTable[len(effectTimeTable)-1][1]


pygame.init()
displayMenu = GroupedOptions()
mainMenu = GroupedOptions()
settingsMenu = GroupedOptions()
size = constants.display_width, constants.display_height
screen = pygame.display.set_mode(size)

# initialize pictures
light = pygame.image.load('assets/images/circle.png')
light = pygame.transform.scale(light, (300, 300))
bg = pygame.image.load("assets/images/background.jpg")
bg = pygame.transform.scale(bg, size)


def start_game():
    """
    Function under New Game button
    :return: none
    """
    bot1 = bots.bots.RandomAttacker()
    bot2 = bots.bots.RandomAttacker(name="Random 2")
    bot3 = bots.bots.RandomAttacker(name="Random 3")
    GameManager(constants.tanks_number, [bot1, bot2, bot3]).run()
