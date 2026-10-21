# Goal
Establish safe hosted baseline evidence before resolving sound_lib #13's platform_utils 1.6.2-to-1.6.3 proposal. Independently classify historical config PR #2.

# State
Fresh default 65c9e45235f93c32e633c33e7bdea4e00f4d5520. Owned draft PR #14 remains published at ece964d6fc8ce4615dfe331abc7627db9a470486. Isolated repair/task6-sound-lib-scope starts at that exact head; separate archive/task6-sound-lib-scope-published and -local refs preserve it, and -canonical preserves 3f54865d7635d8ddee838f6ad8047065d89e473f. Canonical master is eight ahead/one behind with native/plugin work and many untracked artifacts; all remain untouched. Original #2/#13 archives, baseline worktree and local #13 successor 6e88bfd6e06658fd5595cd02631fae42c374cd70 are preserved.

# Decisions and why
Run the existing eight offline updater tests in three named files using their real HTML/mock/file fixtures, then build distributions and validate the declared long description. The five stream tests in tests/test_new_stream_functions.py import native BASS before installing mocks, as does sound_lib.external.__init__; do not collect or import them in this safe gate. The updater modules have no native imports or import-time service calls. This is explicit offline subset coverage, not a full native/audio suite. The gate uses Python 3.12/Linux without changing the existing >=3.7 support declaration. It does not exercise playback, recording, live downloads, binary loaders or releases. Existing tag release workflow remains unchanged.

# Surprises
PR #2's seven-line Dependabot file has identical blob 491deae0af2cae800a8fd1bc1ffb5ecd09221266 on current default (introduced independently at ebbd9c6). The PR is content-superseded, not an ancestor/already-merged claim; do not revive its old branch.

The original CI-only head c1a7b3121536b154c320579f9367c85aaf24479a was reviewed and published as owned draft #14. Hosted run 39528315288 at that exact head ran eight offline tests successfully (8 passed in 0.35s) and built both distribution archives, then strict Twine failed both with `long_description missing`. Build logs independently report the declared README.md cannot be found. This is a confirmed baseline package-description defect, not a build failure or audio/runtime failure.

The published correction points pyproject.readme at existing tracked docs/intro.rst. Hosted run 39528756254 at exact ece964d6 succeeded: eight tests passed in 0.44s, wheel/sdist built, and strict Twine passed both archives. This is prior-head hosted evidence; the readme content, dependency/support declarations, native binaries and product source remain unchanged.

Review report reports/claude-sound-lib-14-ece964d6.md requested removal of the four added monthly github-actions Dependabot lines. This prerequisite needs existing-test CI and the confirmed readme fix, not recurring maintenance changes. Remove only that addition, restoring exact master config blob 491deae0af2cae800a8fd1bc1ffb5ecd09221266. All workflow/package/source/test/release/support/version files stay identical to published ece964d6.

# Next step
Return the complete two-file config/existing-note correction and exact local head for coordinator review before any publication. Historical actionlint 1.7.12/offline zizmor 1.31.1 results apply to the unchanged workflow; no new test/build/audit/model/native action runs here. Fresh exact-head hosted checks remain required after separately authorized publication. Subsequent actual review remains on hold until the parent clears the stopped clarification route; this independent local fix does not retry or replace that action. No push, merge, settings/security/release or PR-description change is authorized here. Preserve original #13 published head a2f7c2703696fc8a8ebe98030bb9965e05c6ebca and canonical native work.
