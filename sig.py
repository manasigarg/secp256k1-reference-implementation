# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import os
import sys
from hashlib import sha256
import hashlib
from py2specials import *
from py3specials import *
import hmac


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

        self.ec = Elliptic_Curve()
        self.rng = RNG(limit = self.ec.order)

    def generate_key_pair(self,load=True):

        logger.debug("\n\n----------------- PUB,PRI GENERATION -----------------\n")

        if load == False:
            self.pri_key = self.rng.generate()
        elif load == True:
            self.pri_key = self.rng.read()#34390819888240390953029010971248455142986221947941601700148038000926730363672
        logger.info("Pri Key: {}".format(self.pri_key))
        logger.info("Pri Key Hex: {}".format(hex(self.pri_key)))

        self.G = Point(self.ec.Gx, self.ec.Gy, self.ec)
        self.pub_key = self.G * self.pri_key
        logger.debug("Pub Key x: {}".format(self.pub_key.x))
        logger.debug("Pub Key y: {}".format(self.pub_key.y))

    def sign(self,msg,byte_format=False):

        logger.debug("\n\n----------------- SIGNING -----------------\n")

        if byte_format == False:

            self.msg = msg
            logger.info("msg: {}".format(self.msg))

            # 0) Encode the message into a form which can be hashed
            self.msg_bytes = bytearray.fromhex(self.msg)
        else:
            self.msg_bytes = msg
        logger.info("msg_bytes: {}".format(self.msg_bytes))

        # 1)  e = hash(msg)
        # self.e = sha256(self.msg_bytes)
        self.e = self.msg_bytes
        # logger.info("int from bytes: {}".format(int.from_bytes(self.msg_bytes, "big")))
        # logger.info("e (msg_hash): {}".format(self.e.hexdigest()))
        logger.info("e: {}".format(self.e))

        # 2) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
        # self.z = self.e.hexdigest()[int(-self.ec.size/4):]
        # self.z_int = int(self.z,16)
        self.z_int = int.from_bytes(self.e, "big")
        # logger.info("z (in str): {}".format(self.z))
        logger.info("z (in int): {}".format(self.z_int))

        # 3) Select a cryptographically secure random integer k from [1,n-1]
        # self.k = self.rng.read()
        self.k = deterministic_generate_k(self.e,self.pri_key)
        logger.info("k: {}".format(self.k))

        # 4) Calculate the curve point (x1,y1) = k x G
        self.kG = self.k*self.G
        logger.info("kG x: {}".format(self.kG.x))
        logger.info("kG y: {}".format(self.kG.y))

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
        s_raw = kzrd % self.ec.order
        v = 27 + ((self.kG.y % 2) ^ (0 if s_raw * 2 < self.ec.order else 1))
        logger.info("v: {}".format(v))
        s = s_raw if s_raw * 2 < self.ec.order else self.ec.order - s_raw
        logger.debug("(k^-1)*(z + r*da) mod n: {}".format(s))
        if s == 0:
            raise("s is equal to 0! Just generate another k and kGx")
        else:
            logger.debug("Congratz, s mod n != 0")
            logger.debug("s: {}".format(s))

        return r,s

    def verify(self,msg,r,s,byte_format=False):

        logger.debug("\n\n-----------------VERIFYING-----------------\n")

        if byte_format == False:
            self.msg = msg
            logger.debug("msg: {}".format(self.msg))

            # 0) Encode the message into a form which can be hashed
            self.msg_bytes = bytes(self.msg, 'utf8')
            logger.debug("msg_bytes: {}".format(self.msg_bytes))
        else:
            self.msg_bytes = msg

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
        u2Q = u2*self.pub_key
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

def deterministic_generate_k(msghash, priv):

    v = b'\x01' * 32
    k = b'\x00' * 32
    priv = encode_privkey(priv, 'bin')
    msghash = encode(hash_to_int(msghash), 256, 32)
    k = hmac.new(k, v + b'\x00' + priv + msghash,
                 hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b'\x01' + priv + msghash,
                 hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return decode(hmac.new(k, v, hashlib.sha256).digest(), 256)

def encode_privkey(priv, formt, vbyte=0):
    if not isinstance(priv, int_types):
        return encode_privkey(decode_privkey(priv), formt, vbyte)
    if formt == 'decimal':
        return priv
    elif formt == 'bin':
        return encode(priv, 256, 32)
    elif formt == 'bin_compressed':
        return encode(priv, 256, 32) + b'\x01'
    elif formt == 'hex':
        return encode(priv, 16, 64)
    elif formt == 'hex_compressed':
        return encode(priv, 16, 64) + '01'
    elif formt == 'wif':
        return bin_to_b58check(encode(priv, 256, 32), 128 + int(vbyte))
    elif formt == 'wif_compressed':
        return bin_to_b58check(encode(priv, 256, 32) + b'\x01',
                               128 + int(vbyte))
    else:
        raise Exception("Invalid format!")

def decode_privkey(priv, formt=None):
    if not formt: formt = get_privkey_format(priv)
    if formt == 'decimal':
        return priv
    elif formt == 'bin':
        return decode(priv, 256)
    elif formt == 'bin_compressed':
        return decode(priv[:32], 256)
    elif formt == 'hex':
        return decode(priv, 16)
    elif formt == 'hex_compressed':
        return decode(priv[:64], 16)
    elif formt == 'wif':
        return decode(b58check_to_bin(priv), 256)
    elif formt == 'wif_compressed':
        return decode(b58check_to_bin(priv)[:32], 256)
    else:
        raise Exception("WIF does not represent privkey")

def get_privkey_format(priv):
    if isinstance(priv, int_types):
        return 'decimal'
    elif len(priv) == 32:
        return 'bin'
    elif len(priv) == 33:
        return 'bin_compressed'
    elif len(priv) == 64:
        return 'hex'
    elif len(priv) == 66:
        return 'hex_compressed'
    else:
        bin_p = b58check_to_bin(priv)
        if len(bin_p) == 32:
            return 'wif'
        elif len(bin_p) == 33:
            return 'wif_compressed'
        else:
            raise Exception("WIF does not represent privkey")

def b58check_to_bin(inp):
    leadingzbytes = len(re.match('^1*', inp).group(0))
    data = b'\x00' * leadingzbytes + changebase(inp, 58, 256)
    assert bin_dbl_sha256(data[:-4])[:4] == data[-4:]
    return data[1:-4]

def hash_to_int(x):
    if len(x) in [40, 64]:
        return decode(x, 16)
    return decode(x, 256)

# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)  # UNCOMMENT THIS AND COMMENT THE LINE ABOVE TO SEE ALL PRINTS

    sig = Signature()

    sig.generate_key_pair(read=True)

    r,s = sig.sign(msg="Hello Blockchain!")

    logger.info("r: {}".format(r))
    logger.info("s: {}".format(s))

    sig.verify(msg="Hello Blockchain!",r=r,s=s)