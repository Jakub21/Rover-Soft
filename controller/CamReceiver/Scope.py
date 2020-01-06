import zmq
import base64

import contextlib # Disables PyGame hello message
with contextlib.redirect_stdout(None):
  import pygame.camera as pgc
