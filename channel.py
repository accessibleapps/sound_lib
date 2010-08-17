from pybass import *
from main import bass_call, bass_call_0

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
