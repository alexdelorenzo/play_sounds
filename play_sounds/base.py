from contextlib import contextmanager, asynccontextmanager, \
    AbstractContextManager, AbstractAsyncContextManager
from typing import Callable, AsyncContextManager, Any, \
    ContextManager, Awaitable, Optional, Set
from multiprocessing import Process
from platform import platform
from pathlib import Path
from asyncio import sleep
import logging
import sys

from .wrap import to_thread
from .proc import play_process, kill_process


BLOCK_WHILE_PLAYING: bool = True
DEFAULT_WAIT: float = 0.25


def get_assets_dir() -> Path:
  filename = __loader__.get_filename()
  return Path(filename).parent / 'assets'


DEFAULT_ASSETS = get_assets_dir()
DEFAULT_SONG = DEFAULT_ASSETS / 'song.mp3'
DEFAULT_SOUND = DEFAULT_ASSETS / 'ding.mp3'

PLATFORM = platform().lower()
MAJOR, MINOR, *_ = sys.version_info


if 'windows' in PLATFORM or 'nt' in PLATFORM:
  from playsound import playsound

  def play_file(file: Path, block: bool = BLOCK_WHILE_PLAYING):
    filename = str(file.absolute())
    playsound(filename, block=block)

    if not block:
      logging.warning("Playback must block on Windows.")

else:
  from boombox import BoomBox

  def play_file(file: Path, block: bool = BLOCK_WHILE_PLAYING):
    player = BoomBox(file, wait=block)
    player.play()


def play_loop(file: Path, block: bool = True):
  try:
    while True:
      play_file(file, block)

  except Exception as e:
    logging.error(f"Error while trying to play {file}: {e}")


@contextmanager
def play_while_running(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING,
  loop: bool = True
) -> ContextManager[Process]:
  play_func = play_loop if loop else play_file
  proc = play_process(file, target=play_func, block=block)

  try:
    yield proc

  finally:
    kill_process(proc)


@contextmanager
def play_after(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING
) -> ContextManager[Path]:
  try:
    yield file

  finally:
    play_file(file, block)


async def play_file_async(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING,
  loop: bool = False,
  interval: float = DEFAULT_WAIT,
):
  play_func = play_loop if loop else play_file
  proc = None
 
  try:
    proc = await to_thread(play_process, file, block=block, target=play_func)

    while proc.is_alive():
      await sleep(interval)

  finally:
    if proc:
      await to_thread(kill_process, proc)


@asynccontextmanager
async def play_while_running_async(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING,
  loop: bool = True
) -> AsyncContextManager[Process]:
  play_func = play_loop if loop else play_file

  try:
    proc = await to_thread(play_process, file, block=block, target=play_func)
    yield proc

  finally:
    await to_thread(kill_process, proc)


@asynccontextmanager
async def play_after_async(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING,
  loop: bool = False,
  interval: float = DEFAULT_WAIT,
) -> AsyncContextManager[Path]:
  try:
    yield file

  finally:
    await play_file_async(file, block, loop, interval)


#@dataclass
#class play_sound(AbstractContextManager, AbstractAsyncContextManager):
  #def __call__(self, func: Callable) -> Callable:
    #if iscoroutinefunction(func):
      #@wraps(func)
      #async def new_coro(*args, **kwargs) -> Awaitable[Any]:
        #async with self as proc:
          #pass
    #with play_while_running(file) as proc:
      #return func

  #def __enter__(self) -> ContextManager[Process]:
    #with play_while_running(file) as proc:
      #return proc

  #def __exit__(self, *args):
    #pass

  #async def __aenter__(self) -> Awaitable[AsyncContextManager[Process]]:
    #with play_while_running_async(file) as proc:
      #return proc


  #async def __aexit__(self, *args):
    #pass
