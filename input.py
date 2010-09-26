from ctypes import string_at
import wave

from pybass import *

from main import bass_call

class BassSoundInput (object):
 def __init__ (self, device=-1):
  bass_call(BASS_RecordInit, device)
#  self.RECORDPROC = WINFUNCTYPE(c_bool, HRECORD, c_void_p, c_ulong, c_void_p)

class SoundRecording(object):

 def __init__ (self, frequency=44100, channels=2, flags=0, callback=None, *args, **kwargs):
  super(SoundRecording, self).__init__(*args, **kwargs)
  self.frequency = frequency
  self.channels = channels
  self.flags = flags
  self.callback = RECORDPROC(callback)
  self.stream = None

 def start (self):
  self.is_recording = True
  self.stream = BASS_RecordStart(self.frequency, self.channels, self.flags, self.callback, None)

 def stop (self):
  self.is_recording = False
  bass_call(BASS_ChannelStop, self.stream)

class FileRecording (SoundRecording):

 def __init__(self, callback=None, filename=None, *args, **kwargs):
  callback = callback or self.recording_callback
  super(FileRecording, self).__init__(callback=callback, *args, **kwargs)
  self.filename = filename
  self.file = None

 def recording_callback(self, handle, buffer, length, user):
  buf = string_at(buffer, length)
  self.file.writeframes(buf)
  return self.is_recording

 def start (self):
  if not self.file or self.file.closed:
   self._setup_file()
  super(FileRecording, self).start()

 def _setup_file (self):
  self.file = wave.open(self.filename, 'w')
  self.file.setnchannels(self.channels)
  self.file.setsampwidth(4)
  self.file.setframerate(self.frequency/self.channels)


def test_sound_input (filename="test.wav"):
 i = BassSoundInput()
 r = FileRecording(filename=filename)
 r.start()
 return r
