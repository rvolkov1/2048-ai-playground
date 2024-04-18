import random
import math

def random_player(state):
  return math.floor(random.random() * 4)

def expectimax_player(state):
  print(state)
  return 0