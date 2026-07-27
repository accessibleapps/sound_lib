# Building and loading a BASS plugin

This example is a real BASS file-format plugin. It registers `*.tone` files
with BASS's standard stream loader, generates a 44.1 kHz mono sine wave, and is
loaded and decoded through `sound_lib`.

The verification here was performed on Windows x64 on 2026-07-27 with:

- the repository's bundled BASS 2.4.16 runtime;
- the current official BASS add-on API;
- the import library and `bass.h` from the official BASS 2.4.18 package;
- MinGW-w64 `g++`.

The official downloads are:

- [BASS add-on API](https://www.un4seen.com/files/bass-addon.zip)
- [BASS for Windows](https://www.un4seen.com/files/bass24.zip)
- [BASS product page](https://www.un4seen.com/bass.html)
- [BASS_PluginLoad documentation](https://www.un4seen.com/doc/bass/BASS_PluginLoad.html)

The BASS headers and import libraries are not copied into this repository.
Download them from Un4seen and review the BASS license for the intended use.

## What makes a DLL a BASS plugin

A Windows BASS file-format plugin has these parts:

1. It exports `const void *WINAPI BASSplugin(DWORD face)`.
2. During `DLL_PROCESS_ATTACH`, it checks the BASS 2.4 ABI and obtains the
   add-on function table with `GetBassFunc()`.
3. For `BASSPLUGIN_INFO`, `BASSplugin` returns a `BASS_PLUGININFO` describing
   the supported channel type, format name, and extension filter.
4. For `BASSPLUGIN_CREATE`, it returns a `STREAMCREATEPROC`.
5. The creation callback recognizes the file by its contents, calls
   `bassfunc->CreateStream`, and associates the BASS file with that stream via
   `bassfunc->file.SetStream`.
6. The `ADDON_FUNCTIONS` and `STREAMPROC` callbacks provide decoding, length,
   seeking, channel information, and cleanup.

The extension filter is informational. The plugin must inspect the content and
return `BASS_ERROR_FILEFORM` when the file is not its format, because BASS tries
loaded format plugins in load order.

`example_tone.cpp` implements exactly that ABI. It does not add a `sound_lib`
adapter: `sound_lib` already exposes `BASS_PluginLoad`, and its existing
`FileStream` reaches the plugin through BASS's standard
`BASS_StreamCreateFile` path.

The example input is UTF-8 text:

```text
BASSTONE
440
250
```

The second line is frequency in Hz and the third is duration in milliseconds.
The example channel type `0x10f00` is only for this demonstration. A production
add-on should obtain a unique type value from Un4seen, as directed by the
official add-on header.

## Build on Windows x64 with MinGW-w64

Extract `bass-addon.zip` and `bass24.zip`, then set these two paths from the
repository root:

```powershell
$BassAddonSdk = "C:\path\to\extracted\bass-addon"
$BassSdk = "C:\path\to\extracted\bass24"
```

Build the DLL:

```powershell
New-Item -ItemType Directory -Force -Path examples\bass_plugin\build

g++ -std=c++17 -O2 -Wall -Wextra -Werror -shared `
  examples\bass_plugin\example_tone.cpp `
  -I"$BassAddonSdk" `
  -I"$BassSdk\c" `
  -L"$BassSdk\c\x64" `
  -lbass `
  -o examples\bass_plugin\build\example_tone.dll
```

The compiler and linker architecture must match Python and the BASS DLL that
`sound_lib` loads. The command above is x64 because it uses `c\x64\bass.lib`.
For 32-bit Python, use a 32-bit compiler and the top-level `c\bass.lib`.

The official add-on archive also includes `bassraw.vcxproj` for Visual Studio.
It is a useful full-featured reference for dedicated add-on functions,
configuration callbacks, URLs, user-file streams, seeking, and syncs. The
example in this repository is intentionally smaller and uses only the plugin
path exercised here.

To inspect the required export with the MinGW tools:

```powershell
objdump -p examples\bass_plugin\build\example_tone.dll |
  Select-String "BASSplugin|DLL Name"
```

The output must include `BASSplugin` and an import of `bass.dll`.

## Load and exercise it through sound_lib

From a synchronized project environment:

```powershell
uv run examples\bass_plugin\demo.py
```

To test a DLL at another path:

```powershell
uv run examples\bass_plugin\demo.py C:\path\to\example_tone.dll
```

The demo proves more than a successful DLL load:

- `BASS_PluginLoad` returns a non-zero plugin handle;
- `BASS_PluginGetInfo` reports `Example tone` and `*.tone`;
- `sound_lib.stream.FileStream` selects the plugin for `example.tone`;
- `BASS_ChannelGetInfo` reports the plugin's `0x10f00` channel type;
- decoding returns non-zero PCM.

A successful run looks like this; handle values may differ:

```text
plugin_handle=7
plugin_version=0x02040000
format_name=Example tone
format_extensions=*.tone
stream_handle=2147483656
stream_ctype=0x10f00
stream_frequency=44100
stream_channels=1
stream_length_bytes=22050
decoded_nonzero_pcm=true
```

The demo initializes BASS's no-sound device and creates a decoding channel, so
it does not require an audio output device and does not play sound.

## Compatibility and failure diagnosis

The plugin checks the BASS major/minor ABI (`2.4`) when Windows loads the DLL.
The exact source and command above were also run against this repository's
BASS 2.4.16 binary. Do not replace the bundled BASS DLL merely to build the
plugin; the import library is a link-time artifact, while the repository's
loaded DLL is the runtime tested by the demo.

Common failures:

- `BASS_ERROR_FILEOPEN`: the DLL path is wrong or a dependent DLL cannot be
  loaded.
- `BASS_ERROR_FILEFORM`: the DLL does not export the plugin entry point, the
  wrong architecture was built, or the plugin rejected the file content.
- `BASS_ERROR_VERSION`: the plugin and BASS 2.4 runtime are incompatible.
- `BASS_ERROR_ALREADY`: the same plugin is already loaded.

Use `BASS_PluginGetInfo` after every load rather than treating a non-zero handle
as the only proof. For a format plugin, create a stream through the standard
loader and decode data as the final verification gate.
