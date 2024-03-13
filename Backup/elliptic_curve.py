# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import math
import numpy as np
import pandas as pd
import fractions


# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

from plotter import plotter
from logger import *
from ec_point import *


# ==================================================================================================
#                                        Elliptic Curve Class
# ==================================================================================================

class Elliptic_Curve:

    # ----------------------------------------------------------------------------------------------
    #                                      INITIALIZATION
    # ----------------------------------------------------------------------------------------------

    def __init__(self,a=0,b=7,SECP256K1=True):

        # a,b - are parameters used in the elliptic curve equation y^2 = x^3 + a*x + b
        # G   - is the base point (or generator point) consisting of Gx,Gy
        # n   - is the curve group order (a prime number) and is the number of possible points you
        #       can generate through the multiplication of G
        # p   - is the finite field specifier
        # h   - is the co-factor
        # bl  - bit length

        self.a = a
        self.b = b

        if SECP256K1 == True:

            self.p  = 2 ** 256 - 2 ** 32 - 977
            self.n  = 115792089237316195423570985008687907852837564279074904382605163141518161494337
            # G (compressed)   02 79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
            # G (uncompressed) 04 79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
            self.Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
            self.Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
            self.G  = (self.Gx, self.Gy)
            self.h  = 1
            self.bl = 256

    # ----------------------------------------------------------------------------------------------
    #                                           MATH
    # ----------------------------------------------------------------------------------------------

    def calculate_discriminant(self):

        self.discriminant = -16 * (4 * self.a * self.a * self.a + 27 * self.b * self.b)

    def compute_y(self, x):

        # TODO: Tonelli–Shanks algorithm
        y = int(math.sqrt(int( x * x * x + self.a * x + self.b ) % self.p))
        print("x: {}, y: {}".format(x,y))

        return (y,-y)

    def inverse(self,i):

        x, y, d = self.extendedEuclideanAlgorithm(i, self.p)
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

        logger.info("inv(a mod b): {}, inv(b mod a): {}, gcd(a,b): {}".format(x2,y2,a))

        return (x2, y2, a)

    # ----------------------------------------------------------------------------------------------
    #                                        VALIDATING
    # ----------------------------------------------------------------------------------------------

    def is_smooth(self):

        self.calculate_discriminant()
        return self.discriminant != 0

    def is_point_on_curve(self,x,y):

        # logger.info(" int(y*y) mod p: {}".format( int(y*y) % self. p ))
        # logger.info(" int(x^3+7) mod p: {}".format( int(x*x*x + self.a*x + self.b) % self.p ))

        return ( int(y * y) % self.p ) == ( int( x * x * x + self.a * x + self.b ) % self.p )

    def __str__(self):
        return 'y^2 = x^3 + %Gx + %G' % (self.a, self.b)

    # ----------------------------------------------------------------------------------------------
    #                                         PLOTTING
    # ----------------------------------------------------------------------------------------------

    def plot_curve(self,x_end=10,name='SECP256K1'):

        # Creating a sample DF
        # ------------------------------------------------------------------------------------------
        x_list = [x * 0.1 for x in range(-20, x_end*10)]

        data = []
        for x in x_list:
            try:
                y = self.compute_y(x)
                data.append([x, y[0]])
                data.append([x, y[1]])
                logger.debug("{} {} ".format(x, y[0], y[1]))
            except:  # Ignoring where y is non-existent
                pass

        df = pd.DataFrame(data, columns=['x', 'y'])

        # Plotting
        # ------------------------------------------------------------------------------------------
        plot = plotter(type='SCATTER', length_inch=5, width_inch=5)
        plot.set_resolution(resolution=480)

        plot.set_data(data=df,
                      x_signal='x',
                      y_signals=['y'],
                      axes=[0],
                      zorder=[0],
                      legends=['y'],
                      dashes=[''],
                      trendlines=[False])

        plot.populate()

        plot.set_axis_label(0, 'x', 'x', 'black')
        plot.set_axis_label(0, 'y', 'y', 'black')

        plot.set_title('SECP256K1')

        plot.disable_legend()

        plot.save_plot(dir=r'C:\Users\anagarwal\Desktop\ECC', file_name='{}'.format(name))

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
                # TODO: Should it be converted to int before modulus here? Nope. (y2-y1)/(x2−x1) mod p is not doing a division but multiplying by the inverse of (x2−x1) in Zp

                inv = self.curve.inverse(2*y_1)
                # logger.info("2*y_1: {} inv(2*y_1): {}".format(2*y_1,inv))
                m = ( (3 * x_1 * x_1 + self.curve.a) * inv ) % self.curve.p

        else:  # If the 2 points are not the same
            if x_1 == x_2:  # If the line intersecting the 2 points is vertical then result is ideal
                return Ideal(self.curve)
            else:  # If intersecting line is not vertical then return the slope
                # TODO: Should it be converted to int before modulus here? Nope. (y2-y1)/(x2−x1) mod p is not doing a division but multiplying by the inverse of (x2−x1) in Zp

                inv = self.curve.inverse(x_2-x_1)
                # logger.info("x2-x1: {} inv(x2-x1): {}".format(x_2-x_1,inv))
                if (x_2-x_1) < 0:
                    # This propagates denominator's negative to numerator, and makes addition commutative
                    m = (-(y_2 - y_1) * inv) % self.curve.p
                else:
                    m = ((y_2 - y_1) * inv) % self.curve.p

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

                if n & 1 == 1:
                    R = self
                else:
                    R = Ideal(self.curve)  # TODO: What is this condition?

                # This will iterate n-1 times
                i = 2
                while i <= n:
                    logger.info("i: {}".format(i))
                    Q = Q + Q  # Q will double each time this is called

                    if n & i == i: # TODO: What is this condition?
                        R = Q + R  # R is accumulating summation of Q

                    i = i << 1

                return R

    def __rmul__(self, n):

        return self * n


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

# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)


    # Plotting the curve for reference
    # ----------------------------------------------------------------------------------------------

    # curve = Elliptic_Curve()
    # curve.plot_curve(x_end = 10)


    # Some addition tests
    # ----------------------------------------------------------------------------------------------

    curve = Elliptic_Curve()
    P = Point(curve, curve.Gx, curve.Gy)
    Q = Point(curve, curve.Gx, curve.Gy)

    logger.info("P+Q = ({},{})".format((P + Q).x, (P + Q).y))
    logger.info("Q+P = ({},{})".format((Q + P).x, (Q + P).y))
    logger.info("Q+Q = {}".format((Q + Q).x,(Q+Q).y))
    logger.info("P+P+P = ({},{})".format((P + P).x, (P + P).y))
    logger.info("P+P = ({},{})".format((P + P + P).x, (P + P + P).y))
    logger.info("5*P = ({},{})".format((5*P).x,(5*P).y))
    logger.info("Q-3*P = ({},{})".format((Q-3*P).x, (Q-3*P).y))
    print(curve.is_point_on_curve(curve.Gx,curve.Gy))

    for x in range(-1,1000000):
        for y in range(-1000000,1000000):
            # print("Trying x = {}".format(x))
            try:
                # P = Point(curve,x,curve.compute_y(x)[0])
                if curve.is_point_on_curve(x,y):
                    print("{} {} {}".format(x,y,curve.is_point_on_curve(x,y)))
            except:
                pass
    # Q = Point(curve,curve.Gx,curve.Gy)

    # logger.info("P+Q = ({},{})".format((P + Q).x, (P + Q).y))
    # logger.info("Q+P = ({},{})".format((Q + P).x, (Q + P).y))
    # logger.info("Q+Q = {}".format(Q + Q))
    # logger.info("P+P = ({},{})".format((P + P).x, (P + P).y))
    # logger.info("P+P+P = ({},{})".format((P + P + P).x, (P + P + P).y))
    # logger.info("5*P = ({},{})".format((5*P).x,(5*P).y))
    # logger.info("Q-3*P = ({},{})".format((Q-3*P).x, (Q-3*P).y))
    # # logger.info("P+P+P = ({},{})".format((P + P + P).x, (P + P + P).y))


    # Some addition, subtraction and multiplication tests
    # ----------------------------------------------------------------------------------------------

    # frac = fractions.Fraction
    #
    # curve = Elliptic_Curve(a=frac(-2), b=frac(4))
    # P = Point(curve, frac(3), frac(5))
    # Q = Point(curve, frac(-2), frac(0))
    #
    # logger.info("P-Q = ({},{})".format((P - Q).x, (P - Q).y))
    # logger.info("P+P+P+P+P = ({},{})".format((P + P + P + P + P).x, (P - Q).y))
    # logger.info("5*P = ({},{})".format((5*P).x,(5*P).y))
    # logger.info("Q-3*P = ({},{})".format((Q-3*P).x, (Q-3*P).y))
    # logger.info("-20*P = ({},{})".format((-20 * P).x, (-20 * P).y))


    # Testing with finite fields
    # ----------------------------------------------------------------------------------------------

    # ec = Elliptic_Curve()
    # P = Point(ec,ec.Gx,ec.Gy)


