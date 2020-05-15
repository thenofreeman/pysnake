# player.py

from entity import Entity

class Player(Entity):
    def __init__(self, game, speed, pos=(0,0)):
        super().__init__(game, speed, pos)
        self.teleport()
