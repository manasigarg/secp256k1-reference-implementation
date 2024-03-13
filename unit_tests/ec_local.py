# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

from logger import *
from point import Point


# ==================================================================================================
#                                       Elliptic Curve Class
# ==================================================================================================

class Elliptic_Curve():

    # An elliptic curve defined by the equation: y²=x³+a*x+b.
    #
    #       - name (str)              : curve unique name
    #       - bl -> size (int)        : bit size
    #       - a    (int)              : `a` equation coefficient
    #       - b    (int)              : `b` equation coefficient
    #       - p -> field (inf)        : field value
    #       - G -> generator (int[2]) : x,y coordinate of generator
    #       - n -> order (int)        : order of generator
    #       - h -> cofactor (int)     : cofactor

    def __init__(self):

        self.name = 'secp256k1'
        self.field = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
        self.order = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        # G (compressed)   02 79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        # G (uncompressed) 04 79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        #                     483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        self.Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        self.G = (self.Gx, self.Gy)
        self.cofactor = 1
        self.size = 256
        self.a = 0
        self.b = 7

    def is_on_curve(self, P):
        """ See :func:`Curve.is_on_curve` """
        q = self.field
        x = P.x
        sq3x = (x * x * x) % q
        y = P.y
        sqy = (y * y) % q
        left = sqy
        right = (sq3x + self.a * x + self.b) % q
        return left == right

    def add_point(self, P, Q):
        """ See :func:`Curve.add_point` """
        q = self.field
        if (P == Q):
            Px, Py, Pz = self._aff2jac(P.x, P.y, q)
            x, y, z = self._dbl_jac(Px, Py, Pz, q, self.a)
        else:
            Px, Py, Pz = self._aff2jac(P.x, P.y, q)
            Qx, Qy, Qz = self._aff2jac(Q.x, Q.y, q)
            x, y, z = self._add_jac(Px, Py, Pz, Qx, Qy, Qz, q)
        x, y = self._jac2aff(x, y, z, q)
        PQ = Point(x, y, self)
        return PQ

    def mul_point(self, k, P):
        """ See :func:`Curve.mul_point` """
        q = self.field
        a = self.a
        x1, y1, z1 = self._aff2jac(P.x, P.y, q)
        k = bin(k)
        k = k[2:]
        sz = len(k)
        x2, y2, z2 = self._dbl_jac(x1, y1, z1, q, a)
        for i in range(1, sz):
            if k[i] == '1':
                x1, y1, z1 = self._add_jac(x2, y2, z2, x1, y1, z1, q)
                x2, y2, z2 = self._dbl_jac(x2, y2, z2, q, a)
            else:
                x2, y2, z2 = self._add_jac(x1, y1, z1, x2, y2, z2, q)
                x1, y1, z1 = self._dbl_jac(x1, y1, z1, q, a)
        x, y = self._jac2aff(x1, y1, z1, q)
        return Point(x, y, self)

    def compute_y(self, x, sign=0):
        """ """
        p = self.field
        y2 = (x * x * x + self.a * x + self.b) % p
        y = self._sqrt(y2, p, sign)
        return y

    @staticmethod
    def _aff2jac(x, y, q):
        return (x, y, 1)

    @staticmethod
    def _jac2aff(x, y, z, q):
        invz = pow(z, q - 2, q)
        sqinvz = (invz * invz) % q
        x = (x * sqinvz) % q
        y = (y * sqinvz * invz) % q
        return (x, y)

    @staticmethod
    def _dbl_jac(X1, Y1, Z1, q, a):
        XX = (X1 * X1) % q
        YY = (Y1 * Y1) % q
        YYYY = (YY * YY) % q
        ZZ = (Z1 * Z1) % q
        S = (2 * ((X1 + YY) * (X1 + YY) - XX - YYYY)) % q
        M = (3 * XX + a * ZZ * ZZ) % q
        T = (M * M - 2 * S) % q
        X3 = (T) % q
        Y3 = (M * (S - T) - 8 * YYYY) % q
        Z3 = ((Y1 + Z1) * (Y1 + Z1) - YY - ZZ) % q
        return X3, Y3, Z3

    @staticmethod
    def _add_jac(X1, Y1, Z1, X2, Y2, Z2, q):
        Z1Z1 = (Z1 * Z1) % q
        Z2Z2 = (Z2 * Z2) % q
        U1 = (X1 * Z2Z2) % q
        U2 = (X2 * Z1Z1) % q
        S1 = (Y1 * Z2 * Z2Z2) % q
        S2 = (Y2 * Z1 * Z1Z1) % q
        H = (U2 - U1) % q
        I = ((2 * H) * (2 * H)) % q
        J = (H * I) % q
        r = (2 * (S2 - S1)) % q
        V = (U1 * I) % q
        X3 = (r * r - J - 2 * V) % q
        Y3 = (r * (V - X3) - 2 * S1 * J) % q
        Z3 = (((Z1 + Z2) * (Z1 + Z2) - Z1Z1 - Z2Z2) * H) % q
        return X3, Y3, Z3


if __name__ == '__main__':

    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    p = 2 ** 256 - 2 ** 32 - 977

    logger.setLevel(logging.INFO)

    ec = Elliptic_Curve()

    G = Point(Gx,Gy,ec)

    A = G + G  # 2G

    B = A + G

    C = G * 1
