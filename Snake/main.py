import pygame
from global_names import width, high, block_size
from class_program import Program

pygame.init()
screen = pygame.display.set_mode((width, high))
font = pygame.font.Font(None, block_size * 16 // 10)
clock = pygame.time.Clock()
program = Program(screen)
program.Start()
pygame.quit()
