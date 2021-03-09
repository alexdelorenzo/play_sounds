# 🔊 Play sounds in Python scripts
`play_sounds` provides a simple cross-platform API to play sounds in Python scripts. It includes a synchronous API and an equivalent asynchronous API.

For code examples, you can check out [`onhold`](https://github.com/alexdelorenzo/onhold) and [`ding`](https://github.com/alexdelorenzo/ding), or scroll down to the [Usage section](https://github.com/alexdelorenzo/play_sounds#usage).

# Rationale
[`boombox`](https://pypi.org/project/boombox/) is great and 90% of the way there, however the default options for playing sounds on Windows are limited to WAV files. If the platform is Windows, `play_sounds` will default to the [`playsound`](https://pypi.org/project/playsound/) backend.

# Installation

```bash
python3 -m pip install play_sounds
```

# Usage
This library uses [`pathlib.Path` objects](https://docs.python.org/3/library/pathlib.html#pathlib.Path) when pointing to filenames and paths. 

There's a synchronous API and an asynchronous API that you can use with the `async/await` syntax and `asyncio`. 

## Synchronous API
### Play a file
```python
from play_sounds import play_file, DEFAULT_SONG

play_file(DEFAULT_SONG)  # blocks by default

# play without blocking
play_file(DEFAULT_SONG, block=False) 
```

### Play while work completes
```python
from time import sleep
from play_sounds import play_while_running, DEFAULT_SONG

with play_while_running(DEFAULT_SONG):
  sleep(60)
```

### Play a file after work completes
```python
from time import sleep
from play_sounds import play_after, DEFAULT_SOUND

with play_after(DEFAULT_SOUND):  # blocks by default
  sleep(60)

# play without blocking
with play_after(DEFAULT_SOUND, block=False):
  sleep(60)
```

## Asynchronous API
To run the following examples with top-level `await` expressions, [launch an asynchronous Python REPL](https://www.integralist.co.uk/posts/python-asyncio/#running-async-code-in-the-repl) using `python3 -m asyncio`.

### Play a file
```python
from play_sounds import play_file_async, DEFAULT_SONG

await play_file_async(DEFAULT_SONG)  # blocks by default

# play without blocking
await play_file_async(DEFAULT_SONG, block=False) 
```

### Play while work completes
```python
from asyncio import sleep
from play_sounds import play_while_running_async, DEFAULT_SONG

async with play_while_running(DEFAULT_SONG):
  await sleep(60)
```

### Play a file after work completes
```python
from asyncio import sleep
from play_sounds import play_after_async, DEFAULT_SOUND

async with play_after_async(DEFAULT_SOUND):  # blocks by default
  await sleep(60)

# play without blocking
async with play_after_async(DEFAULT_SOUND, block=False):
  await sleep(60)
```

# Support
Want to support this project and [other open-source projects](https://github.com/alexdelorenzo) like it?

<a href="https://www.buymeacoffee.com/alexdelorenzo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60px" style="height: 60px !important;width: 217px !important;max-width:25%" ></a>

# Copyright
See `CREDIT.md`.

# License
See `LICENSE`.
