

def aeq(*args):
    assert (
        all([_ == args[0] for _ in args]),
        "Arguments are not all equal %s" % str(args)
    )
