from imports import *
from npc import make_npc

screen = None  # set in main.py


def myvars():
    global update
    update = pygame.display.update

def mystuff():
    global avatar_obj
    global avatar_face

def myrandom_npcs(n=10):
    npcs = []
    for i in range(n):
        npcs.append(make_npc(size=(16,16), screen=screen))
    return npcs

def mydo():
    myvars()
    mystuff()
    myrandom_npcs(10)
    update()