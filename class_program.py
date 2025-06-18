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
        """
        Инициализация класса программы

        :param screen: Экран для отрисовки
        """
        self.screen = screen
        # Проверка на завершение программы/игры
        self.program_end = False
        self.game_over = None
        # Текущее положение пользоваетеля в программе
        self.user_location = 'menu'
        # X-параметры
        self.current_level = 0
        self.current_color = green
        self.current_landscape = [pink, red, black]
        self.current_food = 'pie'
        # Результаты по уровням и достижение
        self.achievement_unlocked = False
        self.results = []
        for i in range(levels_cnt):
            self.results.append([])
        # Работа с читами
        self.cheat_is_active = False
        self.walls_are_active = True
        # Зависящие от уровня параметры:
        # активность стен, скорость, ускорение, шанс появление льда
        self.level_walls = [False, False, True, True, True]
        self.level_speed = [10, 18, 10, 12, 15, 18]
        self.level_speedup = [0.1, 0.2, 0.1, 0.15, 0.2, 0.3]
        self.level_ice_chance = [0.05, 0.03, 0.1, 0.08, 0.07, 0.06]

    def Start(self):
        """
        Старт программы

        Ползователь попадает в меню,
        где может начать игру или выбрать
        уровень, цвет, еду, ландшафт (далее x-параметры).

        Показывются лучшие результаты по уровням,
        происходит активация возможности читерства,
        включается музыка для меню
        """
        fon_pic = pygame.transform.scale(pygame.image.load('start/walking.jpeg'), [width, high])
        pygame.display.update()
        fon_music = pygame.mixer.Sound('start/menu_fon.mp3').play(-1)

        while not self.program_end:
            self.screen.blit(fon_pic, [0, 0])
            if self.user_location != 'menu':
                if self.user_location == 'Play':
                    # Пользователь запускает игру с текущими x-параметрами
                    # Включается музыка для соответствующего уровня
                    self.walls_are_active = True
                    fon_music.pause()
                    level_music = pygame.mixer.Sound('game/level' + str(self.current_level + 1) + '.mp3').play(-1)
                    self.Play()
                    level_music.stop()
                    if not self.program_end:
                        self.EndGame()
                # Пользователь меняет какой-то из x-параметров
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
        """
        Старт игры

        Программа рисует змейку длины 3 в центре экрана
        После нажатия одной из клавиш управления
        змейка начинает движение
        """
        screen_centre = pygame.Rect(medium[0] - half_block + 1, medium[1] - 5 * half_block - 1,
                                    block_size - 1, block_size - 1)
        self.game_over = False
        # список кусочков змеи, которые могут появится
        # при проходе сквозь стену
        snake = [PythonSnake(screen_centre, 3, [0, 0], self.current_color, self.level_speed[self.current_level],
                             self.level_speedup[self.current_level])]
        food = Bonus(snake, self.current_food)
        ice = ''

        while not self.game_over:
            # Проверка на смерть змейки
            self.WorkWithCrashing(snake)
            if self.game_over:
                break

            # Отрисовка ландшафта с непрозрачной внутренностью
            # Движение и отрисовка кусков змеи
            DrawLandscape(self.screen, self.current_landscape, False)
            for i in range(len(snake)):
                snake[i].Move()
                snake[i].Draw(self.screen)
            # Отрисовка и создание бонусов (еда и ледяные кубики)
            bonus = [food, ice]
            self.WorkWithBonus(snake, bonus)
            food = bonus[0]
            ice = bonus[1]
            # Удаление кусков змеек, которые вышли за пределы экрана
            DeleteUnusedSnakes(snake)
            # Отрисовка ландшафта с прозрачной внутренностью,
            # чтобы квадраты кусков змеи не было видно на краю поля
            DrawLandscape(self.screen, self.current_landscape, True)

            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(snake[-1].speed)
        # Добавление результата (длина змейки - 3)
        # в список результатов уровня
        self.results[self.current_level].append(snake[-1].Len() - 3)

    def EndGame(self):
        """
        Завершение игры
        Включается музыка и заставка смерти
        Пользователь возвращается в меню
        """
        death = pygame.mixer.Sound('end/gta.mp3').play()
        self.game_over = True
        death_im = pygame.transform.scale(pygame.image.load('end/death_want_2.jpg'), [width, high])
        self.screen.blit(death_im, [medium[0] - death_im.get_size()[0] // 2, medium[1] - death_im.get_size()[1] // 2])
        pygame.display.update()
        self.user_location = 'menu'
        pygame.time.delay(3000)
        death.stop()

    def ChoosingInMenu(self):
        """
        Пользователь выбирает, куда ему переместится:
        игра, выбор уровня, ландшафта, цвета, еды

        Положение записывается в self.user_location
        """
        font = pygame.font.Font(None, block_size * 16 // 10)
        # Создание и отрисовка квадратиков для выбора
        choose_rect = []
        choose_text = ['level', 'land', 'color', 'food', 'Play', 'menu']
        for i in range(4):
            choose_rect.append(pygame.Rect(block_size, medium[1] + (i - 2) * 2 * block_size,
                                           3 * block_size, block_size))

        choose_rect.append(pygame.Rect(medium[0] - block_size, 2 * block_size,
                                       5 * half_block, half_block * 5 // 2))
        choose_rect.append(-1)
        for i in range(5):
            pygame.draw.rect(self.screen, yellow, choose_rect[i])
            self.screen.blit(font.render(choose_text[i], False, red), choose_rect[i])
        pygame.display.update()
        # Если пользователь тыкнул на какой-то из квадратов,
        # то пользователь перемещается в место, соответствующее названию квадрата
        self.ButtonRectChoose(choose_rect)
        self.user_location = choose_text[choose_rect[5]]

    def ChooseLevel(self):
        """
        Выбор уровня

        Записывается в self.current_level
        """
        font = pygame.font.Font(None, block_size * 16 // 10)
        # Создание и отрисовка квадратиков для выбора
        level_rect = []
        for i in range(levels_cnt):
            level_rect.append(pygame.Rect(block_size, medium[1] - levels_cnt * block_size +
                                          i * 2 * block_size, 4 * block_size, block_size))

        level_rect.append('')
        for i in range(levels_cnt):
            pygame.draw.rect(self.screen, yellow, level_rect[i])
            self.screen.blit(font.render('Level ' + str(i + 1), False, red), level_rect[i])
        # Если пользователь тыкнул на какой-то из квадратов,
        # то текущий уровень меняется на тот, что он выбрал
        self.ButtonRectChoose(level_rect)
        if level_rect[levels_cnt] != '':
            self.current_level = level_rect[levels_cnt]
            self.user_location = 'menu'

    def ChooseLandscape(self):
        """
        Выбор ландшафта

        Записывается в self.current_landscape
        """
        up_rect = pygame.Rect(half_block, 2 * block_size, 4 * block_size, 4 * block_size)
        # Создание и отрисовка квадратиков для выбора
        land_rect = []
        different_lands = [[pink, red, black], [yellow, orange, black], [light_blue, blue, black]]
        land_name = ['pink', 'yellow', 'light_blue']
        for i in range(len(land_name)):
            land_rect.append(up_rect.move(0, 5 * i * block_size))
            self.screen.blit(pygame.transform.scale(pygame.image.load('start/' + land_name[i] + '_land.jpg'),
                             up_rect[2::]), land_rect[i])
        land_rect.append(-1)
        # Если пользователь тыкнул на какой-то из квадратов,
        # то текущий ландшафт меняется на тот, что он выбрал
        self.ButtonRectChoose(land_rect)
        if land_rect[len(land_name)] != -1:
            self.current_landscape = different_lands[land_rect[len(land_name)]]
            self.user_location = 'menu'

    def ChooseSnakeColor(self):
        """
        Выбор цвета

        Записывается в self.current_color
        """
        up_rect = pygame.Rect(width - 3 * half_block, 2 * block_size, block_size, block_size)
        # Создание и отрисовка квадратиков для выбора
        color_rect = []
        color_name = [green, white, black, gray, blue, red, orange]
        for i in range(len(color_name)):
            color_rect.append(up_rect.move(0, 2 * i * block_size))
            pygame.draw.rect(self.screen, color_name[i], color_rect[i])
        color_rect.append(-1)
        # Если пользователь тыкнул на какой-то из квадратов,
        # то текущий цвет меняется на тот, что он выбрал
        self.ButtonRectChoose(color_rect)
        if color_rect[len(color_name)] != -1:
            self.current_color = color_name[color_rect[len(color_name)]]
            self.user_location = 'menu'

    def ChooseFood(self):
        """
        Выбор еды

        Записывается в self.current_food
        """
        up_rect = pygame.Rect(half_block, 2 * block_size, 4 * block_size, 4 * block_size)
        # Создание и отрисовка квадратиков для выбора
        food_rect = []
        food_name = ['pie', 'apple', 'peach']
        for i in range(len(food_name)):
            food_rect.append(up_rect.move(0, 5 * i * block_size))
            self.screen.blit(pygame.transform.scale(pygame.image.load('game/' + food_name[i] + '.png'),
                             up_rect[2::]), food_rect[i])
        food_rect.append(-1)
        # Если пользователь тыкнул на какой-то из квадратов,
        # то текущий продукт меняется на тот, что он выбрал
        self.ButtonRectChoose(food_rect)
        if food_rect[len(food_name)] != -1:
            self.current_food = food_name[food_rect[len(food_name)]]
            self.user_location = 'menu'

    def DrawResults(self, fon_music):
        """
        Отрисовка таблички лучших результатов на каждом уровне
        Проверка на достижение 8-ая симфония, если она пройдена, то включается музыка достижения

        :param fon_music: Музыка из меню, которую надо поставить на паузу, при включении музыки достижения
        """
        font = pygame.font.Font(None, block_size * 16 // 10)
        max_res = []
        eight_symphony = []
        results_rect = []
        for i in range(levels_cnt):
            max_res.append('')
            eight_symphony.append(8)
            results_rect.append(pygame.Rect(width - 6 * block_size, medium[1] + (i - levels_cnt) * block_size,
                                            6 * block_size - 5, block_size))
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
        """
        Изменение направления змейки при помощи клавиш
        RIGHT, LEFT, UP, DOWN

        Завершение программы при нажатии на крестик
        Завершение игры при нажатии на ESC

        :param snake: list(PythonSnake) - змейка и ее куски
        """
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
        """
        Проверка нажатия пользователем квадрата из списка buton_rect кроме последнего элемента
        Если квадрат i нажат, то i записывается в конец button_rect

        :param button_rect: list(pygame.Rect()) - лист из квадратов для нажатия пользователем
        """
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
        """
        Проверяет съела ли змейка еду (если съела, то растет) или лед (если съела, то замедляется)
        Создает и рисует эти два бонуса, возвращет их в список bonus

        :param snake: list(PythonSnake) - змейка и ее куски
        :param bonus: list(Bonus) = [food, ice] - лист из бонуса еды и льда
        """
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
        """
        Проверка на смерть змейки
        Если она умерля, то меняем переменную self.game_over
        Иначе пользователь выбирает направление движения для нее

        :param snake: list(PythonSnake) - змейка и ее куски
        """
        # При столкновении с кусками змейки смерть всегда
        if snake[-1].CrashedBySnake(snake):
            self.game_over = True
        # При столкновении со стеной смерть только на уровне больше 2 и активных стенах
        # Если змейка жива при столькновении, то в конец списка змеек добавляется копия
        # текущей змейки, помещенная с другой стороны поля
        if snake[-1].CrashedByEdge() and not (self.walls_are_active * self.level_walls[self.current_level]):
            snake.append(PythonSnake(OppositeRect(snake[-1].Head()).move(snake[-1].direction), snake[-1].Len(),
                                     snake[-1].direction, self.current_color, snake[-1].speed,
                                     self.level_speedup[self.current_level]))
        elif snake[-1].CrashedByEdge():
            self.game_over = True
        else:
            self.GiveDirectByKey(snake[-1])

    def CheckCheatActivity(self, fon_music):
        """
        Проверка на то, что пользователь включил читы
        зажатием C+H+E+A+T

        Включается музыка читерства

        :param fon_music: Музыка из меню, которую надо поставить на паузу, при включении музыки читерства
        """
        keys = pygame.key.get_pressed()
        if not self.cheat_is_active and keys[pygame.K_c] and keys[pygame.K_h] and keys[pygame.K_e] and keys[pygame.K_a]\
                and keys[pygame.K_t]:
            self.cheat_is_active = True
            fon_music.pause()
            cheat_music = pygame.mixer.Sound('start/cheat_activated.mp3').play()
            pygame.time.delay(5000)
            cheat_music.stop()
