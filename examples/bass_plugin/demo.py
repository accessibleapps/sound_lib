"""Load and exercise the example BASS plugin through sound_lib."""

import argparse
from pathlib import Path
from typing import Optional, Sequence

from sound_lib.external.pybass import (
    BASS_Free,
    BASS_Init,
    BASS_PluginFree,
    BASS_PluginGetInfo,
    BASS_PluginLoad,
)
from sound_lib.main import bass_call
from sound_lib.stream import FileStream


EXPECTED_CHANNEL_TYPE = 0x10F00


def parse_args(arguments: Optional[Sequence[str]] = None) -> argparse.Namespace:
    example_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Verify the example tone plugin with sound_lib."
    )
    parser.add_argument(
        "plugin",
        nargs="?",
        type=Path,
        default=example_dir / "build" / "example_tone.dll",
        help="path to the compiled plugin DLL",
    )
    parser.add_argument(
        "--tone",
        type=Path,
        default=example_dir / "example.tone",
        help="path to a BASSTONE input file",
    )
    return parser.parse_args(arguments)


def decode(value: Optional[bytes]) -> str:
    return "" if value is None else value.decode("utf-8")


def main(arguments: Optional[Sequence[str]] = None) -> None:
    args = parse_args(arguments)
    plugin_path = args.plugin.resolve()
    tone_path = args.tone.resolve()
    if not plugin_path.is_file():
        raise FileNotFoundError(f"plugin not found: {plugin_path}")
    if not tone_path.is_file():
        raise FileNotFoundError(f"tone file not found: {tone_path}")

    plugin = bass_call(BASS_PluginLoad, str(plugin_path), 0)
    initialized = False
    stream = None
    try:
        info_pointer = BASS_PluginGetInfo(plugin)
        if not info_pointer:
            raise RuntimeError("BASS_PluginGetInfo returned NULL")
        info = info_pointer.contents
        if info.formatc != 1:
            raise RuntimeError(f"expected one plugin format, got {info.formatc}")
        plugin_format = info.formats[0]
        format_name = decode(plugin_format.name)
        format_extensions = decode(plugin_format.exts)
        if format_name != "Example tone" or format_extensions != "*.tone":
            raise RuntimeError(
                f"unexpected plugin metadata: {format_name!r}, {format_extensions!r}"
            )

        bass_call(BASS_Init, 0, 44100, 0, 0, None)
        initialized = True
        stream = FileStream(file=str(tone_path), decode=True)
        channel_info = stream.get_info()
        if channel_info.ctype != EXPECTED_CHANNEL_TYPE:
            raise RuntimeError(
                "the standard stream loader did not select the tone plugin"
            )
        pcm = stream.get_data(4096).raw
        if not any(pcm):
            raise RuntimeError("the tone plugin returned only silence")

        print(f"plugin_handle={plugin}")
        print(f"plugin_version=0x{info.version:08x}")
        print(f"format_name={format_name}")
        print(f"format_extensions={format_extensions}")
        print(f"stream_handle={stream.handle}")
        print(f"stream_ctype=0x{channel_info.ctype:x}")
        print(f"stream_frequency={channel_info.freq}")
        print(f"stream_channels={channel_info.chans}")
        print(f"stream_length_bytes={stream.get_length()}")
        print("decoded_nonzero_pcm=true")
    finally:
        if stream is not None:
            # FileStream.__del__ owns the BASS_StreamFree call. Delete it while
            # BASS and the plugin are still loaded.
            del stream
        if initialized:
            bass_call(BASS_Free)
        bass_call(BASS_PluginFree, plugin)


if __name__ == "__main__":
    main()
