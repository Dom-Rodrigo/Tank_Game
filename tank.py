import pygame

class Tank:
    def __init__(self, image, destroyed_image, speed, x, y):
        self.speed = speed
        self.image = image
        self.destroyed_image = destroyed_image
        self.rect = image.get_rect()
        self.rect.x = x;
        self.rect.y = y;
        self.turn = 0;
        self.start_time = pygame.time.get_ticks()



    def move(self, up=False, down=False, turn_left=False, turn_right=False):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > 300:
            if turn_right:
                self.turn = self.turn -1
                center = self.rect

                self.image = pygame.transform.rotate(self.image, -90)
                self.destroyed_image = pygame.transform.rotate(self.destroyed_image, -90)

                self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x+40, self.rect.y+40)).center)
                self.start_time = pygame.time.get_ticks()

            if turn_left:
                elapsed = pygame.time.get_ticks() - self.start_time
                self.turn = self.turn  + 1
                center = self.rect

                self.image = pygame.transform.rotate(self.image, 90)
                self.destroyed_image = pygame.transform.rotate(self.destroyed_image, 90)

                self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x+40, self.rect.y+40)).center)
                self.start_time = pygame.time.get_ticks()



        if down:
            if self.turn in [0, 4, -4]: #Tank is poiting to the top
                self.rect.top += self.speed
            if self.turn in [-2, 2]: #Tank is pointing down
                self.rect.top -= self.speed
            if self.turn in [-1, 3]: #Tank is poiting to the right
                self.rect.right -= self.speed
            if self.turn in [1, -3]: #Tank is poiting to the left
                self.rect.right += self.speed

        if up:
            if self.turn in [0, 4, -4]: #Tank is poiting to the top
                self.rect.top -= self.speed
            if self.turn in [-2, 2]: #Tank is pointing down
                self.rect.top += self.speed
            if self.turn in [-1, 3]: #Tank is poiting to the right
                self.rect.right += self.speed
            if self.turn in [1, -3]: #Tank is poiting to the left
                self.rect.right -= self.speed

    def check_ifout(self, screen_rect):
            if self.rect.x < screen_rect.left+80: #doesnt work
                self.rect.x = screen_rect.left+80
            if self.rect.x > screen_rect.right - 80: #works
                self.rect.x = screen_rect.right - 80
            if self.rect.y < screen_rect.top + 80: #dont work
                 self.rect.y = screen_rect.top + 80
            if self.rect.y > screen_rect.height-83: #works
                 self.rect.y = screen_rect.height-83
