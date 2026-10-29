from __future__ import annotations

import wave
from ctypes import string_at
from enum import Enum, IntFlag
from logging import getLogger

from .channel import Channel
from .external.pybass import RECORDPROC, BASS_RecordStart
from .main import bass_call


class RecordingFlags(IntFlag):
    """Flags for recording start options."""

    PAUSE = 0x8000  # Start recording paused


class InputFlags(IntFlag):
    """Flags for recording input state."""

    OFF = 0x10000
    ON = 0x20000


class InputType(Enum):
    """Recording input source types (mutually exclusive).

    Use INPUT_TYPE_MASK (0xFF000000) to extract type from a combined flags value.
    """

    UNDEF = 0x00000000
    DIGITAL = 0x01000000
    LINE = 0x02000000
    MIC = 0x03000000
    SYNTH = 0x04000000
    CD = 0x05000000
    PHONE = 0x06000000
    SPEAKER = 0x07000000
    WAVE = 0x08000000
    AUX = 0x09000000
    ANALOG = 0x0A000000


# Mask for extracting InputType from a combined flags value
INPUT_TYPE_MASK = 0xFF000000

logger = getLogger("sound_lib.recording")


class Recording(Channel):
    """Base class for implementing audio recording functionality.
    Inherits from :class:`sound_lib.channel.Channel`. Everything works based on those functions.
    For example, calling play starts, stop stops, etc etc.
    """

    def __init__(
        self,
        frequency: int = 44100,
        channels: int = 2,
        flags: RecordingFlags | int = RecordingFlags.PAUSE,
        proc=None,
        user=None,
    ):
        if not proc:
            proc = lambda: True
        self.callback = RECORDPROC(proc)
        self._frequency = frequency
        self._channels = channels
        self._flags = flags
        handle = bass_call(
            BASS_RecordStart, frequency, channels, flags, self.callback, user
        )
        super(Recording, self).__init__(handle)
        logger.info("Recording started: freq=%d, channels=%d, handle=%d", frequency, channels, handle)

    def free(self):
        """
        Frees all resources associated with the recording. Automatically called when a channel is destroyed.
        Define this in your subclass, as by default it does nothing.
        """
        pass


class WaveRecording(Recording):
    """Allows for making wave audio recordings to the filesystem."""

    def __init__(self, filename: str = "", proc=None, *args, **kwargs):
        callback = proc or self._recording_callback
        super().__init__(proc=callback, *args, **kwargs)
        self.filename = filename

    def _recording_callback(self, handle, buffer, length, user):
        buf = string_at(buffer, length)
        self.file.writeframes(buf)
        return True

    def _setup_file(self):
        if not self.filename:
            raise ValueError("filename cannot be blank")
        logger.debug("Setting up wave file: %s", self.filename)
        self.file = wave.open(self.filename, "w")
        self.file.setnchannels(self._channels)
        self.file.setsampwidth(2)
        self.file.setframerate(self._frequency)

    def play(self, *args, **kwargs):
        if not self.is_playing:
            self._setup_file()
        super().play(*args, **kwargs)

    def stop(self, *args, **kwargs):
        super().stop(*args, **kwargs)
        self.file.close()
        logger.info("Wave recording stopped: %s", self.filename)
