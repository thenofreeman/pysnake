# ui_text.py

class UIText:
    def __init__(self, title, font, size, color, posx, posy, window):
        self.window = window
        self.text = self.text_format(title, font, size, color)
        self.rect = self.text.get_rect()
        self.title = title
        self.font = font
        self.size = size
        self.color = color
        self.posx = posx
        self.posy = posy
        if posx == 'centerx':
            posx = self.window.width/2 + self.rect[2]/2
        self.blit = self.window.blit(self.text, (posx, posy))

    def text_format(self, message, textFont, textSize, textColor):
        newFont=self.window.pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def change_color(self, color):
        new_text = self.text_format(self.title, self.font, self.size, color)
        self.blit = self.window.blit(new_text, (self.posx, self.posy))
