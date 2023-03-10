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


protagonist = Entity(Rect(0,0, 24, 24), color=(250,250,250), speed=2)

statics = []
for i in range(20):
    entity = Entity(Rect(i*20+60,i*20, 16, 16), parallax=1, color=(250,150,150))
    entity.add_destination(Vector2d(50, 380))
    entity.add_destination(Vector2d(randint(0, display.get_width()), randint(0, display.get_height())))
    entity.add_destination(Vector2d(randint(0, display.get_width()), randint(0, display.get_height())))
    entity.add_destination(Vector2d(randint(0, display.get_width()), randint(0, display.get_height())))
    statics.append(entity)

# elements = statics + [protagonist]
elements = Entities(protagonist, statics)


def main_loop():
    while True:
        for event in pygame.event.get():
            EventManager.manage_event(event, protagonist)

        display.fill(color=(150,150,150))

        camera.move()
        camera.shake()
        # protagonist.move()

        # manage collisions with protagonist
        elements.tick()

        protagonist.move()

        # for element in sorted(elements, key=lambda e: e.parallax, reverse=False):
        for element in sorted(elements.entities, key=lambda e: e.parallax, reverse=False):
            element.move()

        for element in sorted(elements.entities+[protagonist], key=lambda e: e.parallax, reverse=False):
            pygame.draw.rect(camera.surface, color=element.color, rect=camera_draw(camera, element.rect, element.parallax))

        pygame.display.update()

##
#  TESTING
# ##### 
# test.screen = display
# test.mydo()

main_loop()

