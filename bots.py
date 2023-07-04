from abc import ABC, abstractmethod
import random

class ReversiBotInterface(ABC):

    def __init__(self, name, preferred_color=""):
        """"
        Initialises the bot with the initial health and ammo, and the given name.
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
    def play_turn(self, grid, list_of_alive_teams):
        """"
        This will be implemented in the child objects. This function gets 2 params:
        1. grid (List of lists) -
        the grid of the game, a 2-deminsional list that represents the game board
        (The size is 10x10, so indexes are between 0 and 9).
        Every item in the nested lists represents a box in the grid.
        If the box is empty, the item will be None. if a team has conquered the box,
        it will be a string with the team's name.

        2. list_of_alive_teams (List of strings):
        A list of strings with all the names of teams that are currently still in the game.

        It should return the desired move by the team in two values - row and col (the cordinates
        of the box to conquer). The values can be packed in a tuple or a list.

        Note:
           - If the function raises exception, you will use your turn!
           - If you try to move to a box that's already conquered, you will use your turn!
           - If you try to move to illegal box, you will use your turn!
        """
        pass


class RandomPlayer(ReversiBotInterface):
    """"
    This bot will select a random box target, and try to conquer it.
    If it's occupied, it picks a different one.
    """
    def __init__(self, name="SmartRandom", preferred_color="orange"):
        super().__init__(name, preferred_color)

    def play_turn(self, grid):
        n = len(grid)
        row, col = random.randrange(n), random.randrange(n)
        while grid[row][col]:
            row, col = random.randrange(n), random.randrange(n)
        return row, col


class GreedyPlayer(ReversiBotInterface):
    """"
    Smart player that calculates the count of flipping
    for each free box in the grid, and selects the max.
    If all is zero, it selects a random box.
    """
    def __init__(self, name="GreedyPlayer", preferred_color="brown"):
        super().__init__(name, preferred_color)

    def play_turn(self, grid):
        """"
        This bot will select a random box target, and try to conquer it.
        If it's occupied, it picks a different one.
        """
        n = len(grid)
        maxlen = -1
        chosen_row = chosen_col = -1
        for row in range(n):
            for col in range(n):
                if grid[row][col]:
                    continue
                to_be_flipped = self.check_direction(n, grid, self._name, row, col, 0, 1) + \
                                self.check_direction(n, grid, self._name, row, col, 0, -1) + \
                                self.check_direction(n, grid, self._name, row, col, 1, 0) + \
                                self.check_direction(n, grid, self._name, row, col, -1, 0) + \
                                self.check_direction(n, grid, self._name, row, col, 1, 1) + \
                                self.check_direction(n, grid, self._name, row, col, 1, -1) + \
                                self.check_direction(n, grid, self._name, row, col, -1, 1) + \
                                self.check_direction(n, grid, self._name, row, col, -1, -1)
                if len(to_be_flipped) > maxlen:
                    maxlen = len(to_be_flipped)
                    chosen_row = row
                    chosen_col = col
        if maxlen == 0:
            while True:
                chosen_row = random.randrange(n)
                chosen_col = random.randrange(n)
                if not grid[chosen_row][chosen_col]:
                    break
        return chosen_row, chosen_col


    def check_direction(self, board_size, grid, attacking_team_name, positioned_row, positioned_col, increment_row, increment_col):
        """"
        Checks one direction from a certain box (location is positioned_row and positioned_col,
        controlled by  attacking_team_name, to the end of the board.
        Direction is determined by increment_x and increment_y, so you can check all possible directions -
        up, down, left, right and also diagonals.
        Returns list of (row,col) tuples that needs to be flipped.
        """
        # Checks the line in a direction

        row = positioned_row
        col = positioned_col
        to_be_flipped = []
        while True:
            row += increment_row
            col += increment_col
            if row < 0 or row >= board_size or col < 0 or col >= board_size:
                return []
            current_box = grid[row][col]
            if not current_box:
                return []
            if current_box == attacking_team_name:
                return to_be_flipped
            to_be_flipped.append((row, col))