Goal: Restore the declared Python 3.8 Windows import path for QCast's scrambled build.
State: Current integrated sound_lib raises TypeError while importing channel.py on CPython 3.8 at LevelFlags | int. output.py, recording.py and stream.py contain the same evaluated union annotations.
Decisions and why: Smallest repair is one postponed-annotations import in each of the four affected modules. Keep the existing type information, flags, and declared runtime support; no dependency downgrade or product workaround.
Next step: Publish, observe existing CI, consume exact branch in the Windows protected QCast build and validate actual imports and artifact.
