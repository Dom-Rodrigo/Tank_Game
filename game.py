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


tank2_image = pygame.image.load("tank2.png").convert_alpha()
tank2_destroyed_image = pygame.image.load("tank1_destroyed.png").convert_alpha()
tank2 = Tank(tank2_image, tank2_destroyed_image, speed=5, x=0, y=height-80, points=0, endurance=50,  k_up=pygame.K_u, k_down=pygame.K_j, k_left=pygame.K_h, k_right=pygame.K_k, k_fire=pygame.K_o, space_pressed=0, next_bullet_time=100, timer_interval=100)

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
tanks.add(tank2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(grey)

    tanks_points = []
    for tank in tanks:
        tanks_points.append(tank)

    font = pygame.font.Font(None, 40)
    placar = font.render(f"Green {tanks_points[1].points} x Red {tanks_points[0].points}", True, (20, 20, 20))
    screen.blit(placar, (width//2 - placar.get_width()//2, 0))


    for tank in tanks:
        screen.blit(tank.image, tank.rect)
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
        screen.blit(tank.image, tank.rect)
        current_time = pygame.time.get_ticks()
        if current_time > tank.next_bullet_time:
            if keys[tank.k_fire]:
                tank.bullets.add(Bullet(bimg, tank))
                tank.space_pressed = 1
            tank.next_bullet_time += tank.timer_interval

            # WORKS UNTIL HERE
            for bullet in tank.bullets:
                if pygame.sprite.spritecollideany(bullet, tanks):

                    collided = pygame.sprite.spritecollideany(bullet, tanks)
                    print(collided)
                    collided.endurance -= 1
                    if collided.endurance == 0:
                        # collided.speed = 0
                        # collided.image = collided.destroyed_image
                        # collided.rect.x = collided.rect.x - 16
                        # collided.rect.y = collided.rect.y - 16
                        screen.blit(collided.image, collided.rect)
                        pygame.time.delay(2000)
                        if show_game_over_message():
                            collided.points +=1
                            # RENEW THE TANKS
                            ##collided = Tank(tank1_image, tank1_destroyed_image, speed, x=width, y=height, points, endurance,  k_up, k_down, k_left, k_right, k_fire, space_pressed, next_bullet_time, timer_interval)
                            collided.bullets.empty()
                        else:
                            pygame.quit()
                            sys.exit()

    clock.tick(100)
    pygame.display.flip()
