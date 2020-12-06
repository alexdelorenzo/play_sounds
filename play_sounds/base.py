from contextlib import contextmanager, asynccontextmanager, \
    AbstractContextManager, AbstractAsyncContextManager
from typing import Callable, AsyncContextManager, Any, \
    ContextManager, Awaitable, Optional
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, Future
from contextlib import contextmanager
from dataclasses import dataclass
from platform import platform
from sys import stderr
from pathlib import Path
import asyncio
import logging


BLOCK_WHILE_PLAYING = True
PROCS = 1


def get_assets_dir() -> Path:
  filename = __loader__.get_filename()
  return Path(filename).parent / 'assets'


DEFAULT_ASSETS = get_assets_dir()
DEFAULT_SONG = DEFAULT_ASSETS / 'song.mp3'
DEFAULT_SOUND = DEFAULT_ASSETS / 'ding.mp3'

PLATFORM = platform().lower()


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


def play_loop(file: Path):
  try:
    while True:
      play_file(file)

  except Exception as e:
    stderr.write(f"Error while trying to play {file}: {e}\n")


def play_process(file: Path) -> Process:
  proc = Process(target=play_loop, args=(file,))
  proc.start()

  return proc


def kill_process(proc: Process):
  proc.kill()
  proc.join()


@contextmanager
def play_while_running(file: Path) -> ContextManager[Process]:
  proc = play_process(file)

  try:
    yield proc

  finally:
    kill_process(proc)


@asynccontextmanager
async def play_while_running_async(file: Path) -> AsyncContextManager[Future]:
  executor = ProcessPoolExecutor(max_workers=PROCS)
  loop = asyncio.get_event_loop()
  future = loop.run_in_executor(executor, play_file, file)

  try:
    yield future

  finally:
    executor.shutdown(wait=False)


@contextmanager
def play_after(
  file: Optional[Path], 
  block: bool = BLOCK_WHILE_PLAYING
) -> ContextManager[Path]:
  try:
    yield file

  finally:
    if file:
      play_file(file, block)


@asynccontextmanager
async def play_after_async(file: Path) -> AsyncContextManager[Path]:
  try:
    yield file

  finally:
    if file:
      play_file(file, block=False)


#@dataclass
#class play_sound(AbstractContextManager, AbstractAsyncContextManager):
    #def __call__(self, func: Callable) -> Callable:
        #with play_while_running_sync(file) as proc:
          #return func
        #pass

    #def __enter__(self) -> ContextManager[Limiter]:
        #with limit_rate(self.limiter, self.bucket, self.consume) as limiter:
            #return limiter
        #pass

    #def __exit__(self, *args):
        #pass

    #async def __aenter__(self) -> Awaitable[AsyncContextManager[Limiter]]:
        #async with async_limit_rate(self.limiter, self.bucket, self.consume) as limiter:
            #return limiter
        #pass

    #async def __aexit__(self, *args):
        #pass
