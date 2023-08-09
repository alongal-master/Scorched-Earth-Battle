from abc import ABC, abstractmethod
import random
import math

class TankBotInterface(ABC):

    def __init__(self, name, preferred_color=""):
        """
        Initialises the bot with a given name and preferred color.
        """
        self._name = str(name)
        self._preferred_color = str(preferred_color)

    def get_name(self):
        """
        Returns the name of the bot.
        """
        return self._name

    def get_preferred_color(self):
        """
        Returns the preferred color string
        """
        return self._preferred_color

    def update_last_hit(self, position):
        """
        Updates the coordinates of last hit (attack) by this bot.
        """
        try:
            self._last_hit = position
        except Exception:
            return

    @abstractmethod
    def attack(self, other_bots):
        """
        This will be implemented in the child objects. This function gets a list of TankBots (dictionaries),
        It should return the selected attack angle (-90 -> 90) and power (0-100).
        Note:
           - If the function raises exception, you will use your turn!
           - If you return values of the wrong type, you will use your turn!
        """
        pass


class RandomAttacker(TankBotInterface):

    def __init__(self, name="Randomer", preferred_color="green"):
        super().__init__(name, preferred_color)

    def attack(self, other_bots):
        """
        This attack will select a random angle, and attack it with 20 power.
        """
        angle = random.randrange(-90, 90)
        power = random.randrange(0, 100)
        return angle, power


class XBot(TankBotInterface):

    def __init__(self, name="XBot", preferred_color="purple"):
        super().__init__(name, preferred_color)

    def attack(self, other_bots):
        """
        This attack will select a random angle, and attack it with 20 power.
        """

        for bot in other_bots:
            if bot['name'] == 'XBot':
                my_position = bot['position']
                break

        bots = [bot for bot in other_bots if bot['name'] != 'XBot']
        min_health = min(bot['health'] for bot in bots)
        for bot in bots:
            if bot['health'] == min_health:
                target_position = bot['position']

        # Positions
        position1 = target_position
        position2 = my_position

        # Calculate differences in coordinates
        dy = position2[1] - position1[1]
        dx = position2[0] - position1[0]

        # Calculate angle in radians
        angle_rad = math.atan2(dy, dx)

        # Convert radians to degrees
        angle_deg = math.degrees(angle_rad)

        if angle_deg < 0:
            angle_deg += 180
            angle = int(angle_deg) - 90
            power = random.randrange(20, 100)
            return angle, 100

        elif angle_deg > 180:
            angle_deg -= 180
            angle = int(angle_deg) - 90
            power = random.randrange(20, 100)
            return angle, 100


class PreciseAttacker(TankBotInterface):
    'screen = 1600 x900'
    def __init__(self, name="LeTank", preferred_color="red"):
        super().__init__(name, preferred_color)

    def attack(self, other_bots):
        """
        This attack will select an  angle, and attack it with 20 power.
        """
        for bot in other_bots:
            if bot['name'] == 'LeTank':
                our_x_position = bot['position'][0]
                our_y_position = bot['position'][1]

                if our_x_position < 800:
                    angle = random.randrange(5, 30)
                    power = random.randrange(10, 80)
                    return angle, power
                else:
                    angle = random.randrange(-30, -5)
                    power = random.randrange(10, 80)
                    return angle, power


class PhoenixDestructor(TankBotInterface):
    def __init__(self, name="PhoenixDestructor", preferred_color="brown"):
        super().__init__(name, preferred_color)

    def attack(self, other_bots):
        """
        This attack will select a random angle, and attack it with 20 power.
        """
        print(other_bots)
        tanks_count = len(other_bots)
        # print(f"There are {tanks_count} in the list")
        target_tank = None
        our_tank = None
        for i in range(tanks_count):
            tank1 = other_bots[i]
            if tank1['name'] != 'PhoenixDestructor':
                target_tank = tank1
                break

        for i in range(tanks_count):
            tank2 = other_bots[i]
            if tank2['name'] == 'PhoenixDestructor':
                our_tank = tank2
                break

        target_x, target_y = target_tank['position']
        our_x, our_y = our_tank['position']
        # print(target_x, target_y)
        # print(our_x, our_y)

        # calculate h and v distances
        dx = (target_x - our_x)
        dy = (target_y - our_y)


        angle_rad = math.atan(dy/dx)
        angle = math.degrees(angle_rad)  # angle in degress

        # distance
        distance = math.sqrt(dx ** 2 + dy ** 2)
        factor = 0.2
        power = distance * factor
        power = min(100, power)
        # print("distance = ", distance, "factor = ", factor)

        # angle = random.randrange(-90, 90)
        # power = random.randrange(0, 100)
        return angle, power
