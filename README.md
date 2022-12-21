# Project 2 - Fundamentos de Programação 2022/23 
# Comets

Project 2 by Daniela Gameiro nº 21901681 and Nelson Milheiro nº 21904365.

[Git repository](https://github.com/Mikapuccino/Comets.git)

##  Project credits
* Daniela Gameiro

  1. Start screen
  2. Wrap function (player wrap)
  3. Asteroids logic
  4. Asteroids split
  5. Asteroid and bullet image
  6. `READ.md` project report

* Nelson Milheiro

  1. ...
   
## Solution architecture

The `Main.py` is where the function `Comets()` are called to start the game.

`Classes.py` ➞ Is responsible for defining the `Comets` class: encompassing the game loop, player inputs, game logic and screens. Also, it has the `Player`, `Asteroid` and `Bullet` classes with the `GameObject` parameter, which has an essential function, the `collision`.

`Functions.py` ➞ Is responsible for loading the sprites (images), the wrap-around logic (player, bullets and asteroids) and the `random_position`/`random_velocity` of the asteroids.

`Leaderboard.txt` ➞ Is responsible for defining the name and points of each player.

## References

* [Asteroids game tutorial](https://realpython.com/asteroids-game-python/#step-2-input-handling) used for consulting and verifying details along the project.
* [Random module](https://docs.python.org/3/library/random.html) used for calculations that required random values in the project, such as `random_position` and `random_velocity` functions.