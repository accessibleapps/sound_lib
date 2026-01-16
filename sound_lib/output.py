import ctypes
import platform
from ctypes import c_char_p, c_float, pointer, string_at
from enum import IntFlag
from functools import partial
from logging import getLogger
from typing import Any, Callable, Dict, List, Optional, Union

from . import config


class DeviceFlags(IntFlag):
    """Flags for BASS_Init device initialization."""

    NONE = 0
    BITS_8 = 1  # use 8 bit resolution, else 16 bit
    MONO = 2  # use mono, else stereo
    THREE_D = 4  # enable 3D functionality
    REINIT = 128  # reinitialize device
    LATENCY = 256  # calculate device latency (BASS_INFO struct)
    CPSPEAKERS = 1024  # detect speakers via Windows control panel
    SPEAKERS = 2048  # force enabling of speaker assignment
    NOSPEAKER = 4096  # ignore speaker arrangement
    DMIX = 8192  # use "dmix" (shared) output (Linux)
    FREQ = 16384  # set device sample rate
    STEREO = 32768  # limit output to stereo


class DeviceInfoFlags(IntFlag):
    """Device info status flags from BASS_DEVICEINFO."""

    NONE = 0
    ENABLED = 1  # device is enabled
    DEFAULT = 2  # device is the system default
    INIT = 4  # device is initialized
    LOOPBACK = 8  # loopback device
    DEFAULTCOM = 128  # device is the default communication device


class DeviceCaps(IntFlag):
    """Device capabilities (DSCAPS_xxx flags)."""

    NONE = 0
    CONTINUOUSRATE = 0x00000010  # supports all sample rates between min/maxrate
    EMULDRIVER = 0x00000020  # device does NOT have hardware DirectSound support
    CERTIFIED = 0x00000040  # device driver has been certified by Microsoft
    SECONDARYMONO = 0x00000100  # mono
    SECONDARYSTEREO = 0x00000200  # stereo
    SECONDARY8BIT = 0x00000400  # 8 bit
    SECONDARY16BIT = 0x00000800  # 16 bit
from .external.pybass import (
    BASS_3DALG_DEFAULT,
    BASS_3DALG_FULL,
    BASS_3DALG_LIGHT,
    BASS_3DALG_OFF,
    BASS_CONFIG_3DALGORITHM,
    BASS_CONFIG_DEV_DEFAULT,
    BASS_CONFIG_GVOL_STREAM,
    BASS_CONFIG_NET_PROXY,
    BASS_DEVICEINFO,
    BASS_Free,
    BASS_Get3DFactors,
    BASS_GetConfig,
    BASS_GetConfigPtr,
    BASS_GetDevice,
    BASS_GetDeviceInfo,
    BASS_Init,
    BASS_Pause,
    BASS_Set3DFactors,
    BASS_SetConfig,
    BASS_SetConfigPtr,
    BASS_SetDevice,
    BASS_Start,
    BASS_Stop,
)

# EAX is Windows-only
try:
    from .external.pybass import BASS_SetEAXParameters
except ImportError:
    BASS_SetEAXParameters = None
from .main import EAX_ENVIRONMENTS, BassError, bass_call, bass_call_0, update_3d_system

logger = getLogger("sound_lib.output")


def _getter(func: Callable[..., Any], key: str, obj: Dict) -> Any:
    return func(obj)[key]


def _setter(func: Callable[..., Any], kwarg: str, obj: Dict, val: Any) -> Any:
    return func(obj, **{kwarg: val})


class Output(object):
    """Represents the audio output device and its settings.

    This class handles initialization of the output device, volume control,
    and device selection.

    Args:
        device (int): Device to use, -1 = default device
        frequency (int): Output sample rate
        flags (DeviceFlags | int): Device initialization flags
        window (int): Window handle, if using DirectSound output
        clsid: Device identifier
    """

    def __init__(
        self,
        device: int = -1,
        frequency: int = 44100,
        flags: DeviceFlags | int = DeviceFlags.NONE,
        window: int = 0,
        clsid: Optional[Any] = None,
    ) -> None:
        try:
            self.use_default_device()
        except BassError:
            logger.warning("Could not set default device, continuing")
        self._device = device
        self.frequency = frequency
        self.flags = flags
        self.window = window
        self.clsid = clsid
        self.init_device(
            device=device, frequency=frequency, flags=flags, window=window, clsid=clsid
        )
        self.config = config.BassConfig()
        self.proxy: Optional[c_char_p] = None

    def init_device(
        self,
        device: Optional[int] = None,
        frequency: Optional[int] = None,
        flags: Optional[DeviceFlags | int] = None,
        window: Optional[int] = None,
        clsid: Optional[Any] = None,
    ) -> None:
        """Initialize the output device.

        Args:
          device: Device index, -1 = default (Default value = None)
          frequency: Sample rate (Default value = None)
          flags: DeviceFlags for initialization (Default value = None)
          window: Window handle (Default value = None)
          clsid: Device class ID (Default value = None)

        Returns:
            None
        """
        if device is None:
            device = self._device
        self._device = device
        if frequency is None:
            frequency = self.frequency
        self.frequency = frequency
        if flags is None:
            flags = self.flags
        self.flags = flags
        if window is None:
            window = self.window
        self.window = window
        if clsid is None:
            clsid = self.clsid
        self.clsid = clsid
        if (
            platform.system() == "Linux" and device == -1
        ):  # Bass wants default device set to 1 on linux
            device = 1
        bass_call(BASS_Init, device, frequency, flags, window, clsid)
        logger.info("Output device initialized: device=%d, frequency=%d", device, frequency)

    def start(self) -> Any:
        """ """
        return bass_call(BASS_Start)

    def pause(self) -> Any:
        """ """
        return bass_call(BASS_Pause)

    def stop(self) -> Any:
        """ """
        return bass_call(BASS_Stop)

    def get_device(self) -> int:
        """ """
        return bass_call_0(BASS_GetDevice)

    def set_device(self, device: int) -> Any:
        """

        Args:
          device:

        Returns:

        """
        if device == self._device:
            return
        self.free()
        self.init_device(device=device)
        return bass_call(BASS_SetDevice, device)

    device = property(fget=get_device, fset=set_device)

    def get_volume(self) -> float:
        """ """
        volume = BASS_GetConfig(BASS_CONFIG_GVOL_STREAM)
        if volume:
            volume = volume / 10000.0
        return volume

    def set_volume(self, volume: float) -> Any:
        """

        Args:
          volume:

        Returns:

        """
        # Pass in a float 0.0 to 1.0 and watch the volume magically change
        return bass_call(
            BASS_SetConfig, BASS_CONFIG_GVOL_STREAM, int(round(volume * 10000, 2))
        )

    volume = property(get_volume, set_volume)

    @staticmethod
    def free() -> Any:
        """ """
        return bass_call(BASS_Free)

    def get_proxy(self) -> bytes:
        """ """
        ptr = bass_call(BASS_GetConfigPtr, BASS_CONFIG_NET_PROXY)
        return string_at(ptr)

    def set_proxy(self, proxy: Union[str, bytes]) -> Any:
        """

        Args:
          proxy:

        Returns:

        """
        if isinstance(proxy, str):
            proxy = proxy.encode("utf-8")
        self.proxy = c_char_p(proxy)
        return bass_call(BASS_SetConfigPtr, BASS_CONFIG_NET_PROXY, self.proxy)

    def use_default_device(self, use: bool = True) -> None:
        """

        Args:
          use:  (Default value = True)

        Returns:

        """
        return bass_call(BASS_SetConfig, BASS_CONFIG_DEV_DEFAULT, use)

    @staticmethod
    def get_device_names() -> List[str]:
        """Convenience method that returns a list of device names that are considered
                valid by bass.

        Args:

        Returns:
            List[str]: List of device names.
        """

        result: List[str] = []  # empty list to start.
        info = BASS_DEVICEINFO()
        count = 1
        while BASS_GetDeviceInfo(count, ctypes.byref(info)):
            if info.flags & DeviceInfoFlags.ENABLED:
                retrieved = info.name
                if platform.system() == "Windows":
                    retrieved = retrieved.decode("mbcs")
                elif platform.system() == "Darwin":
                    retrieved = retrieved.decode("utf-8")
                retrieved = retrieved.replace("(", "").replace(")", "").strip()
                result.append(retrieved)
            count += 1
        return result

    def find_device_by_name(self, name: str) -> int:
        """

        Args:
          name:

        Returns:

        """
        return self.get_device_names().index(name) + 1

    def find_default_device(self) -> int:
        """ """
        try:
            return self.get_device_names().index("Default") + 1
        except ValueError:
            logger.warning("Could not find default device")
            return -1

    def find_user_provided_device(self, device_name: str) -> int:
        """

        Args:
          device_name:

        Returns:

        """
        try:
            return self.find_device_by_name(device_name)
        except ValueError:
            logger.warning(
                "Could not find device named %s, using default device", device_name
            )
            return self.find_default_device()


class ThreeDOutput(Output):
    """Output device with 3D audio support enabled."""

    def __init__(
        self,
        device: int = -1,
        frequency: int = 44100,
        flags: DeviceFlags | int = DeviceFlags.THREE_D,
        window: int = 0,
        clsid: Optional[Any] = None,
    ) -> None:
        super(ThreeDOutput, self).__init__(
            device=device, frequency=frequency, flags=flags, window=window, clsid=clsid
        )

    def get_3d_factors(self) -> Dict[str, float]:
        """ """
        res = {
            "distance_factor": c_float(),
            "rolloff": c_float(),
            "doppler_factor": c_float(),
        }
        bass_call(
            BASS_Get3DFactors,
            pointer(res["distance_factor"]),
            pointer(res["rolloff"]),
            pointer(res["doppler_factor"]),
        )
        return {k: res[k].value for k in res}

    @update_3d_system
    def set_3d_factors(
        self,
        distance_factor: Union[float, str] = -1,
        rolloff: float = -1,
        doppler_factor: float = -1,
    ) -> Any:
        """

        Args:
          distance_factor:  (Default value = -1)
          rolloff:  (Default value = -1)
          doppler_factor:  (Default value = -1)

        Returns:

        """
        conversions = {"meters": 1.0, "yards": 0.9144, "feet": 0.3048}
        if isinstance(distance_factor, str) and distance_factor in conversions:
            distance_factor = conversions[distance_factor]
        return bass_call(BASS_Set3DFactors, distance_factor, rolloff, doppler_factor)

    distance_factor = property(
        fget=partial(_getter, get_3d_factors, "distance_factor"),
        fset=partial(_setter, set_3d_factors, "distance_factor"),
    )

    rolloff = property(
        fget=partial(_getter, get_3d_factors, "rolloff"),
        fset=partial(_setter, set_3d_factors, "rolloff"),
    )

    doppler_factor = property(
        fget=partial(_getter, get_3d_factors, "doppler_factor"),
        fset=partial(_setter, set_3d_factors, "doppler_factor"),
    )

    def set_eax_parameters(
        self,
        environment: Optional[Union[str, int]] = None,
        volume: Optional[float] = None,
        decay: Optional[float] = None,
        damp: Optional[float] = None,
    ) -> None:
        """

        Args:
          environment:  (Default value = None)
          volume:  (Default value = None)
          decay:  (Default value = None)
          damp:  (Default value = None)

        Returns:

        """
        if BASS_SetEAXParameters is None:
            logger.warning("EAX is only supported on Windows")
            return

        def convert_arg(arg: Optional[Union[str, int, float]]) -> int:
            """

            Args:
              arg:

            Returns:

            """
            if arg is None:
                return -1
            return int(arg) if not isinstance(arg, str) else -1

        if isinstance(environment, str) and environment in EAX_ENVIRONMENTS:
            environment = EAX_ENVIRONMENTS[environment]
        else:
            environment = convert_arg(environment)
        volume = convert_arg(volume)
        decay = convert_arg(decay)
        damp = convert_arg(damp)
        bass_call(BASS_SetEAXParameters, environment, volume, decay, damp)

    def get_3d_algorithm(self) -> int:
        """ """
        return BASS_GetConfig(BASS_CONFIG_3DALGORITHM)

    def set_3d_algorithm(self, algo: Union[str, int]) -> Any:
        """

        Args:
          algo:

        Returns:

        """
        replacements = {
            "default": BASS_3DALG_DEFAULT,
            "off": BASS_3DALG_OFF,
            "full": BASS_3DALG_FULL,
            "light": BASS_3DALG_LIGHT,
        }
        if isinstance(algo, str) and algo in replacements:
            algo = replacements[algo]
        return BASS_SetConfig(BASS_CONFIG_3DALGORITHM, algo)
