from pybass import *

from __main__ import bass_call


class BassSoundOutput (object):

 def __init__ (self, device=-1, frequency=44100, flags=0, window=0, clsid=None):
  BASS_Init(device, frequency, flags, window, clsid)


class Sound (object):

 def __init__ (self, filename, flags=0):
  self.filename = filename
  self.flags = flags
  self.stream = self.create_stream(filename, flags)

 def play (self):
  bass_call(BASS_ChannelPlay, self.stream, False)
  return self.stream

 def stop (self):
  bass_call(BASS_ChannelStop, self.stream)

 @property
 def is_playing (self):
  return BASS_ChannelIsActive(self.stream) == BASS_ACTIVE_PLAYING

 @staticmethod
 def create_stream (filename, flags):
  return bass_call(BASS_StreamCreateFile, False, filename, 0, 0, flags)

def test_sound_output (filename=r"c:\windows\media\tada.wav"):
 o = BassSoundOutput()
 s = Sound(filename)
 s.play()
 return s
