import pygame
from global_names import width, high
from class_program import Program

'''Инициализация библиотеки pygame и запуск программы'''
pygame.init()
screen = pygame.display.set_mode((width, high))
program = Program(screen)
program.Start()
pygame.quit()
