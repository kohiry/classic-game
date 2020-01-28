import pygame
pygame.init()

size = width, height = 800, 600


class Ball:
    def __init__(self, coord, screen, width):
        self.pos = coord
        self.x, self.y = 400, 400
        self.screen = screen
        self.width = width
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(*coord, width, width)
        self.sound = Sound()
        self.start = True

    def run(self, x, y, coord, width, height, start, flag):
        speed = (x, y)
        speeds_all = [(-400, -400), (400, 400), (400, -400), (-400, 400)]

        def help(speed):
            if flag:
                self.sound.play_jump()
                return speed
            else:
                self.sound.play_die()
                return 1, 1

        if speed == speeds_all[0]:
            if coord[0] <= start:
                return help(speeds_all[2])

            if coord[1] <= 0:
                self.sound.play_jump()
                return speeds_all[3]
            else:
                return speed

        elif speed == speeds_all[1]:
            if coord[0] >= width:
                return help(speeds_all[3])

            if coord[1] >= height:
                self.sound.play_jump()
                return speeds_all[2]
            else:
                return speed

        elif speed == speeds_all[2]:
            if coord[0] >= width:
                return help(speeds_all[0])

            if coord[1] <= 0:
                self.sound.play_jump()
                return speeds_all[1]
            else:
                return speed

        elif speed == speeds_all[3]:
            if coord[0] <= start:
                return help(speeds_all[1])

            if coord[1] >= height:
                # звук отпрыгивания
                return speeds_all[0]
            else:
                return speed
        # надо разобраться с тем, какой start пренадлежит какой координате width или height

    def who_start(self, width, height):
        if self.start:
            self.start = False
            self.x, self.y = -400, -400
        else:
            self.start = True
            self.x, self.y = 400, 400
        self.pos = width // 2, height // 2

    def rects(self):
        return pygame.Rect(*self.pos, self.width, self.width)

    def collide(self, rect, width, height, flag):
        if self.rects().colliderect(rect):
            if flag:
                self.x, self.y = self.run(self.x, self.y, self.pos, rect.x - rect.width, height, 0, True)
            else:
                self.x, self.y = self.run(self.x, self.y, self.pos,  width, height, rect.x + rect.width, True)

        else:
            self.x, self.y = self.run(self.x, self.y, self.pos, width + 200, height, 0, False)
        if self.x == 1:
            self.who_start(width, height)

    def draw(self, width, height):
        x, y = self.pos
        x += self.x // 60
        y += self.y // 60
        self.clock.tick(60)
        self.pos = (int(x), int(y))
        pygame.draw.rect(self.screen, (255, 255, 255), (*self.pos, self.width, self.width))



def transforms(sprite, width, height):
    for i in range(len(sprite)):
        sprite[i] = pygame.transform.scale(sprite[i], (width, height))

def menu_sprite():  # download sprite: list with sprite menu
    sprites = []
    for i in range(1, 12):
        sprites.append(pygame.image.load(f'data/menu_{str(i)}.png').convert())
    return sprites


class Hero:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.color = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, flag):  # flag - bool, True = вправо, False = влево
        if flag:
            self.y -= self.speed // 60
        else:
            self.y += self.speed // 60
        self.clock.tick(60)

    def rects(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.color = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(x, y, width, height)

    def AI(self, y, display_height):  # y - координата объекта ball

        if self.y + (self.height // 2) > y and self.y >= 0:
            self.y -= self.speed // 60
        elif self.y + (self.height // 2) < y and self.y <= display_height - self.height:
            self.y += self.speed // 60
        self.clock.tick(60)

    def rects(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class DrawBackground:
    def __init__(self):
        self.jump = 160
        self.width = 10
        self.height = 120
        self.text_y = 10

        self.score = {'enemy':'0', 'hero':'0'}

        font = pygame.font.Font(None, 70)
        White = (255, 255, 255)
        self.enemy_txt = font.render(self.score['enemy'], 1, (255, 255, 255))
        self.hero_txt = font.render(self.score['hero'], 1, (255, 255, 255))

    def change_score(self, who, score):
        if who == 'enemy' or who == 'hero':
            self.score[who] = score
        else:
            print('Неверные даны данные')

    def draw(self, x, Dheight, screen):
        # отрисовка поля
        for i in range(0, Dheight, self.jump):  # отрисовка разграничивающих полос на поле
            pygame.draw.rect(screen, (255, 255, 255), (x - self.width//2, i,\
                             self.width, self.height))

        # отрисовка счёта
        screen.blit(self.enemy_txt, (x // 2 - self.enemy_txt.get_width() // 2, self.text_y))  # 1/4 ширины
        screen.blit(self.hero_txt, ((x + x // 2) - self.hero_txt.get_width() // 2, self.text_y))  # 3/4


class Sound:  # class for downlod and play sound
    def __init__(self):
        self.sound = {'die_sound': pygame.mixer.Sound(r'Sound\die.ogg'),
                      'jump_sound': pygame.mixer.Sound(r'Sound\jump.ogg'),
                      'score_sound': pygame.mixer.Sound(r'Sound\score.ogg')}

    def play_die(self):
        self.sound['die_sound'].play()

    def play_jump(self):
        self.sound['jump_sound'].play()

    def play_score(self):
        self.sound['score_sound'].play()


'''
background = DrawBackground()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    background.draw(width//2, height, screen)
    pygame.display.flip()

pygame.quit()
'''
