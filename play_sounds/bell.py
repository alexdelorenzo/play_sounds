from contextlib import contextmanager
from typing import ContextManager
from subprocess import run


BELL_CMD = "tput bel"


def bell():
  run(BELL_CMD, shell=True)


@contextmanager
def bell_after(play_bell: bool = True) -> ContextManager:
  try:
    yield

  finally:
    if play_bell:
      bell()
