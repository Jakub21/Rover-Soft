
class Parser:
  def __init__(self, responseKeys):
    self.data = b''
    self.received = []
    self.responseKeys = responseKeys

  def push(self, data):
    self.data += data.replace(b'\r',b'')

  def pop(self):
    result = self.received[0].decode('ansi').split()
    self.received = self.received[1:]
    key = int(result[0])
    params = [float(x) for x in result[1:]]
    return Response(self.responseKeys, key, params)

  def isEmpty(self):
    return len(self.received) == 0

  def parse(self):
    while b'\n' in self.data:
      end = self.data.index(b'\n')
      command = self.data[:end]
      self.data = self.data[end+1:]
      self.received += [command]
