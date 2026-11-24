import asyncio


async def serial(factories, limit):
    return [await factory() for factory in factories]


async def unchecked(factories, limit):
    return await asyncio.gather(*(factory() for factory in factories))


async def detach(factories, limit):
    await asyncio.shield(unchecked(factories, limit))

import asyncio


def predict(t, s):
    seen = []
    async def job():
        seen.append("ran")
    pending = job()
    try:
        t.assertEqual(s.prediction, tuple(seen))
    finally:
        pending.close()


def contrast(t, s):
    seen = []
    async def job():
        seen.append("ran")
    asyncio.run(job())
    t.assertEqual(s.contrast, tuple(seen))


def implement(t, s):
    async def scenario():
        active = peak = 0
        async def job(value):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0)
            active -= 1
            return value
        result = await s.run_jobs([lambda n=n: job(n) for n in range(5)], 2)
        t.assertEqual(result, list(range(5)))
        t.assertEqual(peak, 2)
    asyncio.run(scenario())


def break_cases(t, s):
    async def scenario():
        with t.assertRaises(ValueError):
            await s.run_jobs([], 0)
        started, cleaned = asyncio.Event(), asyncio.Event()
        async def pending():
            try:
                started.set()
                await asyncio.Future()
            finally:
                cleaned.set()
        async def fail():
            await started.wait()
            raise LookupError("worker failed")
        with t.assertRaisesRegex(LookupError, "worker failed"):
            await asyncio.wait_for(s.run_jobs([pending, fail], 2), 1)
        t.assertTrue(cleaned.is_set())
    asyncio.run(scenario())


def transfer(t, s):
    async def scenario():
        started, failed = asyncio.Event(), asyncio.Event()
        async def slow():
            started.set()
            await failed.wait()
            return 7
        async def bad():
            await started.wait()
            failed.set()
            raise LookupError("independent failure")
        async def last():
            return 3
        result = await asyncio.wait_for(s.collect_named({"a": slow, "b": bad, "c": last}, 2), 2)
        t.assertEqual(list(result.items()), [("a", ("ok", 7)), ("b", ("error", "LookupError")),
                                            ("c", ("ok", 3))])
    asyncio.run(scenario())
