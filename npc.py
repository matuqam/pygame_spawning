from imports import *

import pygame
from pygame.locals import *


def make_npc(obj:Rect=None, face:pygame.Surface=None, pos:Tuple[int, int]=None, 
        size:Tuple[int,int]=None, screen=None, update=False)->Rect:
    '''Return Rect according to provided params or defaults to size 1x1 at random_pos* on screen
    optinally places rect's Surface on screen and updates screen
    if no screen is given, coordinates are (random(0,1) random(0,1))
    '''
    if obj is None:
        if size is None:
            size = (1,1)
        if pos is None:
            pos = _random_location(screen)
        obj = Rect(*pos, *size)
    if size is None:
        size = (obj.width, obj.height)
    if face is None:
        face = pygame.Surface(size=size)
        face.fill(REDISH)
    if screen is not None:
        screen.blit(face, obj)
        if update:
            pygame.display.update()
    return obj

def _random_location(screen=None):
    if screen is None:
        return randint(0,1)
    return (randint(0, screen.get_width()), randint(0, screen.get_height()))


    

