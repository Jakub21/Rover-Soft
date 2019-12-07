import Pluginable as plg

if __name__ == '__main__':
  prog = plg.Program('Controller')
  prog.customSettings({
    'programVariant': 'controller',
  })
  prog.updateSettings({
    'Compiler.pluginDirectories' : ['./universal', './controller'],
    'Logger.timeMode': 'relative',
  })
  prog.preload()
  prog.init()
  prog.run()
