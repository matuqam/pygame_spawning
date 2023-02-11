import pygame
from pygame.locals import *

from npc import make_npc

SCREEN_RED=(200, 10, 10)
SCREEN_GREEN=(10, 200, 10)
SCREEN_BLUE=(10, 10, 200)
SCREEN_GREY=(125,125,125)


def myvars():
    # global obj
    # global face
    global update
    # obj = Rect
    # face = pygame.Surface
    update = pygame.display.update

def mystuff():
    global avatar_obj
    global avatar_face
    # global npcs
    # dim=(8,16)
    # avatar_obj = Rect(0,0,*dim)
    # avatar_face = pygame.Surface(dim)
    # screen.blit(avatar_face, avatar_obj)

def myrandom_npcs(n=10):
    # global npcs
    npcs = []
    for i in range(n):
        npcs.append(make_npc(size=(4,4), screen=screen))
    return npcs

def mydo():
    myvars()
    mystuff()
    for i in range(16):
        myrandom_npcs(1000)
        update()
    # myrandom_npcs(60000)
    # update()


pygame.init()

# init screen
screen = pygame.display.set_mode(size=(800, 400))
screen.fill(color=SCREEN_GREY)
pygame.display.update()


def move_by_update_only_rect(obj, face, x, y, parent_surface):
    '''
    move rect obj by x and y
    draw object image on parent_surface (aka sprite on screen)
    refresh parent_surface (aka screen) by using fill
    update display'''
    
    obj.x += x; obj.y +=y
    parent_surface.fill(SCREEN_RED)
    parent_surface.blit(face, obj)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

##
#  TESTING
# ##### 
mydo()

