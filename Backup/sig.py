# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import os
import sys
from hashlib import sha256


# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

sys.path.append(os.getcwd() + r'\test')

import sig
import rng
import elliptic_curve
from logger import *
import Multiplication


# ==================================================================================================
#                                            SIGNATURE
# ==================================================================================================


class Signature:

    def __init__(self,ec,rng):

        logger.setLevel(logging.INFO)

        logger.info("\n\n-----------------PUB,PRI GENERATION-----------------\n")

        self.ec = ec
        self.rng = rng

        self.pri_key = 7230495730459
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        p = 2 ** 256 - 2 ** 32 - 977
        self.PubKey_x, self.PubKey_y = Multiplication.mul(Gx, Gy, self.pri_key, p)
        logger.info("Pri Key: {}".format(self.pri_key))
        logger.info("Pub Key X: {}".format(self.PubKey_x))
        logger.info("Pub Key Y: {}".format(self.PubKey_y))
        logger.info("Is pub key on curve: {}".format(self.ec.is_point_on_curve(self.PubKey_x,self.PubKey_y)))

        logger.info(self.ec)

    def sign(self,msg):

        logger.info("\n\n-----------------SIGNING-----------------\n")

        self.msg = msg
        logger.info("msg: {}".format(self.msg))

        # 0) Encode the message into a form which can be hashed
        self.msg_bytes = bytes(self.msg,'utf8')
        logger.info("msg_bytes: {}".format(self.msg_bytes))

        # 1)  e = hash(msg)
        self.e = sha256(self.msg_bytes)
        logger.info("e: {}".format(self.e.hexdigest()))

        # 2) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
        self.z = self.e.hexdigest()[int(-self.ec.bl/4):]
        self.z_int = int(self.z,16)
        logger.info("z (in str): {}".format(self.z))
        logger.info("z (in int): {}".format(self.z_int))

        # 3) Select a cryptographically secure random integer k from [1,n-1]
        self.k = self.rng.read()

        # 4) Calculate the curve point (x1,y1) = k x G
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        p = 2 ** 256 - 2 ** 32 - 977
        kGx , kGy = Multiplication.mul(Gx, Gy, self.k, p)

        # 5) Calculate r = Pubkey_x mod n, if r = 0 go back to step 3)
        if kGx % self.ec.n == 0:
            raise("kGx_x mod n is equal to 0!!! Just generate another k and kGx")
        else:
            logger.info("Congratz, kGx mod n != 0")
            r = kGx
            logger.info("r: {}".format(r))

        # 6) Calculate s = (k^-1)*(z + r*da) mod n
        k_inv = self.ec.inverse(self.k)
        logger.info("k_inv: {}".format(k_inv))
        rda = r*self.pri_key
        logger.info("r*da: {}".format(rda))
        zrda = self.z_int + rda
        logger.info("(z + r*da): {}".format(zrda))
        kzrda = k_inv*zrda
        logger.info("(k^-1)*(z + r*da): {}".format(kzrda))
        s = kzrda % self.ec.n
        logger.info("(k^-1)*(z + r*da) mod n: {}".format(s))
        if s == 0:
            raise("s is equal to 0!!! Just generate another k and kGx")
        else:
            logger.info("Congratz, s mod n != 0")
            logger.info("s: {}".format(s))

        return r,s

    def verify(self,msg,r,s):

        logger.info("\n\n-----------------VERIFYING-----------------\n")

        self.msg = msg
        logger.info("msg: {}".format(self.msg))

        # 0) Encode the message into a form which can be hashed
        self.msg_bytes = bytes(self.msg, 'utf8')
        logger.info("msg_bytes: {}".format(self.msg_bytes))

        # 1) Skipping step 1 since we checked in sign that both r & s are in [1,n-1]
        #TODO: Need to implement this later on

        # 2)  e = hash(msg)
        self.e = sha256(self.msg_bytes)
        logger.info("e: {}".format(self.e.hexdigest()))

        # 3) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
        self.z = self.e.hexdigest()[int(-self.ec.bl / 4):]
        self.z_int = int(self.z, 16)
        logger.info("z (in str): {}".format(self.z))
        logger.info("z (in int): {}".format(self.z_int))

        # 4) Calculate s^-1 mod n
        s_inv = self.ec.inverse(s)
        w = s_inv % self.ec.n
        logger.info("s_inv: {}".format(s_inv))
        logger.info("w: {}".format(w))

        # 5) Calculate u1 = zw mod n and u2 = rw mod n
        u1 = self.z_int * w % self.ec.n
        u2 = r * w % self.ec.n
        # Calculating u1Gx
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        p = 2 ** 256 - 2 ** 32 - 977
        u1Gx, u1Gy = Multiplication.mul(Gx, Gy, u1, p)
        # Calculating u2Qx
        Qx = self.PubKey_x
        Qy = self.PubKey_y
        p = 2 ** 256 - 2 ** 32 - 977
        u2Qx , u2Qy = Multiplication.mul(Qx, Qy, u2, p)
        # Calculating u1G + u2Q
        x1,y1 = Multiplication.add(u1Gx,u1Gy,u2Qx,u2Qy,p)
        logger.info("u1Gx: {}".format(u1Gx))
        logger.info("u1Gy: {}".format(u1Gy))
        logger.info("u2Qx: {}".format(u2Qx))
        logger.info("u2Qy: {}".format(u2Qy))
        logger.info("x1: {}".format(x1))
        logger.info("y1: {}".format(y1))
        logger.info("Is (x1,y1) on curve? {}".format(self.ec.is_point_on_curve(x1,y1)))

        # 6) Check if r = x1 mod n
        logger.info("r mod n = {}".format(r % self.ec.n))
        logger.info("x1 mod n = {}".format(x1 % self.ec.n))
        if (r % self.ec.n) == (x1 % self.ec.n):
            logger.info("OMG! (r % self.ec.n) == (x1 % self.ec.n)")
        else:
            logger.info("Sigh....(r % self.ec.n) != (x1 % self.ec.n)")


# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)

    ec = elliptic_curve.Elliptic_Curve()
    rng = rng.RNG(limit = ec.n)

    sig = Signature(ec,rng)

    r,s = sig.sign(msg="Hello Universe!")

    sig.verify(msg="Hello Universe!",
               r=r,
               s=s)