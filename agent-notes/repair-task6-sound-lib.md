# Goal
Establish safe hosted baseline evidence before resolving sound_lib #13's platform_utils 1.6.2-to-1.6.3 proposal. Independently classify historical config PR #2.

# State
Fresh default 65c9e45235f93c32e633c33e7bdea4e00f4d5520. Canonical master 3f54865d7635d8ddee838f6ad8047065d89e473f is eight ahead/one behind with native/plugin work and many untracked artifacts; preserved under archive/task6-sound-lib-canonical and left untouched. Exact original #2 5060fe43775ff5efacaa0694e8593a99be53094f and #13 a2f7c2703696fc8a8ebe98030bb9965e05c6ebca have separate local/published archives. This branch starts directly from fresh default; no feature pin or canonical work is copied.

# Decisions and why
Run the existing eight offline updater tests in three named files using their real HTML/mock/file fixtures, then build distributions and validate the declared long description. The five stream tests in tests/test_new_stream_functions.py import native BASS before installing mocks, as does sound_lib.external.__init__; do not collect or import them in this safe gate. The updater modules have no native imports or import-time service calls. This is explicit offline subset coverage, not a full native/audio suite. The gate uses Python 3.12/Linux without changing the existing >=3.7 support declaration. It does not exercise playback, recording, live downloads, binary loaders or releases. Existing tag release workflow remains unchanged.

# Surprises
PR #2's seven-line Dependabot file has identical blob 491deae0af2cae800a8fd1bc1ffb5ecd09221266 on current default (introduced independently at ebbd9c6). The PR is content-superseded, not an ancestor/already-merged claim; do not revive its old branch.

Default pyproject.toml declares readme=README.md while that file is absent from the tracked tree; docs/intro.rst exists. No build failure is claimed from that static observation. Per coordinator instruction this first patch is CI-only: obtain actual hosted build/strict-metadata evidence before deciding whether metadata needs a baseline fix. No metadata/support/dependency source changes are made here.

# Next step
actionlint 1.7.12 passed; offline zizmor 1.31.1 reported no findings (one default suppression). Return complete local diff/head for coordinator review before publication. No local full CI, model calls, native execution, settings/merge/release actions or descriptions changed. Actual red/green hosted evidence and the narrowly owned #13 continuation remain pending.
