import pygame
from global_names import *


def DrawLandscape(screen, colors, land_is_transparent):
    """
    Отрисовываем ландшафт

    :param screen: Экран для отрисовки
    :param colors: list((int, int, int)) = [land_color, edge_color, line_color] - список с цветами,
                   в которые нужно покрасить соответственно поле, края и разделяющии линии
    :param land_is_transparent: bool - Нужно ли рисовать поле прозрачным
    """
    if not land_is_transparent:
        screen.fill(colors[0])
    edge = [pygame.Rect(0, 0, block_size, high), pygame.Rect(0, 0, width, block_size),
            pygame.Rect(0, high - block_size, width, block_size), pygame.Rect(width - block_size, 0, block_size, high)]
    for i in range(4):
        pygame.draw.rect(screen, colors[1], edge[i])

    for i in range(width // block_size):
        pygame.draw.line(screen, colors[2],
                         [(i + 1) * block_size, block_size], [(i + 1) * block_size, high - block_size])
    for i in range(high // block_size):
        pygame.draw.line(screen, colors[2],
                         [block_size, (i + 1) * block_size], [width - block_size, (i + 1) * block_size])
