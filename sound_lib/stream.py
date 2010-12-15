from channel import Channel
from main import bass_call
from pybass import *

class BaseStream(Channel):
 
 def free(self):
  return bass_call(BASS_StreamFree, self.handle)

class Stream(BaseStream):

 def __init__(self, freq=44100, chans=2, flags=0, proc=None, user=None):
  self.proc = STREAMPROC(proc)
  handle = bass_call(BASS_StreamCreate, freq, chans, flags, self.proc, user)
  super(Stream, self).__init__(handle)

class FileStream(BaseStream):

 def __init__(self, mem=False, file=None, offset=0, length=0, flags=0):
  """Creates a sample stream from an MP3, MP2, MP1, OGG, WAV, AIFF or plugin supported file."""
  handle = bass_call(BASS_StreamCreateFile, mem, file, offset, length, flags)
  super(FileStream, self).__init__(handle)

class URLStream(BaseStream):

 def __init__(self, url="", offset=0, flags=0, downloadproc=None, user=None):
  self._downloadproc = downloadproc or self._callback #we *must hold on to this
  self.downloadproc = DOWNLOADPROC(self._downloadproc)
  handle = bass_call(BASS_StreamCreateURL, url, offset, flags, self.downloadproc, user)
  super(URLStream, self).__init__(handle)

 def _callback(*args):
  #Stub it out as otherwise it'll crash, hard.
  return 0

