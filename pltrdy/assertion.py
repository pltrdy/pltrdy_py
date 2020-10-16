import numpy as np


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
