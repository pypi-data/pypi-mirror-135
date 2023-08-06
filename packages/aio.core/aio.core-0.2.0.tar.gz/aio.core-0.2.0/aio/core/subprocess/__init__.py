"""aio.core.subprocess."""

from .async_subprocess import AsyncSubprocess


run = AsyncSubprocess.run
parallel = AsyncSubprocess.parallel


__all__ = ("run", "parallel", "AsyncSubprocess")
