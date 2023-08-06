# PyScorchedEarth Bot Version
ScorchedEarth Multiplayer coding game
Written in Python programming language using PyGame library.

Original version created by https://github.com/fdeods

Bot Version was modified by Masterschool.

Game is created for 2-6 players, each side has one tank.
Game continues, until 1 or no players are left.

Controls:
* Space - play next turn

Have fun!

# Bot version
In this version, the tanks are controlled by Bot objects, implemented in code.
The abstract class is TankBotInterface (inside bots/bots.py). To create a bot, inherit from this class
and implement the attack method.

## Requirements
Project is developed in Python 3.5 environments.
File requirements.txt contains all the requirements.
See Installing dependencies below.


### Installing dependencies
Navigate to project root directory and run following line in a shell:
```
pip install -r requirements.txt
```
Hint: you may have to install PyGame in a non-standard way.
Either try to compile it from sources, or let pip do it.
Moreover some may have problems with installing Shapely library.
Easily "google" solution for your platform.



### Running project
Project works only with python version 3.5 and higher
PyScorchedEarth may be started by running script from project root:
```
python PyScorchedEarth.py
```


## Technical details

* **libs** module contains additional libraries (pyIgnition) to use
 in Python 3 with PyGame.


* **PyScorchedEarth** structure
  * **menu** has got some implementation of menu, which is responsible for installing player and tanks number. Simply go to Settings and choose appropriate numbers
  * **game_core** has all files needed to run the game itself. Implementation of Tank, Player, GameManager objects. GameManager takes care of the rest of the classes
  * **assets** is the folder containing all other external dependent files such as music, sounds, fonts
  * **bots** is the folder containing all bot implementations.
  * **test** folder contains automatic tests for the application
