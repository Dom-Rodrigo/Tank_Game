import pygame
from tank import Tank

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.turn = tank.turn
        if self.turn in [0, 4, -4]: #Tank is poiting to the top
            self.rect.center = (tank.rect.x+38, tank.rect.y-20)
        if self.turn in [-2, 2]: #Tank is pointing down
            self.rect.center = (tank.rect.x+38, tank.rect.y+100)

        if self.turn in [-1, 3]: #Tank is poiting to the right
            self.rect.center = (tank.rect.x+85, tank.rect.y+35)

        if self.turn in [1, -3]: #Tank is poiting to the left
            self.rect.center = (tank.rect.x-38, tank.rect.y+35)
        self.tank = tank

        #adjusted to the tip


    def update(self, width, height):
        if self.turn in [0, 4, -4]: #Tank is poiting to the top
            self.rect.move_ip(0, -4)
        if self.turn in [-2, 2]: #Tank is pointing down
            self.rect.move_ip(0, +4)
        if self.turn in [-1, 3]: #Tank is poiting to the right
            self.rect.move_ip(+4, 0)
        if self.turn in [1, -3]: #Tank is poiting to the left
            self.rect.move_ip(-4, 0)
        if self.rect.top < 0:
            self.kill()
        if self.rect.top > height:
            self.kill()
        if self.rect.right > width:
            self.kill()
        if self.rect.right < 0:
            self.kill()
