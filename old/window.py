# window.py

class Window:
    def __init__(self, pygame, dim=(1000,1000), title="PySnake by Nolan Freeman"):
        # store an instance to pygame
        self.pygame = pygame

        self.set_dim(dim)
        self.set_title(title)

    def set_dim(self, dim):
        self.width, self.height = dim
        self.window = self.pygame.display.set_mode(dim)

    def set_title(self, title):
        self.title = title
        self.pygame.display.set_caption(self.title)

    def fill(self, color):
        self.window.fill(color)

    def blit(self, title, coordinates):
        return self.window.blit(title, coordinates)
