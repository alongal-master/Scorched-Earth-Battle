from abc import ABC, abstractmethod
import random


class TankBotInterface(ABC):

    def __init__(self, name, preferred_color=""):
        """"
        Initialises the bot with a given name and preferred color.
        """
        self._name = str(name)
        self._preferred_color = str(preferred_color)

    def get_name(self):
        """"
        Returns the name of the bot.
        """
        return self._name

    def get_preferred_color(self):
        """"
        Returns the preferred color string
        """
        return self._preferred_color

    def update_last_hit(self, position):
        """"
        Updates the coordinates of last hit (attack) by this bot.
        """
        try:
            self._last_hit = position
        except Exception:
            return

    @abstractmethod
    def attack(self, other_bots):
        """"
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
        """"
        This attack will select a random angle, and attack it with 20 power.
        """
        angle = random.randrange(-90, 90)
        power = random.randrange(0, 100)
        return angle, power

