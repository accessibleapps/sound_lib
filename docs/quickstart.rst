Quickstart
===========

Here we give a brief overview of the many features sound_lib has to offer.
It should be at least enough to get up and running.

Playing
-------

To load audio from a filename on the system:

>>> from sound_lib import stream
>>> from sound_lib import output
>>> o = output.Output()
>>> s = stream.FileStream(file = "music.ogg")

Or to load from a URL:

>>> from sound_lib import stream
>>> from sound_lib import output
>>> o = output.Output()
>>> s = stream.URLStream(url = "some_site.com:8000/stream.mp3")

All streams inherit from a channel. In these examples, s is a stream meaning you can call any :class:`sound_lib.channel.Channel` method.

>>> s.play()
>>> s.stop()
>>> s.pan = 1.0 # Set balance all the way to the right
>>> s.play_blocking()

In these examples, o is the :class:`sound_lib.output.Output` object. One must be created when initializing a channel for playback. Failing to do so will raise an exception.
Output objects are like channels, all be it with a few major differences. For example, they always effect playback attributes at a global level, independent of settings given to individual channels.
For instance:

>>> o.volume = 0.2

Will set the volume of all output channels to 0.2.

note: It's recommended to manage attributes of channels independently. Feel free to initialize  output and never touch it again.

note: Attributes on effected channels aren't updated accordingly. This has the potential to be confusing.

>>> s.volume = 1.0
>>> o.volume=0.5
>>> s.volume
1.0
>>> o.volume
0.5

If working with raw audio data, you can create a :class:`sound_lib.stream.PushStream`, which will play everything it receives in realtime.
A more practical example can be found in the pulling it all together section below. Here we're assuming you have audio to feed the stream.

>>> from sound_lib import output
>>> o=output.Output()
>>> p=stream.PushStream()
>>> p.play() #makes it so data is automatically played when added to the stream.
>>> p.push(data) #should start playing data.

Recording
---------

To record to a wave file.

>>> from sound_lib import input
>>> from sound_lib import recording
>>> i = input.Input()
>>> rec = recording.WaveRecording(filename = "test.wav")
>>> rec.play() #starts recording
>>> rec.stop()

A :class:`sound_lib.input.Input` object follows the same general principal as :class:`sound_lib.output.Output`. That is, everything is done at a global level.
See above for notes.

You can easily subclass :class:`sound_lib.recording.Recording` if wishing to do something else with input. See the pulling it all together section.

Pulling it altogether
---------------------

In order to combine recording and playing, the following snippet will act as an audio test. It will take input from the default input device and send it to the default output device. This is mostly useful when verifying functionality of an audio setup in a voice chat application.

.. code-block:: python

    import ctypes
    from sound_lib import input
    from sound_lib import output
    from sound_lib import recording
    from sound_lib import stream

    def record_callback(handle, buffer, length, user):
        """A callback that will receive and process recorded sample data"""
        buffer=ctypes.string_at(buffer, length)
        #Buffer could just as easily be sent to a file or over the network after additional processing.
        push.push(buffer)
        return True #To keep recording. False stops.

    o=output.Output()
    i=input.Input()
    push=stream.PushStream(chans=2)
    push.play()
    rec=recording.Recording(proc=record_callback)
    rec.play_blocking()
