import pygame
import sys
import random
import math

random.seed(0)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

PADDING = 20

BOARD_SIZE = 4
BLOCK_SIZE = (CANVAS_WIDTH - PADDING * 5) / BOARD_SIZE

pygame.init()
WINDOW = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("sandbox")
font = pygame.font.SysFont("Arial", int(BLOCK_SIZE))
clock = pygame.time.Clock()

class Game():
  def __init__(self):
     self.board = [[0,0,2,2],[0,4,0,0],[0,0,0,0],[0,0,0,0]]

     self.colors = {
       "background": "#776E65",
       "empty_tile": "#CDC1B4",
       2: "#EEE4DA",
       4: "#EDE0C8",
       8: "#F2B179",
       16: "#F59563",
       32: "#F67C5F",
       64: "#F65E3B",
       128: "#EDCF72",
       256: "#EDCC61",
       512: "#EDC850",
       1024: "#EDC53F",
       2048: "#EDC22E",
       "greater": "black"
     }

  def update(self, key_pressed):
    if key_pressed == None:
      return

    dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))

    drow, dcol = dirs[key_pressed]

    start_row = 0 if drow < 0 else BOARD_SIZE-1
    end_row = -1 if start_row == BOARD_SIZE - 1 else BOARD_SIZE
    drow = 1 if start_row == 0 else -1

    start_col = 0 if dcol < 0 else BOARD_SIZE-1
    end_col = -1 if start_col == BOARD_SIZE - 1 else BOARD_SIZE
    dcol = 1 if start_col == 0 else -1

    dy, dx= dirs[key_pressed]

    for dim1 in range(start_row, end_row, drow):
      for dim2 in range(start_col, end_col, dcol):
        if self.board[dim1][dim2] == 0:
          continue

        idx1 = dim1
        idx2 = dim2
        joined = False

        while (idx1+ dy>= 0 and idx1 + dy < BOARD_SIZE and idx2 + dx >= 0 and idx2 + dx < BOARD_SIZE):
          if self.board[idx1 + dy][idx2 + dx] == 0:
            self.board[idx1+dy][idx2+dx] = self.board[idx1][idx2]
            self.board[idx1][idx2] = 0
          elif (self.board[idx1+dy][idx2+dx] == self.board[idx1][idx2] and not joined):
            self.board[idx1+dy][idx2+dx] *= 2
            self.board[idx1][idx2] = 0
            joined = True

          idx1 += dy
          idx2 += dx
      
    # create new random tile
    open_indices = []

    for row, arr in enumerate(self.board):
      for col, val in enumerate(arr):
        if (val == 0):
          open_indices.append((row, col))
    
    idx = math.floor(random.random() * len(open_indices))
    val = 2 if random.random() > 0.1 else 4

    self.board[open_indices[idx][0]][open_indices[idx][1]] = val


class UserInput():
  def __init__(self):
    pass

  def get_key():
    key = None

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      
      if pygame.key.get_pressed()[pygame.K_LEFT]:
        key = 0
      elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        key = 1
      elif pygame.key.get_pressed()[pygame.K_UP]:
        key = 2
      elif pygame.key.get_pressed()[pygame.K_DOWN]:
        key = 3
      
    return key

def game_loop():

  game = Game()
  player_input = UserInput()

  def render():
    WINDOW.fill(game.colors["background"])

    for row, array in enumerate(game.board):
      offset_y = (PADDING * (row+1)) + BLOCK_SIZE * row

      for column, tile in enumerate(array):
        offset_x = (PADDING * (column+1)) + BLOCK_SIZE * column

        if (game.board[row][column] == 0):
          color = game.colors["empty_tile"]
        elif (game.board[row][column] > 2048):
          color = game.colors["greater"]
        else:
          color = game.colors[game.board[row][column]]
        
        rect = pygame.Rect(offset_x, offset_y, BLOCK_SIZE, BLOCK_SIZE)
        WINDOW.fill(color, rect=rect)

        if game.board[row][column] > 0:
          text = font.render(str(game.board[row][column]), False, "black")
          WINDOW.blit(text, (offset_x, offset_y))

    pygame.display.flip()

    
  while True:
    # run at max fps
    clock.tick(1000)

    if True:
      key = UserInput.get_key()

    game.update(key)
    render()

game_loop()

