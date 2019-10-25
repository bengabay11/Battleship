import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(self.__class__, self).__init__()
        self.image = pygame.image.load('ship.jpg').convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y


