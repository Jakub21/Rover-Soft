import Pluginable as plg

if __name__ == '__main__':
  prog = plg.Program('Rover')
  prog.customSettings({
    'programVariant': 'rover',
  })
  prog.updateSettings({
    'Kernel.MaxProgramTicksPerSec': 400,
    'Kernel.MaxExecutorTicksPerSec': 400,
    'Compiler.pluginDirectories' : ['./universal', './rover'],
    'Logger.timeMode': 'relative',
  })
  prog.preload()
  prog.run()
