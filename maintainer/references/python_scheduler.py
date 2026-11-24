import asyncio

prediction = ()
contrast = ("ran",)


async def run_jobs(factories, limit):
    if limit < 1:
        raise ValueError("limit must be positive")
    factories = list(factories)
    work = iter(enumerate(factories))
    results = [None] * len(factories)

    async def worker():
        for index, factory in work:
            results[index] = await factory()

    tasks = [asyncio.create_task(worker()) for _ in range(min(limit, len(results)))]
    try:
        await asyncio.gather(*tasks)
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def collect_named(jobs, limit):
    def wrap(factory):
        async def invoke():
            try:
                return "ok", await factory()
            except Exception as error:
                return "error", type(error).__name__

        return invoke

    results = await run_jobs([wrap(factory) for factory in jobs.values()], limit)
    return dict(zip(jobs, results))
