# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import os
import sys
from hashlib import sha256


# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

import sig
from rng import RNG
from ec import Elliptic_Curve
from point import Point
from logger import *


# ==================================================================================================
#                                     SIGNATURE & VERIFICATION
# ==================================================================================================

class Signature:

    def __init__(self):

        logger.debug("\n\n----------------- PUB,PRI GENERATION -----------------\n")

        self.ec = Elliptic_Curve()
        self.rng = RNG(limit = self.ec.order)

        #self.pri_key = 722542342
        #logger.debug("Pri Key: {}".format(self.pri_key))

        self.G = Point(self.ec.Gx, self.ec.Gy, self.ec)
        #self.pub_key = self.G*self.pri_key
        #logger.debug("Pub Key x: {}".format(self.pub_key.x))
        #logger.debug("Pub Key y: {}".format(self.pub_key.y))

    def verify(self,msg,r,s, pub_key, pri_key, k):

        logger.debug("\n\n-----------------VERIFYING-----------------\n")

        self.msg = msg
        logger.debug("msg: {}".format(self.msg))

        # 0) Encode the message into a form which can be hashed
        self.msg_bytes = bytes(self.msg, 'utf8')
        logger.debug("msg_bytes: {}".format(self.msg_bytes))

        # 1) Skipping step 1 since we checked in sign that both r & s are in [1,n-1]
        #TODO: Need to implement this later on

        # 2)  e = hash(msg)
        self.e = sha256(self.msg_bytes)
        logger.debug("e: {}".format(self.e.hexdigest()))

        # 3) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
        self.z = self.e.hexdigest()[int(-self.ec.size / 4):]
        self.z_int = int(self.z, 16)
        logger.debug("z (in str): {}".format(self.z))
        logger.debug("z (in int): {}".format(self.z_int))

        # 4) Calculate s^-1 mod n
        s_inv = pow(s,self.ec.order-2,self.ec.order)
        w = s_inv % self.ec.order
        logger.debug("s_inv: {}".format(s_inv))
        logger.debug("w: {}".format(w))

        # 5) Calculate u1 = zw mod n and u2 = rw mod n
        u1 = (self.z_int * s_inv) % self.ec.order
        u2 = (r * w) % self.ec.order
        u1G = u1*self.G
        u2Q = u2*pub_key
        GQ = u1G + u2Q
        x = (GQ.x % self.ec.order)

        logger.debug("u1G.x: {}".format(u1G.x))
        logger.debug("u1G.y: {}".format(u1G.y))
        logger.debug("u2Q.x: {}".format(u2Q.x))
        logger.debug("u2Q.y: {}".format(u2Q.y))
        logger.debug("x: {}".format(x))

        # 6) Check if r = x mod n
        logger.debug("r mod n = {}".format(r % self.ec.order))
        logger.debug("x mod n = {}".format(x % self.ec.order))
        if (r % self.ec.order) == (x % self.ec.order):
            logger.info("OMG! (r % n) == (x % n)")
        else:
            logger.info("Sigh....(r % n) != (x % n)")

        #************ CORRECTNESS OF ALGORITHM *******************

        logger.info("*****CORRECTNESS*******")

        # 1: C = u1 * G + u2 * Qa
        logger.info("1. Cx = {}".format(GQ.x))
        logger.info("1. Cy = {}".format(GQ.y))

        # 2: C = u1 * G + u2da * G
        var = u2 * pri_key
        u2daG = var * self.G
        C2 = u1G + u2daG
        logger.info ("2. Cx = {}".format(C2.x))
        logger.info ("2. Cy = {}".format(C2.y))
        logger.info ("Step 1 == Step 2: {}".format(GQ == C2))

        # 3: C = (u1 + u2da) * G
        sum = (u1 + (u2 * pri_key))
        C3 = sum * self.G
        logger.info("3. Cx = {}".format(C3.x))
        logger.info("3. Cy = {}".format(C3.y))
        logger.info("Step 2 == Step 3: {}".format(C2 == C3))

        # 4: C = (z s^-1 + r da s^-1) * G
        var1 = ((self.z_int * s_inv) + (r * pri_key * s_inv))
        C4 = var1 * self.G
        logger.info("4. Cx = {}".format(C4.x))
        logger.info("4. Cy = {}".format(C4.y))
        logger.info("Step 3 == Step 4: {}".format(C3 == C4))

        # 5: C = (z + r da) s^-1 * G
        var2 = ((self.z_int + (r * pri_key)) * s_inv)
        C5 = var2 * self.G
        logger.info("5. Cx = {}".format(C5.x))
        logger.info("5. Cy = {}".format(C5.y))
        logger.info("Step 4 == Step 5: {}".format(C4 == C5))

        # 6: C = k * G
        C6 = k * self.G
        logger.info("6. Cx = {}".format(C6.x))
        logger.info("6. Cy = {}".format(C6.y))
        logger.info("Step 5 == Step 6: {}".format(C5 == C6))

# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)  # UNCOMMENT THIS AND COMMENT THE LINE ABOVE TO SEE ALL PRINTS

    sig = Signature()

    dir = os.getcwd() + r"/sign.txt"
    file = open(dir, 'r')
    line = file.read()
    values = line.split(',')

    Gx = int(values[0])
    Gy = int(values[1])
    p = 2 ** 256 - 2 ** 32 - 977
    r = int(values[2])
    s = int(values[3])
    msg = values[4]
    pri_key = int(values[5])
    k = int(values[6])

    file.close()

    ec = Elliptic_Curve()
    pub_key = Point(Gx, Gy, ec)

    # ********************** POSITIVE TEST *******************************************

    logger.info("********** POSITIVE test ***********")
    logger.info("pub_key x: {}".format(Gx))
    logger.info("pub_key y: {}".format(Gy))
    logger.info("r: {}".format(r))
    logger.info("s: {}".format(s))
    logger.info("msg: {}".format(msg))

    sig.verify(msg=msg,r=r,s=s, pub_key = pub_key, pri_key=pri_key, k=k)

    # ********************** NEGATIVE TEST *******************************************

    # New values for parameters to test negative cases
    msg1 = "ab"
    r1 = 123456342536547
    s1 = 8073768746524
    da = 7469375639536
    Px = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Py = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    P = Point(Px, Py, ec)
    pub_key1 = da * P

    logger.info("*********** NEGATIVE test - wrong msg **************")
    logger.info("pub_key x: {}".format(pub_key1.x))
    logger.info("pub_key y: {}".format(pub_key1.y))
    #logger.info("r: {}".format(r1))
    #logger.info("s: {}".format(s1))
    #logger.info("msg: {}".format(msg1))
    # Change parameter values to msg1/r1/s1/pub_key1 for different test cases

    sig.verify(msg=msg, r=r, s=s, pub_key=pub_key1, pri_key=pri_key, k=k)

