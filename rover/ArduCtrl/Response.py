
class Response:
  def __init__(self, responseKeys, key, params):
    self.isValid = True
    try: self.key = responseKeys[key]
    except KeyError:
      self.key = key
      self.isValid = False
    self.params = params

  def __str__(self):
    return f'<Response {self.key} valid={self.isValid} params={self.params}>'
