
class Config:
  PortName = 'dev/ttyusb0'
  Baudrate = 9600
  ReadBytesPerLoop = 512
  MaxCallLength = 16
  RequestReadingsInterval = 50 # in plugin ticks

  OutputKeys = Namespace(
    RequestTmpr = 0,
    SetServo = 1,
  )

  ResponseKeys = {
    1: 'TmprRspb',
    2: 'TmprAccu',
    3: 'TmprCnvrt',
    255: 'Error',
  }
