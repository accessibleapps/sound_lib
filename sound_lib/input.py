from ctypes import string_at
import wave

from pybass import *

from main import bass_call

class Input (object):
 def __init__ (self, device=-1):
  bass_call(BASS_RecordInit, device)
