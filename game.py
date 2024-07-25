import sys, pygame
from tank import Tank
from bullet import Bullet

pygame.mixer.init()
pygame.init()

# sound of bullets
sound_bullet=pygame.mixer.Sound("Pistola22cal.wav")

# destruction sounds
destroy = pygame.mixer.Sound("explosao.wav")

size = width, height = 900, 700
tank_width, tank_height = 100, 100
grey = 112, 112, 112

screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

clock = pygame.time.Clock()
timer_interval = 100
next_bullet_time = 100
next1_bullet_time = 100

positions = [[0, 0], [width-73, width-73], [0, width-73]]
tank_destroyed_image = pygame.image.load("tank1_destroyed.png").convert_alpha()

tank_image = pygame.image.load("tank.png").convert_alpha()
tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=0, endurance=60, k_up=pygame.K_UP, k_down=pygame.K_DOWN, k_left=pygame.K_LEFT, k_right=pygame.K_RIGHT, k_fire=pygame.K_SPACE, space_pressed=0, next_bullet_time=100, timer_interval=100)

tank1_image = pygame.image.load("tank1.png").convert_alpha()
tank1 = Tank(tank1_image, tank_destroyed_image, speed=5, x=width-73, y=width-73, points=0, endurance=60,  k_up=pygame.K_w, k_down=pygame.K_s, k_left=pygame.K_a, k_right=pygame.K_d, k_fire=pygame.K_f, space_pressed=0, next_bullet_time=100, timer_interval=100)


tank2_image = pygame.image.load("tank2.png").convert_alpha()
tank2 = Tank(tank2_image, tank_destroyed_image, speed=5, x=0, y=width-73, points=0, endurance=60,  k_up=pygame.K_u, k_down=pygame.K_j, k_left=pygame.K_h, k_right=pygame.K_k, k_fire=pygame.K_o, space_pressed=0, next_bullet_time=100, timer_interval=100)

bimg = pygame.image.load("bullet.png")

def show_game_over_message():
    font = pygame.font.Font(None, 74)
    pygame.display.flip()
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

def movement(tanks, screen, keys):
    for tank in tanks:
        screen.blit(tank.image, tank.rect)
        tank.check_ifout(screen_rect)
        tank.bullets.draw(screen)

        if tank.space_pressed == 1:
            tank.bullets.update()

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

def firing(tanks, screen, keys):
        for tank in tanks:
            screen.blit(tank.image, tank.rect)
            current_time = pygame.time.get_ticks()

            if current_time > tank.next_bullet_time:
                if keys[tank.k_fire]:
                    if len(tank.bullets) < 10:
                        tank.bullets.add(Bullet(bimg, tank))
                    else:
                        pass
                    print(len(tank.bullets))
                    tank.space_pressed = 1
                    sound_bullet.play()
                tank.next_bullet_time += tank.timer_interval

                # WORKS UNTIL HERE
                for bullet in tank.bullets:
                    if pygame.sprite.spritecollideany(bullet, tanks):

                        collided = pygame.sprite.spritecollideany(bullet, tanks)
                        collided.endurance -= 1
                        if collided.endurance == 0:
                            bullet.tank.bullets.empty()
                            #collided.speed = 0
                            #collided.rect.x = collided.rect.x - 16
                            #collided.rect.y = collided.rect.y - 16
                            screen.blit(collided.destroyed_image, (collided.rect.x-16, collided.rect.y-16))
                            bullet.tank.points +=1
                            collided.endurance = 60
                            i = 0;
                            for tank in tanks:
                                tank.update(positions[i][0], positions[i][1])
                                i+=1
                            if show_game_over_message():
                                print("on restart")
                                # RENEW THE TANKS
                                ##collided = Tank(tank1_image, tank1_destroyed_image, speed, x=width, y=height, points, endurance,  k_up, k_down, k_left, k_right, k_fire, space_pressed, next_bullet_time, timer_interval)
                                #pygame.time.delay(500)
                            else:
                                pygame.quit()
                                sys.exit()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(grey)

    tanks_points = []
    for tank in tanks:
        tanks_points.append(tank)

    font = pygame.font.Font(None, 40)
    placar = font.render(f"Green {tanks_points[0].points} x Red {tanks_points[1].points} x Blue {tanks_points[2].points}", True, (20, 20, 20))
    screen.blit(placar, (width//2 - placar.get_width()//2, 0))

    keys = pygame.key.get_pressed()
    movement(tanks, screen, keys)
    firing(tanks, screen, keys)



    clock.tick(100)
    pygame.display.flip()
