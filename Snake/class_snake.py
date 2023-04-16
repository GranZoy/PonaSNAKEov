import pygame
from global_names import *


class PythonSnake:
    def __init__(self, head_rect, body_len, direction, color, speed, speedup):
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
        return len(self.body)

    def Head(self):
        return self.body[self.Len() - 1]

    def Draw(self, screen):
        for i in range(self.Len()):
            pygame.draw.rect(screen, self.color, self.body[i])
        screen.blit(pygame.transform.scale(pygame.image.load('game/eye.png'), [block_size - 1, block_size - 1]),
                    self.Head())

    def Move(self):
        if not self.direction == [0, 0]:
            self.body.append(self.Head().move(self.direction))
            self.prev_last = self.body.pop(0)

    def Growing(self):
        self.body.insert(0, self.prev_last)
        self.speed += self.speedup

    def CrashedBySnake(self, snake):
        not_crashed = True
        for i in range(len(snake)):
            not_crashed *= 1 - (self.Head() in snake[i].body[:snake[i].Len() - 2:])
        return not not_crashed

    def CrashedByEdge(self):
        return not self.Head() in pygame.Rect(block_size, block_size, width - 2 * block_size, high - 2 * block_size)
