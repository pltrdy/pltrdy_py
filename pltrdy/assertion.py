

def aeq(*args):
    assert len(args) > 1, "aeq a single element is meaningless"
    assert all([_ == args[0] for _ in args]), (
        "Arguments are not all equal %s" % str(args)
    )


def assert_shapes(*shapes):
    """shapes are iterable of same length
       we assert that for all shape i and dimension j
       shapes[0][j] == shapes[i][j]
    """
    for d, sizes in enumerate(zip(*shapes)):
        try:
            aeq(*sizes)
        except AssertionError as e:
            raise AssertionError("On dimension %d size mismatch: %s"
                                 % (d, str(e))) from e
