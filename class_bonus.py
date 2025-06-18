import pygame
from global_names import *
from rects_functions import RandomRect


class Bonus:
    def __init__(self, snake, bonus_type):
        """
        Создание бонуса

        :param snake: list(PythonSnake) - змейка и ее куски
        :param bonus_type: str - строка типа бонуса (pie, apple, peach, ice)
        """
        self.rect = RandomRect()
        not_in_snake = True
        for i in range(len(snake)):
            not_in_snake *= 1 - (self.rect in snake[i].body)
        while not not_in_snake:
            self.rect = RandomRect()
            not_in_snake = True
            for i in range(len(snake)):
                not_in_snake *= 1 - (self.rect in snake[i].body)

        old_image = pygame.image.load('game/' + bonus_type + '.png')
        self.image = pygame.transform.scale(old_image, [block_size - 1, block_size - 1])
        self.image.set_colorkey(white)

    def Draw(self, screen):
        """
        Рисует бонус

        :param screen: экран для отрисовки
        """
        screen.blit(self.image, self.rect)
