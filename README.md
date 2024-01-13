# PyGameChess

Chess using the pygame library for python3.

## Install pygame for python3

First, install the pygame library for python3.
```
pip3 install pygame
```
You can check that pygame is installed using this command:
```
pip3 list
```

Then, check which version of python3 corresponds to pip3.
For me, this is python3.10; this will depend on your pip3 and python3 installations.
```
which pip3

/opt/homebrew/bin/pip3

which python3.10

/opt/homebrew/bin/python3.10
```

You should check that you can import pygame successfully:
```
python3.10
import pygame
```

## Install and run project

First, clone the repository in a directory of your choice.
```
git clone git@github.com:caleb-james-smith/PyGameChess.git
cd PyGameChess
```

Then, you may run any of the following programs.
Make sure that you have already installed pygame for python3, and make sure to use the corresponding version of python3 for all commands.

To start a game with two people (man vs. man), run this program:
```
python3.10 python/play.py
```

To start a game with two computer players (machine vs. machine), run this program:
```
python3.10 python/auto_play.py
```

To start a game against a computer player (man vs. machine), run this program:
```
python3.10 python/play_vs_computer.py
```
