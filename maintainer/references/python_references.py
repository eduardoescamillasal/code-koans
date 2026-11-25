prediction = (True, 2)
contrast = (False, 1, 8)


def snapshot(root):
    memo = {}

    def clone(value):
        if type(value) not in (dict, list):
            return value
        if id(value) in memo:
            return memo[id(value)]
        result = {} if type(value) is dict else []
        memo[id(value)] = result
        if type(value) is dict:
            result.update((key, clone(item)) for key, item in value.items())
        else:
            result.extend(clone(item) for item in value)
        return result

    return clone(root)
