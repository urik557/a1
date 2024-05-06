from pygame import *
mixer.init()
font.init()
from random import *
from time import time as timer

win_width = 700
win_height = 500
win = display.set_mode((win_width,win_height))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.music.load('space.ogg')
mixer.music.play()

monsters = sprite.Group()
asteroids = sprite.Group()

lost = 0
pop = 0
life = 3

font1 = font.SysFont('Arial',30)
font2 = font.SysFont('Arial',70)
font_win = font2.render('YOU WIN!',True,(254,242,0))
font_lose = font2.render('YOU LOSE!',True,(255,19,0))






class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
    
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def go(self):
            keys_pressed = key.get_pressed()

            if keys_pressed[K_a] and self.rect.x > 5:
                self.rect.x -= self.speed
            
            if keys_pressed[K_d] and self.rect.x < 630:
                self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        global bullets
        bullets.add(bullet)

        

class Enemy_Monsters(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50,win_width-50)
            lost = lost + 1
          
class Enemy_Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50,win_width-50)

bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y < 0:
            self.kill()
    

rocket = Player('rocket.png',20,430,70,60,10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy_Monsters('ufo.png',randint(50,win_width-50),-40,80,50,randint(1,5))
    monsters.add(monster)

for i in range(1,4):
    asteroid = Enemy_Asteroid('asteroid.png',randint(50,win_width-50),-40,80,50,randint(1,5))
    asteroids.add(asteroid)



finish = False
play_game = True
rel_time = False #фаг перезарядки(есть ли перезарядка)
col_bullet = 0
while play_game:

    for i in event.get():
        if i.type == QUIT:
            play_game = False
    
    keys_pressed = key.get_pressed()

    if keys_pressed[K_SPACE]:
        if col_bullet < 5 and  rel_time == False:   
            fire_music = mixer.Sound('fire.ogg')
            fire_music.play()
            rocket.fire()
            col_bullet += 1


        if col_bullet >= 5 and rel_time == False:
            start_time = timer()
            rel_time = True


    
    if not finish:
        
        win.blit(background,(0,0))
        rocket.reset()
        rocket.go()  
        monsters.draw(win)
        monsters.update()
        asteroids.draw(win)
        asteroids.update()
        bullets.draw(win)
        bullets.update()

        if rel_time == True:
            now_time = timer()

            if now_time - start_time < 3:
                reload = font1.render('Wait, reload...',1,(150,0,0))
                win.blit(reload,(260,460))
                
            else:
                col_bullet = 0
                rel_time = False


        if sprite.spritecollide(rocket,monsters,True):
            if life == 0:
                finish = True
                win.blit(font_lose,(200,200))
                life -= 1
            else:
                life -= 1

        if lost >= 3:
            finish = True
            win.blit(font_lose,(200,200))

        if sprite.spritecollide(rocket,asteroids,True):
            if life == 1:
                finish = True
                win.blit(font_lose,(200,200))
                life -=1

           
            else:
                life -= 1
        
        if pop != 10:
            if sprite.groupcollide(monsters,bullets,True,True):
                pop += 1
                monster = Enemy_Monsters('ufo.png',randint(50,win_width-50),-40,80,50,randint(1,5))
                monsters.add(monster)


        
        else:
            finish = True
            win.blit(font_win,(200,200))


        text_lost = font1.render('Пропущено:'+str(lost),1,(255,255,255))
        text_win = font1.render('Сбито:'+str(pop),1,(255,255,255))
        lifes = font1.render('Жизней:'+str(life),1,(0,190,0))
        win.blit(text_win,(5,10))
        win.blit(text_lost,(5,30))
        win.blit(lifes,(580,10))



        display.update()
        clock = time.Clock()
        clock.tick(60)
    
    



