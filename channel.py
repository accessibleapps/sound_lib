from pybass import *
from main import bass_call, bass_call_0
from ctypes import pointer, c_float, c_long, c_ulong

class Channel (object):

 def __init__ (self, handle):
  self.handle = handle

 def play (self, restart=False):
  """Starts (or resumes) playback of a sample, stream, MOD music, or recording."""
  return bass_call(BASS_ChannelPlay, self.handle, restart)

 def pause (self):
  return bass_call(BASS_ChannelPause, self.handle)

 def is_active (self):
  "Checks if a sample, stream, or MOD music is active (playing) or stalled. Can also check if a recording is in progress."""
  return bass_call_0(BASS_ChannelIsActive, self.handle)

 def get_position (self, mode=BASS_POS_BYTE):
  """Retrieves the playback position of a sample, stream, or MOD music. Can also be used with a recording channel."""
  return bass_call_0(BASS_ChannelGetPosition, self.handle, mode)

 def set_position (self, pos, mode=BASS_POS_BYTE):
  """Sets the playback position of a sample, MOD music, or stream."""
  return bass_call(BASS_ChannelSetPosition, self.handle, pos, mode)

 position = property(get_position, set_position)

 def stop (self):
  """Stops a sample, stream, MOD music, or recording."""
  return bass_call(BASS_ChannelStop, self.handle)

 def update (self, length):
  """Updates the playback buffer of a stream or MOD music."""
  return bass_call(BASS_ChannelUpdate, self.handle, length)

 def get_length (self, mode=BASS_POS_BYTE):
  return bass_call_0(BASS_ChannelGetLength, self.handle, mode)

 __len__ = get_length

 def get_device(self):
  """Retrieves the device that a channel is using."""
  return bass_call_0( BASS_ChannelGetDevice, self.handle)

 def set_device (self, device):
  """Changes the device that a stream, MOD music or sample is using."""
  bass_call(BASS_ChannelSetDevice, self.handle, device)

 device = property(get_device, set_device)

 def set_fx(self, type, priority=0):
  """Sets an effect on a stream, MOD music, or recording channel."""
  return SoundEffect(bass_call(BASS_ChannelSetFX, type, priority))

 def bytes_to_seconds(self, position=None):
  """Translates a byte position into time (seconds), based on a channel's format."""
  position = position or self.position
  return bass_call_0(BASS_ChannelBytes2Seconds, self.handle, position)

 def seconds_to_bytes(self, position):
  """Translates a time (seconds) position into bytes, based on a channel's format."""
  return bass_call_0(BASS_ChannelSeconds2Bytes, position)

 def get_attribute(self, attribute):
  """Retrieves the value of a channel's attribute."""
  value = pointer(c_float())
  bass_call(BASS_ChannelGetAttribute, self.handle, attribute, value)
  return value.contents.value

 def set_attribute(self, attribute, value):
  """Sets the value of a channel's attribute."""
  return bass_call(BASS_ChannelSetAttribute, self.handle, attribute, value)

 def slide_attribute(self, attribute, value, time):
  """Slides a channel's attribute from its current value to a new value."""
  return bass_call(BASS_ChannelSlideAttribute, self.handle, attribute, value, time)

 def is_sliding (self, attribute=None):
  """Checks if an attribute (or any attribute) of a sample, stream, or MOD music is sliding."""
  return bass_call_0(BASS_ChannelIsSliding, self.handle, attribute)

 def get_info(self):
  """Retrieves information on a channel."""
  value = pointer(BASS_CHANNELINFO())
  bass_call(BASS_ChannelGetInfo, self.handle, value)
  return value[0]

 def get_level(self):
  """Retrieves the level (peak amplitude) of a stream, MOD music or recording channel."""
  return bass_call_0(BASS_ChannelGetLevel, self.handle)

 def lock(self):
  """Locks a stream, MOD music or recording channel to the current thread."""
  return bass_call(BASS_ChannelLock, self.handle, True)

 def unlock(self):
  """Unlocks a stream, MOD music or recording channel from the current thread."""
  return bass_call(BASS_ChannelLock, self.handle, False)

 def get_3d_attributes(self):
  """Retrieves the 3D attributes of a sample, stream, or MOD music channel with 3D functionality."""
  answer = dict(mode=c_ulong(), min=c_float(), max=c_float(), iangle=c_ulong(), oangle=c_ulong(), outvol=c_float())
  bass_call(BASS_ChannelGet3DAttributes, self.handle, pointer(answer['mode']), pointer(answer['min']), pointer(answer['max']), pointer(answer['iangle']), pointer(answer['oangle']), pointer(answer['outvol']))
  for k in answer:
   answer[k] = answer[k].value()
  return answer

 def set_3d_attributes(self, mode=-1, min=0.0, max=0.0, iangle=-1, oangle=-1, outvol=-1):
  """Sets the 3D attributes of a sample, stream, or MOD music channel with 3D functionality."""
  return bass_call(BASS_ChannelSet3DAttributes, self.handle, mode, min, max, iangle, oangle, outvol)
