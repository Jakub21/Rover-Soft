
class Kinematics(Plugin):
  def init(self):
    super().init()
    self.addEventHandler('Gamepad', self.onGamepadChange)

  def update(self):
    super().update()

  def onGamepadChange(self, event):
    self.setPluginOutputs(**event.getArgs())

  def quit(self):
    super().quit()
