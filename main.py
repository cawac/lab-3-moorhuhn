import random
import sys
import pygame
import random as rnd

speed = 200
FPS = 60


class Gun:
    def __init__(self):
        self.clip = 10
        self.capacity_of_clip = 10
        self.timer = 0

    def shoot(self):
        if self.capacity_of_clip > 0 and pygame.time.get_ticks() > self.timer:
            random.choice(shoots).play()
            self.capacity_of_clip -= 1
        else:
            pass  # sound of empty clip

    def reload(self):
        if pygame.time.get_ticks() > self.timer:
            self.capacity_of_clip = self.clip
            reload.play()
            self.timer = pygame.time.get_ticks() + 2000


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.foto = random.randint(0, 12)
        self.image = pygame.transform.flip(alive_bird_list[self.foto], True, False)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = -1

    def draw(self, display):
        display.blit(self.image, self.rect)
        if self.foto + 1 < 12:
            self.foto += 1
        else:
            self.foto = 0
        self.image = pygame.transform.flip(alive_bird_list[self.foto], True, False)
        self.rect = pygame.Rect(self.rect[0], self.rect[1], self.image.get_width(), self.image.get_height())
        self.rect[0] -= self.speed


# def dying(bird):
#     pass

# def shoot_up(pos, birds):
#     for bird in birds:
#         if pos in bird.rect:
#             return bird
#     else:
#         return None


def add_birds_to_background(background: pygame.image, birds: list) -> pygame.image:
    updated_background = background.copy()
    for bird in birds:
        bird.draw(updated_background)
    return updated_background


pygame.init()
pygame.mixer.init()
# initialize
screen = pygame.display.set_mode((1280, 653))
alive_bird_list = [pygame.image.load("sprites/alive bird/bird-sprite(" + str(i) + ").png").convert_alpha() for i in
                   range(13)]
bullet = pygame.image.load("sprites/Cartridge_cross_section.svg.png").convert_alpha()
Top = pygame.image.load("backgrounds/TopBackground.png").convert_alpha()
Middle = pygame.image.load("backgrounds/MiddleBackground.png").convert_alpha()
Bottom = pygame.image.load("backgrounds/BottomBackground.png").convert_alpha()
Backgrounds = [Bottom, Middle, Top]
# make backgrounds
birds = [[Bird(0, random.randint(100, 300)) for i in range(random.randint(2, 6))] for j in range(3)]
pygame.mouse.set_visible(False)
cursor_img = pygame.image.load("sprites/new_cursor.png")
cursor_img = pygame.transform.scale(cursor_img, (100, 100))
cursor_img_rect = cursor_img.get_rect()
# make cursor
pygame.mixer.music.load('music/bg_music.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
shoots = [pygame.mixer.Sound("sound effects/shoot" + str(var) + ".wav") for var in range(3)]
for shoot in shoots:
    shoot.set_volume(0.2)
reload = pygame.mixer.Sound("sound effects/reload.wav")
reload.set_volume(0.2)
# make sound
pygame.display.set_caption("Beta")
clock = pygame.time.Clock()
camera_pos_x = 0
running = True
gun = Gun()
f1 = pygame.font.Font(None, 36)
text1 = f1.render('SCORE: ', True,
                  (255, 255, 255))
total_score = 0
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # and have_bullet():
                gun.shoot()
            if event.button == 3:
                gun.reload()
            mouse_pos = pygame.mouse.get_pos()
            # if event.button == 1:
            #     killed = shoot_up(mouse_pos, birds)
            #     if killed:
            #         dying(killed)
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         birds.append(Bird(rnd.randint(0, 400), rnd.randint(0, 400), rnd.randint(5, 15), rnd.randint(5, 15)))
    kpressed = pygame.key.get_pressed()
    if kpressed[pygame.K_LEFT] and camera_pos_x > 0:
        camera_pos_x -= 1
    elif kpressed[pygame.K_RIGHT] and camera_pos_x < 300:
        camera_pos_x += 1
    currentBottom = Bottom.copy()
    screen.blit(add_birds_to_background(Bottom, birds[0]),
                (-camera_pos_x * ((Bottom.get_width() - screen.get_width() + 0.) / speed), 0))
    screen.blit(add_birds_to_background(Middle, birds[1]),
                (-camera_pos_x * ((Middle.get_width() - screen.get_width() + 0.) / speed), 76))
    screen.blit(add_birds_to_background(Top, birds[2]),
                (-camera_pos_x * ((Top.get_width() - screen.get_width() + 0.) / speed), 0))
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position
    screen.blit(cursor_img, cursor_img_rect)  # draw the cursor
    for bul in range(gun.capacity_of_clip):
        screen.blit(pygame.transform.scale(bullet, (bullet.get_width() / 3., bullet.get_height() / 3.)), (1200 - 45 * bul, 500))
    screen.blit(text1, (1100, 0))
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
