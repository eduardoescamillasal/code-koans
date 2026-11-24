from heapq import heapify, heappop, heappush

prediction = ("compile",)
contrast = ()


def plan(dependencies):
    downstream = {job: [] for job in dependencies}
    remaining = {}
    for job, prerequisites in dependencies.items():
        parents = set(prerequisites)
        remaining[job] = len(parents)
        for parent in parents:
            if parent not in downstream:
                raise ValueError("missing prerequisite")
            downstream[parent].append(job)
    ready = [job for job, count in remaining.items() if count == 0]
    heapify(ready)
    order = []
    while ready:
        parent = heappop(ready)
        order.append(parent)
        for job in downstream[parent]:
            remaining[job] -= 1
            if remaining[job] == 0:
                heappush(ready, job)
    if len(order) != len(remaining):
        raise ValueError("cyclic dependencies")
    return order


def rebuild(dependencies, changed):
    graph = {job: set(parents) for job, parents in dependencies.items()}
    if changed not in graph:
        raise ValueError("unknown job")
    affected = {changed}
    ordered = []
    for job in plan(graph):
        if job in affected or graph[job] & affected:
            affected.add(job)
            ordered.append(job)
    return ordered
