from abc import ABC, abstractmethod
import random

class ReversiBotInterface(ABC):

    def __init__(self, name, preferred_color=""):
        """"
        Initialises the bot with name and preferred color
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

    @abstractmethod
    def play_turn(self, grid):
        """"
        This will be implemented in the child objects. This function gets one param:
        grid (List of lists) -
        The grid of the game, a 2-dimensional list that represents the game board
        (The size is 8x8, so indexes are between 0 and 7).
        Every item in the list represents a single row.
        Every item in the nested lists represents a single box.
        If the box is empty, the value will be None.
        if a team has conquered the box, the value will be a string with the team's name.

        The function should return the desired move by the team in two values - row and col
        (the coordinates of the box to conquer). The values can be packed in a tuple or a list.

        Note:
           - If the function raises exception, you will use your turn!
           - If you try to move to a box that's already conquered, you will use your turn!
           - If you try to move to illegal box, you will use your turn!
        """
        pass


class RandomPlayer(ReversiBotInterface):
    """"
    This bot will select a random box target, and try to conquer it.
    """
    def __init__(self, name="SimpleRandom", preferred_color="orange"):
        super().__init__(name, preferred_color)

    def play_turn(self, grid):
        n = len(grid)
        row, col = random.randrange(n), random.randrange(n)
        return row, col

class SmartRandomPlayer(ReversiBotInterface):
    """"
    This bot will select a random box target, and try to conquer it.
    If it's occupied, it picks a different one.
    """
    def __init__(self, name="SmarterRandom", preferred_color="magenta"):
        super().__init__(name, preferred_color)

    def play_turn(self, grid):
        n = len(grid)
        row, col = random.randrange(n), random.randrange(n)
        while grid[row][col]:
            row, col = random.randrange(n), random.randrange(n)
        return row, col


# To write your own bot, duplicate one of the above classes, and then:
# 1. Change the name and preferred color in the __init__ keyword params
# 2. Change the implementation of play_turn method
