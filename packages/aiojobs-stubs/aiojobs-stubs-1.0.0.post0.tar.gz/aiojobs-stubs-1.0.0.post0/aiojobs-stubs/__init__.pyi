from typing import Any, Awaitable, Callable, Dict, Generic, Optional, TypeVar

from aiojobs_protocols import SchedulerProtocol

_T = TypeVar('_T')
_Context = Dict[str, Any]
_ExceptionHandler = Callable[[SchedulerProtocol, _Context], None]


class Job(Generic[_T]):
    active: bool
    pending: bool
    closed: bool
    async def wait(self, *, timeout: Optional[float] = None) -> _T: ...
    async def close(self, *, timeout: Optional[float] = None) -> None: ...


class Scheduler:
    limit: int
    pending_limit: int
    close_timeout: float
    active_count: int
    pending_count: int
    closed: bool
    exception_handler: _ExceptionHandler
    async def spawn(self, coro: Awaitable[_T]) -> Job[_T]: ...
    async def close(self) -> None: ...
    def call_exception_handler(self, context: _Context) -> None: ...


async def create_scheduler(
    close_timeout: float = ...,
    limit: int = ...,
    pending_limit: int = ...,
    exception_handler: Optional[_ExceptionHandler] = None
) -> Scheduler: ...
