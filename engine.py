from imports import *


# This will be set by the `main` module.
camera = None


class MoveKey(Enum):
    '''Key configuration for movement of the protagonist and the camera.'''
    UP = K_e
    RIGHT = K_f
    DOWN = K_d
    LEFT = K_s
    FORWARD = K_w
    BACKWARD = K_r
    CAMERA_LEFT = K_j
    CAMERA_RIGHT = K_l
    CAMERA_UP = K_i
    CAMERA_DOWN = K_k
    CAMERA_FORWARD = K_u
    CAMERA_BACKWARD = K_o
    CAMERA_SHAKE = K_t  # t for tremblement


class EventManager:
    '''Receives events from `main` module'''
    @classmethod
    def manage_event(cls, event, protagonist:'Entity'=None):
        if event.type == QUIT:
            EventManager.quit()
        elif event.type == KEYDOWN:
            EventManager.key_down(event.key, protagonist)
        elif event.type == KEYUP:
            EventManager.key_up(event.key, protagonist)

    @classmethod
    def key_down(cls, key, protagonist:'Entity'):
        if key == MoveKey.BACKWARD.value:
            protagonist.parallax /= 2
        elif key == MoveKey.FORWARD.value:
            protagonist.parallax *= 2
        elif key == MoveKey.RIGHT.value:
            protagonist.movement.x += protagonist.speed
        elif key == MoveKey.LEFT.value:
            protagonist.movement.x += -protagonist.speed
        elif key == MoveKey.UP.value:
            protagonist.movement.y += -protagonist.speed
        elif key == MoveKey.DOWN.value:
            protagonist.movement.y += protagonist.speed
        elif key == MoveKey.CAMERA_BACKWARD.value:
            camera.parallax /= 2
        elif key == MoveKey.CAMERA_FORWARD.value:
            camera.parallax *= 2
        elif key == MoveKey.CAMERA_RIGHT.value:
            camera.movement.x += protagonist.speed
        elif key == MoveKey.CAMERA_LEFT.value:
            camera.movement.x += -protagonist.speed
        elif key == MoveKey.CAMERA_UP.value:
            camera.movement.y += -protagonist.speed
        elif key == MoveKey.CAMERA_DOWN.value:
            camera.movement.y += protagonist.speed
        elif key == MoveKey.CAMERA_SHAKE.value:
            camera.shake(duration=3, amplitude=2, time_unit=10)

    @classmethod
    def key_up(cls, key:MoveKey, protagonist:'Entity|Camera'):
        if key == MoveKey.RIGHT.value:
            protagonist.movement.x -= protagonist.speed
        elif key == MoveKey.LEFT.value:
            protagonist.movement.x -= -protagonist.speed
        elif key == MoveKey.UP.value:
            protagonist.movement.y -= -protagonist.speed
        elif key == MoveKey.DOWN.value:
            protagonist.movement.y -= protagonist.speed
        elif key == MoveKey.CAMERA_RIGHT.value:
            camera.movement.x -= protagonist.speed
        elif key == MoveKey.CAMERA_LEFT.value:
            camera.movement.x -= -protagonist.speed    
        elif key == MoveKey.CAMERA_UP.value:
            camera.movement.y -= -protagonist.speed
        elif key == MoveKey.CAMERA_DOWN.value:
            camera.movement.y -= protagonist.speed 
    
    @classmethod
    def quit(cls):
        pygame.quit()
        sys.exit()


class Vector3d:
    '''
    Used for position, speed or other in 3d space.
    Note that in 2d space, the `z` axis would be used for parallax effect in
    which case, the code would be refactored to replace parallax with the `z`
    attribute in all the code that calls it. Ex.: `camera_move` function.
    '''
    def __init__(self, x:int, y:int, z:int):
        self.x = x
        self.y = y
        self.z = z


class Vector2d:
    '''
    Used for position, speed or other.
    '''
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        
    def magnitude(self):
        return round((self.x**2 + self.y**2)**0.5)
    
    def __repr__(self):
        return f'(X:{self.x}, Y:{self.y})'
    
    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vector2d(self.x*other, self.y*other)
    
    def __truediv__(self, other):
        return Vector2d(self.x / other, self.y / other)
    
    def __floordiv__(self, other):
        return Vector2d(self.x // other, self.y // other)
    
    def __round__(self, ndigits=0):
        return Vector2d(int(round(self.x, ndigits=ndigits)), 
                        int(round(self.y, ndigits=ndigits)))
    
    __rmul__ = __mul__


class Collision:
    '''
    Temporary entity can be used as an explosion. Often the result of a collision
    '''
    def __init__(self, rect:Rect, parallax:int=1, color=(10,10,10), speed=1, timer=1000):
        self.rect = rect
        self.parallax = parallax
        self.color=color
        self.speed = speed
        self.temporary = True
        self.timer = timer
    
    def tick(self):
        '''
        Perform actions that should be done at each tick of the game.
            * move
            * decrement self.timer
        '''
        self.timer -= 1

    @staticmethod
    def get_collissions(rect:Rect, others:list[Rect])->List[Rect]:
        '''
        Get a list of indices from others that collide with rect.

        rect:
            Rect to check for collisions against

        others:
            List of Rect to get colliders from

        Return:
            list of indices of the others list that collided with rect
        '''
        return rect.collidelistall(others)


class Entity:
    '''Used for the "playable" objects as well as NPCs'''
    def __init__(self, rect:Rect, parallax:int=1, color=(150,150,150), speed=1):
        self.rect = rect
        self.parallax = parallax
        self.color = color
        self.speed = speed
        self.movement = Vector2d(x=0,y=0)
        self.destinations = []
        self.previous_pos = []
        self.trail = 1

    def __repr__(self):
        return f'{self.rect}'

    def _has_destination(self):
        return len(self.destinations) > 0

    def position(self):
        return Vector2d(self.rect.x, self.rect.y)
    
    def pos_center(self):
        return Vector2d(self.rect.centerx, self.rect.centery)

    def trail_length(self, change:int):
        '''
        change:
            the change in length of the trail to be drawn
        '''
        self.trail += change

    def _draw_position_trail(self):
        self.previous_pos.append(self.pos_center())
        for pos in self.previous_pos[-self.trail:]:
            pygame.draw.rect(camera.surface, BLUE, camera_draw(camera, Rect(pos.x, pos.y, 4, 4), self.parallax))

    def move(self, movement:Vector2d=None):
        '''
        movement: Vector2d
            allows to temporarly override the Entitys stored movement vector.
        '''
        self._draw_position_trail()
        
        if self._has_destination():
            delta = self.destinations[0] - Vector2d(self.rect.x, self.rect.y)
            if delta.magnitude() <= self.speed * 10:
                self.cycle_destination()
            if delta.magnitude() > 0.0:
                self.movement = round(delta / delta.magnitude())

        self.rect.x += movement.x if movement is not None else self.movement.x
        self.rect.y += movement.y if movement is not None else self.movement.y

    def add_destination(self, destination: Vector2d):
        self.destinations.append(destination)

    def cycle_destination(self):
        self.destinations = self.destinations[1:] + self.destinations[:1]


class Entities:
    '''
    Has the list of entities in the game.
    It holds the logic to despawn an entity.
    '''
    def __init__(self, protagonist:Rect, objects:List[Entity|Collision]=None):
        self.entities = [] if objects is None else objects
        self.protatonist = protagonist
    
    def tick(self):
        # check for collisions with protagonist
        collisions = Collision.get_collissions(self.protatonist.rect, self.entities)
        if len(collisions) > 0:
            camera.shake(duration=0.5, amplitude=2, time_unit=10)
            self.protatonist.trail_length(change=5)
        # remove elements that collide with protagonist
        self.entities = self.despawn(collisions)

    def spawn(self, object:Entity|Collision):
        '''
        object:
            object to add to self.entities
        '''
        self.entities.append(object)
    
    def despawn(self, indecies):
        '''
        indecies:
            indecies of entities to be removed from self.entities
        
        return:
            list purged of index entitie
        '''
        return [self.entities[i] for i in range(len(self.entities)) if i not in indecies]


class Camera:
    '''
    Similar to an Entity but has 2 differences.
    1- does not have a color; this is because this element will not be drawn.
    2- Has a surface; this is the surface on which other elements are drawn.
    '''
    def __init__(self, surface:pygame.Surface, parallax:int=1):
        self.surface = surface
        self.rect = Rect.copy(surface.get_rect())
        self.parallax = parallax
        self.movement = Vector2d(x=0,y=0)
        self.shake_time = 0
        self.shake_amplitude = 0
        self.shake_unit = 1000
        self.preshake = Vector2d(None, None)

    def position(self):
        return Vector2d(self.rect.x, self.rect.y)

    def move(self, movement:Vector2d=None):
        '''
        Moves the camera. Can be initiated by keyboard events or game events.
        Gets called at every tick of the game.
        movement: Vector2d
            allows to temporarly override the Cameras stored movement vector.
        '''
        self.rect.x += movement.x if movement is not None else self.movement.x
        self.rect.y += movement.y if movement is not None else self.movement.y

    def shake(self, duration=None, amplitude=None, time_unit=None):
        '''
        Allows sporadic movement of the camera to add imphasis on an
        event/action in the game.

        duration: int
        duration in milliseconds

        amplitude: int
            how large the movements should be

        time_unit: int
            Number of milliseconds each duration unit is worth. This allows to
            write 1 instead of 1000 for seconds or 1 instead of 3600000 for
            hours.
        '''
        # use a generator for this?
        # use yield for this?
        if duration is not None and self.shake_time == 0:
            self.preshake = Vector2d(self.rect.x, self.rect.y)
        self.shake_unit = time_unit if time_unit is not None else self.shake_unit
        self.shake_time += duration * self.shake_unit if duration is not None else 0
        self.shake_amplitude = amplitude if amplitude is not None else self.shake_amplitude
        

        if self.shake_time <= 0 and self.preshake.x is not None:
            self.rect.x, self.rect.y = self.preshake.x, self.preshake.y
            self.preshake = Vector2d(None, None)
        if self.shake_time <= 0:
            return
        
        self.shake_time -= 1
        self.move(Vector2d(choice([-1, 1])*randint(1, self.shake_amplitude), 
                           choice([-1, 1])*randint(1, self.shake_amplitude))
                  )


def draw(surface, rect, parallax=1):
    '''
    Used to draw images on a "screen" (aka the surface) CONSIDERING the screen
    acts as a moving camera. As such, a static object will seem to move from
    the cameras perspective. Moreover, an object moving with the same speed
    vector as the camera will seem static.
    
    surface: pygame.Surface
        Surface on which to draw.
    rect: pygame.Rect;
        Rect to reposition and redimention for dispaying on "camera".
    parallax: int;
        Used to recalculate position and size of Rect from the cameras
        perspective

    Return: position and size values of a pygame.Rect (4d)
    '''
    adjusted_x = (surface.get_width()/2) - ((surface.get_width()/2+surface.get_rect().x-rect.x) * parallax)
    adjusted_y = (surface.get_height()/2) - ((surface.get_height()/2+surface.get_rect().y-rect.y) * parallax)
    adjusted_width = rect.width * parallax
    adjusted_height = rect.height * parallax
    parallaxed = [adjusted_x, adjusted_y, adjusted_width, adjusted_height]
    parallaxed = [int(value) for value in parallaxed]
    return pygame.Rect(parallaxed)

def camera_draw(camera: Camera, rect:Rect, parallax:int=1)->Rect:
    '''
    Used to draw images on a "screen" (aka the camera) CONSIDERING the camera
    can move in ALL directions. As such, a static object will seem to move from
    the cameras perspective. Moreover, an object moving with the same speed
    vector as the camera will seem static. When the camera moves on the z-axis
    (aka `parallax`), the objects will seem to change size.
    
    scamerarface: Camera
        has a pygame.Surface on which to draw.
    rect: pygame.Rect;
        Rect to reposition and redimention for dispaying on "camera".
        Aka the item to display on camera
    parallax: int;
        Used to recalculate position and size of Rect from the cameras
        perspective

    Return:
        Rect with position and size values recalculated for camera perspective.
    '''
    adjusted_x = (camera.surface.get_width()/2) - ((camera.surface.get_width()/2+camera.rect.x-rect.x) * parallax/camera.parallax)
    adjusted_y = (camera.surface.get_height()/2) - ((camera.surface.get_height()/2+camera.rect.y-rect.y) * parallax/camera.parallax)
    adjusted_width = rect.width * parallax/camera.parallax
    adjusted_height = rect.height * parallax/camera.parallax
    parallaxed = [adjusted_x, adjusted_y, adjusted_width, adjusted_height]
    parallaxed = [int(value) for value in parallaxed]
    return pygame.Rect(parallaxed)
