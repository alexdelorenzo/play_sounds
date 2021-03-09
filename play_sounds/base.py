from contextlib import contextmanager, asynccontextmanager, \
    AbstractContextManager, AbstractAsyncContextManager
from typing import Callable, AsyncContextManager, Any, \
    ContextManager, Awaitable, Optional
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from asyncio.futures import Future
from asyncio import Task, sleep
from contextlib import contextmanager
from dataclasses import dataclass
from platform import platform
from pathlib import Path
import asyncio
import logging
import sys

import asyncbg

from .wrap import to_thread, to_thread_task, finalize_task


BLOCK_WHILE_PLAYING = True
PROCS = 1
DEFAULT_WAIT: float = 0.25


Executor = ProcessPoolExecutor


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


def play_loop(file: Path):
  try:
    while True:
      play_file(file)

  except Exception as e:
    logging.error(f"Error while trying to play {file}: {e}")


def play_process(file: Path, target: Callable = play_loop) -> Process:
  proc = Process(target=target, args=(file,))
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


async def play_file_async(file: Path, block: bool = BLOCK_WHILE_PLAYING):
  try:
    task = await to_thread_task(play_process, file, target=play_file)
    proc = await task

  finally:
    kill_process(proc)


@asynccontextmanager
async def play_while_running_async(file: Path) -> AsyncContextManager[Task]:
  coro = to_thread_task(play_process, file)
  task = asyncio.create_task(coro)

  yield task
  task.cancel()


@asynccontextmanager
async def play_after_async(file: Path, block: bool = False) -> AsyncContextManager[Path]:
  try:
    yield file

  finally:
    if not file:
      return

    task = await to_thread_task(play_file, file, block=block)
    await finalize_task(task)


#async def play_file_async(file: Path, block: bool = BLOCK_WHILE_PLAYING):
  #task = await to_thread_task(play_file, file, block)
  #await finalize_task(task)


@asynccontextmanager
async def play_while_running_async2(file: Path) -> AsyncContextManager[Future]:
  coro = to_thread(play_process, file, target=play_file)

  try:
    proc = await coro
    yield

  finally:
    await to_thread(kill_process, proc)


async def play_file_async2(
  file: Path,
  block: bool = BLOCK_WHILE_PLAYING,
  interval: float = DEFAULT_WAIT
):
  coro = to_thread(play_process, file, target=play_file)

  try:
    proc = await coro

    while proc.is_alive():
      await sleep(interval)

  finally:
    await to_thread(kill_process, proc)


@asynccontextmanager
async def play_after_async2(file: Path) -> AsyncContextManager[Path]:
  try:
    yield file

  finally:
    if file:
      await play_file_async(file)


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
