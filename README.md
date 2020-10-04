# Play sounds in your Python scripts

This project provides a simple cross-platform API to play sounds in your Python scripts, and allows you to play sounds while a function or code block executes, or afterwards.

It's a simple wrapper over [`playsound`](https://pypi.org/project/playsound/) and [`boombox`](https://pypi.org/project/boombox/).

I use this project in [`onhold`](https://github.com/alexdelorenzo/onhold) and [`ding`](https://github.com/alexdelorenzo/ding).

# Rationale

`boombox` is great and 90% of the way there, however the default options for playing sounds on Windows are limited to WAV files. If the platform is Windows, `play_sounds` will default to the `playsound` backend.

# Installation

```bash
python3 -m pip install play_sounds
```

# Usage
This library uses [`pathlib.Path` objects](https://docs.python.org/3/library/pathlib.html#pathlib.Path) when pointing to filenames and paths. 

## Playing a file
```python
from play_sounds import play_file, DEFAULT_SONG

play_file(DEFAULT_SONG)  # blocks by default

# play without blocking
play_file(DEFAULT_SONG, block=False) 

```

## Playing while work completes
```python
from time import sleep
from play_sounds import play_while_running, DEFAULT_SONG

with play_while_running(DEFAULT_SONG):
  sleep(60)
```

## Play sound after work completes
```python
from time import sleep
from play_sounds import play_after, DEFAULT_SOUND

with play_after(DEFAULT_SOUND):  # blocks by default
  sleep(60)

# play without blocking
with play_after(DEFAULT_SOUND, block=False):
  sleep(60)
```


# Copyright
See `CREDIT.md`.

# License
See `LICENSE`.
