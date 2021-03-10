from typing import Callable, Optional, Set
from multiprocessing import Process
from platform import platform
from pathlib import Path
from weakref import finalize as finalizer
from sys import exit
import signal


PLATFORM: str = platform().lower()
_PROCS: Set[Process] = set()


def play_process(
  file: Path,
  target: Callable,
  *args,
  finalize: bool = True,
  running_procs: Optional[Set[Process]] = _PROCS,
  **kwargs,
) -> Process:
  proc = Process(
    target=target,
    args=(file, *args),
    kwargs=kwargs,
    daemon=True
  )

  if finalize:
    finalizer(proc, kill_process, proc=proc, running_procs=running_procs)

  if running_procs is not None:
    running_procs.add(proc)

  proc.start()

  return proc


def kill_process(
  proc: Process,
  running_procs: Optional[Set[Process]] = _PROCS
):
  proc.kill()
  proc.join()

  if running_procs is not None and proc in running_procs:
    running_procs.remove(proc)


def kill_child_procs(signum: int, frame):
  if _PROCS:
    for proc in _PROCS.copy():
      try:
        kill_process(proc)

      except:
        pass

  exit()


def register_handlers():
  signal.signal(signal.SIGTERM, kill_child_procs)
  signal.signal(signal.SIGINT, kill_child_procs)
  signal.signal(signal.SIGSEGV, kill_child_procs)
  signal.signal(signal.SIGABRT, kill_child_procs)
  signal.signal(signal.SIGILL, kill_child_procs)

  if 'windows' not in PLATFORM:
    signal.signal(signal.SIGPIPE, kill_child_procs)
    signal.signal(signal.SIGQUIT, kill_child_procs)
    signal.signal(signal.SIGBUS, kill_child_procs)
    signal.signal(signal.SIGHUP, kill_child_procs)


register_handlers()
