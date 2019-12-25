
class TcpServer(Plugin):
  def init(self):
    super().init()
    self.parser = Cis.Parser()
    self.ownAddress = self.getOwnAddress()
    self.usedPort = self.cnf.DEFAULTS.usedPort
    self.initSocket()
    self.addEventHandler('Transmit', self.transmit)
    self.addInputNode('Rebind', self.rebind, 'port')
    self.addInputNode('Disconnect', self.disconnect)

  def initSocket(self):
    self.socket = scklib.socket()
    Note(self, f'Binding TPC server to {self.ownAddress}:{self.usedPort}')
    self.socket.setsockopt(scklib.SOL_SOCKET, scklib.SO_REUSEADDR, 1)
    self.socket.bind((self.ownAddress, self.usedPort))
    self.socket.settimeout(self.cnf.timeOut)
    self.connection = Namespace(state=False, socket=None, address='', port=0)
    self.socket.listen(15)

  def update(self):
    super().update()
    self.setPluginOutputs(
      Connected = self.connection.state,
      Address = self.connection.address,
      Port = self.connection.port,
    )
    if self.connection.state:
      if not(self.tick % 128):
        Event(self, 'Transmit', alive='yes', tick=self.tick)
      self.receive()
      self.handleReceivedData()
    else: self.acceptConnection()

  def disconnect(self, params):
    Warn(self, 'Disconnecting')
    self.socket.close()
    self.initSocket()

  def rebind(self, params):
    try: params.port  = int(params.port)
    except ValueError: Warn(self, 'Port must be a number'); return
    self.usedPort = params.port
    self.initSocket()

  def receive(self):
    try:
      data = self.connection.socket.recv(self.cnf.incomingBufferSize)
      if len(data) > 0: Debug(self, data); self.parser.pushBytes(data)
    except scklib.timeout: pass
    except (ConnectionAbortedError, ConnectionResetError, OSError) as exc:
      Error(self, 'Connection was broken')
      self.onDisconnect()

  def transmit(self, event):
    if not self.connection.state: return
    query = Cis.Query(event.id, **event.getArgs())
    data = query.build()
    try: self.connection.socket.send(data)
    except BrokenPipeError:
      Error(self, 'Connection was broken')
      self.onDisconnect()

  def acceptConnection(self):
    try:
      self.connection.socket, address = self.socket.accept()
      self.connection.socket.settimeout(self.cnf.timeOut)
      address, port = address
      self.connection.address, self.connection.port = address, port
      self.connection.state = True
      Note(self, f'Successfully connected to {address}:{port}')
    except (BlockingIOError, OSError):
      self.connection.state = False

  @staticmethod
  def getOwnAddress():
    s = scklib.socket(scklib.AF_INET, scklib.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()[0]
    s.close()
    return address

  def handleReceivedData(self):
    self.parser.parse()
    while not self.parser.queries.empty():
      query = self.parser.queries.pop()
      Debug(self, f'Popped {query}')
      Event(self, query.key, **query.params)

  def onDisconnect(self):
    self.socket.close()
    self.initSocket()

  def quit(self):
    super().quit()
    self.socket.close()
