
class Config:
  title = {
    'controller': 'Controller',
    'rover': 'Rover',
  }
  class WINDOW: # General Tk window settings
    minWidth = 500
    minHeight = 420

  class THEME:
    wind = 'vista'
    unix = 'default'

  class COLORS:
    fg = '#FFF'
    bg = '#282C34'

  class FONT_SIZE:
    heading2 = 18
    heading3 = 14

  class CANVAS: # Canvas for camera feed (only in controller)
    width = 160
    height = 120
    background = '#000'
    hudColor = '#FF0'
    hudStrokeWidth = 3
    hudLines = [
      [(57, 60), (70, 60)], # left hor
      [(90, 60), (103, 60)], # right hor
      [(80, 40), (80, 50)], # upper ver
      [(80, 70), (80, 80)], # lower ver
    ]
