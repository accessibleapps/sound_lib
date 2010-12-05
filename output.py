from pybass import *
import platform

from main import bass_call, bass_call_0

class Output (object):

 def __init__ (self, device=-1, frequency=44100, flags=0, window=0, clsid=None):
  if platform.system() == 'Linux' and device == -1: #Bass wants default device set to 1 on linux
   device = 1
  bass_call(BASS_Init, device, frequency, flags, window, clsid)

 def start(self):
  return bass_call(BASS_Start)

 def pause(self):
  return bass_call(BASS_Pause)

 def stop(self):
  return bass_call(BASS_Stop)

 def get_device(self):
    return bass_call_0(BASS_GetDevice)

 def set_device(self, device):
  return bass_call(BASS_SetDevice, device)

 device = property(get_device, set_device)

 def get_volume (self):
  volume = BASS_GetConfig(BASS_CONFIG_GVOL_STREAM)
  if volume:
   volume = volume / 100.0
  return volume

 def set_volume (self, volume):
  #Pass in a float 0.0 to 100.0 and watch the volume magically change
  return bass_call(BASS_SetConfig, BASS_CONFIG_GVOL_STREAM, int(round(volume*100, 2)))

 volume = property(get_volume, set_volume)


class ThreeDOutput(Output):

 def __init__(self, flags=BASS_DEVICE_3D, *args, **kwargs):
  super(ThreeDOutput, self).__init__(flags=flags, *args, **kwargs)
