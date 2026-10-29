Goal: Refresh BASS binaries for QCast Windows and Mac builds.
State: Current vendor downloads succeeded on Mac in sound_lib branch build/refresh-bass using the existing updater with corrected URL inputs. Local repair/bass-download-links corrects the updater's AAC, FX, and Tags paths and strips URL directories from local download names.
Decisions and why: Keep shared binaries and download machinery in sound_lib. Vendor bass.html links supply the current paths; unchanged guessed filenames returned HTTP 404. No new updater layer.
Surprises: Missing bass_versions.json makes every library appear absent; it does not establish that a binary is outdated. Existing Mac BASS reported 2.4.16.7; refreshed BASS reports 2.4.18.3. FX already reported 2.4.12.6.
Next step: Integrate refreshed binaries and these URL repairs into one reviewed change, verify Windows runtime and Mac playback, and update QCast's consumed dependency. No release or publication yet.
