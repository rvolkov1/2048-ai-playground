import game
import agents

game_instance = game.Game2048(player=agents.random_player)
game_instance.start()
