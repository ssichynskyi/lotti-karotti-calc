![](https://github.com/ssichynskyi/lotti-karotti-calculator/workflows/Lotti-Karotti-Calc%20acceptance/badge.svg)
[![Code Grade](https://www.code-inspector.com/project/13601/score/svg)](https://www.code-inspector.com)
[![Code Grade](https://www.code-inspector.com/project/13601/status/svg)](https://www.code-inspector.com)
[![Coverage Status](https://coveralls.io/repos/github/ssichynskyi/lotti-karotti-calc/badge.svg?branch=master)]
(https://coveralls.io/github/ssichynskyi/lotti-karotti-calc?branch=master)
## Calculator of winning odds in the game Lotti Karotti
This program calculates the winning odds for a certain player
in the game [Lotti Karotti](https://de.wikipedia.org/wiki/Lotti_Karotti)
This program answers the question whether the turn sequence
affects winning odds. Default configuration represents the
most classical variant of this game. Additional rule was added:
every player should have not more than one rabbit on the field
at the same time
ToDo: add link to building jobs

## Requirements
* Python 3.6+
* pip3
* python libs described in requirements.txt
```
$ pip3 install -r requirements.txt
```
or
```
$ make
```


## Usage
Configurable parameters through /config/lotti_config.yaml:
* Number of rabbits (i.e. attempts for every player)
* Number of play fields
* Configuration and sequence of the holes
* Type and quantity of this type of the card in the stack

Parameters configurable using command line options:
* number of players
* number of game runs (e.g. iterations / experiments)

### HOW TO RUN:
* Recommended: to get the preconfigured [binary packages](http://lotti-karotti-calculator.s3-website.eu-central-1.amazonaws.com/)
for linux and ubuntu. No lib/dependecy installation required.
* Compile locally using scripts from ci submodule (you should know what you're doing)
* run python source files:
```
$ python3 game.py <number of players> <number of runs>
```

### Author
Sergii Sichynskyi
