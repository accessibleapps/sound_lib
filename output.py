from pybass import *

from __main__ import bass_call


class BassSoundOutput (object):

 def __init__ (self, device=-1, frequency=44100, flags=0, window=0, clsid=None):
  BASS_Init(device, frequency, flags, window, clsid)


class Sound (object):

 def __init__ (self, filename, flags=0):
  self.filename = filename
  self.flags = flags

 def play (self):
  self.create_stream()
  bass_call(BASS_ChannelPlay, self.stream, False)
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



def test_sound_output (filename=r"c:\windows\media\tada.wav"):
 o = BassSoundOutput()
 s = Sound(filename)
 s.play()
 return s
