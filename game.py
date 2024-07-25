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
tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=0, endurance=50)

tank1_image = pygame.image.load("tank1.png").convert_alpha()
tank1_destroyed_image = pygame.image.load("tank1_destroyed.png").convert_alpha()
tank1 = Tank(tank1_image, tank1_destroyed_image, speed=5, x=width-73, y=height-80, points=0, endurance=50)

bimg = pygame.image.load("bullet.png")

tank_bullets = pygame.sprite.Group()
tank1_bullets = pygame.sprite.Group()

space_pressed = 0
space1_pressed = 0

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




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(grey)

    font = pygame.font.Font(None, 40)
    placar = font.render(f"Green {tank.points} x Red {tank1.points}", True, (20, 20, 20))
    screen.blit(placar, (width//2 - placar.get_width()//2, 0))

    tank.check_ifout(screen_rect)
    tank1.check_ifout(screen_rect)
    tank_bullets.draw(screen)
    tank1_bullets.draw(screen)

    if space1_pressed == 1:
        tank1_bullets.update()

    if space_pressed == 1:
        tank_bullets.update()

    keys = pygame.key.get_pressed()
    start_time = pygame.time.get_ticks()

    if tank1.turn == 4 or tank1.turn == -4:  # one cycle
        tank1.turn = 0

    if tank1.speed != 0:
        if keys[pygame.K_UP]:
            tank1.move(up=True)
        if keys[pygame.K_DOWN]:
            tank1.move(down=True)
        if keys[pygame.K_LEFT]:
            tank1.move(turn_left=True)
        if keys[pygame.K_RIGHT]:
            tank1.move(turn_right=True)

    if tank.turn == 4 or tank.turn == -4:  # one cycle
        tank.turn = 0

    if tank.speed != 0:
        if keys[pygame.K_w]:
            tank.move(up=True)
        if keys[pygame.K_s]:
            tank.move(down=True)
        if keys[pygame.K_a]:
            tank.move(turn_left=True)
        if keys[pygame.K_d]:
            tank.move(turn_right=True)

    current_time = pygame.time.get_ticks()
    if current_time > next1_bullet_time:
        if keys[pygame.K_SPACE]:
            tank1_bullets.add(Bullet(bimg, tank1))
            space1_pressed = 1
        next1_bullet_time += timer_interval

    for tank1_bullet in tank1_bullets:
        if tank1_bullet.rect.colliderect(tank.rect):
            tank.endurance -= 1

            if tank.endurance == 0:
                destroy.play()
                tank.speed = 0
                tank.image = tank.destroyed_image
                tank.rect.x = tank.rect.x - 16
                tank.rect.y = tank.rect.y - 16
                screen.blit(tank.image, tank.rect)
                if show_game_over_message():
                    tank1.points +=1
                    tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=tank.points, endurance=50)
                    tank1 = Tank(tank1_image, tank1_destroyed_image, speed=5, x=width-73, y=height-80, points=tank1.points, endurance=50)
                    tank_bullets.empty()
                    tank1_bullets.empty()
                else:
                    pygame.quit()
                    sys.exit()

    current_time = pygame.time.get_ticks()
    if current_time > next_bullet_time:
        if keys[pygame.K_f]:
            tank_bullets.add(Bullet(bimg, tank))
            space_pressed = 1
        next_bullet_time += timer_interval

    for tank_bullet in tank_bullets:
        if tank_bullet.rect.colliderect(tank1.rect):
            tank1.endurance -= 1

            if tank1.endurance == 0:
                destroy.play()
                tank1.speed = 0
                tank1.image = tank1_destroyed_image
                tank1.rect.x = tank1.rect.x - 16
                tank1.rect.y = tank1.rect.y - 16
                screen.blit(tank1.image, tank1.rect)
                pygame.time.delay(2000)
                if show_game_over_message():
                    tank.points += 1
                    tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=tank.points,  endurance=50)
                    tank1 = Tank(tank1_image, tank1_destroyed_image, speed=5, x=width-73, y=height-80, points=tank1.points,  endurance=50)
                    tank_bullets.empty()
                    tank1_bullets.empty()
                else:
                    pygame.quit()

    screen.blit(tank.image, tank.rect)
    screen.blit(tank1.image, tank1.rect)

    clock.tick(100)
    pygame.display.flip()
