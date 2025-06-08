# Snake Game (dedicated to the internet meme Evgeny Ponasenkov)

This project is available in:
- [Русский] https://github.com/GranZoy/PonaSNAKEov/blob/master/README.ru.md

Hello! I present to you an implementation of the classic Snake game. It includes sound effects, so you may want to turn up your volume :)

## Installation

Before launching the game, you need to install Python 3 and the pygame library on your computer. The latter can be installed with the command:
```
pip install pygame
```

## Launching

You can start the game by running this command in your terminal:
```
python.exe .\main.py
```

To exit the game, click the cross in the top right corner of the window.

## How to Play

### Menu

After launching the game, you'll enter this section.

On the left, you can select the game level, field design, snake color, and food appearance by clicking the buttons:
```
level, landscape, color, food
```

On the right, you'll see your high scores for each level.

In the center, you can start the game by clicking the button:
```
Play
```

### Gameplay

The game features a snake that moves around the screen, eating food to grow longer, and dies if it collides with its own body or walls.

You can only control the snake's movement direction using the arrow keys:
```
RIGHT, LEFT, UP, DOWN
```

On the first two levels, the snake doesn't die when hitting walls but instead appears on the opposite side of the field.

After the snake eats food, it will speed up slightly. There's also a chance that ice will appear on the field - eating it will slow the snake down.

You can end the game and return to the menu by pressing the:
```
ESCAPE
```
key.

### Cheats

The game includes cheat codes that can be activated after simultaneously holding down the letters:
```
C+H+E+A+T
```
on your keyboard (this must be done in the menu).

Then during gameplay, you can hold these combinations:
```
G, S+D, W+U, W+A
```
to respectively: make the snake grow, slow it down, enable wall-passing, or disable wall-passing (the last two combinations don't affect the first two levels).

### Easter Eggs

If your high score on all levels reaches 8, you'll unlock an easter egg.
```
