
class CamSender(Plugin):
  def init(self):
    super().init()
    context = zmq.Context()
    self.socket = context.socket(zmq.PUB)
    self.socket.connect(f'tcp://{self.cnf.receiverAddress}:{self.cnf.receiverPort}')
    self.socket.RCVTIMEO = int(self.cnf.timeOut * 1e3)

    pgc.init()
    self.camera = pgc.Camera(pgc.list_cameras()[self.cnf.cameraIndex])
    self.camera.start()

  def update(self):
    super().update()
    frame = self.camera.get_image()
    Debug(self, f'Frame = {frame}')
    size = self.cnf.transmitSize
    try: frame = ocv.resize(frame, (size.x, size.y))
    except ocv.error: return

    encoded, buffer = ocv.imencode('.jpg', frame)
    data = base64.b64encode(buffer)
    self.socket.send(data)

  def quit(self):
    super().quit()
    pgc.quit()
