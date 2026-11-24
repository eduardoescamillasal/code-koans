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
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    seen: list[str] = []

    async def job() -> None:
        seen.append("ran")
    pending = job()
    try:
        expected: object = __
        t.assertEqual(answers[0] if answers else expected, tuple(seen))
    finally:
        pending.close()


def contrast(t: TestCase, *answers: object) -> None:
    seen: list[str] = []

    async def job() -> None:
        seen.append("ran")

    async def scenario() -> None:
        task = asyncio.create_task(job())
        t.assertEqual(seen, [])
        await task

    asyncio.run(scenario())
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(seen))


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


def practice(t: TestCase, exercise: Exercise) -> None:
    async def immediate(value: int) -> int:
        return value

    result = asyncio.run(exercise.run_jobs([lambda: immediate(8), lambda: immediate(3)], 1))
    t.assertEqual(result, [8, 3])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    # No workers should be needed for empty input.
    t.assertEqual(asyncio.run(exercise.run_jobs([], 3)), [])
    with t.assertRaises(ValueError):
        asyncio.run(exercise.run_jobs([], 0))


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    async def work() -> str:
        return "ok"

    result = asyncio.run(exercise.collect_named({"one": work}, 1))
    t.assertEqual(result, {"one": ("ok", "ok")})
