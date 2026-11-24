prediction = True
contrast = False


def dispatch(registry, allowed, name, args):
    if name not in allowed or name not in registry:
        raise PermissionError("tool unavailable")
    schema, tool = registry[name]
    if not isinstance(args, dict) or args.keys() != schema.keys():
        raise ValueError("argument keys do not match schema")
    if any(type(args[key]) is not expected for key, expected in schema.items()):
        raise ValueError("argument type does not match schema")
    return tool(**args)


def preview_batch(registry, requests):
    results = []
    for name, args in requests:
        try:
            value = dispatch(registry, {"preview"}, name, args)
        except (PermissionError, ValueError):
            results.append(("rejected", None))
        else:
            results.append(("ok", value))
    return results
