import pygame
import random
from global_names import *
from class_snake import PythonSnake
from class_bonus import Bonus
from rects_functions import PointInRect, OppositeRect
from draw_landscape import DrawLandscape
from delete_snakes import DeleteUnusedSnakes


class Program:
    def __init__(self, screen):
        self.screen = screen
        self.program_end = False
        self.game_over = None
        self.walls_are_active = True
        self.cheat_is_active = False
        self.achievement_unlocked = False
        self.user_location = 'menu'
        self.current_level = 0
        self.current_color = green
        self.current_landscape = [pink, red, black]
        self.current_food = 'pie'
        self.results = []
        for i in range(levels_cnt):
            self.results.append([])

        self.level_walls = [False, False, True, True, True]
        self.level_speed = [10, 18, 10, 12, 15, 18]
        self.level_speedup = [0.1, 0.2, 0.1, 0.15, 0.2, 0.3]
        self.level_ice_chance = [0.05, 0.03, 0.1, 0.08, 0.07, 0.06]

    def Start(self):
        fon_pic = pygame.transform.scale(pygame.image.load('start/walking.jpeg'), [width, high])
        pygame.display.update()
        fon_music = pygame.mixer.Sound('start/menu_fon.mp3').play(-1)

        while not self.program_end:
            self.screen.blit(fon_pic, [0, 0])
            if self.user_location != 'menu':
                if self.user_location == 'Play':
                    self.walls_are_active = True
                    fon_music.pause()
                    level_music = pygame.mixer.Sound('game/level' + str(self.current_level + 1) + '.mp3').play(-1)
                    self.Play()
                    level_music.stop()
                    if not self.program_end:
                        self.EndGame()
                elif self.user_location == 'level':
                    self.ChooseLevel()
                elif self.user_location == 'land':
                    self.ChooseLandscape()
                elif self.user_location == 'color':
                    self.ChooseSnakeColor()
                elif self.user_location == 'food':
                    self.ChooseFood()
            else:
                fon_music.unpause()
                self.DrawResults(fon_music)
                self.CheckCheatActivity(fon_music)
                self.ChoosingInMenu()
            pygame.display.update()

    def Play(self):
        screen_centre = pygame.Rect((width - block_size) // 2 + 1, (high - block_size) // 2 - 2 * block_size + 1,
                                    block_size - 1, block_size - 1)
        self.game_over = False
        snake = [PythonSnake(screen_centre, 3, [0, 0], self.current_color, self.level_speed[self.current_level],
                             self.level_speedup[self.current_level])]
        food = Bonus(snake, self.current_food)
        ice = ''

        while not self.game_over:
            self.WorkWithCrashing(snake)
            if self.game_over:
                break

            DrawLandscape(self.screen, self.current_landscape, False)
            for i in range(len(snake)):
                snake[i].Move()
                snake[i].Draw(self.screen)
            bonus = [food, ice]
            self.WorkWithBonus(snake, bonus)
            food = bonus[0]
            ice = bonus[1]
            DeleteUnusedSnakes(snake)
            DrawLandscape(self.screen, self.current_landscape, True)

            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(snake[-1].speed)
        self.results[self.current_level].append(snake[-1].Len() - 3)

    def EndGame(self):
        death = pygame.mixer.Sound('end/gta.mp3').play()
        self.game_over = True
        death_im = pygame.transform.scale(pygame.image.load('end/death_want_2.jpg'), [width, high])
        self.screen.blit(death_im, [(width - death_im.get_size()[0]) // 2, (high - death_im.get_size()[1]) // 2])
        pygame.display.update()
        self.user_location = 'menu'
        pygame.time.delay(3000)
        death.stop()

    def ChoosingInMenu(self):
        font = pygame.font.Font(None, block_size * 16 // 10)
        choose_rect = []
        choose_text = ['level', 'land', 'color', 'food', 'Play', 'menu']
        for i in range(4):
            choose_rect.append(pygame.Rect(block_size, high // 2 - 4 * block_size + i * 2 * block_size,
                                           3 * block_size, block_size))

        choose_rect.append(pygame.Rect(width // 2 - block_size, 2 * block_size,
                                       block_size * 5 // 2, block_size * 5 // 4))
        choose_rect.append(-1)

        for i in range(5):
            pygame.draw.rect(self.screen, yellow, choose_rect[i])
            self.screen.blit(font.render(choose_text[i], False, red), choose_rect[i])
        pygame.display.update()
        self.ButtonRectChoose(choose_rect)
        self.user_location = choose_text[choose_rect[5]]

    def ChooseLevel(self):
        font = pygame.font.Font(None, block_size * 16 // 10)
        level_rect = []
        for i in range(levels_cnt):
            level_rect.append(pygame.Rect(block_size, high // 2 - levels_cnt * block_size +
                                          i * 2 * block_size, 4 * block_size, block_size))

        level_rect.append('')
        for i in range(levels_cnt):
            pygame.draw.rect(self.screen, yellow, level_rect[i])
            self.screen.blit(font.render('Level ' + str(i + 1), False, red), level_rect[i])

        self.ButtonRectChoose(level_rect)
        if level_rect[levels_cnt] != '':
            self.current_level = level_rect[levels_cnt]
            self.user_location = 'menu'

    def ChooseLandscape(self):
        up_rect = pygame.Rect(block_size // 2, 2 * block_size, 4 * block_size, 4 * block_size)
        land_rect = []
        different_lands = [[pink, red, black], [yellow, orange, black], [light_blue, blue, black]]
        land_name = ['pink', 'yellow', 'light_blue']
        for i in range(len(land_name)):
            land_rect.append(up_rect.move(0, 5 * i * block_size))
            self.screen.blit(pygame.transform.scale(pygame.image.load('start/' + land_name[i] + '_land.jpg'),
                             up_rect[2::]), land_rect[i])
        land_rect.append(-1)
        self.ButtonRectChoose(land_rect)
        if land_rect[len(land_name)] != -1:
            self.current_landscape = different_lands[land_rect[len(land_name)]]
            self.user_location = 'menu'

    def ChooseSnakeColor(self):
        up_rect = pygame.Rect(width - block_size * 3 // 2, 2 * block_size, block_size, block_size)
        color_rect = []
        color_name = [green, white, black, gray, blue, red, orange]
        for i in range(len(color_name)):
            color_rect.append(up_rect.move(0, 2 * i * block_size))
            pygame.draw.rect(self.screen, color_name[i], color_rect[i])
        color_rect.append(-1)
        self.ButtonRectChoose(color_rect)
        if color_rect[len(color_name)] != -1:
            self.current_color = color_name[color_rect[len(color_name)]]
            self.user_location = 'menu'

    def ChooseFood(self):
        up_rect = pygame.Rect(block_size // 2, 2 * block_size, 4 * block_size, 4 * block_size)
        food_rect = []
        food_name = ['pie', 'apple', 'peach']
        for i in range(len(food_name)):
            food_rect.append(up_rect.move(0, 5 * i * block_size))
            self.screen.blit(pygame.transform.scale(pygame.image.load('game/' + food_name[i] + '.png'),
                             up_rect[2::]), food_rect[i])
        food_rect.append(-1)
        self.ButtonRectChoose(food_rect)
        if food_rect[len(food_name)] != -1:
            self.current_food = food_name[food_rect[len(food_name)]]
            self.user_location = 'menu'

    def DrawResults(self, fon_music):
        font = pygame.font.Font(None, block_size * 16 // 10)
        max_res = []
        eight_symphony = []
        results_rect = []
        for i in range(levels_cnt):
            max_res.append('')
            eight_symphony.append(8)
            results_rect.append(pygame.Rect(width - 6 * block_size, high // 2 - levels_cnt * block_size +
                                            i * block_size, block_size * 6 - block_size // 5, block_size))
            pygame.draw.rect(self.screen, yellow, results_rect[i])
            if len(self.results[i]) > 0:
                max_res[i] = max(self.results[i])
            self.screen.blit(font.render('Level ' + str(i + 1) + ': ' + str(max_res[i]), False, red), results_rect[i])
        if max_res == eight_symphony and not self.achievement_unlocked:
            fon_music.pause()
            self.achievement_unlocked = True
            self.screen.blit(pygame.transform.scale(pygame.image.load('start/eight_symphony.png'), [width, high]),
                             [0, 0])
            achieve = pygame.mixer.Sound('start/eight_symphony.mp3').play()
            pygame.display.update()
            pygame.time.delay(15000)
            achieve.stop()
            fon_music.unpause()

    def GiveDirectByKey(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program_end = True
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    break
                if event.key == pygame.K_RIGHT and not snake.direction == [-block_size, 0]:
                    snake.direction = [block_size, 0]
                    break
                if event.key == pygame.K_LEFT and not snake.direction == [block_size, 0]:
                    snake.direction = [-block_size, 0]
                    break
                if event.key == pygame.K_UP and not snake.direction == [0, block_size]:
                    snake.direction = [0, -block_size]
                    break
                if event.key == pygame.K_DOWN and not snake.direction == [0, -block_size]:
                    if not snake.direction == [0, 0]:
                        snake.direction = [0, block_size]
                        break
                if self.cheat_is_active:
                    keys = pygame.key.get_pressed()
                    if event.key == pygame.K_g:
                        snake.Growing()
                        break
                    if keys[pygame.K_s] and keys[pygame.K_d] and snake.speed > 1:
                        snake.speed -= 1
                        break
                    if keys[pygame.K_w] and keys[pygame.K_u]:
                        self.walls_are_active = False
                        break
                    if keys[pygame.K_w] and keys[pygame.K_a]:
                        self.walls_are_active = True
                        break

    def ButtonRectChoose(self, button_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program_end = True
                self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(button_rect) - 1):
                        if PointInRect(event.pos, button_rect[i]):
                            button_rect[len(button_rect) - 1] = i

    def WorkWithBonus(self, snake, bonus):
        if snake[-1].Head() == bonus[0].rect:
            snake[-1].Growing()
            bonus[0] = Bonus(snake, self.current_food)
            if random.uniform(0, 1) <= self.level_ice_chance[self.current_level] and bonus[1] == '':
                bonus[1] = Bonus(snake, 'ice')

        if bonus[1] != '' and snake[-1].Head() == bonus[1].rect:
            bonus[1] = ''
            for i in range(len(snake)):
                snake[i].speed -= 1
        if bonus[1] != '':
            bonus[1].Draw(self.screen)
        bonus[0].Draw(self.screen)

    def WorkWithCrashing(self, snake):
        if snake[-1].CrashedBySnake(snake):
            self.game_over = True
        if snake[-1].CrashedByEdge() and not (self.walls_are_active * self.level_walls[self.current_level]):
            snake.append(PythonSnake(OppositeRect(snake[-1].Head()).move(snake[-1].direction), snake[-1].Len(),
                                     snake[-1].direction, self.current_color, snake[-1].speed,
                                     self.level_speedup[self.current_level]))
        elif snake[-1].CrashedByEdge():
            self.game_over = True
        else:
            self.GiveDirectByKey(snake[-1])

    def CheckCheatActivity(self, fon_music):
        keys = pygame.key.get_pressed()
        if not self.cheat_is_active and keys[pygame.K_c] and keys[pygame.K_h] and keys[pygame.K_e] and keys[pygame.K_a]\
                and keys[pygame.K_t]:
            self.cheat_is_active = True
            fon_music.pause()
            cheat_music = pygame.mixer.Sound('start/cheat_activated.mp3').play()
            pygame.time.delay(5000)
            cheat_music.stop()
