
class ArduCtrl(Plugin):
  def init(self):
    super().init()
    self.conn = SerialLib.Serial(self.cnf.PortName, self.cnf.Baudrate, timeout=0)
    self.addEventHandler('Arduino', self.transmit)

  def update(self):
    super().update()
    data = self.conn.read(self.cnf.ReadBytesPerLoop)
    if len(data): Debug(self, f'RECV {data}')
    if not(self.tick % self.executor.tpsMon.tps):
      Event(self, 'Arduino', data=b'DummyDataTransmission')

  def transmit(self, event):
    self.conn.send(event.data)

  def quit(self):
    super().quit()
    self.conn.close()
