from pygame import*
import random

'''mixer.init()
mixer.music.load('mainmenu.ogg')
mixer.music.play(-1)'''

window_widht =700
window_height =500

window = display.set_mode((700,500))
display.set_caption('лабиринт')

back_color = (155,155,155)
window.fill(back_color)
back_ground = transform.scale(image.load('back.jpeg'),(700,500))

win_back_ground = transform.scale(image.load('win.jpeg'),(700,500))

lose_back_ground = transform.scale(image.load('lose.jpeg'),(700,500))

font.init()
font = font.SysFont('Calibri', 40,bold = True, italic = True)
win_text = font.render('You win!!!!!', True, (160, 162, 163))
lose_text = font.render('посиди подумай', True, (230, 235, 235))

class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.picture = picture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


bombs = GameSprite('bomb.png', 70,70,300,230)

class Enemy(GameSprite):
    def __init__(self, picture,w,h,x,y,speed):
        super().__init__(picture, w,h,x,y)
        self.speed = speed
        self.direction_x = 'right'
        self.direction_y = 'up'

    def update(self,x1,y1,x2,y2):
        if self.rect.x <= x1:
            self.direction_x = 'right'
        if self.rect.x >= x2:
            self.direction_x = 'left'
        if self.direction_x == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
'''        if self.rect.y <= y1:
            self.direction_y = 'up'
        if self.rect.y >= y2:
            self.direction_y = 'down'
        if self.direction_y == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed'''

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__ (picture, w,h,x,y)
        self.speed = speed

    def update(self, direction):
        if direction == 'right':
            self.rect.x += self.speed
        if self.rect.x > 1000 or self.rect.x < -50:
            self.kill()





walls = sprite.Group()
walls.add(GameSprite('wall.png',100,400,200,220))
walls.add(GameSprite('wall.png',300,50,130,190))
walls.add(GameSprite('wall.png',80,300,0,330))
walls.add(GameSprite('wall.png',80,80,350,-10))
walls.add(GameSprite('wall.png',250,30,350,60))
walls.add(GameSprite('wall.png',200,400,570,200))
walls.add(GameSprite('wall.png',80,80,0,0)) 
walls.add(GameSprite('wall.png',50,200,400,190)) 
walls.add(GameSprite('wall.png',10,500,0,0))
walls.add(GameSprite('wall.png',400,10,0,0)) 
walls.add(GameSprite('wall.png',700,10,0,490)) 

cts = sprite.Group()
cts.add(Enemy('tvar.png', 70,70,630,90,50))



class Player(GameSprite):
    def __init__(self, picture,w,h,x,y,speed_x,speed_y):
        super().__init__(picture,w,h,x,y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.left = True  
    def update(self):
        self.rect.x += self.speed_x
        
        if self.speed_x == 0:
            self.rect.y += self.speed_y
        else:
            self.speed_y = 0

        walls_touch = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            self.left = False
            for wall in walls_touch:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            if self.left != True:
                self.left = False






            for wall in walls_touch:
                self.rect.left = max(self.rect.left, wall.rect.right)
        
        if self.speed_y > 0:
            for wall in walls_touch:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        elif self.speed_y < 0:
            for wall in walls_touch:
                self.rect.top = max(self.rect.top, wall.rect.bottom)

    def fire(self):
        bullet = Bullet('pula.png',15,20, self.rect.centerx, self.rect.centery,15)
        bullets.add(bullet)

bullets = sprite.Group()

player = Player('terrorist.png',70,70,100,400,5,5)

def move(pers):
    keys_pressed = key.get_pressed()
    if keys_pressed[K_SPACE]:
        pers.fire()
    if keys_pressed[K_d]:
        pers.speed_x = 5
        pers.left = False

    elif keys_pressed[K_a]:
        pers.speed_x = -5
        pers.left = True

    else:
        pers.speed_x = 0

    if keys_pressed[K_s]:
        pers.speed_y = 5
        

    elif keys_pressed[K_w]:
        pers.speed_y = -5

    else:

        pers.speed_y = 0

run = True

finish = ''

while run:
    if finish == '':
        move(player)
        player.update()

        window.blit(back_ground,(0,0))
        walls.draw(window)
        sprite.groupcollide(bullets,cts,True,True)
        sprite.groupcollide(bullets,walls,True,False)
        
        bullets.draw(window)





        for bullet in bullets:
            bullet.update('right')

        for ct in cts:
            ct.reset()
            ct.update(90,610,610,90)

            if sprite.collide_rect(player, ct):
                finish = 'lose'

        bombs.reset()
        
        player.reset()  

        if sprite.collide_rect(player, bombs):
            finish = 'win'

    else:
        if finish == 'win':
            window.blit(win_back_ground,(0,0))
            window.blit(win_text,(230,230))
        else:
            window.blit(lose_back_ground,(0,0))
            window.blit(lose_text,(230,200))

    for e in event.get():
        if e.type == QUIT:
            run = False  

    display.update()
    time.delay(17)
    