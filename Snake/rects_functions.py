import pygame
import random
from global_names import *


def RandomRect():
    """
    :return: list(int) = [rand, rand, block_size - 1, block_size - 1] - список для создания случайного квадрата на поле
    """
    return [random.randrange(block_size, width - block_size, block_size) + 1,
            random.randrange(block_size, high - block_size, block_size) + 1,
            block_size - 1, block_size - 1]


def PointInRect(point, rectangle):
    """
    :param point: точка
    :param rectangle: pygame.Rect - прямугольник
    :return: bool - Лежит ли точка внутри прямоугольника
    """
    return rectangle[0] <= point[0] <= rectangle[0] + rectangle[2] and rectangle[1] <= point[1] <= rectangle[1] + \
        rectangle[3]


def OppositeRect(rect):
    """
    :param rect: pygame.Rect - квадрат, лежащий на краю
    :return: pygame.Rect - квадрат, лежащий на противоположной стороне прямоугольника краев, прямо напротив начального
    """
    if rect[0] == 1 or rect[0] == width - block_size + 1:
        return pygame.Rect(width - block_size + 2 - rect[0], rect[1], rect[2], rect[3])
    else:
        return pygame.Rect(rect[0], high - block_size + 2 - rect[1], rect[2], rect[3])
