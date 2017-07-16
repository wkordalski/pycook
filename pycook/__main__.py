from .game import Game
from .levels.example import Level

level = Level()
game = Game(level)
game.loop()