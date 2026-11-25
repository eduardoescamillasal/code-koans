"""Reason about calling versus awaiting a coroutine.
Implement async run_jobs(factories, limit). Invoke each zero-argument async
factory at most once, limit active jobs and preserve input order in results.
Reject a nonpositive limit, propagate the original error, cancel and drain
siblings on failure or caller cancellation. Finite inputs are supported.

For transfer, collect named independent jobs as a dict in input iteration order.
Store ("ok", value) for success or ("error", exception type name) for an
ordinary job failure. Keep the same concurrency cap and caller cancellation
behavior. Jobs is an insertion-ordered mapping from name to async factory.
"""

import asyncio
from collections.abc import Awaitable, Callable, Iterable, Mapping
from typing import Literal, TypeVar, cast

from koans import Koan, __, todo


class AboutAsyncScheduling(Koan):
    def test_creating_a_coroutine_does_not_run_it(self) -> None:
        seen: list[str] = []

        async def job() -> None:
            seen.append("ran")
        pending = job()
        try:
            self.assertEqual(__, tuple(seen))
        finally:
            pending.close()

    def test_awaiting_a_task_observes_its_work(self) -> None:
        seen: list[str] = []

        async def job() -> None:
            seen.append("ran")

        async def scenario() -> None:
            task = asyncio.create_task(job())
            self.assertEqual(seen, [])
            await task

        asyncio.run(scenario())
        self.assertEqual(__, tuple(seen))

    def test_gather_preserves_input_order_after_out_of_order_completion(self) -> None:
        async def scenario() -> tuple[list[str], list[str]]:
            ready = asyncio.Event()
            finished: list[str] = []

            async def first() -> str:
                await ready.wait()
                finished.append("first")
                return "first"

            async def second() -> str:
                finished.append("second")
                ready.set()
                return "second"

            ordered = await asyncio.gather(first(), second())
            return finished, ordered

        finished, ordered = asyncio.run(scenario())
        self.assertEqual(__, finished)
        self.assertEqual(__, ordered)

    def test_cancelling_a_running_coroutine_executes_finally(self) -> None:
        async def scenario() -> list[str]:
            started = asyncio.Event()
            seen: list[str] = []

            async def worker() -> None:
                try:
                    started.set()
                    await asyncio.Future()
                finally:
                    seen.append("cleanup")

            task = asyncio.create_task(worker())
            await started.wait()
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                seen.append("cancelled")
            return seen

        self.assertEqual(__, asyncio.run(scenario()))

    def test_gather_can_report_an_error_without_losing_other_results(self) -> None:
        async def fail() -> int:
            raise ValueError("missing input")

        async def continue_work() -> int:
            return 7

        async def scenario() -> list[int | BaseException]:
            return await asyncio.gather(fail(), continue_work(), return_exceptions=True)

        first, second = asyncio.run(scenario())
        self.assertEqual(__, type(first).__name__)
        self.assertEqual(__, second)


T = TypeVar("T")
Factory = Callable[[], Awaitable[T]]
Outcome = tuple[Literal["ok"], T] | tuple[Literal["error"], str]


async def run_jobs(factories: Iterable[Factory[T]], limit: int) -> list[T]:
    if limit < 1:
        raise ValueError("limit must be positive")
    factories = list(factories)
    work = iter(enumerate(factories))
    results: list[T | None] = [None] * len(factories)

    async def worker() -> None:
        # Each worker takes the next unclaimed pair before its first await.
        todo("run jobs from the shared iterator and place results by input index")

    # Start no more than limit workers. Await all of them. On exit, cancel
    # unfinished workers and await their cleanup, preserving the original error.
    todo("start, await, and drain the workers")
    return cast(list[T], results)


async def collect_named(jobs: Mapping[str, Factory[T]], limit: int) -> dict[str, Outcome[T]]:
    def wrap(factory: Factory[T]) -> Factory[Outcome[T]]:
        async def attempt() -> Outcome[T]:
            # Turn ordinary exceptions into outcomes, leaving cancellation alone.
            todo("return the job's success or error outcome")
        return attempt

    todo("schedule wrapped jobs and associate each outcome with its name")
