import pygame
from global_names import *


class PythonSnake:
    def __init__(self, head_rect, body_len, direction, color, speed, speedup):
        """
        Создание змейки
        :param head_rect: pygame.Rect() - квадрат для головы/начала змейки
        :param body_len: int - длина змейки
        :param direction: list(int) = [x, y] - направление движения змейки
                          (за кадр ее голова перемещается на x вправо и y вниз)
        :param color: (int, int, int) - цвет змейки
        :param speed: int - скорость змейки
        :param speedup: int - ускорение змейки при поедании пищи
        """
        if direction == [0, 0]:
            self.body = [head_rect.move(0, (body_len - i) * block_size) for i in range(body_len)]
        else:
            self.body = [head_rect.move((-body_len + i) * direction[0], (-body_len + i) * direction[1]) for i in
                         range(body_len)]
        self.prev_last = self.body[0]
        self.color = color
        self.direction = direction
        self.speed = speed
        self.speedup = speedup

    def Len(self):
        """
        :return: int - длина змейки
        """
        return len(self.body)

    def Head(self):
        """
        :return: pygame.Rect() - голова или начало змейик
        """
        return self.body[-1]

    def Draw(self, screen):
        """
        Рисует змейку
        При этом на голове змейки находится глаз
        :param screen: Экран для рисования
        """
        for i in range(self.Len()):
            pygame.draw.rect(screen, self.color, self.body[i])
        screen.blit(pygame.transform.scale(pygame.image.load('game/eye.png'), [block_size - 1, block_size - 1]),
                    self.Head())

    def Move(self):
        """
        Змейка движется по ее направлению
        :return:
        """
        if not self.direction == [0, 0]:
            self.body.append(self.Head().move(self.direction))
            self.prev_last = self.body.pop(0)

    def Growing(self):
        """
        Длина змейки растет на 1
        """
        self.body.insert(0, self.prev_last)
        self.speed += self.speedup

    def CrashedBySnake(self, snake):
        """
        :param snake: list(PythonSnake) - змейка и ее куски
        :return: bool - Врезалась ли змейка в себя или свой кусок
        """
        not_crashed = True
        for i in range(len(snake)):
            not_crashed *= 1 - (self.Head() in snake[i].body[:snake[i].Len() - 2:])
        return not not_crashed

    def CrashedByEdge(self):
        """
        :return: bool - Врезалась ли змейка в стену
        """
        return not self.Head() in pygame.Rect(block_size, block_size, width - 2 * block_size, high - 2 * block_size)
