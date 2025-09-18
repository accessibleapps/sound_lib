"""Test cases for new BASS_STREAM functions added to sound_lib."""

import io
import pytest
from unittest.mock import Mock

from sound_lib.stream import FileUserStream, PushStream, BaseStream
from sound_lib.main import bass_call
from sound_lib.external.pybass import BASS_Init, STREAMFILE_NOBUFFER


class TestBaseStream:
    """Test BaseStream put_file_data method."""

    def test_put_file_data_with_data(self):
        """Test put_file_data with actual data."""
        # Create a mock stream
        stream = BaseStream(handle=1)  # Mock handle

        # Mock the bass_call_0 function to avoid actual BASS calls
        import sound_lib.stream
        original_bass_call_0 = sound_lib.stream.bass_call_0

        def mock_bass_call_0(func, handle, data, length):
            # Simulate successful put_file_data call
            return length if data else 0

        sound_lib.stream.bass_call_0 = mock_bass_call_0

        try:
            # Test with data
            test_data = b"test data"
            result = stream.put_file_data(test_data)
            assert result == len(test_data)

            # Test with None (end of file)
            result = stream.put_file_data(None)
            assert result == 0
        finally:
            # Restore original function
            sound_lib.stream.bass_call_0 = original_bass_call_0


class TestFileUserStream:
    """Test FileUserStream class with file-like objects."""

    def test_bytesio_integration(self):
        """Test FileUserStream with BytesIO object."""
        # Create sample data
        sample_data = b'\x00' * 1024  # 1KB of silence
        file_obj = io.BytesIO(sample_data)

        # Mock BASS initialization and stream creation
        import sound_lib.stream
        original_bass_call = sound_lib.stream.bass_call

        def mock_bass_call(func, *args):
            # Return a mock handle for stream creation
            return 12345

        sound_lib.stream.bass_call = mock_bass_call

        try:
            # Test stream creation
            stream = FileUserStream(file_obj, system=STREAMFILE_NOBUFFER, decode=True)
            assert stream.handle == 12345
            assert stream.file_obj is file_obj

            # Test that callbacks are properly created
            assert hasattr(stream, '_close_func')
            assert hasattr(stream, '_length_func')
            assert hasattr(stream, '_read_func')
            assert hasattr(stream, '_seek_func')
            assert hasattr(stream, 'file_procs')

        finally:
            sound_lib.stream.bass_call = original_bass_call

    def test_custom_file_like_object(self):
        """Test FileUserStream with custom file-like object."""

        class MockFile:
            def __init__(self, data):
                self.data = data
                self.position = 0
                self.closed = False

            def read(self, size):
                start = self.position
                end = min(start + size, len(self.data))
                result = self.data[start:end]
                self.position = end
                return result

            def seek(self, offset, whence=0):
                if whence == 0:  # SEEK_SET
                    self.position = offset
                elif whence == 2:  # SEEK_END
                    self.position = len(self.data) + offset
                else:  # SEEK_CUR
                    self.position += offset

            def tell(self):
                return self.position

            def close(self):
                self.closed = True

            def getvalue(self):
                return self.data

        # Mock BASS functions
        import sound_lib.stream
        original_bass_call = sound_lib.stream.bass_call
        sound_lib.stream.bass_call = lambda func, *args: 54321

        try:
            mock_data = b'\x00' * 2048
            mock_file = MockFile(mock_data)

            stream = FileUserStream(mock_file, decode=True)
            assert stream.handle == 54321
            assert stream.file_obj is mock_file

        finally:
            sound_lib.stream.bass_call = original_bass_call


class TestPushStream:
    """Test PushStream convenience methods."""

    def test_push_stream_methods(self):
        """Test new PushStream convenience methods."""
        # Mock BASS functions to avoid actual initialization
        import sound_lib.stream
        original_bass_call = sound_lib.stream.bass_call
        original_bass_call_0 = sound_lib.stream.bass_call_0

        def mock_bass_call(func, *args):
            return 67890  # Mock handle

        def mock_bass_call_0(func, handle, data, length):
            # Simulate different behaviors based on parameters
            if data is None:
                if length == 0:
                    return 1024  # Queue level
                elif length == -2147483648:  # BASS_STREAMPROC_END
                    return 512   # Final queue level
                else:
                    return length  # Allocated space
            else:
                return 2048  # Queued data after push

        sound_lib.stream.bass_call = mock_bass_call
        sound_lib.stream.bass_call_0 = mock_bass_call_0

        try:
            # Create push stream
            stream = PushStream(freq=44100, chans=2, decode=True)
            assert stream.handle == 67890

            # Test queue level
            level = stream.get_queue_level()
            assert level == 1024

            # Test allocate queue space
            allocated = stream.allocate_queue_space(2048)
            assert allocated == 2048

            # Test push end
            final_level = stream.push_end()
            assert final_level == 512

        finally:
            sound_lib.stream.bass_call = original_bass_call
            sound_lib.stream.bass_call_0 = original_bass_call_0


class TestCallbackSafety:
    """Test callback garbage collection safety."""

    def test_callback_references_preserved(self):
        """Test that callback functions are properly preserved."""
        import sound_lib.stream
        original_bass_call = sound_lib.stream.bass_call
        sound_lib.stream.bass_call = lambda func, *args: 11111

        try:
            file_obj = io.BytesIO(b'test data')
            stream = FileUserStream(file_obj)

            # Check that callback references are stored
            assert hasattr(stream, '_close_func')
            assert hasattr(stream, '_length_func')
            assert hasattr(stream, '_read_func')
            assert hasattr(stream, '_seek_func')

            # Check that these are the actual ctypes function objects
            from sound_lib.external.pybass import (FILECLOSEPROC, FILELENPROC,
                                                   FILEREADPROC, FILESEEKPROC)
            assert isinstance(stream._close_func, type(FILECLOSEPROC()))
            assert isinstance(stream._length_func, type(FILELENPROC()))
            assert isinstance(stream._read_func, type(FILEREADPROC()))
            assert isinstance(stream._seek_func, type(FILESEEKPROC()))

        finally:
            sound_lib.stream.bass_call = original_bass_call