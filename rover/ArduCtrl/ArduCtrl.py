
class ArduCtrl(Plugin):
  def init(self):
    super().init()
    self.conn = SerialLib.Serial(self.cnf.PortName, self.cnf.Baudrate, timeout=0)
    self.addEventHandler('ArduSend', self.transmit)
    self.parser = Parser()
    self.outFuncKeys = Namespace(
      RequestTmprReadings = self.itob(0),
      SetServoPositions = self.itob(1),
    )
    self.inFuncKeys = {
      1: 'TmprRaspberry',
      2: 'TmprBattery',
      3: 'TmprConverters',
    }

  def update(self):
    super().update()
    self.self.setPluginOutputs()
    data = self.conn.read(self.cnf.ReadBytesPerLoop)
    if len(data): self.parser.push(data)
    if not(self.__pluginable__.tick % (2 * self.executor.tpsMon.tps)):
      Event(self, 'ArduSend', data=self.outFuncKeys.RequestTmprReadings)
    self.parser.parse()
    while True:
      try:
        received = self.parser.pop()
        Debug(self, f'RECV {received}')
      except IndexError: break

  def transmit(self, event):
    Debug(self, f'SEND {event.data}')
    self.conn.write(event.data)

  def quit(self):
    super().quit()
    self.conn.close()

  @staticmethod
  def itob(*ints):
    result = b''
    for i in list(ints): result += bytes([i])
    return result
