"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Lili Mkrtchyan lm688
# 12/8/2021
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.
    """

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, coord_x, b=SHIP_BOTTOM, s=SHIP_IMAGE,  w=SHIP_WIDTH, h=SHIP_HEIGHT):
        """
        Initializes the ship.

        Parameter coord_x: The x coordinate of the center of the ship
        Precondition: coord_x is an int or float

        Parameter b: The bottom coordinate of the ship.
        Precondition: b is an int or float

        Parameter s: The source of the image
        Precondition: s is a string refering to a valid file

        Parameter w: The width of the ship.
        Precondition: w is an int or float > 0

        Parameter h: The height of the ship.
        Precondition: h is an int or float > 0
        """
        assert type(coord_x) == int or type(coord_x) == float
        assert type(b) == int or type(b) == float
        assert type(w) == int or type(w) == float
        assert w > 0
        assert type(h) == int or type(h) == float
        assert h > 0
        assert type(s) == str

        super().__init__(format = (2,4),x=coord_x, bottom=b, width=w, height=h,
         source=s)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self, bolt):
        """
        Returns: True if the ship has collided with the bolt, False otherwise.

        Parameter bolt: bolt to check the collision with
        Precondition: bolt is an object of the class Bolt.
        """
        assert isinstance(bolt, Bolt)
        if self.contains((bolt.x-BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)):
            return True
        else:
            return False


class Alien(GImage):
    """
    A class to represent a single alien.
    """

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, s, coord_x, coord_y, w=ALIEN_WIDTH, h=ALIEN_HEIGHT):
        """
        Initializes an alien.

        Parameter s: The source of the image of alien.
        Precondition: s is a string refering to a valid file.

        Parameter coord_x: The x coordinate of the center of the alien.
        Precondition: coord_x is an int or float.

        Parameter coord_y: The y coordinate of the center of the alien.
        Precondition: coord_y is an int or float.

        Parameter w: The width of the alien.
        Precondition: w is an int or float > 0.

        Parameter h: The height of the alien.
        Precondition: h is an int or float > 0.
        """
        assert type(coord_x) == int or type(coord_x) == float
        assert type(coord_y) == int or type(coord_y) == float
        assert type(w) == int or type(w) == float
        assert w > 0
        assert type(h) == int or type(h) == float
        assert h > 0
        assert type(s) == str
        super().__init__(width=w, height=h, source=s, x=coord_x, y=coord_y)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        Returns: True if the alien has collided with the bolt, False otherwise.

        Parameter bolt: bolt to check the collision with
        Precondition: bolt is an object of the class Bolt.
        """
        assert isinstance(bolt, Bolt)
        if self.contains((bolt.x-BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)):
            return True
        else:
            return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Method to get the velocity of the bolt.
        """
        return self._velocity
        
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x_coord, y_coord, vel):
        """
        Initializes a bolt.

        Parameter x_coord: The x coordinate of the center of the bolt.
        Precondition: x_coord is an int or a float.

        Parameter y_coord: The y coordinate of the center of the bolt.
        Precondiotion: y_coord is an int or float.

        Parameter vel: The velocity of the bolt.
        Precondition: vel is an int.
        """
        assert type(x_coord) == int or type(x_coord) == float
        assert type(y_coord) == int or type(y_coord) == float
        assert type(vel) == int
        super().__init__(x=x_coord, y=y_coord, fillcolor='red', linecolor='red',
         height = BOLT_HEIGHT, width = BOLT_WIDTH)
        self._velocity = vel

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns: True if the bolt belongs to the player, False otherwise.
        """
        if self._velocity == BOLT_SPEED:
            return True
        else:
            return False
