
import pygame
import random
import math

class Block:
    def __init__(self, pos, color, canvasdim, customwh=None):
        if customwh:
            self.size = customwh
        else:
            self.size = BLOCK_SIZE, BLOCK_SIZE
        self.speedx, self.speedy = 0,0
        self.color = color
        self.canvasdim = canvasdim
        self.posx, self.posy = self.get_random_pos(self.canvasdim) if pos == () else pos

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.posx, self.posy, self.size[0], self.size[1]))

    def update(self):
        self.posx += self.speedx
        self.posy += self.speedy

    def move(self, xydir):
        self.speedx = xydir[0] * self.size[0]
        self.speedy = xydir[1] * self.size[1]

    def transport(self, coordinates):
        self.posx, self.posy = self.get_random_pos(self.canvasdim) if coordinates == () else coordinates

    def get_random_pos(self, canvasdim):
        x = random.randint(canvasdim[0], canvasdim[2]) // self.size[0] * self.size[0]
        y = random.randint(canvasdim[1], canvasdim[3]) // self.size[1] * self.size[1]
        return x, y

    def distance(self, block):
        bcenter = (block.posx+block.size[0]/2, block.posy+block.size[1]/2)
        self.center = (self.posx+self.size[0]/2, self.posy+self.size[1]/2)
        a = abs(self.center[0] - bcenter[0])
        b = abs(self.center[1] - bcenter[1])
        return math.sqrt(a**2 + b**2)

class Snake:
    def __init__(self, pos, color, canvasdim):
        self.head = Block(pos, color, canvasdim)
        self.body = []
        self.pos = pos
        self.color = color
        self.canvasdim = canvasdim
        self.inventory = [None, None, None, None]

    def draw(self, window):
        self.head.draw(window)
        for block in self.body:
            block.draw(window)

    def update(self):
        self.move_body()
        self.head.update()
        for block in self.body:
            block.update()

    def move(self, xydir):
        self.head.move(xydir)

    def move_body(self):
        for i in range(len(self.body), 0, -1):
            if i == 1:
                self.body[i-1].posx = self.head.posx
                self.body[i-1].posy = self.head.posy
            else:
                self.body[i-1].posx = self.body[i-2].posx
                self.body[i-1].posy = self.body[i-2].posy

    def pick_up(self, powerup):
        for i, _ in enumerate(self.inventory):
            if self.inventory[i] == None:
                self.inventory[i] = powerup

    def use_inventory(self, key, game):
        if key == 'h':
            index = 0
        if key == 'j':
            index = 1
        if key == 'k':
            index = 2
        if key == 'l':
            index = 3

        if self.inventory[index] == None:
            pass
        else:
            if self.inventory[index].item_type == 'w':
                game.wraparound_on = True
            elif self.inventory[index].item_type == 'd':
                self.body = []
            elif self.inventory[index].item_type == 'p':
                game.passtrhough_on = True
            elif self.inventory[index].item_type == 'm':
                game.magnet_on = True
            self.inventory[index] = None

    def add_block(self):
        new_block = Block((self.head.posx, self.head.posy), self.color, self.canvasdim)
        self.body.append(new_block)

    def distance(self, block):
        return self.head.distance(block)

    def body_collision(self):
        for block in self.body:
            print(self.distance(block))
            if self.head.distance(block) < BLOCK_SIZE:
                 return True
        return False
class Food(Block):
    def __init__(self, pos, color, canvasdim):
        super().__init__(pos, color, canvasdim)

class Powerup(Block):
    def __init__(self, item_type, color, canvasdim):
        super().__init__((), color, canvasdim)
        self.item_type = item_type
        if item_type == 'w':
            self.visthreshold = random.randint(1, 20)
            pass
        elif item_type == 'd':
            self.visthreshold = random.randint(25, 60)
            pass
        elif item_type == 'p':
            self.visthreshold = random.randint(8, 20)
            pass
        elif item_type == 'm':
            self.visthreshold = random.randint(1, 4)
            pass
        print(self.visthreshold)

        self.canvasdim = canvasdim
        self.isvis = False

    def isvisible(self, player_length):
        if player_length > self.visthreshold:
            self.isvis = True
        else:
            self.isvis = False
        return self.isvis

    def draw(self, window):
        if self.isvis:
            super().draw(window)

    def update(self):
        if self.isvis:
            super().update()

class TextBox:
    def __init__(self, text, font, size, color, pos, window):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.posx, self.posy = pos
        self.window = window

        self.styled = pygame.font.Font(self.font, self.size)
        self.rendered = self.styled.render(self.text, 0, self.color)
        self.rect = self.rendered.get_rect()

        if self.posx == 'center':
            self.posx = self.window.get_width()/2 - self.rect[2]/2
        elif self.posx == 'margin-left':
            self.posx = 50
        elif self.posx == 'margin-right-center':
            self.posx = self.window.get_width() - 50 - self.rect.width

    def draw(self):
        self.blit = self.window.blit(self.rendered, (self.posx, self.posy))

    def update(self):
        pass

    def change_color(self, color):
        self.rendered = self.styled.render(self.text, 0, color)

    def change_text(self, text):
        self.rendered = self.styled.render(text, 0, self.color)

class Game:
    def __init__(self):
        self.selected_map = MAPS[0]
        self.rows, self.cols = self.selected_map
        self.width, self.height = self.cols * BLOCK_SIZE, self.rows * BLOCK_SIZE + HUD_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))

        self.canvasdim = (0, HUD_HEIGHT, self.width, self.height)

        self.running = True
        self.clock = pygame.time.Clock()

        self.theme = THEMES['default']
        self.state = 'play'
        self.score = 0
        self.highscore = int(open("scores.txt", 'r').read())

        self.num_foods = 1
        self.speed = 1

        self.selected_items = [0,1,1,1,0,2,0]
        self.players = []
        self.items = []
        self.obstacles = []
        self.powerups = []

        self.menu_headers = []
        self.menu_items = []

        self.menu()

        self.passthrough_on = False
        self.magnet_on = False

    def main(self):
        while self.running:
            pygame.time.delay(math.floor(60 / self.speed))
            self.clock.tick(10)

            self.update()
            self.draw()

    def draw(self):
        self.window.fill(self.theme[self.state + ' bg'])

        if self.state == 'menu':
            for header in self.menu_headers:
                if self.headings[self.selected_header] == header.text:
                    header.change_color(self.theme['menu item selected'])
                else:
                    header.change_color(self.theme['menu title color'])
                header.draw()
            for i, item in enumerate(self.menu_items):
                item[self.selected_items[i]].draw()
        elif self.state == 'play':
            # draw HUD
            pygame.draw.rect(self.window, self.theme['hud bg color'], (0, 0, self.width, self.canvasdim[1]))
            self.score_text.change_text("Score: " + str(self.score))
            self.score_text.draw()
            self.highscore_text.change_text("Highscore: " + str(self.highscore))
            self.highscore_text.draw()
            for i, powerup_container in enumerate(self.powerups_container_array):
                powerup_container.draw(self.window)
            for i, powerup in enumerate(self.powerup_inventory_array):
                if powerup:
                    powerup.posx = self.powerups_container_array[i].posx + self.powerups_container_array[i].size[0]/4
                    powerup.posy = self.powerups_container_array[i].posy + self.powerups_container_array[i].size[1]/4
                    powerup.draw(self.window)
            for item in self.items:
                item.draw(self.window)
            for obstacle in self.obstacles:
                obstacle.draw(self.window)
            for powerup in self.powerups:
                if powerup:
                    powerup.draw(self.window)
            for player in self.players:
                player.draw(self.window)
        elif self.state == 'pause':
            self.paused_press_space_text.draw()
            self.paused_press_M_text.draw()
            self.paused_text.draw()
        elif self.state == 'gameover':
            self.gameover_text.draw()
            self.finalscore_text.draw()
            self.gameover_press_space_text.draw()
            self.gameover_press_M_text.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_a]:
                if self.state == 'menu':
                    self.selected_items[self.selected_header] = self.selected_items[self.selected_header] + 1 if self.selected_items[self.selected_header] < len(self.menu_items[self.selected_header])-1 else 0
                if self.state == 'play':
                    self.players[0].move((-1,0))
            if keys[pygame.K_d]:
                if self.state == 'menu':
                    self.selected_items[self.selected_header] = self.selected_items[self.selected_header] - 1 if self.selected_items[self.selected_header] > 0 else len(self.menu_items[self.selected_header])-1
                if self.state == 'play':
                    self.players[0].move((1,0))
            if keys[pygame.K_w]:
                if self.state == 'menu':
                    self.selected_header = self.selected_header - 1 if self.selected_header > 0 else len(self.headings)-1
                if self.state == 'play':
                    self.players[0].move((0,-1))
            if keys[pygame.K_s]:
                if self.state == 'menu':
                    self.selected_header = self.selected_header + 1 if self.selected_header < len(self.headings)-1 else 0
                if self.state == 'play':
                    self.players[0].move((0,1))
            if keys[pygame.K_SPACE]:
                if self.state == 'menu':
                    self.mode = self.selected_items[0]
                    if self.selected_items[1] == 0:
                        self.speed = 0.5
                    if self.selected_items[1] == 1:
                        self.speed = 1
                    if self.selected_items[1] == 2:
                        self.speed = 1.5
                    if self.selected_items[1] == 3:
                        self.speed = 2
                    self.wraparound_on = self.selected_items[2]
                    self.powerups_on = self.selected_items[3]
                    self.obstacles_on = self.selected_items[4]
                    self.num_foods = self.selected_items[5] + 1
                    self.selected_map = MAPS[self.selected_items[6]]
                    self.rows, self.cols = self.selected_map
                    self.width, self.height = self.cols * BLOCK_SIZE, self.rows * BLOCK_SIZE + HUD_HEIGHT
                    self.window = pygame.display.set_mode((self.width, self.height))
                    self.canvasdim = (0, HUD_HEIGHT, self.width, self.height)
                    self.play()
                elif self.state == 'play':
                    self.pause()
                elif self.state == 'pause':
                    self.resume()
                elif self.state == 'gameover':
                    self.play()
            if keys[pygame.K_m]:
                if self.state != 'menu':
                    self.menu()
            if self.state == 'play' and self.powerups_on:
                if keys[pygame.K_h]:
                    for player in self.players:
                        player.use_inventory('h', self)
                        self.remove_powerup_from_screen(0)
                if keys[pygame.K_j]:
                    for player in self.players:
                        player.use_inventory('j', self)
                        self.remove_powerup_from_screen(1)
                if keys[pygame.K_k]:
                    for player in self.players:
                        player.use_inventory('k', self)
                        self.remove_powerup_from_screen(2)
                if keys[pygame.K_l]:
                    for player in self.players:
                        player.use_inventory('l', self)
                        self.remove_powerup_from_screen(3)

        if self.state == 'play':
            for player in self.players:
                for obstacle in self.obstacles:
                    obstacle.update()
                    if player.distance(obstacle) < BLOCK_SIZE:
                        self.gameover()
                for i, powerup in enumerate(self.powerups):
                    if powerup:
                        if powerup.isvisible(len(player.body)+1):
                            if player.distance(powerup) < BLOCK_SIZE:
                                player.pick_up(powerup)
                                self.add_powerup_to_screen(powerup)
                                self.powerups[i] = None
                player.update()
                if player.head.posx < self.canvasdim[0] or player.head.posx > self.canvasdim[2] or player.head.posy < self.canvasdim[1] or player.head.posy >= self.canvasdim[3]:
                    if self.wraparound_on:
                        if player.head.posx >= self.canvasdim[2]:
                            player.head.posx = self.canvasdim[0]
                        elif player.head.posx < self.canvasdim[0]:
                            player.head.posx = self.canvasdim[2] - BLOCK_SIZE
                        else:
                            player.head.posx %= self.canvasdim[2]

                        if player.head.posy >= self.canvasdim[3]:
                            player.head.posy = self.canvasdim[1]
                        elif player.head.posy < self.canvasdim[1]:
                            player.head.posy = self.canvasdim[3] - BLOCK_SIZE
                        else:
                            player.head.posy %= self.canvasdim[3]
                    else:
                        self.gameover()
                if self.passthrough_on == False:
                    if player.body_collision():
                        self.gameover()
                for item in self.items:
                    if self.magnet_on:
                        if player.head.posx > item.posx:
                            dirx = 1
                        elif player.head.posx == item.posx:
                            dirx = 0
                        elif player.head.posx < item.posx:
                            dirx = -1
                        if player.head.posy > item.posy:
                            diry = 1
                        elif player.head.posy == item.posy:
                            diry = 0
                        elif player.head.posy < item.posy:
                            diry = -1
                        item.move((dirx, diry))
                        item.update()
                    if player.distance(item) < BLOCK_SIZE:
                        item.transport(())
                        if isinstance(item, Food):
                            player.add_block()
                            if self.magnet_on:
                                self.total_magnet_eats += 1
                                if self.total_magnet_eats < 6:
                                    self.magnet_on = False
                            self.score += int(10 * self.speed)
                            if self.score > self.highscore:
                                self.highscore = self.score

        pygame.display.update()

    def menu(self):
        self.state = 'menu'
        self.selected_header = 0
        self.menu_items = []

        title = TextBox(MENU_TEXT['title'], self.theme['font'], 150, self.theme['menu title color'], ('center', 10), self.window)
        space_to_begin = TextBox('Press SPACE to Begin', self.theme['font'], 40, self.theme['menu title color'], (210, 120), self.window)
        self.headings = ['Mode', 'Speed', 'Wraparound', 'Power Ups', 'Obstacles', 'Num Food', 'Map']
        ypos = 10+150+10
        for heading_i, heading in enumerate(self.headings):
            heading_box = TextBox(heading, self.theme['font'], 75, self.theme['menu title color'], ('margin-left', ypos), self.window)
            self.menu_headers.append(heading_box)
            array_of_menu_items = []
            for item in MENU_TEXT[heading]:
                item_box = TextBox(item, self.theme['font'], 75, self.theme['menu title color'], ('margin-right-center', ypos), self.window)
                array_of_menu_items.append(item_box)

            self.menu_items.append(array_of_menu_items)
            ypos += 75

        self.menu_headers.append(title)
        self.menu_headers.append(space_to_begin)

    def play(self):
        self.players = []
        self.items = []
        self.score = 0
        self.total_magnet_eats = 0
        self.state = 'play'
        player1 = Snake((), self.theme['player color'], self.canvasdim)
        self.players.append(player1)
        for i in range(self.num_foods):
            food = Food((), self.theme['food color'], self.canvasdim)
            self.items.append(food)
        self.highscore_text = TextBox("Highscore: " + str(self.highscore), self.theme['font'], 50, (0,0,0), ('margin-right-center', 5), self.window)
        self.score_text = TextBox("Score: " + str(self.score), self.theme['font'], 50, (0,0,0), ('margin-right-center', 50), self.window)

        self.powerup_inventory_array = [None, None, None, None]
        self.powerups_container_array = []
        for i in range(4):
            new_powerup_container = Block((20*i*2*1.1 +5,50), (44, 62, 80), self.canvasdim, customwh=(BLOCK_SIZE*2, BLOCK_SIZE*2))
            self.powerups_container_array.append(new_powerup_container)

        if self.obstacles_on:
            for i in range(random.randint(1, 4)):
                new_obstacle = Block((), self.theme['obstacle color'], self.canvasdim)
                self.obstacles.append(new_obstacle)
        magnet = Powerup('m', self.theme['magnet powerup color'], self.canvasdim)
        passthrough = Powerup('p', self.theme['passthrough powerup color'], self.canvasdim)
        del_body = Powerup('d', self.theme['del_body powerup color'], self.canvasdim)
        wraparound = Powerup('w', self.theme['wraparound powerup color'], self.canvasdim)
        self.powerups = [magnet, passthrough, del_body, wraparound]

    def pause(self):
        self.state = 'pause'
        self.paused_text = TextBox("Paused", self.theme['font'], 150, (255,255,255), ('center', self.height/2 - 75), self.window)
        self.paused_press_space_text = TextBox("Press SPACE to resume", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 180), self.window)
        self.paused_press_M_text = TextBox("Press M for Menu", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 225), self.window)
        self.paused_text.draw()
        self.paused_press_space_text.draw()
        self.paused_press_M_text.draw()

    def resume(self):
        self.state = 'play'

    def gameover(self):
        self.state = 'gameover'
        self.window.fill(self.theme['gameover bg'])
        print(self.score)
        self.gameover_text = TextBox("Game Over", self.theme['font'], 150, (255,255,255), ('center', self.height/2 - 75), self.window)
        self.finalscore_text = TextBox("Final Score: " + str(self.score), self.theme['font'], 50, (255,255,255), ('center', self.height/2 + 75), self.window)
        self.gameover_press_space_text = TextBox("Press SPACE to play again", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 180), self.window)
        self.gameover_press_M_text = TextBox("Press M for Menu", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 225), self.window)
        self.gameover_text.draw()
        self.finalscore_text.draw()
        self.gameover_press_space_text.draw()
        self.gameover_press_M_text.draw()

        self.score = 0
        self.obstacles = []
        scorefile = open("scores.txt", 'w')
        scorefile.write(str(self.highscore))

    def add_powerup_to_screen(self, powerup):
        for i, _ in enumerate(self.powerup_inventory_array):
            if self.powerup_inventory_array[i] == None:
                self.powerup_inventory_array[i] = powerup
                break

    def remove_powerup_from_screen(self, index):
        self.powerup_inventory_array[index] = None

# Global Constants
BLOCK_SIZE = 20
HUD_HEIGHT = 100
THEMES = {'default': {'font': 'Retro.ttf', 'player color': (26, 188, 156), 'food color': (192, 57, 43), 'menu title color': (44, 62, 80), 'obstacle color': (127, 140, 141), 'magnet powerup color': (230, 126, 34), 'passthrough powerup color': (155, 89, 182), 'del_body powerup color': (41, 128, 185), 'wraparound powerup color': (241, 196, 15), 'menu bg': (39, 174, 96), 'play bg': (44, 62, 80), 'pause bg': (41, 128, 185), 'gameover bg': (30, 39, 46), 'hud bg color': (52, 73, 94), 'menu item selected': (236, 240, 241)}}
STATES = ['menu', 'play', 'paused', 'gameover']

MENU_TEXT = {'title': 'PySnake', 'Mode': ['Normal', 'Team', 'Battle', 'Zone'], 'Speed': ['0.5x', '1x', '1.5x', '2x'], 'Wraparound': ['off', 'on'], 'Power Ups': ['off', 'on'], 'Obstacles': ['off', 'on'], 'Num Food': ['1', '2', '3'], 'Map': ['1', '2', '3', '4']}
MAPS = [(30, 30), (50, 50), (50, 25), (80, 80)]

pygame.init()
game = Game()
game.main()

pygame.quit()
