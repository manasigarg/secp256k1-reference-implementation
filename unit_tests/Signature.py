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

        self.pri_key = self.rng.generate()
        logger.info("Pri Key: {}".format(self.pri_key))

        self.G = Point(self.ec.Gx, self.ec.Gy, self.ec)
        self.pub_key = self.G*self.pri_key
        logger.info("Pub Key x: {}".format(self.pub_key.x))
        logger.info("Pub Key y: {}".format(self.pub_key.y))

    def sign(self,msg):

        logger.debug("\n\n----------------- SIGNING -----------------\n")

        self.msg = msg
        logger.debug("msg: {}".format(self.msg))

        # 0) Encode the message into a form which can be hashed
        self.msg_bytes = bytes(self.msg,'utf8')
        logger.debug("msg_bytes: {}".format(self.msg_bytes))

        # 1)  e = hash(msg)
        self.e = sha256(self.msg_bytes)
        logger.debug("e: {}".format(self.e.hexdigest()))

        # 2) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
        self.z = self.e.hexdigest()[int(-self.ec.size/4):]
        self.z_int = int(self.z,16)
        logger.debug("z (in str): {}".format(self.z))
        logger.debug("z (in int): {}".format(self.z_int))

        # 3) Select a cryptographically secure random integer k from [1,n-1]
        self.k = self.rng.generate()
        logger.info("k: {}".format(self.k))

        # 4) Calculate the curve point (x1,y1) = k x G
        self.kG = self.k*self.G
        logger.debug("kG x: {}".format(self.kG.x))
        logger.debug("kG y: {}".format(self.kG.y))

        # 5) Calculate r = Pubkey_x mod n, if r = 0 go back to step 3)
        if self.kG.x % self.ec.order == 0:
            raise("kGx_x mod n is equal to 0!!! Just generate another k and kGx")
        else:
            logger.debug("Congratz, kGx mod n != 0")
            r = self.kG.x
            logger.debug("r: {}".format(r))

        # 6) Calculate s = (k^-1)*(z + r*da) mod n
        k_inv = pow(self.k,self.ec.order-2,self.ec.order)  # TODO: Understand -why is self.ec.order-2?
        logger.debug("k_inv: {}".format(k_inv))
        rd = r*self.pri_key
        logger.debug("r*da: {}".format(rd))
        zrd = self.z_int + rd
        logger.debug("(z + r*da): {}".format(zrd))
        kzrd = k_inv*zrd
        logger.debug("(k^-1)*(z + r*da): {}".format(kzrd))
        s = kzrd % self.ec.order
        logger.debug("(k^-1)*(z + r*da) mod n: {}".format(s))
        if s == 0:
            raise("s is equal to 0! Just generate another k and kGx")
        else:
            logger.debug("Congratz, s mod n != 0")
            logger.debug("s: {}".format(s))

        return r,s


# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)  # UNCOMMENT THIS AND COMMENT THE LINE ABOVE TO SEE ALL PRINTS

    sig = Signature()

    msg = "Hello Blockchain!"
    r,s = sig.sign(msg=msg)

    logger.info("r: {}".format(r))
    logger.info("s: {}".format(s))

    dir = os.getcwd() + r"/sign.txt"
    file = open(dir, 'w')
    file.write('{},{},{},{},{},{},{}'.format(str(sig.pub_key.x), str(sig.pub_key.y), str(r), str(s), msg, str(sig.pri_key), str(sig.k)))
    file.close()