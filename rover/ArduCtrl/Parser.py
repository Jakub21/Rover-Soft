
class Parser:
  def __init__(self):
    self.data = b''
    self.received = []

  def push(self, data):
    self.data += data

  def pop(self):
    result = self.received[0]
    self.received = self.received[1:]
    return result

  def parse(self):
    while b'\n' in self.data:
      end = self.data.index(b'\n')
      command = self.data[:end]
      self.data = self.data[end:]
      self.received += [command]
