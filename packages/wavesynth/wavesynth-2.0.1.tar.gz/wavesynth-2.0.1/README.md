# `wavesynth`

A simple sound-synthesis library that provides a simplified stateful API
for generating music. The API is intentionally analogous to the `turtle`
API to assist in the creation of music-based assignments that duplicate
lessons from graphics-based assignments for more accessible course
design.

The library has fairly unsophisticated synthesis resulting in pretty
basic sounds, and is also not super performant, although both of these
things could be improved.

A log of notes is printed to assist with debugging and/or for matching
desired output.

Designed by Peter Mawhorter.
Contributions from Lyn & Ohana Turbak.


## Dependencies

Writing audio to `.wav` files can be accomplished using just the built-in
Python modules, but if you want to play audio, the `simpleaudio` package
will be needed.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python -m pip install wavesynth
```

Once it's installed, you can run a built-in example using:

```sh
python -m wavesynth
```


## Documentation

See [the
documentation](https://cs.wellesley.edu/~pmwh/wavesynth/docs/wavesynth)
for more details on how to use it and what each function does.


## Changelog

- Version 2.0.0 replaces `stepUp` and `stepDown` with `climbUp` and
  `climbDown` and removes `leapUp` and `leapDown`. New functions like
  `setFundamental` and `setScaleType` manage an internal notion of key
  signature which controls how `climbUp` and `climbDown` change pitches.
  To emulate the old `leap` functionality, set the scale type to a
  pentatonic scale and use the `climb` functions.
