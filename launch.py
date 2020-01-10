import Pluginable as plg

if __name__ == '__main__':
  prog = plg.Program('Rover')
  prog.customSettings({
    'programVariant': 'rover',
  })
  prog.updateSettings({
    'Kernel.MaxProgramTicksPerSec': 100,
    'Kernel.MaxExecutorTicksPerSec': 80,
    'Compiler.pluginDirectories' : ['./universal', './rover'],
    'Logger.timeMode': 'relative',
  })
  prog.preload()
  prog.configPlugin('ArduCtrl', {
    'PortName': '/dev/ttyUSB0',
  })
  prog.configPlugin('CamSender', {
    'cameraIndex': 0,
    'receiverAddress': '192.168.1.102',
  })
  prog.run()
