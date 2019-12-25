
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
    self.addInputNode('Rebind', self.rebind, 'port')
    self.addInputNode('Connect', self.connect, 'address', 'port')
    self.addInputNode('Disconnect', self.disconnect)

  def initSocket(self):
    self.socket = scklib.socket()
    Note(self, f'Binding TPC client to {self.ownAddress}:{self.usedPort}')
    self.socket.bind((self.ownAddress, self.usedPort))
    self.socket.settimeout(self.cnf.timeOut)
    self.connection = Namespace(state=False)

  def update(self):
    super().update()
    self.setPluginOutputs(Connected=self.connection.state)
    if self.connection.state:
      self.receive()
      self.handleReceivedData()

  def connect(self, params):
    try: params.port  = int(params.port)
    except ValueError: Warn(self, 'Port must be a number'); return
    Info(self, f'Connecting to {params.address}:{params.port}')
    self.socket.settimeout(self.cnf.connTimeOut)
    try:
      socket = self.socket.connect((params.address, params.port))
      self.connection.state = True
      Note(self, 'Connected')
    except (scklib.gaierror, BlockingIOError, scklib.timeout):
      Warn(self, 'Failed to establish connection')
    except OSError:
      Warn(self, 'OS Error (try connecting from another port)')
    self.socket.settimeout(self.cnf.connTimeOut)

  def disconnect(self, params, reinit=True):
    try:
      self.socket.shutdown(1)
      self.socket.close()
    except OSError: Warn(self, 'Can not disconnect (not connected)'); return
    if reinit: self.initSocket()

  def rebind(self, params):
    if self.connection.state: self.disconnect(reinit=False)
    try: params.port  = int(params.port)
    except ValueError: Warn(self, 'Port must be a number'); return
    self.usedPort = params.port
    self.initSocket()

  def receive(self):
    try:
      data = self.socket.recv(self.cnf.incomingBufferSize)
      if len(data) > 0: Debug(self, data); self.parser.pushBytes(data)
    except scklib.timeout: pass
    except (ConnectionAbortedError, ConnectionResetError) as exc:
      Error(self, 'Connection was broken')
      self.initSocket()

  def transmit(self, event):
    if not self.connection.state: return
    query = Cis.Query(event.id, **event.getArgs())
    data = query.build()
    try: self.socket.send(data)
    except scklib.timeout as exc:
      Error(self, 'Transmission timeout')
      self.initSocket()
    except (ConnectionAbortedError, ConnectionResetError) as exc:
      Error(self, 'Connection was broken')
      self.initSocket()

  @staticmethod
  def getOwnAddress():
    s = scklib.socket(scklib.AF_INET, scklib.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    address = s.getsockname()[0]
    s.close()
    return address

  def handleReceivedData(self):
    while not self.parser.queries.empty():
      Debug(self, 'Popped CIS query')
      query = self.parser.queries.pop()
      PluginEvent(self, query.key, **query.params)

  def quit(self):
    super().quit()
    self.disconnect(reinit=False)
