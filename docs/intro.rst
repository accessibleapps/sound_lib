Introduction
=============

.. image:: https://img.shields.io/pypi/v/sound-lib.svg
   :target: https://pypi.org/project/sound-lib/
   :alt: PyPI Version

.. image:: https://img.shields.io/github/stars/accessibleapps/sound_lib.svg
   :target: https://github.com/accessibleapps/sound_lib
   :alt: GitHub Stars

.. image:: https://img.shields.io/github/forks/accessibleapps/sound_lib.svg
   :target: https://github.com/accessibleapps/sound_lib
   :alt: GitHub Forks

.. image:: https://img.shields.io/pypi/pyversions/sound-lib.svg
   :target: https://pypi.org/project/sound-lib/
   :alt: Python Versions

.. image:: https://img.shields.io/github/license/accessibleapps/sound_lib.svg
   :target: https://github.com/accessibleapps/sound_lib/blob/master/LICENSE
   :alt: License

.. image:: https://readthedocs.org/projects/sound-lib/badge/?version=latest
   :target: https://sound-lib.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Sound_lib is a Python library that simplifies working with audio in Python applications.

It serves as a high-level wrapper around the powerful BASS audio library, incorporating most of BASS's add-ons to provide a comprehensive audio solution.

Installation
------------

Install from PyPI::

    pip install sound_lib

Quick Start
-----------

Here's a simple example to get you started::

    import sound_lib
    from sound_lib.stream import FileStream
    from sound_lib.output import Output
    import time

    # Initialize audio output
    output = Output()

    # Load and play an audio file
    stream = FileStream(file="example.mp3")
    stream.play()

    # Wait for playback to finish
    while stream.is_playing:
        time.sleep(0.1)

    # Clean up
    stream.free()

Why Sound_lib?
--------------

Sound_lib aims to make audio programming in Python more accessible and intuitive. It abstracts away many of the low-level details of the BASS library while still providing access to its powerful features.

Features
---------

* Cross-platform, tested on Microsoft Windows, MacOS, and Linux
* Support for playback of an incredible variety of audio formats
* Support for recording from a microphone or other input device
* Support for reencoding audio to a variety of formats
* Comprehensive audio effects system with DirectX and BASS_FX effects
* Real-time tempo, pitch, and frequency modification
* Support for streaming files from disk, memory, or the internet
* 3D positional audio support
* Small yet efficient
* Well-documented

Audio Effects System
--------------------

Sound_lib provides a comprehensive effects processing system that wraps both BASS built-in effects and BASS_FX effects. The effects system features automatic parameter mapping between C-style BASS parameter names and Pythonic naming conventions.

Built-in BASS Effects
~~~~~~~~~~~~~~~~~~~~~~

DirectX 8 effects available in the base BASS library:

* **Reverb**: Environmental reverb with configurable decay time and mix levels
* **Echo/Delay**: Digital delay effects with separate left/right channel control
* **Chorus**: Rich modulation effect with configurable depth and frequency
* **Compressor**: Dynamic range compression with threshold, ratio, and timing controls
* **Distortion**: Audio distortion and overdrive effects
* **Flanger**: Sweeping comb filter effect for classic modulation
* **Gargle**: Amplitude modulation effect
* **I3DL2Reverb**: Advanced 3D reverb with environmental presets
* **ParamEq**: Parametric equalizer for frequency-specific adjustments

Example usage::

    from sound_lib.effects.bass import Reverb
    from sound_lib.stream import FileStream

    stream = FileStream(file="audio.mp3")
    reverb = Reverb(stream)

    # Set parameters using Pythonic names
    reverb.reverb_time = 1000        # Reverb time in milliseconds
    reverb.reverb_mix = 0.8          # Wet/dry mix
    reverb.high_freq_rt_ratio = 0.5  # High frequency ratio

    stream.play()

BASS_FX Effects
~~~~~~~~~~~~~~~

Extended effects from the BASS_FX add-on:

* **Volume**: Real-time volume control
* **Peak Equalizer**: Advanced frequency-specific equalization
* **Tempo Processing**: Real-time tempo, pitch, and frequency modification

Real-time Tempo Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

The tempo system allows independent modification of tempo, pitch, and frequency without affecting other characteristics::

    from sound_lib.effects.tempo import Tempo
    from sound_lib.stream import FileStream

    # Create source stream
    source = FileStream(file="music.mp3")

    # Create tempo processor
    tempo = Tempo(source, free_source=True)

    # Modify audio characteristics
    tempo.tempo = 10          # 10% faster tempo
    tempo.tempo_pitch = -2    # Lower pitch by 2 semitones
    tempo.tempo_freq = 5      # Increase frequency by 5%

    tempo.play()

Effect Parameter Mapping
~~~~~~~~~~~~~~~~~~~~~~~~

The effects system automatically converts between BASS C-style parameter names and Python conventions:

* ``fWetDryMix`` becomes ``wet_dry_mix``
* ``fReverbTime`` becomes ``reverb_time``
* ``lWaveform`` becomes ``waveform``
* ``fHighFreqRTRatio`` becomes ``high_freq_rt_ratio``

Multiple effects can be chained on the same audio channel with configurable priority ordering.

Other Examples
--------------

Recording from microphone::

    from sound_lib.input import Input
    from sound_lib.recording import WaveRecording

    # Initialize input device
    input_device = Input()

    # Start recording to file
    recorder = WaveRecording(filename="recording.wav")
    recorder.play()  # Start recording

    # Stop after some time
    recorder.stop()

3D Positional Audio::

    from sound_lib.stream import FileStream
    from sound_lib.listener import Listener

    # Create 3D audio stream
    stream = FileStream(file="audio.mp3", three_d=True)
    listener = Listener()

    # Position sound source in 3D space
    stream.set_3d_position(x=10, y=0, z=5)

    # Set listener position and orientation
    listener.set_position(x=0, y=0, z=0)
    stream.play()

Requirements
------------

* Python 3.7 or higher
* Windows, macOS, or Linux
* BASS audio libraries (included with package)

For commercial use, a BASS license from `un4seen developments <http://www.un4seen.com/bass.html>`_ is required.

License
-------

Sound_lib is released under the MIT License. The underlying BASS library is free for non-commercial use.

Getting Help
------------

If you're hung up on a certain function, class, or method it might be helpful to take a look at the comprehensive bass documentation directly (distributed with sound_lib but also obtainable online).

Bass also has a highly active `forum <http://www.un4seen.com/forum/>`_. When interacting there, it's important to remember that most of the good folks you'll encounter have never used and have no idea what sound_lib is or does. Thus, it's in your best interest to either describe the problem in layman's terms or point to actual bass functions.

If you're willing and able, do have a look at the portion of sound_lib that happens to be giving you trouble. It's quite possible that you might be facing a simple misunderstanding with the way things work. The force is with those who read the code after all.

If all else fails, you may have found a  bug in sound_lib. Please do let us know at our `github issue tracker <https://github.com/accessibleapps/sound_lib/issues/>`_. Thanks in advance for contributions!

Links
-----

* **Documentation**: https://sound-lib.readthedocs.io/
* **PyPI Package**: https://pypi.org/project/sound-lib/
* **GitHub Repository**: https://github.com/accessibleapps/sound_lib
* **Issue Tracker**: https://github.com/accessibleapps/sound_lib/issues
* **BASS Library**: https://un4seen.com
* **BASS Forum**: http://www.un4seen.com/forum/
