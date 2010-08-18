from pybass import *


from main import bass_call
from channel import Channel

class BassSoundOutput (object):

 def __init__ (self, device=-1, frequency=44100, flags=BASS_DEVICE_3D, window=0, clsid=None):
  BASS_Init(device, frequency, flags, window, clsid)

 def get_volume (self):
  volume = BASS_GetConfig(BASS_CONFIG_GVOL_STREAM)
  if volume:
   volume = volume / 100.0
  return volume

 def set_volume (self, volume):
  #Pass in a float 0.0 to 100.0 and watch the volume magically change
  bass_call(BASS_SetConfig, BASS_CONFIG_GVOL_STREAM, int(round(volume*100, 2)))

 volume = property(get_volume, set_volume)


class Sound (Channel):

 def __init__ (self, filename, flags=0):
  self.filename = filename
  self.flags = flags

 def play (self, restart=False):
  self.create_stream()
  bass_call(BASS_ChannelPlay, self.stream, restart)
  return self.stream

 def stop (self):
  bass_call(BASS_ChannelStop, self.stream)

 @property
 def is_playing (self):
  return BASS_ChannelIsActive(self.stream) == BASS_ACTIVE_PLAYING

 def create_stream (self):
  if not hasattr(self, 'stream') or not self.stream:
   self.stream = self._create_stream(self.filename, self.flags)

 @staticmethod
 def _create_stream (filename, flags):
  return bass_call(BASS_StreamCreateFile, False, filename, 0, 0, flags)

 def destroy_stream (self):
  bass_call(BASS_StreamFree, self.stream)
  self.stream = None


class StreamingSound (Sound):

 def __init__ (self, filename, flags=BASS_STREAM_AUTOFREE):
  super(StreamingSound, self).__init__(filename, flags=flags)
  self.callback = DOWNLOADPROC(self._callback)

 def _callback (*args):
  return 0

 def _create_stream (self, filename, flags):
  return bass_call(BASS_StreamCreateURL, filename, 0, flags, self.callback, None)

 def play (self, restart=True):
  super(StreamingSound, self).play(restart=restart)

 def stop (self):
  super(StreamingSound, self).stop()
  self.stream = None


def test_sound_output (filename=r"c:\windows\media\tada.wav"):
 o = BassSoundOutput()
 s = Sound(filename)
 s.play()
 return s
