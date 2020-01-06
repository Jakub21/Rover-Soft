
class CamSender(Plugin):
  def init(self):
    super().init()
    context = zmq.Context()
    self.socket = context.socket(zmq.PUB)
    self.socket.connect(f'tcp://{self.cnf.receiverAddress}:{self.cnf.receiverPort}')
    self.socket.RCVTIMEO = int(self.cnf.timeOut * 1e3)

    self.camera = ocv.VideoCapture(self.cnf.cameraIndex)

  def update(self):
    super().update()
    success, frame = self.camera.read()
    size = self.cnf.transmitSize
    try: frame = ocv.resize(frame, (size.x, size.y))
    except ocv.error: return

    encoded, buffer = ocv.imencode('.jpg', frame)
    data = base64.b64encode(buffer)
    self.socket.send(data)

  def quit(self):
    super().quit()
    self.camera.release()
