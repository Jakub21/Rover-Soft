import Pluginable as plg

if __name__ == '__main__':
  prog = plg.Program('Controller')
  prog.customSettings({
    'programVariant': 'controller',
  })
  prog.updateSettings({
    'Kernel.MaxProgramTicksPerSec': 400,
    'Kernel.MaxExecutorTicksPerSec': 400,
    'Compiler.pluginDirectories' : ['./universal', './controller'],
    'Logger.timeMode': 'relative',
  })
  prog.preload()
  prog.run()
