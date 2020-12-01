from contextlib import contextmanager
from typing import ContextManager


BELL_CMD = "tput bel"
BELL_CHAR = '\a'


def bell():
  print(BELL_CHAR, end='')


@contextmanager
def bell_after(play_bell: bool = True) -> ContextManager:
  try:
    yield

  finally:
    if play_bell:
      bell()
