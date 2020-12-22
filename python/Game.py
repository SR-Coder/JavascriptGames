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
screenHeight = 800
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
ba = .90                    # ball efficiency

FRAME_RATE = 1
TIME_STEP = 1 / FRAME_RATE

screen = pygame.display.set_mode([screenWidth,screenHeight])


def nextPosition(s, v, time):
    nextPos = round(s + v * time,0)
    # print(f'next position ---> {nextPos}')
    return nextPos

def nextVelocity(v, a, time):
    windResistance = (.5*p*(v*v)*Cd*CA)/m
    A = a - (windResistance) # make sure that resistance is always a factor.  will have to apply this to x directions as well
    print(f'Cumulative Accel ---> {A}')
    nextVelo = v + A * time
    print(f'Wind Resistance ---> {windResistance} {CA}')
    nextVelo = round(nextVelo,10)
    return nextVelo

# Key Controls
def reset(k):
    global startPos
    if k[K_DOWN]:
        startPos = 100
        ba = .95
        V = 0
    
def pause(k):
    if k[K_UP]:
        time.sleep(2)
    return False

# this is the game loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    my_timer1 = pygame.time.get_ticks()/1000
    print(my_timer1)
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,255), (250,startPos), ballRadius)
    pygame.display.flip()

    #see where the ball will be next
    next_y = nextPosition(startPos, V, TIME_STEP)

    # Will the ball hit the floor?
    if next_y + ballRadius >= screenHeight:
        # Decrease ball effeciency if it bounces closer to the ground
        abV = abs(V)
        print(abV)
        if abV<16 and abV > 5 and ba>0.1:
            ba = ba - .01
            print(f'here ------------------------------> {ba}')
        V = (-V * ba)
        drec = -drec
    
    # compute the next steps
    startPos = nextPosition(startPos, V, TIME_STEP)
    print(f'next pos ---> {startPos}')
    V = nextVelocity(V, 9.8, TIME_STEP)
    print(f'next velocity ---> {V}, ball Efficiency---->>> {ba}')
    
    reset(keys)
    pause(keys)

    # print(my_timer)


    my_timer2 = pygame.time.get_ticks()/1000
    TIME_STEP = (my_timer2-my_timer1)*15
    print(f'TIME STEP -------------> {TIME_STEP}')
pygame.quit
