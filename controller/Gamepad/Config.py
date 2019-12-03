
class Config:
  # Index of connected gamepad, if you have only one keep it equal to 0th pad
  gamepadIndex = 0

  # Specification of connected gamepad
  class gpSpecs:
    buttons = 10; axes = 5; hats = 1; balls = 0

  # Name controls (different order/names for each Gamepad model)
  # Each name must be unique

  # [PLAYSTATION 3 GAMEPAD]
  keysButtons = [
    'Down', 'Right', 'Left', 'Up', # Right-hand buttons with symbols
    'BackLeft', 'BackRight', # Back panel
    'CentralLeft', 'CentralRight', # Central panel
    'JsPressLeft', 'JsPressRight', # Joystick press buttons
  ]
  keysAxes = [
    'JsLeftX', 'JsLeftY', 'BackAxis', 'JsRightY', 'JsRightX'
  ]
  keysHats = [
    ('LeftHatX', 'LeftHatY') # Left-hand 2-axis hat
  ]
  keysBalls = []
