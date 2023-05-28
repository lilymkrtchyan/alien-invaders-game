"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Lili Mkrtchyan lm688
# 12/8/2021
"""
from consts import *
from game2d import *
from wave import *
import introcs
import random
import math

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # #Attribute lastkeys: the number of keys pressed last frame
    # Invariant: laskeys is an int >= 0
    #

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # IMPLEMENT ME
        states = [STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, STATE_COMPLETE]

        self._state = STATE_INACTIVE
        if self._state == STATE_INACTIVE:
            self._text = GLabel(text = 'Press "S" To Continue', font_size = 30,
            x = self.width/2, y = self.height/2, bold = True)
            self._wave = None
            self._lastkeys = 0

        assert self._state in states
        if self._state != STATE_INACTIVE:
            assert isinstance(self._wave, Wave)
        else:
            assert self._wave is None
        if self._state != STATE_ACTIVE:
            assert isinstance(self._text, GLabel)
        else:
            assert self._text is None
        assert type(self._lastkeys) == int and self._lastkeys >= 0

    def update(self,dt):
        """
        Determines the current state and animates a single frame in the game.

        The primary purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        The states are: STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay. The player can
        move the ship and fire laser bolts. This state also restores the
        ship after it was destroyed.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen. When the player presses a key,
        the state changes to STATE_CONTINUE.

        STATE_CONTINUE: This state stops the animation of ship explosion.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame. This state only lasts one animation frame before
        switching to STATE_ACTIVE automatically.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        assert type(dt) == int or type(dt) == float
        self._determineState()
        if self._state != STATE_INACTIVE:
            self._text = None
        if self._state == STATE_NEWWAVE:
            self._animateNewWave()
        if self._state == STATE_ACTIVE:
            self._animateStateActive(dt)
        if self._state == STATE_PAUSED:
            self._animateStatePaused()
        if self._state == STATE_CONTINUE:
            self._animateStateContinue()
        if self._state == STATE_COMPLETE:
            self._animateStateComplete()

    def draw(self):
        """
        Draws the game objects to the view.
        """
        # IMPLEMENT ME
        if self._text is not None:
            self._text.draw(self.view)
        if self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
        if self._state == STATE_PAUSED:
            self._wave.draw(self.view)

    # # HELPER METHODS FOR THE STATES GO HERE

    def _determineState(self):
        """
        Determines the current state and if necessary changes it to the
        according state.

        This method checks for a key press, and if there is
        one, changes the state to the assigned value.  A key
        press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as
        we hold down the key. The user must release the
        key and press it again to change the state.
        """
        #Adjusted the state.py code from example code
        if self._state == STATE_INACTIVE or self._state == STATE_PAUSED:
            curr_keys = self.input.key_count
            change = curr_keys > 0 and self.lastkeys == 0 and self.input.is_key_down('s')
            if change:
                self._state = (self._state + 1) % NUM_STATES
            self.lastkeys= curr_keys
        elif self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE
        elif self._state == STATE_COMPLETE:
            self._state = STATE_INACTIVE

    def _animateNewWave(self):
        """
        Animates the STATE_NEWWAVE.

        This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.
        """
        print('STATE_NEWWAVE')
        self._wave = Wave()
        self._state = STATE_ACTIVE
        self_text = None

    def _animateStateActive(self, dt):
        """
        Animates the STATE_ACTIVE.

        This is a session of normal gameplay. The player can
        move the ship and fire laser bolts. This state also restores the
        ship after it was destroyed.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float
        if not self._wave.getShip() is None:
            self._wave.update(self.input, dt)
        else:
            if self._wave.getLives()>0:
                self._state = STATE_PAUSED
                self._wave.setShip(Ship(self._wave._ship_x))
            else:
                self._wave.setEnding('Lost')
                self._state = STATE_COMPLETE
        if self._wave.getEnding() == 'Win':
            self._state = STATE_COMPLETE
        if self._wave.getEnding() == 'Lost':
            self._state = STATE_COMPLETE

    def _animateStatePaused(self):
        """
        Animates the STATE_PAUSED.

        Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen. When the player presses a key,
        the state changes to STATE_CONTINUE.
        """
        self._text = GLabel(text = 'Press "S" To Continue', font_size = 30,
        x = self.width/2, y = self.height/2, bold = True)
        self._determineState()

    def _animateStateContinue(self):
        """
        Animate the STATE_CONTINUE.

        This state stops the animation of ship explosion.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame. This state only lasts one animation frame before
        switching to STATE_ACTIVE automatically.
        """
        self._wave.setExplosion(None)
        self._determineState()

    def _animateStateComplete(self):
        """
        Animates the STATE_COMPLETE.

        In this state the wave is over, and is either won or lost.
        """
        if self._wave.getEnding() == 'Lost':
            self._text = GLabel(text = "You have lost the Game, Press 'S' to start again!", font_size = 30,
            x = self.width/2, y = self.height/2, bold = True)
        if self._wave.getEnding() == 'Lost':
            self._text = GLabel(text = "You have lost the Game, Press 'S' to start again!", font_size = 30,
            x = self.width/2, y = self.height/2, bold = True)
        if self._wave.getEnding() == 'Win':
            self._text = GLabel(text = "You have won the Game, Press 'S' to start again!", font_size = 30,
            x = self.width/2, y = self.height/2, bold = True)
        self._determineState()
