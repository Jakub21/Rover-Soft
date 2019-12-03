
class TcpClient(Plugin):
  def init(self):
    super().init()
    self.parser = Cis.Parser()
    self.ownAddress = self.getOwnAddress()
    self.usedPort = self.cnf.DEFAULTS.usedPort
    self.target = Namespace(
      address = self.cnf.DEFAULTS.targetAddress,
      port = self.cnf.DEFAULTS.targetPort)
    self.initSocket()
    self.addEventHandler('Transmit', self.transmit)

  def initSocket(self):
    self.socket = scklib.socket()
    Note(self, f'Binding new socket to {self.ownAddress}:{self.usedPort}')
    self.socket.bind((self.ownAddress, self.usedPort))
    self.socket.settimeout(self.cnf.timeOut)
    self.connection = Namespace(state=False)

  def update(self):
    super().update()
    if self.connection.state:
      self.receive()
      self.handleReceivedData()

  def receive(self):
    try:
      data = self.socket.recv(self.cnf.incomingBufferSize)
      if len(data) > 0: self.parser.pushBytes(data)
    except scklib.timeout: pass
    except (ConnectionAbortedError, ConnectionResetError) as exc:
      self.raiseError(exc.__class__.__name__, exc, False, 'Connection was broken')

  def transmit(self, event):
    query = Cis.Query(event.id, **event.getArgs())
    data = query.build()
    self.socket.send(data)

  @staticmethod
  def getOwnAddress():
    s = scklib.socket(scklib.AF_INET, scklib.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()[0]
    s.close()
    return address

  def handleReceivedData(self):
    while not self.parser.queries.empty():
      query = self.parser.queries.pop()
      PluginEvent(self, query.key, **query.params)

  def quit(self):
    super().quit()
