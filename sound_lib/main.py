from __future__ import absolute_import
from typing import Any, Callable, Dict, TypeVar
from .external.pybass import (
    BASS_Apply3D,
    BASS_ErrorGetCode,
    EAX_ENVIRONMENT_GENERIC,
    EAX_ENVIRONMENT_PADDEDCELL,
    EAX_ENVIRONMENT_ROOM,
    EAX_ENVIRONMENT_BATHROOM,
    EAX_ENVIRONMENT_LIVINGROOM,
    EAX_ENVIRONMENT_STONEROOM,
    EAX_ENVIRONMENT_AUDITORIUM,
    EAX_ENVIRONMENT_CONCERTHALL,
    EAX_ENVIRONMENT_CAVE,
    EAX_ENVIRONMENT_ARENA,
    EAX_ENVIRONMENT_HANGAR,
    EAX_ENVIRONMENT_CARPETEDHALLWAY,
    EAX_ENVIRONMENT_HALLWAY,
    EAX_ENVIRONMENT_STONECORRIDOR,
    EAX_ENVIRONMENT_ALLEY,
    EAX_ENVIRONMENT_FOREST,
    EAX_ENVIRONMENT_CITY,
    EAX_ENVIRONMENT_MOUNTAINS,
    EAX_ENVIRONMENT_QUARRY,
    EAX_ENVIRONMENT_PLAIN,
    EAX_ENVIRONMENT_PARKINGLOT,
    EAX_ENVIRONMENT_SEWERPIPE,
    EAX_ENVIRONMENT_UNDERWATER,
    EAX_ENVIRONMENT_DRUGGED,
    EAX_ENVIRONMENT_DIZZY,
    EAX_ENVIRONMENT_PSYCHOTIC,
    BASS_SAMPLE_LOOP,
    BASS_STREAM_AUTOFREE,
    BASS_SAMPLE_MONO,
    BASS_SAMPLE_SOFTWARE,
    BASS_SAMPLE_3D,
    BASS_SAMPLE_FX,
    BASS_STREAM_DECODE,
    get_error_description,
)
from functools import update_wrapper

F = TypeVar("F", bound=Callable[..., Any])

EAX_ENVIRONMENTS: Dict[str, int] = {
    "generic": EAX_ENVIRONMENT_GENERIC,
    "padded_cell": EAX_ENVIRONMENT_PADDEDCELL,
    "room": EAX_ENVIRONMENT_ROOM,
    "bathroom": EAX_ENVIRONMENT_BATHROOM,
    "living_room": EAX_ENVIRONMENT_LIVINGROOM,
    "stone_room": EAX_ENVIRONMENT_STONEROOM,
    "auditorium": EAX_ENVIRONMENT_AUDITORIUM,
    "concert_hall": EAX_ENVIRONMENT_CONCERTHALL,
    "cave": EAX_ENVIRONMENT_CAVE,
    "arena": EAX_ENVIRONMENT_ARENA,
    "hanger": EAX_ENVIRONMENT_HANGAR,
    "carpeted_hallway": EAX_ENVIRONMENT_CARPETEDHALLWAY,
    "hallway": EAX_ENVIRONMENT_HALLWAY,
    "stone_corridor": EAX_ENVIRONMENT_STONECORRIDOR,
    "alley": EAX_ENVIRONMENT_ALLEY,
    "forest": EAX_ENVIRONMENT_FOREST,
    "city": EAX_ENVIRONMENT_CITY,
    "mountains": EAX_ENVIRONMENT_MOUNTAINS,
    "quarry": EAX_ENVIRONMENT_QUARRY,
    "plain": EAX_ENVIRONMENT_PLAIN,
    "parking_lot": EAX_ENVIRONMENT_PARKINGLOT,
    "sewer_pipe": EAX_ENVIRONMENT_SEWERPIPE,
    "underwater": EAX_ENVIRONMENT_UNDERWATER,
    "drugged": EAX_ENVIRONMENT_DRUGGED,
    "dizzy": EAX_ENVIRONMENT_DIZZY,
    "psychotic": EAX_ENVIRONMENT_PSYCHOTIC,
}


class BassError(Exception):
    """Error that is raised when there is a problem with a Bass call."""

    def __init__(self, code: int, description: str) -> None:
        self.code = code
        self.description = description

    def __str__(self) -> str:
        return "%d, %s" % (self.code, self.description)


def bass_call(function: Callable[..., Any], *args: Any) -> Any:
    """Makes a call to bass and raises an exception if it fails.
    This will most likely prove unnecessary for external usage, however we keep it just in case.

    Args:
      function (str): Name of the internal bass function to be called.
      *args: Arguments that will be passed to function.

    Returns:
        Raw output from the specified bass function. Refer to the official docs.

    """
    res = function(*args)
    if res == 0 or res == -1:
        code = BASS_ErrorGetCode()
        raise BassError(code, get_error_description(code))
    return res


def bass_call_0(function: Callable[..., Any], *args: Any) -> Any:
    """Makes a call to bass and raises an exception if it fails.  Does not consider 0 an error.
    This will most likely prove unnecessary for external usage, however we keep it just in case.

    Args:
      function (str): Name of the internal bass function to be called.
      *args: Arguments that will be passed to function.

    Returns:
        Raw output from the specified bass function. Refer to the official docs.
    """
    res = function(*args)
    if res == -1:
        code = BASS_ErrorGetCode()
        raise BassError(code, get_error_description(code))
    return res


def update_3d_system(func: F) -> F:
    """Decorator to automatically update the 3d system after a function call."""

    def update_3d_system_wrapper(*args: Any, **kwargs: Any) -> Any:
        """

        Args:
          *args:
          **kwargs:

        Returns:

        """
        val = func(*args, **kwargs)
        bass_call(BASS_Apply3D)
        return val

    update_wrapper(update_3d_system_wrapper, func)
    return update_3d_system_wrapper  # type: ignore


class FlagObject(object):
    """An object which translates bass flags into human-readable/usable items"""

    flag_mapping: Dict[str, int] = {}

    def flags_for(self, **flags: bool) -> int:
        """Retrieves flags for given attributes.

        Args:
          **flags: A mapping of human-readable attribute names to numeric values.

        Returns:
            int: A bitmask containing the specified flags, or 0 if nothing was provided.
        """
        res = 0
        for k, v in flags.items():
            if v:
                res |= self.flag_mapping[k]
        return res

    def setup_flag_mapping(self) -> None:
        """Sets up a class-level mapping of common flags, in the format human-readable name:value.
        Tipically expanded upon in a subclass.
        """
        self.flag_mapping = {
            "loop": BASS_SAMPLE_LOOP,
            "autofree": BASS_STREAM_AUTOFREE,
            "mono": BASS_SAMPLE_MONO,
            "software": BASS_SAMPLE_SOFTWARE,
            "three_d": BASS_SAMPLE_3D,
            "fx": BASS_SAMPLE_FX,
            "decode": BASS_STREAM_DECODE,
        }
