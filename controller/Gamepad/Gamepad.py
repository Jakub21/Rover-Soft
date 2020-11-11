
class Gamepad(Plugin):
  def init(self):
    super().init()
    self.prevStatus = Namespace()
    self.status = Namespace()
    cnf = self.cnf

    # Point SDL Videodriver to dummy and initialize PyGame
    environ['SDL_VIDEODRIVER'] = 'dummy'
    pg.init()
    pg.display.init()
    screen = pg.display.set_mode((1, 1))

    # Check if any gamepads are connected and connect to one specified in config
    if pgPads.get_count() == 0:
      raise ValueError('No gamepads were found')
    self.pad = GamePad(cnf.gamepadIndex)
    self.pad.init()

    # Check if gamepad specification is the same as in config
    if cnf.gpSpecs.buttons != self.pad.get_numbuttons() or \
        cnf.gpSpecs.axes != self.pad.get_numaxes() or \
        cnf.gpSpecs.hats != self.pad.get_numhats() or \
        cnf.gpSpecs.balls != self.pad.get_numballs():
      raise ValueError('Invalid gamepad specification')

    # Check if amount of controls in config bindings is the same as in specification
    if cnf.gpSpecs.buttons != len(cnf.keysButtons) or \
        cnf.gpSpecs.axes != len(cnf.keysAxes) or \
        cnf.gpSpecs.hats != len(cnf.keysHats) or \
        cnf.gpSpecs.balls != len(cnf.keysBalls):
      raise ValueError('Invalid gamepad specification (controlls amount mismatch)')

  def update(self):
    super().update()
    self.readGamepadStatus()
    self.setPluginOutputs(**self.status.__dict__)
    changed = False
    for key, val in self.status.items():
      try:
        if self.prevStatus[key] != val: changed = True; break
      except KeyError: changed = True; break
    if changed: Event(self, 'Transmit', key='Gamepad', **self.status.__dict__)

  def readGamepadStatus(self):
    cnf = self.cnf
    for evt in pg.event.get(): pass
    self.prevStatus = self.status
    self.status = Namespace()
    for i in range(cnf.gpSpecs.buttons):
      self.status[cnf.keysButtons[i]] = self.pad.get_button(i)
    for i in range(cnf.gpSpecs.axes):
      self.status[cnf.keysAxes[i]] = self.pad.get_axis(i)
    for i in range(cnf.gpSpecs.hats):
      keys = cnf.keysHats[i]
      values = self.pad.get_hat(i)
      for j in range(len(keys)):
        self.status[keys[j]] = values[j]
    for i in range(cnf.gpSpecs.balls):
      self.status[cnf.keysBalls[i]] = self.pad.get_ball(i)

  def quit(self):
    super().quit()
