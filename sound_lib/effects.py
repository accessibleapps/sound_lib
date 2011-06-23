import ctypes
from external import pybass, pybass_fx
from stream import BaseStream
from channel import Channel
from main import bass_call, bass_call_0

class Tempo(BaseStream):

 def __init__(self, channel, flags=0, loop=False, software=False, three_d=False, sample_fx=False, autofree=False, decode=False, free_source=False):
  flags = flags | self.flags_for(loop=False, software=False, three_d=False, sample_fx=False, autofree=False, decode=False, free_source=False)
  if isinstance(channel, Channel):
   channel = channel.handle
  self.handle = bass_call(pybass_fx.BASS_FX_TempoCreate, channel, flags)

 @property
 def tempo(self):
  """The tempo of a channel."""
  return self.get_attribute(pybass_fx.BASS_ATTRIB_TEMPO)
 
 @tempo.setter
 def tempo(self, val):
  self.set_attribute(pybass_fx.BASS_ATTRIB_TEMPO, val)

 @property
 def pitch(self):
  return self.get_attribute(pybass_fx.BASS_ATTRIB_TEMPO_PITCH)

 @pitch.setter
 def pitch(self, val):
  self.set_attribute(pybass_fx.BASS_ATTRIB_TEMPO_PITCH, val)

 @staticmethod
 def flags_for(loop=False, software=False, three_d=False, sample_fx=False, autofree=False, decode=False, free_source=False):
  flags = 0
  if loop:
   flags |= pybass.BASS_SAMPLE_LOOP
  if software:
   flags |= pybass.BASS_SAMPLE_SOFTWARE
  if three_d:
   flags |= pybass.BASS_SAMPLE_3D
  if sample_fx:
   flags |= pybass.BASS_SAMPLE_FX
  if autofree:
   flags |= pybass.BASS_STREAM_AUTOFREE
  if decode:
   flags |= BASS_STREAM_DECODE
  if free_source:
   flags |= pybass_fx.BASS_FX_FREESOURCE
  return flags
