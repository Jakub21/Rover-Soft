import Pluginable as plg

if __name__ == '__main__':
  prog = plg.Program('Controller')
  prog.customSettings({
    'programVariant': 'controller',
  })
  prog.updateSettings({
    'Kernel.MaxProgramTicksPerSec': 100,
    'Kernel.MaxExecutorTicksPerSec': 80,
    'Kernel.AutoAddTpsToPluginOutputs': True,
    'Compiler.pluginDirectories' : ['./universal', './controller'],
    'Logger.timeMode': 'relative',
  })
  prog.preload()
  prog.run()
