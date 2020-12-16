import pygame, time

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
screenWidth = 1200
screenHeight = 800
ballRadius = 75
startPos =100
V = 0
Accel = 9.8

FRAME_RATE = 4
TIME_STEP = 1 / FRAME_RATE

screen = pygame.display.set_mode([screenWidth,screenHeight])


def nextPosition(s, v, time):
    nextPos = s + v * time
    # print(f'next position ---> {nextPos}')
    return nextPos

def nextVelocity(v, a, time):
    nextVelo = v + a * time
    print(f'next velo ---> {nextVelo}, {v} , {a} ')
    nextVelo = round(nextVelo,2)
    return nextVelo

# this is the game loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    my_timer = pygame.time.get_ticks()/1000
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,255), (250,startPos), ballRadius)
    pygame.display.flip()

    #see where the ball will be next
    next_y = nextPosition(startPos, V, TIME_STEP)

    # Will the ball hit the floor?
    if next_y + ballRadius > 800:
        V = round((-V * .750),1)
    
    # compute the next steps
    startPos = nextPosition(startPos, V, TIME_STEP)
    print(f'next pos ---> {startPos}')
    V = nextVelocity(V, 9.8, TIME_STEP)
    print(f'next velocity ---> {V}')

    # print(my_timer)




pygame.quit
