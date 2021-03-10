from typing import Callable, Any, Awaitable
from asyncio import Task, create_task
from functools import wraps, partial
import contextvars

try:
  from asyncio import to_thread

except ImportError:
  from asyncio import get_running_loop

  async def to_thread(func: Callable, /, *args, **kwargs) -> Any:
    loop = get_running_loop()
    ctx = contextvars.copy_context()
    func_call = partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


async def to_thread_task(func: Callable, *args, **kwargs) -> Task:
  coro = to_thread(func, *args, **kwargs)
  return create_task(coro)


async def finalize_task(task: Task) -> Any:
  try:
    return await task

  finally:
    if not task.cancelled():
      task.cancel()


CoroutineResult = Awaitable[Any]
CoroutineFunction = Callable[..., CoroutineResult]
CoroutineMethod = Callable[..., CoroutineResult]


def func_as_method_coro(func: Callable) -> CoroutineMethod:
  @wraps(func)
  async def method(self, *args, **kwargs) -> Any:
    return await to_thread(func, *args, **kwargs)

  return method


def coro_as_method_coro(coro: CoroutineFunction) -> CoroutineMethod:
  @wraps(coro)
  async def method(self, *args, **kwargs) -> Any:
    return await coro(*args, **kwargs)

  return method
