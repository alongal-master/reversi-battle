import grid
import bots
import game

def main():
    # Instantiate some SpaceBots (use your own SpaceBot class here)
    bot1 = bots.GreedyPlayer()
    bot2 = bots.GreedyPlayer("Greedy2")
    # bot3 = bots.SmartRandom("The Randoms3", "blue")
    # bot4 = bots.SmartRandom("The Randoms4", "blue")



    new_game = game.ReversiGame()
    new_game.add_team(bot1)
    new_game.add_team(bot2)
    new_game.start()


if __name__ == "__main__":
    main()

