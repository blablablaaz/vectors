import pygame
import random
from math import sqrt

WIDTH = 800
HEIGHT = 650
FPS = 30
tile_size = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))


count = 0


def length(a):
    return int(sqrt((a[0] ** 2) + (a[1] ** 2)))


def distance(a, b):
    return length(sub(a, b))


def sum(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def normalize(a):
    la = length(a)
    if la == 0:
        return [0, 0]
    else:
        return mul(a, 1 / la)


def mul(a, b):
    return [a[0] * b, a[1] * b]


def inv(a):
    return [-a[0], -a[1]]


class Mouse(pygame.sprite.Sprite):
    mouse_image = pygame.image.load('mouse_going.jpg')

    def __init__(self, cheese, mouses, cat= None):
        pygame.sprite.Sprite.__init__(self)
        self.image = Mouse.mouse_image
        self.rect = self.image.get_rect()
        mouse_x = (random.randrange(0, WIDTH))
        mouse_y = (random.randrange(0, HEIGHT))
        self.rect.x = mouse_x
        self.rect.y = mouse_y
        self.image = pygame.transform.scale(self.image, (30, 30))  # размер мыши
        self.image.set_colorkey((255, 255, 255))
        self.pos = [mouse_x, mouse_y]
        self.vel = [0, 0]
        self.speed = 0.3
        self.cheese = cheese
        self.cat = cat
        cat.mouse = self
        self.mouses = mouses






    def update(self):
        if not self.cat or distance(self.pos, self.cat.pos) >= 100:
            self.vel = mul((normalize(sub(self.cheese.pos, self.pos))), self.speed)
        else:
            self.vel = inv(mul((normalize(sub(self.cat.pos, self.pos))), self.speed))
        for mouse in self.mouses:
            if mouse != self:
                if distance(self.pos, mouse.pos) <= 30:
                    self.vel = (mul((normalize(sub(self.pos, mouse.pos))), self.speed))
        self.pos = sum(self.pos, self.vel)







        if distance(self.pos, self.cheese.pos) <= 25:
            self.cheese.get_eaten()



        # csh - mouse
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])



        if distance(self.pos, cat.pos) <= 15:
            mouses.remove(self)
            mouse_sprite.remove(self)
            global count
            global running
            count += 1
            if count == 99 or len(mouses) == 0:
                running = False
                print('ВСЕ МЫШИ МЕРТВЫ!!!!!!!!!!!!!')




class Cheese(pygame.sprite.Sprite):
    cheese_image = pygame.image.load('cheese.jpg')


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Cheese.cheese_image
        self.rect = self.image.get_rect()
        cheese_x = (random.randrange(0, WIDTH))
        cheese_y = (random.randrange(0, HEIGHT))
        self.rect.x = cheese_x
        self.rect.y = cheese_y
        self.pos = [self.rect.x, self.rect.y]
        self.image = pygame.transform.scale(self.image, (10, 10))  # размер сыра
        self.image.set_colorkey((215, 238, 254))



    def get_eaten(self):
        mouse = Mouse(cheese, mouses, cat)
        mouse.pos = list(cheese.pos)
        mouse_sprite.add(mouse)
        mouses.append(mouse)
        self.rect.x = (random.randrange(0, WIDTH))
        self.rect.y = (random.randrange(0, HEIGHT))
        self.pos = [self.rect.x, self.rect.y]




class Cat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cat.png")
        self.image = pygame.transform.scale(self.image, (30, 35))
        self.rect = self.image.get_rect()
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.mouse = None
        self.speed = 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed / FPS
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed / FPS
        if keys[pygame.K_s]:
            self.pos[1] += self.speed / FPS
        if keys[pygame.K_d]:
            self.pos[0] += self.speed / FPS
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def walls(self):
            # Make sure the cat doesn't go outside the screen
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] > WIDTH - 30:
                self.pos[0] = WIDTH - 30

            if self.pos[1] < 0:
                self.pos[1] = 0
            elif self.pos[1] > HEIGHT - 30:
                self.pos[1] = HEIGHT - 30



pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Cat vs Mouses")
clock = pygame.time.Clock()
mouse_sprite = pygame.sprite.Group()
cheese_sprite = pygame.sprite.Group()
cheese = Cheese()
cat = Cat()
mouses = []
mouse = Mouse(cheese, mouses, cat)
mouse_sprite.add(mouse)
mouses.append(mouse)
mouse_sprite.add(cat)
cheese_sprite.add(cheese)

font = pygame.font.Font(None, 46)

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
    screen.fill('black')
    mouse_sprite.update()
    cheese_sprite.update()
    mouse_sprite.draw(screen)
    cheese_sprite.draw(screen)
    text = font.render(str(count), True, (150, 100, 100))
    screen.blit(text, (755, 20))
    pygame.display.flip()


pygame.quit()
