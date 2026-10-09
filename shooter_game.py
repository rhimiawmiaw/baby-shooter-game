from pygame import *
from random import*
#rom time import*
win_width = 700
win_height = 500
game_time = 50
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
win = mixer.Sound('yippe.mp3')
lose_music = mixer.Sound('german-song_bthHEHd.mp3')
score = 0
bullets_scream = mixer.Sound('bayi.mp3')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x , player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y)) 
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width-80:
           self.rect.x += self.speed
   def tembak(self):
       bullet = BUllet("ufo.png", self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
class Enemy(GameSprite):
   direction = "left"
   def update(self):
       self.rect.y += self.speed
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)  
           self.rect.y = 0 

class BUllet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
font.init()
font1 = font.Font(None, 70) 
font2 = font.Font(None, 40)
win = font1.render('YIPPE MENANG COY!', True, (255, 215, 0))
lose = font1.render('BARIS SANA DI LAPANG KAU GGRRRRRRRRRRRRRRRR!', True, (180, 0, 0))     
player = Player('ufo.png', 5, 420,80,50, 2)
enemy = Enemy('asteroid.png', 700-80, 280, 80, 80, 4)
game = True
finish = False
clock = time.Clock()

start_ticks = time.get_ticks()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullets_scream.play()
                player.tembak()
                score+= 1
    if finish != True:
        window.blit(background,(0,0))
        seconds = (time.get_ticks() - start_ticks) // 1000 
        remaining_time = game_time - seconds
        player.update()
        enemy.update()
        player.reset()
        enemy.reset()
        bullets.update()
        bullets.draw(window)
        text = font2.render("Anak:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        time_label = font2.render('Time:'+ str(max(0, remaining_time)), True, (255, 153, 51))
        window.blit(time_label, (10, 80))
        if sprite.collide_rect(player, enemy):
            finish = True
            window.blit(lose, (0, 200))
            lose_music.play()
        collides = sprite.spritecollide(enemy, bullets, True)
        if collides: 
            enemy = Enemy('asteroid.png', 700-80, 280, 80, 80, 4)

        if remaining_time <= 0:
            finish = True  
            window.blit(win, (50, 200))  
    display.update()
    clock.tick(FPS)
