
class Interface(Plugin):
  def init(self):
    super().init()
    self.statusWidgets = {}
    self.nodes = {} # automated handling of plugin input nodes
    self.addEventHandler('PluginStatus', self.handleStatus)

    grid = tki.positioners.Register.get('Grid')
    grid.DEFAULTS.marginX = 4
    grid.DEFAULTS.marginY = 4

    variant = Settings.Custom.programVariant
    self.root = tki.Root(self.cnf.title[variant])
    self.root.setMinSize(self.cnf.WINDOW.minWidth, self.cnf.WINDOW.minHeight)
    self.root.setSlotsWeights(0, 0, 1)

    style = tki.Style()
    if systemName == 'nt': style.setTheme(self.cnf.THEME.wind)
    else: style.setTheme(self.cnf.THEME.unix)

    for key, val in self.cnf.COLORS.__dict__.items():
      if key.startswith('__'): continue
      style.setColor(key, val)
    for key, val in self.cnf.FONT_SIZE.__dict__.items():
      if key.startswith('__'): continue
      style.setFontSize(key, val)
    self.root.applyStyle(style)

    self.header = tki.HeaderView(self.root, 'header0')
    self.header.setColWeights(1)
    tkw.Label(self.header, self.cnf.title[variant], heading=3)
    tkw.Separator(self.header)

    view = tki.View(self.root, 'home', 0)
    view.pst.setColWrap(2)
    self.root.show('home')

  def update(self):
    super().update()
    if self.root.leave: self.stopProgram()
    else: self.root.update()

  def quit(self):
    super().quit()
    try: self.root.quit()
    except TclError: pass

  def handleStatus(self, event):
    for key, val in event.data.items():
      id = f'{event.pluginKey}::{key}'
      if type(val) == float: val = round(val, 3)
      val = str(val)
      if id in self.statusWidgets.keys():
        self.statusWidgets[id].setContent(val)
      else:
        view = self.root.views['home']
        tkw.Label(view, id)
        self.statusWidgets[id] = tkw.Output(view, id, val)

  def onProgramInit(self, event):
    view = self.root.views['home']
    self.nodes = {k:Namespace(**d) for k, d in event.nodes.items()}
    for node in self.nodes.values():
      id = f'{node.owner}_{node.key}'
      tkw.Label(view, f'{node.owner} {node.key}', heading=3)
      view.pst.newLine()
      for param in node.paramKeys:
        tkw.Label(view, f'{param}')
        tkw.Input(view, f'{id}_In_{param}')
      def addButton(inst, _id):
        tkw.Button(view, f'{_id}_Confirm_', node.key, lambda: inst.onAutoButton(_id))
      addButton(self, id)
      view.pst.newLine()

  def onAutoButton(self, id):
    node = self.nodes[id]
    params = {key: self.root.getByKey(f'{id}_In_{key}').read() \
      for key in node.paramKeys}
    event = Event(self, f'$_{id}', **params)
