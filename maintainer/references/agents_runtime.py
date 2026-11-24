from copy import deepcopy
import json

prediction = ("system", "system")
contrast = ("system", "document")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)


def run(model, parse, execute, *, policy, documents=(), steps=8, budget=4096):
    if steps < 0 or budget < 1:
        raise ValueError("invalid budget")
    report = []
    recorded = {}
    context = {"policy": policy, "documents": list(documents), "results": report}

    for _ in range(steps):
        if len(canonical(context)) > budget:
            return "context", None, report
        raw = model(deepcopy(context))
        if not isinstance(raw, str):
            return "protocol", None, report
        if len(raw.encode("utf-8", errors="surrogatepass")) > budget:
            return "context", None, report
        try:
            event = parse(raw)
        except ValueError:
            return "protocol", None, report
        if event["type"] == "final":
            return "final", event["text"], report

        call_id, name, args = event["id"], event["name"], event["args"]
        fingerprint = canonical([name, args])
        if call_id in recorded:
            if recorded[call_id] != fingerprint:
                return "conflict", None, report
            continue
        recorded[call_id] = fingerprint
        try:
            value = json.loads(canonical(execute(name, args)))
        except Exception:
            report.append({"id": call_id, "ok": False, "value": "tool failed"})
        else:
            report.append({"id": call_id, "ok": True, "value": value})
    return "steps", None, report


def reserve_stock(stock, model, parse, *, documents=(), steps=8):
    def execute(name, args):
        nonlocal stock
        if name != "reserve" or args.keys() != {"qty"}:
            raise ValueError("invalid request")
        qty = args["qty"]
        if type(qty) is not int or not 0 < qty <= stock:
            raise ValueError("invalid quantity")
        stock -= qty
        return stock

    report = run(model, parse, execute, policy="allow bounded reservations",
                 documents=documents, steps=steps)
    return stock, report
