from external import pybass, pybassenc
from main import bass_call, bass_call_0, FlagObject

class Encoder(FlagObject):

	def setup_flag_mapping(self):
		#super(Encoder, self).setup_flag_mapping()
		self.flag_mapping = {
			'pcm': pybassenc.BASS_ENCODE_PCM,
			'no_header': pybassenc.BASS_ENCODE_NOHEAD,
			'rf64': pybassenc.BASS_ENCODE_RF64,
			'big_endian': pybassenc.BASS_ENCODE_BIGEND,
			'fp_8bit': pybassenc.BASS_ENCODE_FP_8BIT,
			'fp_16bit': pybassenc.BASS_ENCODE_FP_16BIT,
			'fp_24bit': pybassenc.BASS_ENCODE_FP_24BIT,
			'fp_32bit': pybassenc.BASS_ENCODE_FP_32BIT,
			'queue': pybassenc.BASS_ENCODE_QUEUE,
			'limit': pybassenc.BASS_ENCODE_LIMIT,
			'no_limit': pybassenc.BASS_ENCODE_CAST_NOLIMIT,
			'pause': pybassenc.BASS_ENCODE_PAUSE,
			'autofree': pybassenc.BASS_ENCODE_AUTOFREE,
			'unicode': pybass.BASS_UNICODE,
		}

	def __init__(self, source, command_line, pcm=False, no_header=False, rf64=False, big_endian=False, fp_8bit=False, fp_16bit=False, fp_24bit=False, fp_32bit=False, queue=False, limit=False, no_limit=False, pause=True, autofree=False, callback=None, user=None):
		self.setup_flag_mapping()
		flags = self.flags_for(pcm=pcm, no_header=no_header, rf64=rf64, big_endian=big_endian, fp_8bit=fp_8bit, fp_16bit=fp_16bit, fp_24bit=fp_24bit, fp_32bit=fp_32bit, queue=queue, limit=limit, no_limit=no_limit, pause=pause, autofree=autofree) #fwiw!
		self.source = source
		source_handle = source.handle
		if callback is None:
			callback = lambda *a: None
		callback = pybassenc.ENCODEPROC(callback)
		self.callback = callback
		self.handle = bass_call(pybassenc.BASS_Encode_Start, source_handle, command_line, flags, callback, user)

	@property
	def paused(self):
		return bass_call_0(pybassenc.BASS_Encode_IsActive, self.handle) == pybass.BASS_ACTIVE_PAUSED

	@paused.setter
	def paused(self, paused):
		return bass_call(pybassenc.BASS_Encode_SetPaused, self.handle, paused)
	
	def is_stopped(self):
		return bass_call_0(pybassenc.BASS_Encode_IsActive, self.handle) == pybass.BASS_ACTIVE_STOPPED


	def stop(self):
		return bass_call(pybassenc.BASS_Encode_Stop, self.handle)

class BroadcastEncoder(Encoder):

	def __init__(self, source_encoder, server, password, content, name=None, url=None, genre=None, description=None, headers=None, bitrate=0, public=False):
		contents = {
			'mp3': pybassenc.BASS_ENCODE_TYPE_MP3,
			'ogg': pybassenc.BASS_ENCODE_TYPE_OGG,
			'aac': pybassenc.BASS_ENCODE_TYPE_AAC
		}
		if content in contents:
			content = contents[content]
		self.source_encoder = source_encoder
		handle = source_encoder.handle
		self.server = server
		self.password = password
		self.status = bass_call(pybassenc.BASS_Encode_CastInit, handle, server, password, content, name, url, genre, description, headers, bitrate, public)

	def set_title(self, title=None, url=None):
		return bass_call(pybassenc.BASS_Encode_CastSetTitle, self.source_encoder.handle, title, url)

	def get_stats(self, type, password=None):
		types = {
			'shoutcast': pybassenc.BASS_ENCODE_STATS_SHOUT,
			'icecast': pybassenc.BASS_ENCODE_STATS_ICE,
			'icecast_server': pybassenc.BASS_ENCODE_STATS_ICESERV,
		}
		if type in types:
			type = types[type]
		if password is None:
			password = self.password  
		return bass_call(pybassenc.BASS_Encode_CastGetStats, self.handle, type, password)
