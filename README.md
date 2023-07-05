
# Reversi Battle Game

Welcome to our Reversi battle! 
In this coding game, each team write it's own bot to play Reversi against other bots. Here are some quick rules of the game, 
and a guide to help you implement your own player.

## Game Rules

Reversi (also known as Othello) is a board game that involves strategy and tactics.

The game is played on an 8x8 uncheckered board. 

Players take turns conquering boxes with their team's color. You can choose any free box on the board.

If you move to a box which is positioned in such a way that it creates a continuous straight line 
(horizontal, vertical, or diagonal) with another box of your own color, 
with one or more of your opponent's discs in between, you can "flip" them.

When this is done, all boxes in between are turned to your color. 
The game ends when the board is full. The team with the most boxes of their color wins the game.

## Implementing a Player

To implement a player, you will need to create a class that extends the `ReversiBotInterface` abstract class from the `bots` module. This class will need to have the following methods implemented:

- `__init__(self, name, preferred_color)`: 
  - This method will be used to initialize your bot. 
  - Here, you can set your bots name and preferred color by calling the super() with those values.

- `play_turn(self, grid)`:  
  - This method will be called when it's your bot's turn to play.

  - The method is passed the current state of the game grid (2D list of rows),
  where the values are either **None** for blank box or **team's name (str)** if it's occupied.
  - The `play_turn` method should return two values (packed in a tuple or a list) 
  indicating the row and column of the box your bot wants to conquer on the grid. 
  - Be careful – if you choose a box that is already conquered or is out of the grid, or raise an exception, 
  your bot will lose its turn.

You can see a simple template for a bot in **bots.py**.

---

That's it! You're ready to start implementing your own bot. Happy coding, and may the best bot win!

---
