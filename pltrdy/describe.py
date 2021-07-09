import sys


def has_module(module_name):
    return module_name in sys.modules


def tab_print(*args, sep="        ", lvl=0, **kwargs):
    args = list(args)
    if lvl > 0:
        tabs = sep * lvl
        args[0] = tabs + args[0]
    print(*args, **kwargs)


def describe(o, max_elements=20, max_depth=100, depth=1):
    next_kwargs = {
        "max_elements": max_elements,
        "max_depth": (max_depth - 1),
        "depth": (depth + 1),
    }

    if max_depth == 0:
        print("(max depth reached)")
        return

    if isinstance(o, dict):
        keys = o.keys()
        n = len(o)
        print("Dict (len: %d)" % n)
        if n <= max_elements:
            keys = sorted(o.keys())
            for k in keys:
                v = o[k]
                tab_print("%s:" % k, lvl=depth, end=" ")
                describe(v, **next_kwargs)
    elif isinstance(o, list):
        n = len(o)
        print("List (len: %d)" % n)
        if n <= max_elements:
            for i, v in enumerate(o):
                tab_print("#%d:" % i, lvl=depth, end=" ")
                describe(v, **next_kwargs)
    elif has_module("torch") and isinstance(o, torch.Tensor):
        tensor_shape = str(list(o.size()))
        tensor_type = str(o.type())

        print("%s: %s" % (tensor_type, tensor_shape))
    else:
        print(repr(o))
