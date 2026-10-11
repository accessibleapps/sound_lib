# BASS plugin investigation

## Goal

Figure out how to build plugins for BASS, demonstrate a working plugin, build an
example plugin, load it through `sound_lib`, and document the process.

## Current repository state

- Branch: `master`, seven commits ahead of `origin/master`.
- No tracked worktree modifications were present at the start.
- Many pre-existing untracked artifacts are present and must be preserved.
- `sound_lib/external/pybass.py` already binds `BASS_PluginLoad`,
  `BASS_PluginFree`, and `BASS_PluginGetInfo`.
- The bundled x64 `bass.dll` reports file version 2.4.16.
- Commit `39dc058` adds the first kept source slice:
  `examples/bass_plugin/example_tone.cpp` and `example.tone`.
- Commit `054fdd4` adds the kept demo/documentation slice:
  `.gitignore`, `README.md`, and `demo.py`.
- There are no tracked worktree modifications. The task note and all
  pre-existing untracked files remain uncommitted. The compiled
  `examples/bass_plugin/build/example_tone.dll` is ignored.

## Authoritative findings

- The official BASS page currently provides a "BASS add-on API" download for
  creating C/C++ add-ons:
  `https://www.un4seen.com/files/bass-addon.zip`.
- The official add-on archive contains:
  `bass-addon.h`, `bassraw.cpp`, `bassraw.h`, `bassraw.def`, and a Visual Studio
  project. `bassraw.cpp` is a complete RAW/PCM format plugin example.
- The current official Windows BASS package is:
  `https://www.un4seen.com/files/bass24.zip`.
- The current download reports BASS file version 2.4.18; the repository bundles
  2.4.16, so the example must be built and tested against the repository's
  actual library rather than silently replacing it.
- The plugin entry point is an exported
  `const void *WINAPI BASSplugin(DWORD face)`.
- `BASSPLUGIN_INFO` returns a `BASS_PLUGININFO`; `BASSPLUGIN_CREATE` returns the
  file/user/URL stream creation callback.
- The plugin obtains BASS's internal add-on function tables using
  `GetBassFunc()`/`GetBassFunc2()`, creates the stream through
  `bassfunc->CreateStream`, associates the file through
  `bassfunc->file.SetStream`, and exports `BASSplugin`.
- Official consumer documentation says `BASS_PluginLoad` adds the plugin's
  formats to the standard stream/sample creation functions and that
  `BASS_PluginGetInfo` reports the supported formats.

## Environment observations

- Available compilers/tools include MinGW `g++`/`gcc`, `clang-cl`, and CMake.
- MSVC `cl` and `msbuild` are not currently on `PATH`.
- The official BASS add-on SDK and current BASS package were downloaded and
  extracted under
  `C:\Users\Q\AppData\Local\Temp\sound_lib_bass_addon_20260727`.
- The official `bassraw.cpp` example does not compile with strict MinGW C++
  because its callback takes `BYTE *` while the current table requires
  `void *`; it compiles with `-fpermissive`. The repository example uses the
  exact `void *` signature and compiles cleanly with
  `-Wall -Wextra -Werror`.

## Verified runtime result

- The custom plugin compiled to `example_tone.dll` while linking against the
  official BASS import library.
- The DLL imports `bass.dll` and exports exactly the required `BASSplugin`
  symbol.
- The repository's bundled BASS 2.4.16 loaded it with handle `7`.
- `BASS_PluginGetInfo` reported version `0x02040000`, one format named
  `Example tone`, and extension filter `*.tone`.
- `sound_lib.stream.FileStream` loaded `example.tone` through the standard
  BASS stream loader with plugin channel type `0x10f00`, 44.1 kHz mono output,
  a 22,050-byte length, and non-zero decoded PCM.
- The first temporary demo explicitly freed the stream and then its destructor
  attempted a second free, logging `invalid handle`. The tracked demo avoids
  that unrelated wrapper behavior by deleting the `FileStream` while BASS is
  still initialized, so its existing destructor owns the one free operation.
- The documented default command,
  `uv run examples\bass_plugin\demo.py`, passed against the DLL produced by the
  documented default build path.

## Validation gates

- C++ build:
  `g++ -std=c++17 -O2 -Wall -Wextra -Werror -shared ...` passed.
- DLL inspection showed an import of `bass.dll` and an exported `BASSplugin`.
- `uv run ruff check examples\bass_plugin\demo.py` passed.
- `uv run ruff format --check examples\bass_plugin\demo.py` passed.
- `uv run pyright examples\bass_plugin\demo.py` passed with zero errors and
  zero warnings.
- `uv run pytest` passed all 13 repository tests.

## Current blocker

No external blocker is established.

## Next action

Complete the requirement-by-requirement audit, then mark the active goal
complete if the committed artifacts and live evidence cover every objective.
