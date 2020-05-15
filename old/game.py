# game.py

DEFAULT = 'default'

font = 'Retro.ttf'

themes = {DEFAULT: {'player_color': (0,0,0),'menu_color': (0, 0, 255), 'bg_color': (0, 255, 0), 'gameover_color': (0, 0, 0), 'menu_item_selected':(255,255,255), 'menu_item_unselected':(0,0,0)}}

# states
MENU = 'menu'
PLAY = 'play'
PAUSED = 'paused'
GAMEOVER = 'gameover'

white = (255,255,255)
black = (0,0,0)

maps = [(500, 500), (1000, 1000), (1000, 500), (1500, 500)]

from ui_text import UIText
from player import Player

class Game:
    def __init__(self, window):
        self.theme = themes[DEFAULT]
        self.window = window
        self.canvas_size = (1000, 1000)
        self.state = MENU

        self.headings = ['Mode', 'Speed', 'Wraparound', 'PowerUps', 'Obstacles', '# Food', 'Map']

        self.entity_size = 25

        self.mode_items_array = ['normal', 'team', 'battle', 'zone']
        self.speed_items_array = ['0.75x', '1x', '1.5x', '2x']
        self.wrap_items_array =    ['off', 'on']
        self.powerup_items_array = ['off', 'on']
        self.obstacle_items_array = ['off', 'on']
        self.food_items_array = ['1', '2', '3']
        self.map_items_array = ['1', '2', '3', '4']

        self.top_boundry = 0
        self.bottom_boundry = self.canvas_size[0]
        self.left_boundry = 0
        self.right_boundry = self.canvas_size[1]

        self.heading_items = [self.mode_items_array, self.speed_items_array, self.wrap_items_array, self.powerup_items_array, self.obstacle_items_array, self.food_items_array, self.map_items_array]

        self.selected_heading = 0
        self.selected_items = [0,1,0,0,0,0,1]

        self.prev_selected_heading = 1
        self.selected_item = 1

        self.menu_headers, self.menu_items, self.menu_title = self.build_menu()

    # redraws any changes made in update
    def draw(self):
        if self.state == MENU:
            self.display_menu()
        if self.state == PLAY:
            self.display_play()
        if self.state == PAUSED:
            self.display_pause()
        if self.state == GAMEOVER:
            self.display_gameover()

    # updates logic like player location
    def update(self):
        for event in self.window.pygame.event.get():
            # Break the game loop if QUIT event arises (eg. hitting 'x' on window)
            if event.type == self.window.pygame.QUIT:
                running = False
                self.window.pygame.quit()
                break

        self.window.pygame.event.pump()
        keys = self.window.pygame.key.get_pressed()

        if self.state == MENU:
            if keys['K_UP']:
                self.selected_heading = self.selected_heading - 1 if self.selected_heading > 0 else len(self.headings)-1
                self.selected_item = self.selected_items[self.selected_heading]
            if keys[K_DOWN]:
                self.selected_heading = self.selected_heading + 1 if self.selected_heading < len(self.headings)-1 else 0
                self.selected_item = self.selected_items[self.selected_heading]
            if keys[K_LEFT]:
                self.selected_item = self.selected_item - 1 if self.selected_item > 0 else len(self.heading_items[self.selected_heading])-1
                self.selected_items[self.selected_heading] = self.selected_item
            if keys[K_RIGHT]:
                self.selected_item = self.selected_item + 1 if self.selected_item < len(self.heading_items[self.selected_heading])-1 else 0
                self.selected_items[self.selected_heading] = self.selected_item
            if keys[K_SPACE]:
                self.build_play()
        if self.state == PLAY:
            if keys[K_UP]:
                self.players_list[0].move_up()
            if keys[K_DOWN]:
                self.players_list[0].move_down()
            if keys[K_LEFT]:
                self.players_list[0].move_left()
            if keys[K_RIGHT]:
                self.players_list[0].move_right()
            if keys[K_SPACE]:
                pass
        for player in self.players_list:
            player.check_collisions()
            player.move()
        if self.state == PAUSED:
            if keys[K_UP]:
                pass
            if keys[K_DOWN]:
                pass
            if keys[K_LEFT]:
                pass
            if keys[K_RIGHT]:
                pass
            if keys[K_SPACE]:
                pass
        if self.state == GAMEOVER:
            if keys[K_UP]:
                pass
            if keys[K_DOWN]:
                pass
            if keys[K_LEFT]:
                pass
            if keys[K_RIGHT]:
                pass
            if keys[K_SPACE]:
                pass

    def set_canvas_size(self, size):
        self.canvas_size = size

    def display_menu(self):
        self.window.fill(self.theme['menu_color'])

        for i, header in enumerate(self.menu_headers):
            header.change_color(self.theme['menu_item_unselected'])
            self.menu_items[i][self.selected_items[i]].change_color(self.theme['menu_item_unselected'])

        self.menu_headers[self.selected_heading].change_color(self.theme['menu_item_selected'])
        self.menu_items[self.selected_heading][self.selected_item].change_color(self.theme['menu_item_selected'])


    def display_pause(self):
        self.window.fill(self.theme['menu_color'])

    def display_play(self):
        self.window.fill(self.theme['bg_color'])
        for player in self.players_list:
            player.draw()

    def display_gameover(self):
        self.window.fill(self.theme['gameover_color'])

    def text_format(self, message, textFont, textSize, textColor):
        newFont=self.window.pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

        self.headings = ['Mode', 'Speed', 'Wraparound', 'PowerUps', 'Obstacles', '# Food', 'Map']
    def build_play(self):
        self.players_list= []
        self.items_list = []

        self.num_players = 1

        if self.selected_items[0] == 0:
            self.num_players = 1
        elif self.selected_items[0] == 1:
            pass
        elif self.selected_items[0] == 2:
            pass
        elif self.selected_items[0] == 3:
            pass

        self.player_speed = 0

        if self.selected_items[1] == 0:
            self.player_speed = 0.75 * self.entity_size
        elif self.selected_items[1] == 1:
            self.player_speed = 1 * self.entity_size
        elif self.selected_items[1] == 2:
            self.player_speed = 1.5 * self.entity_size
        elif self.selected_items[1] == 3:
            self.player_speed = 2 * self.entity_size

        if self.selected_items[2]:
            self.wraparound_on = True
        else:
            self.wraparound_on = False

        if self.selected_items[3]:
            self.powerups_on = True
        else:
            self.powerups_on = False

        if self.selected_items[4]:
            self.obstacles_on = True
        else:
            self.obstacles_on = False

        self.num_food = self.selected_items[5] + 1

        self.map = maps[self.selected_items[6]]

        self.set_canvas_size(self.map)

        for player in range(self.num_players):
            new_player = Player(self, self.player_speed)
            self.players_list.append(new_player)

        self.state = PLAY

    def build_menu(self):
        menu_headers = []
        menu_header_items = []

        title = UIText('PySnake', font, 150, black, 'centerx', 40, self.window)

        for header_i, header in enumerate(self.heading_items):
            new_header = UIText(self.headings[header_i], font, 75, black, self.window.width/8, 220 + (75 * header_i) + 10, self.window)
            menu_headers.append(new_header)
            menu_items = []
            for item_i, item in enumerate(header):
                new_item = UIText(self.heading_items[header_i][item_i], font, 50, black, self.window.width/8*5, 220 + (75 * header_i) + 10, self.window)
                menu_items.append(new_item)

            menu_header_items.append(menu_items)
        return (menu_headers, menu_header_items, title)
