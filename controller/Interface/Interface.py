
# Uses experimental TkiWrapper

class Interface(Plugin):
  def init(self):
    super().init()
    self.statusWidgets = {}
    self.nodes = {}
    self.frames = Namespace()
    self.addEventHandler('PluginStatus', self.handleStatus)
    self.addEventHandler('NewCamFrame', self.handleCamFrame)
    self.root = tki.Root(self.cnf.Title)
    self.root.setMinSize(self.cnf.Window.minWidth, self.cnf.Window.minHeight)
    self.root.setColWeights(0, 1)
    self.root.setRowWeights(1)

    # TODO: Apply styles, cannot do now as new experimental version of TkiWrapper
    # does not support it yet

    with tki.FrameScrollable(self.root, tki.Point(0,0)) as frame:
      self.frames.home = frame
      frame.showOnKey('F1')
      frame.show()
      frame.setColWeights(1)
      frame.pst.setWrap(2)
      tkw.Label(frame, 'Home')

    with tki.FrameSimple(self.root, tki.Point(1,0)) as frame:
      self.frames.camera = frame
      frame.showOnKey('F2')
      frame.setColWeights(1)
      frame.setRowWeights(1)
      tkw.Label(frame, 'Camera')

  def update(self):
    super().update()
    if self.root.isRunning(): self.root.update()
    else: self.stopProgram()
    self.setPluginOutputs()

  def handleStatus(self, event):
    for key, val in event.data.items():
      id = f'{event.pluginKey}::{key}'
      if type(val) == float: val = round(val, 3)
      val = str(val)
      if id not in self.statusWidgets.keys():
        frame = self.frames.home
        tkw.Label(frame, id)
        self.statusWidgets[id] = tkw.TextField(frame)
      self.statusWidgets[id].set(val)

  def onProgramInit(self, event):
    frame = self.frames.home
    self.nodes = {k:Namespace(**d) for k, d in event.nodes.items()}
    for key, node in self.nodes.items():
      node.textFields = Namespace()
      tkw.Label(frame, f'{node.owner} {node.key}')
      frame.pst.nextRow()
      for param in node.paramKeys:
        tkw.Label(frame, param)
        node.textFields[param] = tkw.TextField(frame)
      tkw.Button(frame, node.key, lambda: self.onAutoButton(key))
      frame.pst.nextRow()

  def onAutoButton(self, id):
    node = self.nodes[id]
    params = {p:node.textFields[p].get() for p in node.paramKeys}
    event = Event(self, f'$_{id}', **params)

  def handleCamFrame(self, event):
    return
    # if not self.frameHolderExists:
    #   frame = self.frames.camera
    #   self.canvas = tkc.Canvas(view, 'cameraCanvas', (40,30))
    #   self.canvas.persistent(True)
    #   self.canvas.background('#000')
    #   self.frameHolderExists = True
    # elms = self.canvas.elements.persistent
    # if len(elms) >= 5: elms[0].remove() # TEMP
    # tkce.OcvImage(self.canvas, (0,0), (40,30), event.frame)
