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

from koans import __

prediction = __
contrast = __

async def run_jobs(factories, limit):
    raise AssertionError("Implement scheduler")


async def collect_named(jobs, limit):
    raise AssertionError("Implement collect_named")
