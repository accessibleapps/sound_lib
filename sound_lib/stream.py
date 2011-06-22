from channel import Channel
from main import bass_call
from external.pybass import *

class BaseStream(Channel):
 @staticmethod
 def flags_for(three_d=False, autofree=False, decode=False, mono=False):
  flags = 0
  if three_d:
   flags = flags | BASS_SAMPLE_3D
  if autofree:
   flags = flags | BASS_STREAM_AUTOFREE
  if decode:
   flags = flags | BASS_STREAM_DECODE
  if mono:
   flags = flags | BASS_SAMPLE_MONO
  return flags

 def _callback(*args):
  #Stub it out as otherwise it'll crash, hard.  Used for stubbing download procs
  return 0
 
 def free(self):
  return bass_call(BASS_StreamFree, self.handle)

class Stream(BaseStream):

 def __init__(self, freq=44100, chans=2, flags=0, proc=None, user=None, three_d=False, autofree=False, decode=False):
  self.proc = STREAMPROC(proc)
  flags = flags | self.flags_for(three_d=three_d, autofree=autofree, decode=decode)
  handle = bass_call(BASS_StreamCreate, freq, chans, flags, self.proc, user)
  super(Stream, self).__init__(handle)

class FileStream(BaseStream):

 def __init__(self, mem=False, file=None, offset=0, length=0, flags=0, three_d=False, mono=False, autofree=False, decode=False):
  """Creates a sample stream from an MP3, MP2, MP1, OGG, WAV, AIFF or plugin supported file."""
  flags = flags | self.flags_for(three_d=three_d, autofree=autofree, mono=mono, decode=decode)
  if isinstance(file, unicode):
   file = file.encode('UTF-8')
  self.file = file
  handle = bass_call(BASS_StreamCreateFile, mem, file, offset, length, flags)
  super(FileStream, self).__init__(handle)

class URLStream(BaseStream):

 def __init__(self, url="", offset=0, flags=0, downloadproc=None, user=None):
  self._downloadproc = downloadproc or self._callback #we *must hold on to this
  self.downloadproc = DOWNLOADPROC(self._downloadproc)
  self.url = url
  handle = bass_call(BASS_StreamCreateURL, url, offset, flags, self.downloadproc, user)
  super(URLStream, self).__init__(handle)

