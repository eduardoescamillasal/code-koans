import asyncio


async def serial(factories, limit):
    return [await factory() for factory in factories]


async def unchecked(factories, limit):
    return await asyncio.gather(*(factory() for factory in factories))


async def detach(factories, limit):
    await asyncio.shield(unchecked(factories, limit))

async def collect_empty(jobs, limit):
    return {}


CASES = {
    "predict": {"prediction": ("ran",)},
    "contrast": {"contrast": ()},
    "implement": {"run_jobs": serial},
    "break_cases": {"run_jobs": unchecked},
    "transfer": {"collect_named": collect_empty},
}
