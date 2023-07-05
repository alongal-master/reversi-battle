import random
import grid

class ReversiGame():

    _board_size = 8
    _empty_box_value = None

    def __init__(self):
        self._teams = {}  # Team (k) and instance (v)
        self._free_colors = ['red', 'green', 'blue', 'purple', 'yellow', 'orange', 'cyan', 'magenta']
        self._current_grid = [[self._empty_box_value] * self._board_size for _ in range(self._board_size)]

    def start(self):
        """"
        Prepare things for the game and then starts the UI.
        """
        self._interface = grid.GridUI(self, self._current_grid, self._board_size, self._teams)
        # Run the long-running function in a separate thread
        # Create a randomized list of the teams for turn order for 200 rounds
        self._game_order = list(self._teams.values())
        random.shuffle(self._game_order)
        self._interface.log_line("Game Started!")
        # Battle until one team remains
        self._round = 1
        self._interface._root.mainloop()

    def add_team(self, team_obj):
        """"
        Adds a new team to our dictionary. Checks if their preferred color is valid and not taken,
        if not - picks a different one.
        """
        preferred_color = team_obj.get_preferred_color()
        # Color is valid and not taken
        if preferred_color not in self._teams.keys() and grid.GridUI.is_valid_color(preferred_color):
            self._teams[preferred_color] = team_obj
        # Color already taken or invalid :(
        else:
            self._teams[self._free_colors.pop()] = team_obj

    def check_move(self, attacker, attack_axis):
        """"
        Gets team and row,col of an attack, Checks that they are valid and returns True.
        If not, returns False.
        """
        # Try to unpack and convert to ints x and y
        try:
            row, col = attack_axis
            row = int(row)
            col = int(col)
        except Exception:
            self._interface.log_line(f"ERROR! Attacker {attacker.get_name()} returned wrong type for row and/or col ({e})")
            return False

        # Checks that target box is free
        if not self._current_grid[row][col] == None:
            self._interface.log_line(f"ERROR! Attacker {attacker.get_name()} tried to attack an occupied box at {row},{col}!")
            return False

        return True

    def team_current_score(self, team):
        """"
        Counts the amount of position conquered by a team object.
        This function counts blanks also, when given the value of None.
        """
        count = 0
        for i in range(self._board_size):
            for j in range(self._board_size):
                if team and self._current_grid[i][j] == team.get_name():
                    count += 1
                if team == None and self._current_grid[i][j] == None:
                    count += 1
        return count

    def check_direction(self, attacking_team_name, positioned_row, positioned_col, increment_row, increment_col):
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
            if row < 0 or row >= self._board_size or col < 0 or col >= self._board_size:
                return []
            current_box = self._current_grid[row][col]
            if not current_box:
                return []
            if current_box == attacking_team_name:
                return to_be_flipped
            to_be_flipped.append((row, col))

    def update_grid_if_succesful_attacks(self, attacking_team_name, row, col):
        """"
        Call this function after a turn was made.
        This checks all directions from the new conquered box, and checks if
        there is a successful flip to be made.
        Then, flips all those boxes to the attacking team.
        """
        # Checks eight directions, and concat all boxes to be flipped to one list of tuples
        to_be_flipped = self.check_direction(attacking_team_name, row, col, 0, 1) + \
                        self.check_direction(attacking_team_name, row, col, 0, -1) + \
                        self.check_direction(attacking_team_name, row, col, 1, 0) + \
                        self.check_direction(attacking_team_name, row, col, -1, 0) + \
                        self.check_direction(attacking_team_name, row, col, 1, 1) + \
                        self.check_direction(attacking_team_name, row, col, 1, -1) + \
                        self.check_direction(attacking_team_name, row, col, -1, 1) + \
                        self.check_direction(attacking_team_name, row, col, -1, -1)
        # Flip all the boxes to the attacking team
        if to_be_flipped:
            self._interface.log_line(f"Wow! {attacking_team_name} has flipped {len(to_be_flipped)} boxes!")
            for row, col in to_be_flipped:
                self._current_grid[row][col] = attacking_team_name

    def perform_move(self, team):
        """"
        Performs a single move of the given team
        """
        try:
            target = team.play_turn(self._current_grid)
        except Exception as e:
            # If attacker function raised an error
            self._interface.log_line(f"ERROR! Attacker {team.get_name()} function crashed ({e})")
            attack_is_legal = False
        else:
            # If didn't crash, check that attack is legal
            attack_is_legal = self.check_move(team, target)

        # Perform the attack.
        if attack_is_legal:
            self._interface.log_line(f"{team.get_name()} played at row={target[0]} col={target[1]}")
            row, col = target
            self._current_grid[row][col] = team.get_name()
            # Update GUI based on player move
            self._interface.update_grid(self._current_grid)
            # Update grid based on new flips
            self.update_grid_if_succesful_attacks(team.get_name(), row, col)
            # Update GUI again
            self._interface.update_gui()
            self._interface._root.after(2000, lambda: self._interface.update_grid(self._current_grid))

        else:
            self._interface.log_line(f"Skipping {team.get_name()}..")

    def game_is_over(self, round):
        """"
        Checks is game is over (when the board is full), returns True or False.
        """
        blank_counts = self.team_current_score(None)
        if not blank_counts:
            self._interface.log_line("Board is full! Game over!")
            return True

        return False

    def the_winners(self):
        """"
        Returns a list of the winner(s) of the game (by number of conquered boxes).
        If few have the same number, they all win!
        """
        teams_and_scores = {}
        for team in self._teams.values():
            teams_and_scores[team] = self.team_current_score(team)
        winner_score = max(teams_and_scores.values())
        winner_teams = [team for team in self._teams.values() if self.team_current_score(team) == winner_score]
        return winner_teams

    def play_one_turn(self):
        """"
        Plays the next team in the game order queue.
        """
        # Determine who's turn is it based on the round number
        attacker = self._game_order[(self._round - 1) % len(self._game_order)]
        # Play move
        if not self.game_is_over(self._round):
            self.perform_move(attacker)
            self._round += 1
        # Game is over!
        else:
            self._interface.log_line("Game is over!")
            # Announce the winner
            winners = self.the_winners()
            if len(winners) == 1:
                self._interface.log_line(f"The winner is {winners[0].get_name()}!")
            else:
                for i, team in enumerate(winners, 1):
                    self._interface.log_line(f"Winner #{i} is {team.get_name()}!")

        #self._interface._root.after(1100, self.play_one_turn)

    def start_game(self):
        """"
        Plays all rounds of the game, until it ends
        """
