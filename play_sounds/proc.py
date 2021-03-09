from typing import Callable, Optional, Set
from multiprocessing import Process
from pathlib import Path

import signal


_PIDS: Set[Process] = set()


def kill_child_procs(signum: int, frame):
  for proc in _PIDS.copy():
    try:
      kill_process(proc)

    except:
      pass


def play_process(
  file: Path,
  target: Callable,
  running_procs: Optional[Set[Process]] = _PIDS
) -> Process:
  proc = Process(target=target, args=(file,))
  proc.start()

  if running_procs is not None:
    running_procs.add(proc)

  return proc


def kill_process(
  proc: Process,
  running_procs: Optional[Set[Process]] = _PIDS
):
  proc.kill()
  proc.join()

  if running_procs is not None and proc in running_procs:
    running_procs.remove(proc)


signal.signal(signal.SIGTERM, kill_child_procs)
signal.signal(signal.SIGINT, kill_child_procs)
signal.signal(signal.SIGPIPE, kill_child_procs)
signal.signal(signal.SIGSEGV, kill_child_procs)
signal.signal(signal.SIGABRT, kill_child_procs)
signal.signal(signal.SIGILL, kill_child_procs)
