# entity.py

import random

class Entity:
    def __init__(self, game, speed, pos=()):
        self.width, self.height = 25,25
        self.speed = speed
        self.game = game
        self.direction = 'stop'
        self.body = []
        self.teleport(pos)

    def teleport(self, coor=()):
        if coor == ():
            x = random.randint(self.game.left_boundry, self.game.right_boundry) // self.width * self.width
            y = random.randint(self.game.top_boundry, self.game.bottom_boundry) // self.height * self.height
            self.posx, self.posy = x, y
        #else:
            #self.posx, self.posy = coor

    def move_up(self):
        if self.direction != "down" or len(self.body) < 1:
            self.direction = "up"

    def move_down(self):
        if self.direction != "up" or len(self.body) < 1:
            self.direction = "down"

    def move_left(self):
        if self.direction != "right" or len(self.body) < 1:
            self.direction = "left"

    def move_right(self):
        if self.direction != "left" or len(self.body) < 1:
            self.direction = "right"

    def move(self):
        if self.direction == "up":
            self.posy -= self.speed

        if self.direction == "down":
            self.posy += self.speed

        if self.direction == "left":
            self.posx -= self.speed

        if self.direction == "right":
            self.posx += self.speed

    def check_collisions(self):
        if self.game.wraparound_on:
            pass
        else:
            # if crossing border
            if self.posx < 0 or self.posx > self.game.canvas_size[0] or self.posy < 0 or self.posy > self.game.canvas_size[1]:
                print(self.game.canvas_size)
                self.direction = 'stop'
                self.game.state = 'gameover'
            # if touching food or item
            for item in self.game.items_list:
                if self.distance(item) < 0:
                    if item.get_type() == 'food':
                        self.eat_food()
                    if item.get_type() == 'obstacle':
                        pass
                    if item.get_type() == 'powerup':
                        pass
            # if touching body

    def draw(self):
        self.game.window.pygame.draw.rect(self.game.window.window, self.game.theme['player_color'], (self.posx, self.posy, self.width, self.height), 2)
