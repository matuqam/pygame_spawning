'''
manage movement considering colisions'''
from typing import Tuple

from pygame.locals import *


def compute_destination(obj, movement)->Tuple[int, int]:
    '''obj: pygame.Rect, object to move
    movement: Tuple[int, int], x and y modifications to be applied
    returns: Tuple[int, int] destination coordinates
    '''
    return (obj.x+movement[0], obj.y+movement[1])

def destination_available(obj, destination)->bool:
    pass