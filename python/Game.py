import pygame, time, sys, os

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init()

# define some constants
screenWidth = 400
screenHeight = 1200
ballRadius = 75
startPos =100
drec = 1
V = 0

# Physical Constants
Accel = 9.8
br = ballRadius/1000
CA = 3.14*(br*br)           # Crossectional Area
Cd = .5                     # Coeficient of Drag
p = 1.225                   # Density of air STP
m = 20                      # mass of the ball.
ba = .85                    # ball efficiency

FRAME_RATE = 10
TIME_STEP = 1 / FRAME_RATE

screen = pygame.display.set_mode([screenWidth,screenHeight])


def nextPosition(s, v, time):
    nextPos = round(s + v * time,0)
    # print(f'next position ---> {nextPos}')
    return nextPos

def nextVelocity(v, a, time):
    windResistance = (.5*p*(v*v)*Cd*CA)/m
    A = a - (windResistance * drec)
    nextVelo = v + A * time
    print(f'next velo ---> {nextVelo}, {v} , {a} ')
    print(f'Wind Resistance ---> {windResistance} {CA}')
    nextVelo = round(nextVelo,10)
    return nextVelo

# Key Controls
def reset(k):
    global startPos
    if k[K_DOWN]:
        startPos = 100
    

# this is the game loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    my_timer = pygame.time.get_ticks()/1000
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,255), (250,startPos), ballRadius)
    pygame.display.flip()

    #see where the ball will be next
    next_y = nextPosition(startPos, V, TIME_STEP)

    # Will the ball hit the floor?
    if next_y + ballRadius > screenHeight:
        V = round((-V * ba),1)
        drec = -drec
    
    # compute the next steps
    startPos = nextPosition(startPos, V, TIME_STEP)
    print(f'next pos ---> {startPos}')
    V = nextVelocity(V, 9.8, TIME_STEP)
    print(f'next velocity ---> {V}')
    
    reset(keys)

    # print(my_timer)




pygame.quit
