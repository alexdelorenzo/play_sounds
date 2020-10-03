from typing import Optional, ContextManager
from multiprocessing import Process
from contextlib import contextmanager
from platform import platform
from sys import stderr
from pathlib import Path


BLOCK_WHILE_PLAYING = True


def get_assets_dir() -> Path:
  return Path(__file__).parent / 'assets'


DEFAULT_ASSETS = get_assets_dir()
DEFAULT_SONG = DEFAULT_ASSETS / 'song.mp3'
DEFAULT_SOUND = DEFAULT_ASSETS / 'ding.ogg'

PLATFORM = platform().lower()


if 'windows' in PLATFORM or 'nt' in PLATFORM:
  from playsound import playsound

  def play_file(file: Path, block: bool = BLOCK_WHILE_PLAYING):
    playsound(str(file.absolute()))

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


@contextmanager
def play_after(file: Path) -> ContextManager[Path]:
  try:
    yield file

  finally:
    if file:
      play_file(file)

