import bots
import game

def main():
    # Instantiate some SpaceBots (use your own SpaceBot class here)
    bot1 = bots.SmartRandomPlayer()
    bot2 = bots.RandomPlayer()

    # Create the game instance and add the teams
    new_game = game.ReversiGame()
    new_game.add_team(bot1)
    new_game.add_team(bot2)

    # Start the game (mainloop of UI starts)
    new_game.start()


if __name__ == "__main__":
    main()

