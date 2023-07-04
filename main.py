import bots
import game

def main():
    # Instantiate some SpaceBots (use your own SpaceBot class here)
    bot1 = bots.RandomPlayer()
    bot2 = bots.GreedyPlayer()
    bot3 = bots.RandomPlayer(name="Another Random")

    # Create the game instance and add the teams
    new_game = game.ReversiGame()
    new_game.add_team(bot1)
    new_game.add_team(bot2)
    new_game.add_team(bot3)

    # Start the game (mainloop of UI starts)
    new_game.start()


if __name__ == "__main__":
    main()

