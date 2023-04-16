import pygame
from global_names import *


def DeleteUnusedSnakes(snake):
    for i in range(len(snake)):
        if not snake[i].body[0] in pygame.Rect(-2 * snake[-1].Len() * block_size,
                                               -2 * snake[-1].Len() * block_size,
                                               width + 4 * snake[-1].Len() * block_size,
                                               high + 4 * snake[-1].Len() * block_size):
            snake.pop(i)
            break
