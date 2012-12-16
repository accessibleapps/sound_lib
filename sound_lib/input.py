from ctypes import string_at
import wave

from external.pybass import *
import config
from main import bass_call

class Input (object):

 def __init__ (self, device=-1):
  bass_call(BASS_RecordInit, device)
  self.config = config.BassConfig()

 def free(self):
  """Frees all resources used by the recording device."""
  return bass_call(BASS_RecordFree)
