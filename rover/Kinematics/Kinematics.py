
class Kinematics(Plugin):
  def init(self):
    super().init()
    self.addEventHandler('Gamepad', self.onGamepadChange)

  def update(self):
    super().update()

  def onGamepadChange(self, event):
    state = event.getArgs()
    del state['issuer']
    self.setPluginOutputs(**state)

  def quit(self):
    super().quit()
