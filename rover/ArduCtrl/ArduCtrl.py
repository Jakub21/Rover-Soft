
class ArduCtrl(Plugin):
  def init(self):
    super().init()
    self.conn = SerialLib.Serial(self.cnf.PortName, self.cnf.Baudrate, timeout=0)
    self.addEventHandler('ArduSend', self.transmit)
    self.parser = Parser(self.cnf.ResponseKeys)
    # Store sensor readings
    self.addEventHandler('ArduTmprRspb',
      lambda evt: self.setReading('TmprRspb', evt))
    self.addEventHandler('ArduTmprAccu',
      lambda evt: self.setReading('TmprAccu', evt))
    self.addEventHandler('ArduTmprCnvrt',
      lambda evt: self.setReading('TmprCnvrt', evt))
    self.readings = Namespace()

  def update(self):
    super().update()
    self.setPluginOutputs(**self.readings.__dict__)
    if not(self.__pluginable__.tick % self.cnf.RequestReadingsInterval):
      Event(self, 'ArduSend', key='RequestTmpr')
    data = self.conn.read(self.cnf.ReadBytesPerLoop)
    if len(data): self.parser.push(data)
    self.parser.parse()
    while not self.parser.isEmpty():
      try: response = self.parser.pop()
      except ValueError: continue
      Event(self, f'Ardu{response.key}', params=response.params)

  def transmit(self, event):
    try: key = self.itob(self.cnf.OutputKeys[event.key])
    except KeyError as exc: raise KeyError(f'Invalid ArudCtrl output key "{event.key}"')
    try: event.params
    except AttributeError: event.params = []
    cleanParams = b''
    if len(event.params) > self.cnf.MaxCallLength -1:
      raise ValueError(f'Only {self.cnf.MaxCallLength} characters per call are allowed')
    for param in event.params:
      if type(param) != int:
        raise TypeError('Only ints are allowed in ArduSend parameters')
      cleanParams += self.itob(param)
    self.conn.write(key + cleanParams + b';')

  def setReading(self, readingKey, event):
    if readingKey in ['TmprRspb', 'TmprAccu', 'TmprCnvrt']:
      self.readings[readingKey] = event.params[0]
    else:
      Warn(self, 'Can not set reading, setter not implemented')

  def quit(self):
    super().quit()
    self.conn.close()

  @staticmethod
  def itob(*ints):
    result = b''
    for i in list(ints): result += bytes([i])
    return result
