#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
display.set_caption("Shooter game")
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
run = True
class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def disp(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class player(Gamesprite):
    def ctrl(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 695:
            self.rect.x += self.speed
    def fire(self):
        bullets = bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        peluru.add(bullets)
class enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1
class bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
peluru = sprite.Group()

score = 0
font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 100)
monsters = sprite.Group()
for e in range(1, 6):
    alien = enemy('ufo.png', randint(80, 480), -80, 80, 50, randint(1, 2))
    monsters.add(alien)
asteroids = sprite.Group()
for e in range(1, 3):
    asteroid = enemy('asteroid.png', randint(80, 480), -80, 80, 50, randint(1, 2))
    asteroids.add(asteroid)
lost = 0
num_fire = 0
ship = player('rocket.png', 100, 400, 80, 100, 10)
finish = False
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False :
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Score:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        txtlose = font2.render("Missed:" + str(lost), 1, (255, 255, 255))
        window.blit(txtlose, (10, 45))
        ship.disp()
        ship.ctrl()
        monsters.update()
        monsters.draw(window)
        peluru.update()
        peluru.draw(window)
        asteroids.update()
        asteroids.draw(window)
        collide = sprite.groupcollide(monsters, peluru, True, True)
        collides = sprite.groupcollide(asteroids, peluru, True, True)
        for c in collide:
            score = score + 1
            monster = enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
        for c in collides:
            score = score + 1
            asteroid = enemy('asteroid.png', randint(80, 480), -80, 80, 50, randint(1, 2))
            asteroids.add(asteroid)
        if score >= 10:
            win = font3.render("You win", 1, (255, 231, 1))
            window.blit(win, (200, 200))
            finish = True
        if lost > 90 or sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            lose = font3.render("You lose", 1, (124, 10, 10))
            window.blit(lose, (200, 200))
            finish = True
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        
        
    display.update()
    clock.tick(60)
time.delay(50)
