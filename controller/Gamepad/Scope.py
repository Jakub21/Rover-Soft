from os import environ

import contextlib # Disables PyGame hello message
with contextlib.redirect_stdout(None):
  import pygame as pg
  from pygame import joystick as pgPads
  from pygame.joystick import Joystick as GamePad
