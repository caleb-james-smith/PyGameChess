# PyGameChess
Chess using the pygame library.


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

Use this command to clone the repository in a directory of your choice.
```
git clone git@github.com:caleb-james-smith/PyGameChess.git
```

To launch the game, run this script using the python3 version that has pygame installed:
```
cd PyGameChess 
python3.10 play.py
```
