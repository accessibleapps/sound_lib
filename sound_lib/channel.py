from __future__ import absolute_import
from typing import Any, Dict, List, Optional, Union
from .external.pybass import (
    BASS_ACTIVE_PAUSED,
    BASS_ACTIVE_PAUSED_DEVICE,
    BASS_ACTIVE_PLAYING,
    BASS_ACTIVE_STALLED,
    BASS_ACTIVE_STOPPED,
    BASS_ATTRIB_EAXMIX,
    BASS_ATTRIB_FREQ,
    BASS_ATTRIB_PAN,
    BASS_ATTRIB_VOL,
    BASS_ChannelBytes2Seconds,
    BASS_ChannelFlags,
    BASS_ChannelFree,
    BASS_ChannelGet3DAttributes,
    BASS_ChannelGet3DPosition,
    BASS_ChannelGetAttribute,
    BASS_ChannelGetAttributeEx,
    BASS_ChannelGetData,
    BASS_ChannelGetDevice,
    BASS_ChannelGetInfo,
    BASS_ChannelGetLength,
    BASS_ChannelGetLevel,
    BASS_ChannelGetLevelEx,
    BASS_ChannelGetPosition,
    BASS_ChannelIsActive,
    BASS_ChannelIsSliding,
    BASS_ChannelLock,
    BASS_ChannelPause,
    BASS_ChannelPlay,
    BASS_ChannelRemoveLink,
    BASS_ChannelSeconds2Bytes,
    BASS_ChannelSet3DAttributes,
    BASS_ChannelSet3DPosition,
    BASS_ChannelSetAttribute,
    BASS_ChannelSetAttributeEx,
    BASS_ChannelSetDevice,
    BASS_ChannelSetFX,
    BASS_ChannelSetLink,
    BASS_ChannelSetPosition,
    BASS_ChannelSlideAttribute,
    BASS_ChannelStop,
    BASS_ChannelUpdate,
    BASS_CHANNELINFO,
    BASS_LEVEL_MONO,
    BASS_LEVEL_NOREMOVE,
    BASS_LEVEL_RMS,
    BASS_LEVEL_STEREO,
    BASS_LEVEL_VOLPAN,
    BASS_POS_BYTE,
    BASS_POS_DECODE,
    BASS_SAMPLE_LOOP,
    BASS_3DVECTOR,
)
from .main import BassError, FlagObject, bass_call, bass_call_0, update_3d_system
from ctypes import c_buffer, c_float, c_long, c_ulong, pointer, sizeof


class Channel(FlagObject):
    """A "channel" represents an audio stream that can be manipulated.

    It can be one of the following:
    - A sample playback channel (HCHANNEL)
    - A sample stream (HSTREAM)
    - A MOD music (HMUSIC)
    - A recording (HRECORD)

    Most audio playback and manipulation in sound_lib is done through Channel objects.
    """

    attribute_mapping: Dict[str, int] = {}

    def __init__(self, handle: int) -> None:
        self.handle = handle
        self.attribute_mapping = {
            "eaxmix": BASS_ATTRIB_EAXMIX,
            "frequency": BASS_ATTRIB_FREQ,
            "pan": BASS_ATTRIB_PAN,
            "volume": BASS_ATTRIB_VOL,
            "byte": BASS_POS_BYTE,
            "decode": BASS_POS_DECODE,
        }

    def add_attributes_to_mapping(self, **attrs: int) -> None:
        self.attribute_mapping.update(**attrs)

    def play(self, restart: bool = False) -> Any:
        """Starts (or resumes) playback of a sample, stream, MOD music, or recording.

        Args:
          restart (bool):  Specifies whether playback position should be thrown to the beginning of the stream. Defaults to False

        Returns:
            bool: True on success, False otherwise.
        """
        return bass_call(BASS_ChannelPlay, self.handle, restart)

    def play_blocking(self, restart: bool = False) -> None:
        """Starts (or resumes) playback, waiting to return until reaching the end of the stream

        Args:
          restart (bool):  Specifies whether playback position should be thrown to the beginning of the stream. Defaults to False.
        """
        self.play(restart=restart)
        while self.is_playing:
            pass

    def pause(self) -> Any:
        """Pauses a sample, stream, MOD music, or recording.

        Returns:
            bool: True on success, False otherwise.

        raises:
            sound_lib.main.BassError: If this channel isn't currently playing, already paused, or is a decoding channel and thus not playable.
        """
        return bass_call(BASS_ChannelPause, self.handle)

    def is_active(self) -> int:
        """Checks if a sample, stream, or MOD music is active (playing) or stalled. Can also check if a recording is in progress."""
        return bass_call_0(BASS_ChannelIsActive, self.handle)

    @property
    def is_playing(self):
        """Checks whether the stream is currently playing or recording.

        Returns:
            bool: True if playing, False otherwise.
        """
        return self.is_active() == BASS_ACTIVE_PLAYING

    @property
    def is_paused(self):
        """
        Checks whether the stream is currently paused.

        Returns:
            bool: True if paused, False otherwise.
        """
        return self.is_active() == BASS_ACTIVE_PAUSED

    @property
    def is_stopped(self):
        """
        Checks whether the stream is currently stopped.

        Returns:
            bool: True if stopped, False otherwise.
        """
        return self.is_active() == BASS_ACTIVE_STOPPED

    @property
    def is_device_paused(self):
        """
        Checks whether the output device is currently paused.

        Returns:
            bool: True if device is paused, False otherwise.
        """
        return self.is_active() == BASS_ACTIVE_PAUSED_DEVICE

    @property
    def is_stalled(self):
        """
        Checks whether playback of a stream has been stalled.
        This is due to a lack of sample data. Playback will automatically resume once there is sufficient data to do so.

        Returns:
            bool: True if stalled, False otherwise.
        """
        return self.is_active() == BASS_ACTIVE_STALLED

    def get_position(self, mode: int = BASS_POS_BYTE) -> int:
        """Retrieves the playback position of a sample, stream, or MOD music. Can also be used with a recording channel.

        Args:
          mode (str):  How to retrieve the position. Defaults to "byte".

        Returns:
            int: The current position.

        raises:
            sound_lib.main.BassError: If the requested position is not available.
        """
        return bass_call_0(BASS_ChannelGetPosition, self.handle, mode)

    def set_position(self, pos: int, mode: int = BASS_POS_BYTE) -> Any:
        """Sets the playback position of a sample, MOD music, or stream.

        Args:
          pos (int): The position, in units determined by the mode.
          mode:  (str): How to set the position. Defaults to "byte".

        Returns:
            bool: True if the position was set, False otherwise.

        raises:
            sound_lib.main.BassError: If the stream is not a sound_lib.stream.FileStream or the requested position/mode is not available.
        """
        return bass_call(BASS_ChannelSetPosition, self.handle, pos, mode)

    position = property(get_position, set_position)

    def stop(self) -> Any:
        """Stops a sample, stream, MOD music, or recording."""
        return bass_call(BASS_ChannelStop, self.handle)

    def update(self, length: int = 0) -> Any:
        """Updates the playback buffer of a stream or MOD music.

        Args:
          length (int): The amount of data to render, in milliseconds...
              0 = default (2 x update period). This is capped at the space available in the buffer.

        Returns:
            bool: True on success, False otherwise.

        raises:
            sound_lib.main.BassError: If this channel has ended or doesn't have an output -buffer.
        """
        return bass_call(BASS_ChannelUpdate, self.handle, length)

    def get_length(self, mode: int = BASS_POS_BYTE) -> int:
        """Retrieves the playback length of this channel.

        Args:
          mode:  How to retrieve the length. Can take either a flag attribute (string) or bass constent (int). Defaults to "byte".

        Returns:
            int: The channel length on success, -1 on failure.

        raises:
            sound_lib.main.BassError: If the requested mode is not available.
        """
        return bass_call_0(BASS_ChannelGetLength, self.handle, mode)

    __len__ = get_length

    def __nonzero__(self) -> bool:
        return True

    def get_device(self) -> int:
        """Retrieves the device in use by this channel.

        returns:
            int: The device number, -1 on failure.
        """
        return bass_call_0(BASS_ChannelGetDevice, self.handle)

    def set_device(self, device: int) -> None:
        """Changes the device in use by this channel. Must be a stream, MOD music or sample.

        Args:
          device: The device to use... 0 = no sound, 1 = first real output device, BASS_NODEVICE = no device.

        Returns:
            bool: True on success, False otherwise.

        raises:
            sound_lib.main.BassError: If device is invalid, device hasn't been initialized, this channel is already using the requested device, the sample format is not supported by the device/drivers or there is insufficient memory.
        """
        bass_call(BASS_ChannelSetDevice, self.handle, device)

    device = property(get_device, set_device)

    def set_fx(self, type: int, priority: int = 0) -> Any:
        """Sets an effect on a stream, MOD music, or recording channel.

        Args:
          type: The type of effect
          priority: The priority of the new FX, which determines its position in the DSP chain. DSP/FX with higher priority are applied before those with lower. This parameter has no effect with DX8 effects when the "with FX flag" DX8 effect implementation is used. Defaults to 0.

        Returns:
            A handle to the new effect on success, False otherwise.

        raises:
            sound_lib.main.BassError: If type is invalid, the specified DX8 effect is unavailable or this channel's format is not supported by the effect.
        """
        from .effects.bass_fx import SoundEffect

        return SoundEffect(bass_call(BASS_ChannelSetFX, type, priority))

    def bytes_to_seconds(self, position: Optional[int] = None) -> float:
        """Translates a byte position into time (seconds), based on the format in use by this channel.

        Args:
          position:  The position to translate. Defaults to None

        Returns:
            int: The translated length on success, a negative bass error code on failure.
        """
        position = position or self.position
        return bass_call_0(BASS_ChannelBytes2Seconds, self.handle, position)

    def length_in_seconds(self) -> float:
        """Retrieves the length of the stream, in seconds, regardless of position.

        returns:
            int: The length on success, a negative bass error code on failure.
        """
        return self.bytes_to_seconds(self.get_length())

    def seconds_to_bytes(self, position: float) -> int:
        """Translates a time (seconds) position into bytes, based on the format in use by this channel.

        Args:
          position:  The position to translate.

        Returns:
            int: The translated length on success, a negative bass error code on failure.
        """
        return bass_call_0(BASS_ChannelSeconds2Bytes, self.handle, position)

    def get_attribute(self, attribute: Union[str, int]) -> float:
        """Retrieves the value of this channel's attribute.

        Args:
          attribute: The attribute to get the value of. Can either be an of type str or int.

        Returns:
            The value on success, None on failure.

        raises:
            sound_lib.main.BassError: If the attribute is either unavailable or invalid.
                Some attributes have additional possible instances where an exception might be raised.
        """
        value = pointer(c_float())
        if isinstance(attribute, str) and attribute in self.attribute_mapping:
            attribute = self.attribute_mapping[attribute]
        bass_call(BASS_ChannelGetAttribute, self.handle, attribute, value)
        return value.contents.value

    def set_attribute(self, attribute: Union[str, int], value: float) -> Any:
        """Sets the value of an attribute on this channel.

        Args:
          attribute: The attribute to set the value of. Can either be of type str or int.
          value:

        Returns:
            bool: True on success, False on failure.

        raises:
            sound_lib.main.BassError: If either attribute or value is invalid.
        """
        if isinstance(attribute, str) and attribute in self.attribute_mapping:
            attribute = self.attribute_mapping[attribute]
        return bass_call(BASS_ChannelSetAttribute, self.handle, attribute, value)

    def get_attribute_ex(self, attribute: Union[str, int], size: Optional[int] = None) -> Optional[bytes]:
        """Get extended attribute data of variable size.

        Args:
            attribute: Attribute constant (BASS_ATTRIB_SCANINFO, BASS_ATTRIB_USER, etc.)
            size (int, optional): Buffer size in bytes. If None, queries size first.

        Returns:
            bytes: Raw attribute data, or None if not available

        raises:
            sound_lib.main.BassError: If attribute is invalid or not available
        """
        if isinstance(attribute, str) and attribute in self.attribute_mapping:
            attribute = self.attribute_mapping[attribute]

        # If size not provided, query it first
        if size is None:
            size = bass_call_0(
                BASS_ChannelGetAttributeEx, self.handle, attribute, None, 0
            )
            if size == 0:
                return None

        # Allocate buffer and get the data
        buffer = c_buffer(size)
        actual_size = bass_call_0(
            BASS_ChannelGetAttributeEx, self.handle, attribute, buffer, size
        )
        if actual_size == 0:
            return None

        return buffer.raw[:actual_size]

    def set_attribute_ex(self, attribute: Union[str, int], data: Union[bytes, Any]) -> Any:
        """Set extended attribute with variable-size data.

        Args:
            attribute: Attribute constant
            data (bytes): Raw data to set

        Returns:
            bool: True on success

        raises:
            sound_lib.main.BassError: If attribute is invalid or data is malformed
        """
        if isinstance(attribute, str) and attribute in self.attribute_mapping:
            attribute = self.attribute_mapping[attribute]

        # Convert data to ctypes buffer if needed
        if isinstance(data, bytes):
            buffer = c_buffer(data)
            size = len(data)
        else:
            # Assume it's already a ctypes buffer
            buffer = data
            size = sizeof(data)

        return bass_call(
            BASS_ChannelSetAttributeEx, self.handle, attribute, buffer, size
        )

    def slide_attribute(self, attribute: Union[str, int], value: float, time: float) -> Any:
        """Slides this channel's attribute from its current value to a new value.

        Args:
          attribute: The attribute to slide the value of.
          value: The new attribute value. Consult specific documentation depending on the one in question.
          time: The length of time (in milliseconds) that it should take for the attribute to reach the value.

        Returns:
            bool: True on success, False on failure.

        raises:
            sound_lib.main.BassError: If attribute is invalid, or the attributes value is set to go from positive to negative or vice versa when the BASS_SLIDE_LOG flag is used.
        """
        if isinstance(attribute, str) and attribute in self.attribute_mapping:
            attribute = self.attribute_mapping[attribute]
        return bass_call(
            BASS_ChannelSlideAttribute, self.handle, attribute, value, time * 1000
        )

    def is_sliding(self, attribute: int = 0) -> bool:
        """Checks if an attribute (or any attribute) of this channel is sliding. Must be a sample, stream, or MOD music.

        Args:
          attribute: The attribute to check for sliding, or0 for any. Defaults to 0.

        Returns:
            bool: True if sliding, False otherwise.

        """
        return bass_call_0(BASS_ChannelIsSliding, self.handle, attribute)

    def get_info(self) -> Any:
        """Retrieves information on this channel.

        returns:
            A BASS_CHANNELINFO structure.
        """
        value = pointer(BASS_CHANNELINFO())
        bass_call(BASS_ChannelGetInfo, self.handle, value)
        return value[0]

    def get_level(self) -> int:
        """Retrieves the level (peak amplitude) of a stream, MOD music or recording channel.

        returns:
            int: -1 on error. If successful, the level of the left channel is returned in the low word (low 16 bits), and the level of the right channel is returned in the high word (high 16 bits).
                If the channel is mono, then the low word is duplicated in the high word. The level ranges linearly from 0 (silent) to 32768 (max).
                0 will be returned when a channel is stalled.

        raises:
            sound_lib.main.BassError: If this channel is not playing, or this is a decoding channel which has reached the end
        """
        return bass_call_0(BASS_ChannelGetLevel, self.handle)

    def get_level_ex(
        self,
        length: float = 0.02,
        mono: bool = False,
        stereo: bool = False,
        rms: bool = False,
        apply_volume_pan: bool = False,
        no_remove: bool = False,
    ) -> List[float]:
        """Enhanced level measurement with configurable options.

        Args:
            length (float): Seconds of data to analyze (default 0.02 = 20ms, max 1.0 for non-decoding channels)
            mono (bool): Get single mono level from all channels
            stereo (bool): Get stereo level (left from even channels, right from odd channels)
            rms (bool): Get RMS level instead of peak level
            apply_volume_pan (bool): Apply current volume/pan settings to the reading
            no_remove (bool): Don't remove inspected data from recording channel buffer

        Returns:
            list: List of float levels. Length depends on mono/stereo flags:
                - mono=True: Single level [level]
                - stereo=True: Two levels [left, right]
                - Neither: One level per channel [ch1, ch2, ...]

        raises:
            sound_lib.main.BassError: If channel is invalid, not playing, or has reached end (decoding channels)
        """
        # Build flags
        flags = 0
        if mono:
            flags |= BASS_LEVEL_MONO
        if stereo:
            flags |= BASS_LEVEL_STEREO
        if rms:
            flags |= BASS_LEVEL_RMS
        if apply_volume_pan:
            flags |= BASS_LEVEL_VOLPAN
        if no_remove:
            flags |= BASS_LEVEL_NOREMOVE

        # Determine array size needed
        if mono:
            num_levels = 1
        elif stereo:
            num_levels = 2
        else:
            # Get channel count from info
            info = self.get_info()
            num_levels = info.chans

        # Allocate array for levels
        levels_array = (c_float * num_levels)()

        # Call BASS function
        bass_call(BASS_ChannelGetLevelEx, self.handle, levels_array, length, flags)

        # Convert to Python list
        return [levels_array[i] for i in range(num_levels)]

    def get_rms_level(self, length: float = 0.02, mono: bool = False) -> Union[float, List[float]]:
        """Get RMS (Root Mean Square) level measurement.

        Args:
            length (float): Seconds of data to analyze (default 0.02 = 20ms)
            mono (bool): Get single mono level instead of per-channel levels

        Returns:
            float or list: Single RMS level (mono=True) or list of RMS levels per channel
        """
        return self.get_level_ex(length=length, mono=mono, rms=True)

    def get_stereo_levels(self, length: float = 0.02, rms: bool = False) -> List[float]:
        """Get stereo level measurement (left/right).

        Args:
            length (float): Seconds of data to analyze (default 0.02 = 20ms)
            rms (bool): Get RMS level instead of peak level

        Returns:
            list: [left_level, right_level] where left is from even channels, right from odd
        """
        return self.get_level_ex(length=length, stereo=True, rms=rms)

    def lock(self) -> Any:
        """Locks a stream, MOD music or recording channel to the current thread.

        returns:
            bool: True on success, False on failure.
        """
        return bass_call(BASS_ChannelLock, self.handle, True)

    def unlock(self) -> Any:
        """Unlocks a stream, MOD music or recording channel from the current thread.

        returns:
            bool: True on success, False on failure.
        """
        return bass_call(BASS_ChannelLock, self.handle, False)

    def get_3d_attributes(self) -> Dict[str, Union[int, float]]:
        """Retrieves the 3D attributes of a sample, stream, or MOD music channel with 3D functionality.

        returns:
            dict: A dict containing the stream's 3d attributes

        raises:
            sound_lib.main.BassError: If this channel does not have 3d functionality.
        """
        answer = dict(
            mode=c_ulong(),
            min=c_float(),
            max=c_float(),
            iangle=c_ulong(),
            oangle=c_ulong(),
            outvol=c_float(),
        )
        bass_call(
            BASS_ChannelGet3DAttributes,
            self.handle,
            pointer(answer["mode"]),
            pointer(answer["min"]),
            pointer(answer["max"]),
            pointer(answer["iangle"]),
            pointer(answer["oangle"]),
            pointer(answer["outvol"]),
        )
        res = {}
        for k in answer:
            res[k] = answer[k].value  # type: ignore
        return res

    @update_3d_system
    def set_3d_attributes(
        self, mode: int = -1, min: float = 0.0, max: float = 0.0, iangle: int = -1, oangle: int = -1, outvol: float = -1
    ) -> Any:
        """Sets the 3D attributes of a sample, stream, or MOD music channel with 3D functionality.

        Args:
          mode:  The 3D processing mode. Defaults to -1.
          min (float):  The minimum distance. The channel's volume is at maximum when the listener is within this distance... 0 or less = leave current. Defaults to 0.0.
          max (float):  The maximum distance. The channel's volume stops decreasing when the listener is beyond this distance... 0 or less = leave current. Defaults to 0.0.
          iangle (int):  The angle of the inside projection cone in degrees... 0 (no cone) to 360 (sphere), -1 = leave current. Defaults to -1.
          oangle (int):  The angle of the inside projection cone in degrees... 0 (no cone) to 360 (sphere), -1 = leave current. Defaults to -1.
          outvol (float):  The delta-volume outside the outer projection cone... 0 (silent) to 1 (same as inside the cone), less than 0 = leave current. Defaults to -1.0.

        Returns:
            bool: True on success, False otherwise.

        raises:
            sound_lib.main.BassError: If this channel does not have 3d functionality, or one or more attribute values are invalid.
        """
        return bass_call(
            BASS_ChannelSet3DAttributes,
            self.handle,
            mode,
            min,
            max,
            iangle,
            oangle,
            outvol,
        )

    def get_3d_position(self) -> Dict[str, Any]:
        """Retrieves the 3D position of a sample, stream, or MOD music channel with 3D functionality.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        answer = dict(
            position=BASS_3DVECTOR(),
            orientation=BASS_3DVECTOR(),
            velocity=BASS_3DVECTOR(),
        )
        bass_call(
            BASS_ChannelGet3DPosition,
            self.handle,
            pointer(answer["position"]),
            pointer(answer["orientation"]),
            pointer(answer["velocity"]),
        )
        return answer

    @update_3d_system
    def set_3d_position(self, position: Optional[Any] = None, orientation: Optional[Any] = None, velocity: Optional[Any] = None) -> Any:
        """Sets the 3D position of a sample, stream, or MOD music channel with 3D functionality.

        Args:
          position: Defaults to None.
          orientation: Defaults to None.
          velocity: Defaults to None

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        if position:
            position = pointer(position)
        if orientation:
            orientation = pointer(orientation)
        if velocity:
            velocity = pointer(velocity)
        return bass_call(
            BASS_ChannelSet3DPosition, self.handle, position, orientation, velocity
        )

    def set_link(self, handle: Union[int, 'Channel']) -> None:
        """Links two MOD music or stream channels together.

        Args:
          handle: The bass handle to link with this one. Can take both a sound_lib.channel or bass handle. Must be HMUSIC or HSTREAM.

        Returns:
            bool: True on success, False on failure.

        raises:
            sound_lib.main.BassError: If handle points to an invalid channel, either one is a decoding channel, or this channel is already linked to handle.
        """
        if isinstance(handle, Channel):
            handle = handle.handle
        bass_call(BASS_ChannelSetLink, self.handle, handle)

    def remove_link(self, handle: Union[int, 'Channel']) -> Any:
        """Removes a link between two MOD music or stream channels.

        Args:
          handle: The bass handle to unlink with this one. Can take both a sound_lib.channel or bass handle. Must be a HMUSIC or HSTREAM. Must currently be linked.

        Returns:
            bool: True on success, False on failure.
        raises:
            sound_lib.main.BassError: If chan is either not a valid channel, or is not already linked to handle.

        """
        if isinstance(handle, Channel):
            handle = handle.handle
        return bass_call(BASS_ChannelRemoveLink, self.handle, handle)

    def __iadd__(self, other: 'Channel') -> 'Channel':
        """Convenience method to link this channel to another.  Calls set_link on the passed in item's handle"""
        self.set_link(other.handle)
        return self

    def __isub__(self, other: 'Channel') -> 'Channel':
        """Convenience method to unlink this channel from another.  Calls remove_link on the passed in item's handle"""
        self.remove_link(other.handle)
        return self

    def get_frequency(self) -> float:
        """Retrieves sample frequency (sample rate).

        returns:
            bool: True on success, False on failure.
        """
        return self.get_attribute(BASS_ATTRIB_FREQ)

    def set_frequency(self, frequency: float) -> None:
        """Sets the frequency (sample rate) of this channel.

        Args:
          frequency (float): The sample rate... 0 = original rate (when the channel was created).

        Returns:
            bool: True on success, False on failure.
        """
        self.set_attribute(BASS_ATTRIB_FREQ, frequency)

    frequency = property(fget=get_frequency, fset=set_frequency)

    def get_pan(self) -> float:
        """Gets the panning/balance position of this channel."""
        return self.get_attribute(BASS_ATTRIB_PAN)

    def set_pan(self, pan: float) -> Any:
        """Sets the panning/balance position of this channel.

        Args:
          pan (float): The pan position... -1 (full left) to +1 (full right), 0 = centre.

        Returns:
            bool: True on success, False on Failure.

        """
        return self.set_attribute(BASS_ATTRIB_PAN, pan)

    pan = property(fget=get_pan, fset=set_pan)

    def get_volume(self) -> float:
        """Gets the volume level of a channel.

        returns:
            float: The volume level... 0 = silent, 1.0 = normal, above 1.0 = amplification.
        """
        return self.get_attribute(BASS_ATTRIB_VOL)

    def set_volume(self, volume: float) -> None:
        """sets the volume level of a channel.

        Args:
          volume (float): The volume level... 0 = silent, 1.0 = normal, above 1.0 = amplification.

        Returns:
            True on success, False on failure.
        """
        self.set_attribute(BASS_ATTRIB_VOL, volume)

    volume = property(fget=get_volume, fset=set_volume)

    def get_data(self, length: int = 16384) -> Any:
        """Retrieves the immediate sample data (or an FFT representation of it) of this channel. Must be a sample channel, stream, MOD music, or recording channel.

        Args:
          length: Number of bytes wanted (up to 268435455 or 0xFFFFFFF). Defaults to 16384.

        Returns:
            The requested bytes.

        raises:
            sound_lib.main.BassError: If this channel has reached the end, or the BASS_DATA_AVAILABLE flag was used and this is a decoding channel.
        """
        buf = c_buffer(length)
        bass_call_0(BASS_ChannelGetData, self.handle, pointer(buf), length)
        return buf

    def get_looping(self) -> bool:
        """Returns whether this channel is currently setup to loop."""
        return bass_call_0(BASS_ChannelFlags, self.handle, BASS_SAMPLE_LOOP, 0) == 20

    def set_looping(self, looping: bool) -> Any:
        """Determines whether this channel is setup to loop.

        Args:
          looping: (bool): Specifies whether this channel should loop.
        """
        if looping:
            return bass_call_0(
                BASS_ChannelFlags, self.handle, BASS_SAMPLE_LOOP, BASS_SAMPLE_LOOP
            )
        return bass_call_0(BASS_ChannelFlags, self.handle, 0, BASS_SAMPLE_LOOP)

    looping = property(fget=get_looping, fset=set_looping)

    def free(self) -> Any:
        """Frees a channel.

        Returns:
            bool: True on success, False on failure.
        """
        return bass_call(BASS_ChannelFree, self.handle)

    def __del__(self) -> None:
        try:
            self.free()
        except:
            pass

    def get_x(self) -> float:
        """Retrieves this channel's position on the X-axis, if 3d functionality is available.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        return self.get_3d_position()["position"].x

    def set_x(self, val: float) -> None:
        """Sets positioning of this channel on the X-axis, if 3d functionality is available.

        Args:
            val: The coordinate position.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        pos = self.get_3d_position()
        pos["position"].x = val
        self.set_3d_position(**pos)

    x = property(fget=get_x, fset=set_x)

    def get_y(self) -> float:
        """Retrieves this channel's position on the Y-axis, if 3d functionality is available.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        return self.get_3d_position()["position"].y

    def set_y(self, val: float) -> None:
        """Sets positioning of this channel on the Y-axis, if 3d functionality is available.

        Args:
          val: The coordinate position.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        pos = self.get_3d_position()
        pos["position"].y = val
        self.set_3d_position(**pos)

    y = property(fget=get_y, fset=set_y)

    def get_z(self) -> float:
        """Retrieves this channel's position on the Z-axis, if 3d functionality is available.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        return self.get_3d_position()["position"].z

    def set_z(self, val: float) -> None:
        """Sets positioning of this channel on the Z-axis, if 3d functionality is available.

        Args:
          val: The coordinate position.

        raises:
            sound_lib.main.BassError: If this channel was not initialized with support for 3d functionality.
        """
        pos = self.get_3d_position()
        pos["position"].z = val
        self.set_3d_position(**pos)

    z = property(fget=get_z, fset=set_z)

    def get_attributes(self) -> Dict[str, float]:
        """Retrieves all values of all attributes from this object and displays them in a dictionary whose keys are determined by this object's attribute_mapping"""
        res = {}
        for k in self.attribute_mapping:
            try:
                res[k] = self.get_attribute(k)
            except BassError:
                pass
        return res
