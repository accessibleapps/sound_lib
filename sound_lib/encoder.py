from enum import IntFlag
from logging import getLogger
from typing import Any, Optional

from .channel import ActiveState
from .external import pybass, pybassenc
from .main import FlagObject, bass_call, bass_call_0


class EncodeFlags(IntFlag):
    """Flags for encoder creation."""

    NOHEAD = 1  # Don't send a WAV header to the encoder
    FP_8BIT = 2  # Convert floating-point sample data to 8-bit integer
    FP_16BIT = 4  # Convert floating-point sample data to 16-bit integer
    FP_24BIT = 6  # Convert floating-point sample data to 24-bit integer
    FP_32BIT = 8  # Convert floating-point sample data to 32-bit integer
    BIGEND = 16  # Big-endian sample data
    PAUSE = 32  # Start encoding paused
    PCM = 64  # Write PCM sample data (no encoder)
    RF64 = 128  # Send an RF64 header
    MONO = 256  # Convert to mono (if not already)
    QUEUE = 512  # Queue data to feed encoder asynchronously
    CAST_NOLIMIT = 0x1000  # Don't limit casting data rate
    LIMIT = 0x2000  # Limit data rate to real-time
    AUTOFREE = 0x40000  # Free the encoder when the channel is freed


class EncodeNotify(IntFlag):
    """Encoder notification status codes."""

    ENCODER = 1  # Encoder died
    CAST = 2  # Cast server connection died
    CAST_TIMEOUT = 0x10000  # Cast timeout
    QUEUE_FULL = 0x10001  # Queue is out of space

logger = getLogger("sound_lib.encoder")


class Encoder(FlagObject):
    """ """

    def setup_flag_mapping(self):
        """ """
        # super(Encoder, self).setup_flag_mapping()
        self.flag_mapping = {
            "pcm": EncodeFlags.PCM,
            "no_header": EncodeFlags.NOHEAD,
            "rf64": EncodeFlags.RF64,
            "big_endian": EncodeFlags.BIGEND,
            "fp_8bit": EncodeFlags.FP_8BIT,
            "fp_16bit": EncodeFlags.FP_16BIT,
            "fp_24bit": EncodeFlags.FP_24BIT,
            "fp_32bit": EncodeFlags.FP_32BIT,
            "queue": EncodeFlags.QUEUE,
            "limit": EncodeFlags.LIMIT,
            "no_limit": EncodeFlags.CAST_NOLIMIT,
            "pause": EncodeFlags.PAUSE,
            "autofree": EncodeFlags.AUTOFREE,
            "unicode": pybass.BASS_UNICODE,
        }

    def __init__(
        self,
        source,
        command_line: str,
        pcm: bool = False,
        no_header: bool = False,
        rf64=False,
        big_endian=False,
        fp_8bit=False,
        fp_16bit=False,
        fp_24bit=False,
        fp_32bit=False,
        queue=False,
        limit=False,
        no_limit=False,
        pause=True,
        autofree=False,
        callback=None,
        user=None,
    ):
        self.setup_flag_mapping()
        flags = self.flags_for(
            pcm=pcm,
            no_header=no_header,
            rf64=rf64,
            big_endian=big_endian,
            fp_8bit=fp_8bit,
            fp_16bit=fp_16bit,
            fp_24bit=fp_24bit,
            fp_32bit=fp_32bit,
            queue=queue,
            limit=limit,
            no_limit=no_limit,
            pause=pause,
            autofree=autofree,
        )  # fwiw!
        self.source = source
        source_handle = source.handle
        if callback is not None:
            callback = pybassenc.ENCODEPROC(callback)
        self.callback = callback
        self.handle = bass_call(
            pybassenc.BASS_Encode_Start,
            source_handle,
            command_line,
            flags,
            callback,
            user,
        )
        logger.info("Encoder started: handle=%d", self.handle)

    def set_title(self, title=None, url=None):
        """

        Args:
          title:  (Default value = None)
          url:  (Default value = None)

        Returns:

        """
        return bass_call(pybassenc.BASS_Encode_CastSetTitle, self.handle, title, url)

    @property
    def paused(self):
        """ """
        return (
            bass_call_0(pybassenc.BASS_Encode_IsActive, self.handle)
            == ActiveState.PAUSED
        )

    @paused.setter
    def paused(self, paused: bool):
        """

        Args:
          paused:

        Returns:

        """
        return bass_call(pybassenc.BASS_Encode_SetPaused, self.handle, paused)

    def is_stopped(self) -> bool:
        """ """
        return (
            bass_call_0(pybassenc.BASS_Encode_IsActive, self.handle)
            == ActiveState.STOPPED
        )

    def stop(self):
        """ """
        return bass_call(pybassenc.BASS_Encode_Stop, self.handle)


class BroadcastEncoder(Encoder):
    """ """

    def __init__(
        self,
        source_encoder,
        server,
        password: str,
        content,
        name: Optional[str] = None,
        url: Optional[str] = None,
        genre: Optional[str] = None,
        description: Optional[str] = None,
        headers: Optional[str] = None,
        bitrate: int = 0,
        public: bool = False,
    ):
        contents = {
            "mp3": pybassenc.BASS_ENCODE_TYPE_MP3,
            "ogg": pybassenc.BASS_ENCODE_TYPE_OGG,
            "aac": pybassenc.BASS_ENCODE_TYPE_AAC,
        }
        if content in contents:
            content = contents[content]
        self.source_encoder = source_encoder
        handle = source_encoder.handle
        self.server = server
        self.password = password
        self.status = bass_call(
            pybassenc.BASS_Encode_CastInit,
            handle,
            server,
            password,
            content,
            name,
            url,
            genre,
            description,
            headers,
            bitrate,
            public,
        )

    def get_stats(self, type, password: Optional[str] = None):
        """

        Args:
          type:
          password:  (Default value = None)

        Returns:

        """
        types = {
            "shoutcast": pybassenc.BASS_ENCODE_STATS_SHOUT,
            "icecast": pybassenc.BASS_ENCODE_STATS_ICE,
            "icecast_server": pybassenc.BASS_ENCODE_STATS_ICESERV,
        }
        if type in types:
            type = types[type]
        if password is None:
            password = self.password
        return bass_call(
            pybassenc.BASS_Encode_CastGetStats, self.handle, type, password
        )


class Server:
    """Local Audio Server"""

    # DWORD BASSENCDEF(BASS_Encode_ServerInit)(HENCODE handle, const char *port, DWORD buffer, DWORD burst, DWORD flags, ENCODECLIENTPROC *proc, void *user);
    def __init__(
        self,
        encoder,
        port,
        buffer: int = 64000,
        burst: int = 64000,
        user: Optional[Any] = None,
    ):
        self.encoder = encoder
        self.port = port
        self.buffer = buffer
        self.burst = burst
        self.user = user
        self._callback = pybassenc.ENCODECLIENTPROC(self.client_callback)
        self.handle = bass_call(
            pybassenc.BASS_Encode_ServerInit,
            encoder.handle,
            str(port).encode("ascii"),
            buffer,
            burst,
            0,  # flags
            self._callback,
            user,
        )
        logger.info("Encoder server started on port %s", port)

    def client_callback(self, handle, connect, client, headers, user):
        """

        Args:
            handle:
            client:
            connect:
            user:

        Returns:
            An integer 0 or 1 if the connection should be accepted
        """
        logger.debug("Client %s", "connected" if connect else "disconnected")
        logger.debug("Headers: %s", headers)
        return True
