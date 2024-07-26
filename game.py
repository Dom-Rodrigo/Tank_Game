import sys, pygame
from tank import Tank
from bullet import Bullet

pygame.mixer.init()
pygame.init()

# sound of bullets
sound_bullet=pygame.mixer.Sound("shot.wav")
metal_impact=pygame.mixer.Sound("metal_impact.wav")

# destruction sounds
destroy = pygame.mixer.Sound("explosao.wav")

size = width, height = 900, 700
tank_width, tank_height = 100, 100
grey = 112, 112, 112

screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

#define font
font=pygame.font.SysFont("arialblack", 40)

#define colors
TEXT_COL=(255,255,255)

def draw_text(display_text, font, text_col, x, y):
    img = font.render(display_text, True, text_col)
    screen.blit(img, (x, y))
def show_menu():
    menu=True
    while menu:
       screen.fill((52,78,91))
       draw_text('TANK GAME', font, TEXT_COL, (width//2)-150, 100)
       draw_text("Press P to play", font, TEXT_COL, (width//2)-150, 200)
       draw_text("Press Q to quit", font, TEXT_COL, (width//2)-150, 300)

       for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                     menu=False
                if event.key == pygame.K_q:
                     pygame.quit()
                     sys.exit()
       pygame.display.update()
       clock.tick(60)
def main():

   positions = [[0, 0], [width-73, width-73], [0, width-73]]
   tank_destroyed_image = pygame.image.load("tank1_destroyed.png").convert_alpha()

   tank_image = pygame.image.load("tank.png").convert_alpha()
   tank = Tank(tank_image, tank_destroyed_image, speed=5, x=0, y=0, points=0, endurance=60, k_up=pygame.K_UP, k_down=pygame.K_DOWN, k_left=pygame.K_LEFT, k_right=pygame.K_RIGHT, k_fire=pygame.K_SPACE, space_pressed=0, next_bullet_time=100, timer_interval=100)

   tank1_image = pygame.image.load("tank1.png").convert_alpha()
   tank1 = Tank(tank1_image, tank_destroyed_image, speed=5, x=width-73, y=width-73, points=0, endurance=60,  k_up=pygame.K_w, k_down=pygame.K_s, k_left=pygame.K_a, k_right=pygame.K_d, k_fire=pygame.K_f, space_pressed=0, next_bullet_time=100, timer_interval=100)


   tank2_image = pygame.image.load("tank2.png").convert_alpha()
   tank2 = Tank(tank2_image, tank_destroyed_image, speed=5, x=0, y=width-73, points=0, endurance=60,  k_up=pygame.K_u, k_down=pygame.K_j, k_left=pygame.K_h, k_right=pygame.K_k, k_fire=pygame.K_o, space_pressed=0, next_bullet_time=100, timer_interval=100)

   bimg = pygame.image.load("bullet.png")
   tanks = pygame.sprite.Group()
   tanks.add(tank)
   tanks.add(tank1)
   tanks.add(tank2)
   run_game = True
   while run_game:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_q:
                   pygame.quit()
                   sys.exit()
               if event.key == pygame.K_p:
                   show_menu()
       screen.fill(grey)
       tanks_points = []
       for tank in tanks:
           tanks_points.append(tank)
       placar = font.render(f"Green {tanks_points[0].points} x Red {tanks_points[1].points} x Blue {tanks_points[2].points}", True, (20, 20, 20))
       screen.blit(placar, (width//2 - placar.get_width()//2, 0))
       keys = pygame.key.get_pressed()
       movement(tanks, screen, keys)
       firing(tanks, screen, keys,bimg,positions)
       clock.tick(100)
       pygame.display.flip()
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
def firing(tanks, screen, keys,bimg,positions):
        for tank in tanks:
            screen.blit(tank.image, tank.rect)
            current_time = pygame.time.get_ticks()

            if current_time > tank.next_bullet_time:
                if keys[tank.k_fire]:
                    if len(tank.bullets) < 10:
                        tank.bullets.add(Bullet(bimg, tank))
                        tank.space_pressed = 1
                        sound_bullet.play(maxtime=500)

                    else:
                        pass
                    print(len(tank.bullets))
                tank.next_bullet_time += tank.timer_interval

                # WORKS UNTIL HERE
                for bullet in tank.bullets:
                    if pygame.sprite.spritecollideany(bullet, tanks):
                        metal_impact.play(maxtime=300)
                        collided = pygame.sprite.spritecollideany(bullet, tanks)
                        collided.endurance -= 1
                        if collided.endurance == 0:
                            bullet.tank.bullets.empty()
                            screen.blit(collided.destroyed_image, (collided.rect.x-16, collided.rect.y-16))
                            bullet.tank.points +=1
                            collided.endurance = 60
                            i = 0;
                            for tank in tanks:
                                tank.update(positions[i][0], positions[i][1])
                                i+=1
                            if show_game_over_message():
                                restart_game(tanks, positions)
                            else:
                                pygame.quit()
                                sys.exit()
def restart_game(tanks, positions):
    for i, tank in enumerate(tanks):
        tank.endurance = 60
        #tank.points = 0
        tank.rect.topleft = positions[i]
        tank.bullets.empty()
        #colocar os placares

if __name__ == "__main__":
    clock = pygame.time.Clock()
    show_menu()
    main()
