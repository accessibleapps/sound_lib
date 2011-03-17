from functools import partial
import platform
from ctypes import c_char_p, c_float, pointer, string_at
from pybass import *
from main import bass_call, bass_call_0, EAX_ENVIRONMENTS, update_3d_system

_getter = lambda func, key, obj: func(obj)[key]
_setter = lambda func, kwarg, obj, val: func(obj, **{kwarg: val})

class Output (object):

 def __init__(self, device=-1, frequency=44100, flags=0, window=0, clsid=None):
  try:
   self.use_default_device()
  except:
   pass
  self.init_device(device=device, frequency=frequency, flags=flags, window=window, clsid=clsid)
  self.proxy = None

 def init_device(self, device=-1, frequency=44100, flags=0, window=0, clsid=None):
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

 def free(self):
  return bass_call(BASS_Free)

 def get_proxy(self):
  ptr = bass_call(BASS_GetConfigPtr, BASS_CONFIG_NET_PROXY)
  return string_at(ptr)

 def set_proxy(self, proxy):
  self.proxy = c_char_p(proxy)
  return bass_call(BASS_SetConfigPtr, BASS_CONFIG_NET_PROXY, self.proxy)

 def use_default_device(self, use=True):
  return bass_call(BASS_SetConfig, BASS_CONFIG_DEV_DEFAULT, use)

 @staticmethod
 def get_device_names():
  """Convenience method that returns a list of device names that are considered
 valid by bass.
	
  Parameters: none.
  returns: list of devices, 0-indexed.
  """
  result = [] # empty list to start.
  info = BASS_DEVICEINFO()
  count = 1
  while BASS_GetDeviceInfo(count, ctypes.byref(info)):
   if info.flags & BASS_DEVICE_ENABLED:
    result.append(info.name)
   count += 1
  return result



class ThreeDOutput(Output):

 def __init__(self, flags=BASS_DEVICE_3D, *args, **kwargs):
  super(ThreeDOutput, self).__init__(flags=flags, *args, **kwargs)

 def get_3d_factors(self):
  res = {
   'distance_factor': c_float(),
   'rolloff': c_float(),
   'doppler_factor': c_float()
  }
  bass_call(BASS_Get3DFactors, pointer(res['distance_factor']), pointer(res['rolloff']), pointer(res['doppler_factor']))
  return {k: res[k].value for k in res}

 @update_3d_system
 def set_3d_factors(self, distance_factor=-1, rolloff=-1, doppler_factor=-1):
  conversions = {
   'meters': 1.0,
   'yards': 0.9144,
   'feet': 0.3048
  }
  if distance_factor in conversions:
   distance_factor = conversions[distance_factor]
  return bass_call(BASS_Set3DFactors, distance_factor, rolloff, doppler_factor)

 distance_factor = property(fget=partial(_getter, get_3d_factors, 'distance_factor'), fset=partial(_setter, set_3d_factors, 'distance_factor'))

 rolloff = property(fget=partial(_getter, get_3d_factors, 'rolloff'), fset=partial(_setter, set_3d_factors, 'rolloff'))

 doppler_factor = property(fget=partial(_getter, get_3d_factors, 'doppler_factor'), fset=partial(_setter, set_3d_factors, 'doppler_factor'))

 def set_eax_parameters(self, environment=None, volume=None, decay=None, damp=None):
  def convert_arg(arg):
   if arg is None:
    arg = -1
   return arg
  environment = convert_arg(environment)
  if isinstance(environment, basestring) and environment in EAX_ENVIRONMENTS:
   environment = EAX_ENVIRONMENTS[environment]
  volume = convert_arg(volume)
  decay = convert_arg(decay)
  damp = convert_arg(damp)
  bass_call(BASS_SetEAXParameters, environment, volume, decay, damp)
