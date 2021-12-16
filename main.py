from typing_extensions import runtime
import pygame
import math
import random

#------------------------------#

pygame.init()  # 1

WIDTH = 800   # 18
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # 2
pygame.display.set_caption('Cow VS Covid-19 By B1ackmonday')  # 5
icon = pygame.image.load('icon.png') # 6
pygame.display.set_icon(icon)  # 7
background = pygame.image.load('bg.png')

############## COW ##############

psize = 128  # 8 (Player) 

pimg = pygame.image.load('cow.png')
px = 100
py = HEIGHT - psize  
pxchange = 0 # 15

def Player(x,y):
    screen.blit(pimg,(x,y))

############## EMEMY #############

esize = 32
eimg = pygame.image.load('virus.png') # 20
ex = 50
ey = 0
eychange = 1
def Enemy(x,y):
    screen.blit(eimg,(x,y))

########### MULTI ENEMY ##########

exlist = []
eylist = []
ey_change_list = [] # enemy speed
allenemy = 5

for i in range(allenemy):
    exlist.append(random.randint(50,WIDTH - esize))
    eylist.append(random.randint(0,100))
    # ey_change_list.append(random.randint(1,5)) # enemy random speed
    ey_change_list.append(1) # annual speed by 1 then increase after shooted

############## MEAT ##############
msize = 32
mimg = pygame.image.load('beef.png')
mx = 100
my = HEIGHT - psize
mychange = 20 # speed player
mstate = 'ready'

def fire_meat(x,y):
    global mstate
    mstate = 'fire'
    screen.blit(mimg,(x,y))

########## COLLISION #############

def isCollision(ecx,ecy,mcx,mcy):
    distance = math.sqrt(math.pow(ecx - mcx,2)+math.pow(ecy - mcy,2))
    print(distance)
    if distance < (esize / 2) + (msize / 2): # collision distance
        return True
    else:
        return False

########## SCORE #############

allscore = 0
fontscore = pygame.font.Font('arial.ttf',20)

def showscore():
    score = fontscore.render('Points: {}'.format(allscore),True,(125, 125, 125))
    screen.blit(score,(30,30))

########## SOUND #############

pygame.mixer.music.load('field.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sound = pygame.mixer.Sound('cowsound.wav')
sound.play()

########## GAME OVER #############

fontover = pygame.font.Font('arial.ttf',50)
fontover2 = pygame.font.Font('arial.ttf',30)
playsound = False
gameover = False
def Gameover():
    global playsound
    global gameover
    overtext = fontover.render('Game Over',True,(225,0,0))
    screen.blit(overtext,(260,200))
    overtext2 = fontover2.render('Press [N] New Game',True,(125, 125, 125))
    screen.blit(overtext2,(250,255))
    if playsound == False:
        gsound = pygame.mixer.Sound('gameover.mp3')
        gsound.play()
        playsound = True
    # if gameover == False:
    #     gameover = True

########## GAME LOOP #############

running = True  # 3
clock = pygame.time.Clock()  # 12
FPS = 30

while running:   # 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pxchange = -20
            if event.key == pygame.K_RIGHT:
                pxchange = 20
            
            if event.key == pygame.K_SPACE:
                if mstate == 'ready':
                    sound = pygame.mixer.Sound('chop.mp3')
                    sound.play()
                    mx = px + 50 # position meat
                    fire_meat(mx,my)
            if event.key == pygame.K_n:
                # gameover = False
                playsound = False
                allscore = 0
                for i in range(allenemy):
                    eylist[i] = random.randint(0,100)
                    exlist[i] = random.randint(50,WIDTH - esize)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pxchange = 0

########## RUN PLAYER ##########
    
    Player(px,py)  # 9

#--------LEFT RIGHT------------#
    
    if px <= 0:   # 14
        px = 0    
        px += pxchange  # 16
    elif px >= WIDTH - psize:
        px = WIDTH - psize
        px += pxchange # 17
    else:
        px += pxchange
    
######## RUN ENEMY SINGLE ########

    # Enemy(ex,ey)
    # ey += eychange

    collision = isCollision(ex,ey,mx,my)
    if collision:
        my = HEIGHT - psize
        mstate = 'ready'
        ey = 0
        ex = random.randint(50,WIDTH - esize) 
        allscore += 10
        
######## RUN MULTI ENEMY #########

    for i in range(allenemy):
        # increase enemy speed
        if eylist[i] > HEIGHT - esize and gameover == False:
            for i in range(allenemy):
                eylist[i] = 800
            Gameover()
            break       

        eylist[i] += ey_change_list[i]
        collisionmulti = isCollision(exlist[i], eylist[i],mx,my)
        if collisionmulti:
            my = HEIGHT - psize
            mstate = 'ready'
            eylist[i] = 0
            exlist[i] = random.randint(50,WIDTH - esize)
            allscore += 10
            ey_change_list[i] += 1 # make increase speed
            sound = pygame.mixer.Sound('broken.wav')
            sound.play()
        Enemy(exlist[i], eylist[i])

########## FIRE MEAT ##########

    if mstate == 'fire':
        fire_meat(mx,my)
        my = my - mychange # my -= mychange
    
    if my <= 0:
        my = HEIGHT - psize
        mstate = 'ready'

    showscore()    
    print(px,py)
    pygame.display.update() # 10
    pygame.display.flip() # 19
    pygame.event.pump()
    screen.fill((0,0,0)) # solving image mess paint
    screen.blit(background,(0,0))
    clock.tick(FPS)


        
    


