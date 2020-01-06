
class CamReceiver(Plugin):
  def init(self):
    super().init()
    context = zmq.Context()
    self.socket = context.socket(zmq.SUB)
    self.socket.bind(f'tcp://*:{self.cnf.usedPort}')
    self.socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    self.socket.RCVTIMEO = int(self.cnf.timeOut * 1e3)
    self.lastFrame = None

  def update(self):
    super().update()
    try: raw = self.socket.recv_string()
    except zmq.error.Again: return
    img = base64.b64decode(raw)
    img = np.frombuffer(img, dtype=np.uint8)
    frame = ocv.imdecode(img, 1)
    Event(self, 'NewCamFrame', frame=frame)
    self.lastFrame = frame

  def quit(self):
    super().quit()
