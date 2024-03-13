# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

from logger import *


# ==================================================================================================
#                                            Point Class
# ==================================================================================================

class Point:

    # ----------------------------------------------------------------------------------------------
    #                                      INITIALIZATION
    # ----------------------------------------------------------------------------------------------

    def __init__(self, curve, x, y):

        self.curve = curve

        if not curve.is_point_on_curve(x,y):
            raise Exception("The point ({},{}) is not on the SECP256K1 curve.".format(x,y))
        else:
            self.x = x
            self.y = y

    # ----------------------------------------------------------------------------------------------
    #                      MATH with Operator Overloading! (lovely isn't it)
    # ----------------------------------------------------------------------------------------------

    def __neg__(self):

        return Point(self.curve, self.x, -self.y)

    def __add__(self, Q):

        if isinstance(Q, Ideal):  # If Q is ideal then the result must be ideal
            return self

        x_1, y_1, x_2, y_2 = self.x, self.y, Q.x, Q.y

        if (x_1, y_1) == (x_2, y_2):  # If the 2 points are the same
            if y_1 == 0:  # If the tangent line to both points is vertical then result is ideal
                return Ideal(self.curve)
            else:  # If the tangent line is not vertical then return the slope (derivative)

                inv = self.inverse(2*y_1)
                # logger.info("2*y_1: {} inv(2*y_1): {}".format(2*y_1,inv))
                m = ( (3 * x_1 * x_1 + self.curve.a) * inv ) % self.curve.p

        else:  # If the 2 points are not the same
            if x_1 == x_2:  # If the line intersecting the 2 points is vertical then result is ideal
                return Ideal(self.curve)
            else:  # If intersecting line is not vertical then return the slope

                inv = self.inverse(x_2-x_1)
                logger.info("x2-x1: {} inv(x2-x1): {}".format(x_2-x_1,inv))
                m = ( (y_2 - y_1) * inv ) % self.curve.p

        # Calculating the 3rd point
        x_3 = ( m * m - x_2 - x_1 ) % self.curve.p
        y_3 = ( m * (x_3 - x_1) + y_1 ) % self.curve.p

        return Point(self.curve, x_3, -y_3)  # Returning reflection of the 3rd point across y-axis

    def __sub__(self, Q):

        return self + -Q

    def __mul__(self, n):

        if not isinstance(n, int):
            raise Exception("Can't scale a point by something which isn't an integer!")
        else:
            if n < 0:
                return -self * -n
            if n == 0:
                return Ideal(self.curve)
            else:
                Q = self
                R = self if n & 1 == 1 else Ideal(self.curve)  # TODO: What is this condition?

                # This will iterate n-1 times
                i = 2
                while i <= n:
                    Q = Q + Q  # Q will double each time this is called

                    if n & i == i: # TODO: What is this condition?
                        # logger.info("i: {}".format(i))
                        # logger.info("Rx: {} Ry: {}".format(R.x,R.y))
                        # logger.info("Qx: {} Qy: {}".format(Q.x,Q.y))
                        R = Q + R  # R is accumulating summation of Q

                    i = i << 1

                return R

    def __rmul__(self, n):

        return self * n

    def inverse(self,i):

        x, y, d = self.extendedEuclideanAlgorithm(i, self.curve.p)
        return x

    def extendedEuclideanAlgorithm(self, a, b):

        if abs(b) > abs(a):
            (x, y, d) = self.extendedEuclideanAlgorithm(b, a)
            return (y, x, d)

        if abs(b) == 0:
            return (1, 0, a)

        x1, x2, y1, y2 = 0, 1, 1, 0
        while abs(b) > 0:
            q, r = divmod(a, b)
            x = x2 - q * x1
            y = y2 - q * y1
            a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

        return (x2, y2, a)


# ==================================================================================================
#                                         Ideal Point Class
# ==================================================================================================

class Ideal(Point):

    # ----------------------------------------------------------------------------------------------
    #                                      INITIALIZATION
    # ----------------------------------------------------------------------------------------------

    def __init__(self, curve):

        self.curve = curve

    def __str__(self):

        return "Ideal"

    def __neg__(self):

        return self

    def __add__(self, Q):

        return Q

    def __sub__(self, Q):

        return self + -Q

    def __mul__(self, n):

        if not isinstance(n, int):
            raise Exception("Can't scale a point by something which isn't an int!")
        else:
            return self