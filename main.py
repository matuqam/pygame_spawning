from imports import *

import engine
from engine import *
from npc import make_npc
import test


pygame.init()

display = pygame.display.set_mode(size=(800, 400))
display.fill(color=SCREEN_GREY)
camera = Camera(display)
engine.camera = camera


protagonist = Entity(Rect(0,0, 16, 16), color=(250,250,250))

statics = []
for i in range(20):
    entity = Entity(Rect(i*20,i*20, 16, 16), parallax=0.5, color=(250,150,150))
    entity.movement = Vector2d(choice((-1, 1)), 0)
    statics.append(entity)

elements = statics + [protagonist]


def main_loop():
    while True:
        for event in pygame.event.get():
            EventManager.manage_event(event, protagonist)

        camera.move()
        camera.shake()
        # protagonist.move()

        display.fill(color=(150,150,150))

        for element in sorted(elements, key=lambda e: e.parallax, reverse=False):
            element.move()
            pygame.draw.rect(camera.surface, color=element.color, rect=camera_draw(camera, element.rect, element.parallax))

        pygame.display.update()

##
#  TESTING
# ##### 
# test.screen = display
# test.mydo()

main_loop()

