"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Lili Mkrtchyan lm688
# 12/8/2021
"""
from game2d import *
from consts import *
from models import *
import random
from math import *
import app

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    #Attribute _animating: Whether we are in the process of animating
    #Invariant: _animating is a boolean
    #
    #Attribute _turn_left: Whether the ship moves to the left
    #Invariant: _turn_Left is a boolean
    #
    #Attribute _turn_right: Whether the ship moves to the right
    #Invariant: _turn_right is a boolean
    #
    #Attribute _alien_left: Keeps track of whether aliens move to the left
    #Invariant: _alien_Left is a boolean
    #
    #Attribute _alien_right: Keeps trak of whether aliens move to the right
    #Invariant: _alien_right is a boolean
    #
    #Attribute _alien_step: Counts the steps of alien wave
    #Invariant: _alien_step is an int >= 0
    #
    #Attribute _move_bolt: Whether bolts are being _animate_slide
    #Invariant: _move_bolt is a boolean
    #
    #Attribute _player_shot: Whether the bolt belongs to the player's ship
    #Invariant: _player_shot is a boolean
    #
    #Attribute _explosion: A coroutine for performing an animation
    #Invariant: _explosion is a generator-based coroutine (or None)
    #
    #Attribute _ending: Whether the player lost or won
    #Invariant: _ending is either 'Lost' or 'Win' or an empty string
    #
    #Attribute _ship_x:The previous ship's x coordinate.Used to restore the ship.
    #Invariant: _ship_x is an int or float


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setShip(self, value):
        """
        Method to set the value of the Ship attribute.

        Parameter value: value to set the attribute ship to/
        Precondition: value should be an object of the Ship class.
        """
        assert isinstance(value, Ship)
        self._ship = value

    def getEnding(self):
        """
        Method to get the value of ending.
        """
        return self._ending

    def setEnding(self, value):
        """
        Method to set the value of ending.

        parameter value: value to set the attribute ending to.
        precondition: value should be string, either 'Lost' or 'Win'
        """
        assert value == 'Lost' or value == 'Win'
        self._ending = value

    def setExplosion(self, value):
        """
        Method to set the value of explosion.

        Other classes can set the value of attribute explosion only to None.

        parameter value: value to set the attribute explosion to.
        precondition: value should be None.
        """
        assert value == None
        self._explosion = None

    def getShip(self):
        """
        Method to get the ship tribute.
        """
        if not self._ship is None:
            return self._ship
        else:
            return None

    def getLives(self):
        """
        Method to get the lives attribute.
        """
        return self._lives
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the game with the ship, aliens, defense line, and bolts.
        """
        self._aliens = self.init_alien_list()
        self._ship = Ship(GAME_WIDTH/2)
        self._lives = SHIP_LIVES
        self._dline = GPath(linecolor='black',linewidth=1, y=DEFENSE_LINE,
        points=[0,0,GAME_WIDTH,0])
        self._bolts = []
        self._animating = False
        self._turn_left = False
        self._turn_right = False
        self._alien_left = False
        self._alien_right = True
        self._move_bolt = False
        self._alien_step = 0
        self._player_shot = False
        self._explosion = None
        self._time = 0.0
        self._ending = ''
        self._ship_x = GAME_WIDTH/2

        self.assert_invariants()

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates the game.

        A bolt is created when the player presses the key 'up'. Only one player
        bolt is allowed in the screen. The player ship is moved by the key
        presses 'left' and 'right'. When the player bolt hits any alien, the
        alien disappears. When the alien bolt hits the player ship, the ship
        exploits. Aliens move right and left, and go down when reach the edge
        of the screen. The game is over when all the aliens are disappeared, with
        the player win. Or with the player loss when the aliens reach the defense
        line or hit the player ship 3 times (as the player ship has 3 lives).

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self.check_the_line()
        if self._explosion is None:
            self._move_bolt = True
            self.move_the_ship(input, dt)
            self.animate_move_bolt(dt)
            self.players_bolt(input)
            self.aliens(dt)
            self.collisions()
        else:
            try:
                self._explosion.send(dt)
            except:
                self.finish_explosion()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game.

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if not self._aliens[i][j] is None:
                    self._aliens[i][j].draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        self._dline.draw(view)
        if len(self._bolts)>0:
            for bolt in range(len(self._bolts)):
                self._bolts[bolt].draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def assert_invariants(self):
        """
        Checks all the invariants of the attributes with assert statements.
        """

        assert isinstance(self._ship, Ship)
        for alien_row in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                alieen = self._aliens[alien_row][alien]
                assert isinstance(alieen, Alien) or alieen is None
        for bolt in range(len(self._bolts)):
            assert isinstance(self._bolts[bolt], Bolt)
        assert isinstance(self._dline, GPath)
        assert type(self._lives) == int and self._lives >= 0
        assert type(self._time) == float and self._time >= 0
        assert self._animating == True or self._animating == False
        assert self._turn_right == True or self._turn_right == False
        assert self._turn_left == True or self._turn_left == False
        assert self._alien_left == True or self._alien_left == False
        assert self._alien_right == True or self._alien_right == False
        assert self._move_bolt == True or self._move_bolt == False
        assert self._player_shot == True or self._player_shot == False
        assert self._ending == 'Lost' or self._ending == 'Win' or self._ending == ''
        assert type(self._ship_x) == int or type(self._ship_x) == float

    def finish_explosion(self):
        """
        Finishes the explosion of the ship.

        After the explosion this method clears all the bolts from the screen.
        Sets the generator attribute to None. Clears the ship from the screen,
        and decreases the lives of the player by one.
        """
        self._bolts.clear()
        self._explosion = None
        self._ship = None
        self._lives=self._lives-1

    def move_the_ship(self, input, dt):
        """
        Moves the ship either to the left or to the right.

        Checks the key pressed by the player and moves the ship accordingly.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float
        assert isinstance(input, GInput)
        if self._animating:
            if self._turn_left:
                self.animate_move_left(dt)
            elif self._turn_right:
                self.animate_move_right(dt)
        elif input.is_key_down('left'):
            self._animating = True
            self._turn_left = True
        elif input.is_key_down('right'):
            self._animating = True
            self._turn_right = True

    def check_the_line(self):
        """
        Checks if the alien wave has crossed the defense line.

        Once the alien wave crosses the defense line, the player loses the game.
        """
        for alien_row in range(1,ALIEN_ROWS+1):
            for alien in range(ALIENS_IN_ROW):
                if not self._aliens[-alien_row][alien] is None:
                    if self._aliens[-alien_row][alien].y < DEFENSE_LINE+ALIEN_HEIGHT/2:
                        self._ending = 'Lost'

    def collisions(self):
        """
        Checks if the bolts have collided with either aliens or the ship.

        If the bolt belongs to the player ship, checks if the bolt has hit any
        alien. If so, erases the alien from the screen - sets the alien value in
        the list to None. Also removes the bolt that has been collided from the
        screen so that the player is able to shoot again. If the bolt does not
        belong to the player, checks if it has collided with the player ship.
        If yes, removes the bolt, sets the generator attribute of explosion to
        True for the ship to explode.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                for alien_row in range(ALIEN_ROWS):
                    for alien in range(ALIENS_IN_ROW):
                        if not self._aliens[alien_row][alien] is None:
                            if self._aliens[alien_row][alien].collides(bolt):
                                print('collision detected')
                                self._bolts.remove(bolt)
                                self._player_shot = False
                                self._aliens[alien_row][alien] = None
            else:
                if not self._ship is None:
                    if self._ship.collides(bolt):
                        self._ship_x = self._ship.x
                        self._bolts.remove(bolt)
                        self._explosion = self.makeExplosion()
                        next(self._explosion)

    def aliens(self, dt):
        """
        Makes aliens walk and shoot at the randomly assigned times.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        random_number = random.randint(1, BOLT_RATE)
        random_alien = self.random_alien()

        self._time = self._time + dt
        if self._time >= ALIEN_SPEED:
            self.animate_move_aliens()
            self._alien_step +=1
            if self._alien_step > random_number:
                self._alien_step = 0
                if not random_alien is None:
                    self._bolts.append(Bolt(random_alien.x,
                     random_alien.y-ALIEN_HEIGHT/2, -BOLT_SPEED))

    def players_bolt(self, input):
        """
        Returns: True if the bolt belongs to the player ship.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        assert isinstance(input, GInput)

        if input.is_key_down('up') and self._player_shot == False:
            self._bolts.append(Bolt(self._ship.x, self._ship.y+SHIP_HEIGHT/2,
             BOLT_SPEED))
            self._player_shot = True

    def makeExplosion(self):
        """
        The animation coroutine.

        This have a yield expression that receives the dt and calculates which
        sprite frame to animate.
        """
        seconds = 0
        self._ship.frame = 1
        while self._ship.frame<7:
            dt = (yield)
            seconds = seconds + dt
            frame = seconds/DEATH_SPEED*7
            self._ship.frame =self._ship.frame + round(frame)
        self._ship.frame = 7 #8?

    def aliens_exist(self):
        """
        Returns: True if there are aliens remaining in the list, False otherwise.
        """
        for alien in range(ALIENS_IN_ROW):
            for alien_row in range(ALIEN_ROWS):
                if not self._aliens[alien_row][alien] is None:
                    aliens_remaining = True
                    return True
                    print('true thingy')
                else:
                    aliens_remaining = False
        return aliens_remaining

    def random_alien(self):
        """
        Out of all the remaining (not_None) aliens randomly chooses an alien
        to shoot.
        """
        if self.aliens_exist():
            rand_alien = random.randint(0, ALIENS_IN_ROW-1)
            for row in range(ALIEN_ROWS):
                if not self._aliens[row][rand_alien] is None:
                    return self._aliens[row][rand_alien]
            else:
                rand_alien = random.randint(0, ALIENS_IN_ROW-1)

    def most_left_alien(self):
        """
        Returns: the most left alien out of all the remaining (not-None) aliens.
        """
        for alien in range(ALIENS_IN_ROW):
            for alien_row in range(ALIEN_ROWS):
                if not self._aliens[alien_row][alien] is None:
                    return self._aliens[alien_row][alien]

    def most_right_alien(self):
        """
        Returns: the most right alien out of all the remaining (not-None) aliens.
        """
        for alien in range(1, ALIENS_IN_ROW+1):
            for alien_row in range(ALIEN_ROWS):
                if not self._aliens[alien_row][-alien] is None:
                    return self._aliens[alien_row][-alien]

    def init_alien_list(self):
        """
        Returns: a 2d list of aliens.

        Alien rows are far from each other by ALIEN_V_SEP. And aliens in a row
        are far from each other by ALIEN_H_SEP. The top aliens are far from the
        top edge of the window by ALIEN_CEILING.
        """
        alist = []
        for j in range(ALIEN_ROWS):
            alist.append([])
            for i in range(1, ALIENS_IN_ROW+1):
                image = j//2 % len(ALIEN_IMAGES)
                alien = Alien(ALIEN_IMAGES[image],
                 i*ALIEN_H_SEP+(i+0.5)*ALIEN_WIDTH,
                 GAME_HEIGHT-(ALIEN_CEILING+(ALIEN_ROWS-(j+0.5))*ALIEN_HEIGHT+(ALIEN_ROWS-j)*ALIEN_V_SEP))
                alist[j].append(alien)
        return alist

    def animate_move_left(self, dt):
        """
        Moves the player ship to the left.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        steps = SHIP_MOVEMENT
        amount = steps * dt
        self._ship.x = self._ship.x - amount
        if abs(self._ship.x) > amount:
            self._ship.x = self._ship.x - steps
            self._animating = False
            self._turn_left = False
        if min(SHIP_WIDTH/2, self._ship.x)==self._ship.x:
            self._ship.x = SHIP_WIDTH/2

    def animate_move_right(self, dt):
        """
        Moves the player ship to the right.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        steps = SHIP_MOVEMENT
        amount = steps * dt
        self._ship.x = self._ship.x + amount
        if abs(self._ship.x) > amount:
            self._ship.x = self._ship.x + steps
            self._animating = False
            self._turn_right = False
        if max(self._ship.x, GAME_WIDTH-SHIP_WIDTH/2) == self._ship.x:
            self._ship.x = GAME_WIDTH-SHIP_WIDTH/2

    def animate_move_bolt(self, dt):
        """
        Animates the bolts.

        Gets the velocity of the bolt to determine whether the bolt goes up or
        down. Checks if the bolt is out of the screen, delets it.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        for bolt in self._bolts:
            bolt.y = bolt.y + dt*bolt.getVelocity()
            if bolt.y - BOLT_HEIGHT/2 > GAME_HEIGHT:
                self._bolts.remove(bolt)
                self._player_shot = False
            if bolt.y + BOLT_HEIGHT/2<0:
                self._bolts.remove(bolt)

    def animate_move_aliens(self):
        """
        Moves aliens left, right, or vertically.

        If aliens still exist, moves the aliens accordingly.If the aliens are
        moving to the right, checks the right edge of the window. If they are
        too close to the edge of the window, moves them vertically down by
        ALIEN_V_WALK. If the aliens are moving to the left, checks the
        left edge of the window. If they are too close to the edge, moves them
        vertically down by ALIEN_V_WALK. If there are no more aliens, stops
        moving the aliens and sets the ending of the game to the player win.
        """
        if self.aliens_exist():
            right_alien = self.most_right_alien()
            left_alien = self.most_left_alien()
            if self._alien_right and GAME_WIDTH-right_alien.x>2*ALIEN_H_SEP:
                for alien_row in range(ALIEN_ROWS):
                    for alien in range(ALIENS_IN_ROW):
                        if not self._aliens[alien_row][alien] is None:
                            alin = self._aliens[alien_row][alien]
                            self._aliens[alien_row][alien].x=alin.x+ALIEN_H_WALK
            elif self._alien_left and left_alien.x > 2*ALIEN_H_SEP:
                for alien_row in range(ALIEN_ROWS):
                    for alien in range(ALIENS_IN_ROW):
                        if not self._aliens[alien_row][alien] is None:
                            alin = self._aliens[alien_row][alien]
                            self._aliens[alien_row][alien].x=alin.x-ALIEN_H_WALK
            else:
                for alien_row in range(ALIEN_ROWS):
                    for alien in range(ALIENS_IN_ROW):
                        if not self._aliens[alien_row][alien] is None:
                            alin = self._aliens[alien_row][alien]
                            self._aliens[alien_row][alien].y=alin.y-ALIEN_V_WALK
                    if self._alien_right == True:
                        self._alien_right = False
                        self._alien_left = True
                    else:
                        self._alien_left = False
                        self._alien_right = True
            self._time = 0
        else:
            self._ending = 'Win'
