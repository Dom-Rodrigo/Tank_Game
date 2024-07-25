import sys, pygame
from tank import Tank
from bullet import Bullet

pygame.mixer.init()
pygame.init()

# Carrega o som de destruição
destroy = pygame.mixer.Sound("explosao.wav")

size = width, height = 900, 700
speed = [1, 0]
tank_width, tank_height = 100, 100
grey = 112, 112, 112
i = 0

screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

clock = pygame.time.Clock()
timer_interval = 100
next_bullet_time = 100
next1_bullet_time = 100

tank_image = pygame.image.load("tank.png").convert_alpha()
tank_destroyed_image = pygame.image.load("tank_destroyed.png").convert_alpha()
tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=0, endurance=50, k_up=pygame.K_UP, k_down=pygame.K_DOWN, k_left=pygame.K_LEFT, k_right=pygame.K_RIGHT, k_fire=pygame.K_SPACE, space_pressed=0, next_bullet_time=100, timer_interval=100)

tank1_image = pygame.image.load("tank1.png").convert_alpha()
tank1_destroyed_image = pygame.image.load("tank1_destroyed.png").convert_alpha()
tank1 = Tank(tank1_image, tank1_destroyed_image, speed=5, x=width-73, y=height-80, points=0, endurance=50,  k_up=pygame.K_w, k_down=pygame.K_s, k_left=pygame.K_a, k_right=pygame.K_d, k_fire=pygame.K_f, space_pressed=0, next_bullet_time=100, timer_interval=100)

bimg = pygame.image.load("bullet.png")

def show_game_over_message():
    font = pygame.font.Font(None, 74)
    pygame.display.flip()
    pygame.time.delay(500)
    destroy.play()

    error_text = font.render("Tank Destroyed!", True, (255, 0, 0))
    question_text = font.render("Restart? (Y/N)", True, (255, 255, 255))
    screen.blit(error_text, (width//2 - error_text.get_width()//2, height//2 - 50))
    screen.blit(question_text, (width//2 - question_text.get_width()//2, height//2 + 50))
    pygame.display.flip()

    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False


tanks = pygame.sprite.Group()
tanks.add(tank)
tanks.add(tank1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(grey)

    font = pygame.font.Font(None, 40)
    placar = font.render(f"Green {tank.points} x Red {tank1.points}", True, (20, 20, 20))
    screen.blit(placar, (width//2 - placar.get_width()//2, 0))


    for tank in tanks:
        tank.check_ifout(screen_rect)
        tank.bullets.draw(screen)

        if tank.space_pressed == 1:
            tank.bullets.update()


        keys = pygame.key.get_pressed()
        start_time = pygame.time.get_ticks()

        if tank.turn == 4 or tank.turn == -4:  # one cycle
            tank.turn = 0

        if tank.speed != 0:
            if keys[tank.k_up]:
                tank.move(up=True)
            if keys[tank.k_down]:
                tank.move(down=True)
            if keys[tank.k_left]:
                tank.move(turn_left=True)
            if keys[tank.k_right]:
                tank.move(turn_right=True)

    for tank in tanks:
        current_time = pygame.time.get_ticks()
        if current_time > tank.next_bullet_time:
            if keys[tank.k_fire]:
                tank.bullets.add(Bullet(bimg, tank))
                tank.space_pressed = 1
            tank.next_bullet_time += tank.timer_interval
        #
        # for bullet in tank.bullets:
        #     if bullet.rect.colliderect(tank.rect):
        #         tank.endurance -= 1
        #
        #         if tank.endurance == 0:
        #             destroy.play()
        #             tank.speed = 0
        #             tank.image = tank.destroyed_image
        #             tank.rect.x = tank.rect.x - 16
        #             tank.rect.y = tank.rect.y - 16
        #             screen.blit(tank.image, tank.rect)
        #             if show_game_over_message():
        #                 tank.points +=1
        #                 tank.bullets.empty()
        #             else:
        #                 pygame.quit()
        #                 sys.exit()

        screen.blit(tank.image, tank.rect)
    clock.tick(100)
    pygame.display.flip()
