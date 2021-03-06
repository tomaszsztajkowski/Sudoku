# Sudoku by Tomasz Sztajkowski
> a simple sudoku game and solver

<a href="https://imgur.com/BFmwbYe"><img src="https://i.imgur.com/BFmwbYe.gif" title="source: imgur.com" /></a>

### Installation
- Install Python 3.x, preferably Python 3.8.2
- Install needed modules by running the command below in the terminal
```shell
pip install -r requirements.txt
```
##### sidenote: if Python 2.x is installed on your machine it may be required to use one of the two following commands:
```shell
pip3 install -r requirements.txt
python3 -mpip install -r requirements.txt
```

### Setup

- Run 'run.py'
- If that doesn't work open terminal at the location of the project and type one of the below:
```shell
python run.py
python3 run.py
```
## Rules
- The big 9x9 square divided into 9 smaller 3x3 squares has to be completely filled with numbers 1 to 9
- No line, row, or smaller square can contain repeating numbers
## Instructions
- left mouse button - select a tile for regular number input
- right mouse button - select a tile for marking
- 1 to 9 - insert a number/mark into the selected tile
###### sidenote: multiple marks can be inserted into one tile, marks do not affect validity check
- 0 - clear the selected tile
- q, w, e - load in a new map (easy, medium, hard)
- spacebar - start solving
- '-' and '='- while solving decrease and increase the speed of solving
###### sidenote: don't be suprised if solving time changes drastically between different puzzles or if solving easier puzzles takes more time than the hard ones, backtracking method solving time does not depend on deterministic difficulty
- escape - clear the board
#
<a href="https://imgur.com/5IFHui4"><img src="https://i.imgur.com/5IFHui4.png" title="source: imgur.com" /></a>
