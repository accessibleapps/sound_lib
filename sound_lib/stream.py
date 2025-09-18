from __future__ import absolute_import

import ctypes
import os
import platform
import sys

from .channel import Channel
from .external.pybass import (
    BASS_FILEDATA_END,
    BASS_FILEPROCS,
    BASS_STREAMPROC_END,
    BASS_StreamCreate,
    BASS_StreamCreateFile,
    BASS_StreamCreateFileUser,
    BASS_StreamCreateURL,
    BASS_StreamFree,
    BASS_StreamGetFilePosition,
    BASS_StreamPutData,
    BASS_UNICODE,
    DOWNLOADPROC,
    FILECLOSEPROC,
    FILELENPROC,
    FILEREADPROC,
    FILESEEKPROC,
    STREAMFILE_BUFFER,
    STREAMFILE_BUFFERPUSH,
    STREAMFILE_NOBUFFER,
    STREAMPROC,
    STREAMPROC_PUSH,
    BASS_StreamPutFileData,
)
from .main import bass_call, bass_call_0

try:
    convert_to_unicode = unicode
except NameError:
    convert_to_unicode = str


class BaseStream(Channel):
    """ """

    def _callback(*args):
        """

        Args:
          *args:

        Returns:

        """
        # Stub it out as otherwise it'll crash, hard.  Used for stubbing download procs
        return 0

    def free(self):
        """Frees a sample stream's resources, including any sync/DSP/FX it has."""
        return bass_call(BASS_StreamFree, self.handle)

    def get_file_position(self, mode):
        """
        Retrieves the file position/status of a stream.

        Args:
          mode:

        Returns:
            int: The requested file position on success, -1 otherwise.

        raises:
            sound_lib.main.BassError: If the handle is invalid, the stream is not a FileStream, or the requested position is not available.
        """
        return bass_call_0(BASS_StreamGetFilePosition, self.handle, mode)

    def put_file_data(self, data):
        """
        Adds data to a push buffered user file stream's buffer.

        Args:
            data (bytes): File data to add, or None to end the file

        Returns:
            int: Number of bytes read from data on success, -1 otherwise

        raises:
            sound_lib.main.BassError: If the handle is invalid, stream is not using STREAMFILE_BUFFERPUSH, or the file has ended.
        """
        if data is None:
            return bass_call_0(
                BASS_StreamPutFileData, self.handle, None, BASS_FILEDATA_END
            )
        return bass_call_0(BASS_StreamPutFileData, self.handle, data, len(data))

    def setup_flag_mapping(self):
        """ """
        super(BaseStream, self).setup_flag_mapping()
        self.flag_mapping.update({"unicode": BASS_UNICODE})


class Stream(BaseStream):
    """A sample stream.
    Higher-level streams are used in 90% of cases."""

    def __init__(
        self,
        freq=44100,
        chans=2,
        flags=0,
        proc=None,
        user=None,
        three_d=False,
        autofree=False,
        decode=False,
    ):
        self.proc = STREAMPROC(proc)
        self.setup_flag_mapping()
        flags = flags | self.flags_for(
            three_d=three_d, autofree=autofree, decode=decode
        )
        handle = bass_call(BASS_StreamCreate, freq, chans, flags, self.proc, user)
        super(Stream, self).__init__(handle)


class FileStream(BaseStream):
    """A sample stream that loads from a supported audio file format.

    This class can load audio from both disk files and memory.

    Args:
        mem (bool): If True, load from memory. If False, load from file.
        file (str): Path to the audio file or memory address.
        offset (int): Offset in bytes when reading from memory.
        length (int): Data length in bytes when reading from memory.
        flags (int): BASS_STREAM_xxx flags.
        three_d (bool): Enable 3D functionality.
        mono (bool): Force mono audio.
        autofree (bool): Automatically free the stream when playback ends.
        decode (bool): Create a decoding channel.
        unicode (bool): Filename is in Unicode format.
    """

    def __init__(
        self,
        mem=False,
        file=None,
        offset=0,
        length=0,
        flags=0,
        three_d=False,
        mono=False,
        autofree=False,
        decode=False,
        unicode=True,
    ):
        if platform.system() == "Darwin" and file and not mem:
            unicode = False
            file = file.encode(sys.getfilesystemencoding())
        self.setup_flag_mapping()
        flags = flags | self.flags_for(
            three_d=three_d,
            autofree=autofree,
            mono=mono,
            decode=decode,
            unicode=unicode,
        )
        if unicode and isinstance(file, str):
            file = convert_to_unicode(file)
        self.file = file

        handle = bass_call(BASS_StreamCreateFile, mem, file, offset, length, flags)
        super(FileStream, self).__init__(handle)


class URLStream(BaseStream):
    """Creates a sample stream from a file found on the internet.
    Downloaded data can optionally be received through a callback function for further manipulation."""

    def __init__(
        self,
        url="",
        offset=0,
        flags=0,
        downloadproc=None,
        user=None,
        three_d=False,
        autofree=False,
        decode=False,
        unicode=True,
    ):
        if platform.system() in ("Darwin", "Linux"):
            unicode = False
            url = url.encode(sys.getfilesystemencoding())
        self._downloadproc = downloadproc or self._callback  # we *must hold on to this
        self.downloadproc = DOWNLOADPROC(self._downloadproc)
        self.url = url
        self.setup_flag_mapping()
        flags = flags | self.flags_for(
            three_d=three_d, autofree=autofree, decode=decode, unicode=unicode
        )
        offset = int(offset)
        handle = bass_call(
            BASS_StreamCreateURL, url, offset, flags, self.downloadproc, user
        )
        super(URLStream, self).__init__(handle)


class PushStream(BaseStream):
    """A stream that receives and plays raw audio data in realtime."""

    def __init__(
        self,
        freq=44100,
        chans=2,
        flags=0,
        user=None,
        three_d=False,
        autofree=False,
        decode=False,
    ):
        self.proc = STREAMPROC_PUSH
        self.setup_flag_mapping()
        flags = flags | self.flags_for(
            three_d=three_d, autofree=autofree, decode=decode
        )
        handle = bass_call(BASS_StreamCreate, freq, chans, flags, self.proc, user)
        super(PushStream, self).__init__(handle)

    def push(self, data):
        """
        Adds sample data to the stream.

        Args:
          data (bytes): Data to be sent.

        Returns:
            int: The amount of queued data on success, -1 otherwise.

        raises:
            sound_lib.main.BassError: If the stream has ended or there is insufficient memory.
        """
        return bass_call_0(BASS_StreamPutData, self.handle, data, len(data))

    def push_end(self):
        """
        Signal end of stream data.

        Returns:
            int: The amount of queued data on success, -1 otherwise

        raises:
            sound_lib.main.BassError: If the handle is invalid or stream is not using push system.
        """
        return bass_call_0(BASS_StreamPutData, self.handle, None, BASS_STREAMPROC_END)

    def get_queue_level(self):
        """
        Get amount of data currently queued for playback.

        Returns:
            int: Amount of data in bytes currently queued, -1 on error

        raises:
            sound_lib.main.BassError: If the handle is invalid or stream is not using push system.
        """
        return bass_call_0(BASS_StreamPutData, self.handle, None, 0)

    def allocate_queue_space(self, length):
        """
        Allocate space in the queue buffer to ensure at least 'length' bytes are available.

        Args:
            length (int): Minimum number of bytes of free space to ensure

        Returns:
            int: The amount of queued data on success, -1 otherwise

        raises:
            sound_lib.main.BassError: If there is insufficient memory or the push limit is exceeded.
        """
        return bass_call_0(BASS_StreamPutData, self.handle, None, length)


class FileUserStream(BaseStream):
    """A sample stream created from a file-like object using custom file operations.

    This class allows streaming from any file-like object (file handles, BytesIO,
    custom objects) by implementing the necessary callback functions internally.

    Args:
        file_obj: File-like object with read(), seek(), close() methods
        system (int): File system type (STREAMFILE_NOBUFFER, STREAMFILE_BUFFER, STREAMFILE_BUFFERPUSH)
        flags (int): BASS_STREAM_xxx flags
        three_d (bool): Enable 3D functionality
        mono (bool): Force mono audio
        autofree (bool): Automatically free the stream when playback ends
        decode (bool): Create a decoding channel
    """

    def __init__(
        self,
        file_obj,
        system=STREAMFILE_NOBUFFER,
        flags=0,
        three_d=False,
        mono=False,
        autofree=False,
        decode=False,
    ):
        self.file_obj = file_obj
        self.setup_flag_mapping()
        flags = flags | self.flags_for(
            three_d=three_d,
            autofree=autofree,
            mono=mono,
            decode=decode,
        )

        # Store original position for length calculation
        self._original_position = None
        if hasattr(file_obj, "tell"):
            try:
                self._original_position = file_obj.tell()
            except (OSError, IOError):
                pass  # Some file objects don't support tell()

        # Create callback functions that operate on our file object
        def close_callback(user):
            """Callback for closing the file"""
            if hasattr(self.file_obj, "close"):
                try:
                    self.file_obj.close()
                except (OSError, IOError):
                    pass

        def length_callback(user):
            """Callback for getting file length"""
            try:
                # Try various approaches to get file length
                if hasattr(self.file_obj, "size"):
                    return self.file_obj.size

                if hasattr(self.file_obj, "getvalue"):
                    # BytesIO and similar objects
                    return len(self.file_obj.getvalue())

                if hasattr(self.file_obj, "seek") and hasattr(self.file_obj, "tell"):
                    # Seekable file-like objects
                    current = self.file_obj.tell()
                    self.file_obj.seek(0, 2)  # Seek to end
                    size = self.file_obj.tell()
                    self.file_obj.seek(current)  # Restore position
                    return size

                if hasattr(self.file_obj, "name") and os.path.exists(
                    self.file_obj.name
                ):
                    # Regular file objects
                    return os.path.getsize(self.file_obj.name)

            except (OSError, IOError, AttributeError):
                pass
            return 0  # Unknown size

        def read_callback(buffer, length, user):
            """Callback for reading data from file"""
            try:
                data = self.file_obj.read(length)
                if data:
                    # Copy data to BASS buffer
                    data_bytes = data if isinstance(data, bytes) else data.encode()
                    bytes_to_copy = min(len(data_bytes), length)
                    ctypes.memmove(buffer, data_bytes, bytes_to_copy)
                    return bytes_to_copy
                return 0
            except (OSError, IOError, AttributeError):
                return 0

        def seek_callback(offset, user):
            """Callback for seeking in file"""
            try:
                if hasattr(self.file_obj, "seek"):
                    self.file_obj.seek(offset)
                    return True
            except (OSError, IOError, AttributeError):
                pass
            return False

        # Create the callback structure
        # Store callbacks to prevent garbage collection
        self._close_func = FILECLOSEPROC(close_callback)
        self._length_func = FILELENPROC(length_callback)
        self._read_func = FILEREADPROC(read_callback)
        self._seek_func = FILESEEKPROC(seek_callback)

        self.file_procs = BASS_FILEPROCS(
            close=self._close_func,
            length=self._length_func,
            read=self._read_func,
            seek=self._seek_func,
        )

        handle = bass_call(
            BASS_StreamCreateFileUser,
            system,
            flags,
            ctypes.byref(self.file_procs),
            None,
        )
        super(FileUserStream, self).__init__(handle)
