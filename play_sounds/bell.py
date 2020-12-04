from contextlib import contextmanager
from typing import ContextManager


BELL_CHAR = '\a'
NO_NEWLINE = ''


def bell():
  print(BELL_CHAR, end=NO_NEWLINE)


@contextmanager
def bell_after(play_bell: bool = True) -> ContextManager:
  try:
    yield

  finally:
    if play_bell:
      bell()
