# ==================================================================================================
#                                            Point Class
# ==================================================================================================

class Point:

    """
    Immutable Elliptic Curve Point.

    A Point support the following operator:

        - `+` : Point Addition, with automatic doubling support.
        - `*` : Scalar multiplication, can write as k*P or P*k, with P :class:Point and  k :class:int
        - `==`: Point comparison

    Attributes:
        x (int)       : Affine x coordinate
        y (int)       : Affine y coordinate
        curve (Curve) : Curve on which the point is define


    Args:
        x (int) :     x coordinate
        y (int) :     y coordinate
        check (bool): if True enforce x,y is on curve

    Raises:
        ECPyException : if check=True and x,y is not on curve
    """

    __slots__ = '_x', '_y', '_curve'

    def __init__(self, x, y, curve, check=True):
        self._curve = curve
        if x:
            self._x = int(x)
        if y:
            self._y = int(y)
        if not x or not y:
            check = False
        if check and not curve.is_on_curve(self):
            raise("Point not on curve")

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def curve(self):
        return self._curve

    def __neg__(self):
        curve = self.curve
        return Point(self.x, curve.field - self.y, curve)

    def __add__(self, Q):
        if isinstance(Q, Point):
            return self.curve.add_point(self, Q)
        raise NotImplementedError('__add__: type not supported: %s' % type(Q))

    def __sub__(self, Q):
        if isinstance(Q, Point):
            return self.curve.sub_point(self, Q)
        raise NotImplementedError('__sub__: type not supported: %s' % type(Q))

    def __mul__(self, scal):
        if isinstance(scal, int):
            return self.curve.mul_point(scal, self)
        raise NotImplementedError('__mul__: type not supported: %s' % type(scal))

    def __rmul__(self, scal):
        return self.__mul__(scal)

    def __eq__(self, Q):
        if isinstance(Q, Point):
            return ((self._curve.name == Q._curve.name or
                     self._curve.name == None or
                     Q._curve.name == None) and
                    self._x == Q._x and
                    self._y == Q._y)
        raise NotImplementedError('eq: type not supported: %s' % (type(Q)))

    def __str__(self):
        return "x: %x\n  y: %x" % (self._x, self._y)

    def neg(self):
        return self.__neg__()

    def add(self, Q):
        return self.__add__(Q)

    def sub(self, Q):
        return self.__sub__(Q)

    def mul(self, k):
        return self.__mul__(k)

    def eq(self, Q):
        return self.__eq__(Q)