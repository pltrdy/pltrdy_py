import numpy as np


def equal(x, y, almost=False, epsilon=1e-7):
    if not almost:
        return x == y
    else:
        try:
            return (y - epsilon) <= x <= (y + epsilon)
        except TypeError:
            raise ValueError(
                "Invalid types (%s, %s) for almost comparison"
                % (type(x), type(y)))


def aeq(*args, almost=False, epsilon=1e-7, msg=None):
    assert len(args) > 1, "aeq a single element is meaningless"
    if msg is not None:
        msg = "[%s] " % msg
    else:
        msg = ""
    assert all([
        equal(_,
              args[0],
              almost=almost,
              epsilon=epsilon)
        for _ in args
    ]), (
        "%sArguments are not all equal %s" % (msg, str(args))
    )


def aaeq(*args, almost=False, epsilon=1e-7, msg=None):
    assert len(args) > 1, "aaeq a single element is meaningless, use aeq"
    if msg is not None:
        msg = "[%s] " % msg
    else:
        msg = ""

    for i, args_i in enumerate(zip(*args)):
        assert all([
            equal(_,
                  args_i[0],
                  almost=almost,
                  epsilon=epsilon)
            for _ in args_i[1:]]
        ), (
            "%sArguments are not all equal for element %d, %s."
            % (msgi, str(args_i))
        )


def assert_shapes(*shapes):
    """shapes are iterable of same length
       we assert that for all shape i and dimension j
       shapes[0][j] == shapes[i][j]
    """
    def fix_shape(shape):
        if isinstance(shape, np.ndarray):
            shape = shape.shape
        return shape
    shapes = [fix_shape(s) for s in shapes]

    for i, sizes in enumerate(zip(*shapes)):
        try:
            aeq(*sizes)
        except AssertionError as e:
            shapes_str = ", ".join([
                "[%s]" % (", ".join([
                    str(d) if j != i else "*%d*" % d
                    for j, d in enumerate(s)
                ])) for s in shapes
            ])
            raise AssertionError("Size mismatch on dimension %d: %s"
                                 % (i, shapes_str)) from e
