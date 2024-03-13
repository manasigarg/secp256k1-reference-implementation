from hashlib import sha256

pri_key = 7230495730459
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
p = 2 ** 256 - 2 ** 32 - 977
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
bl = 256

def inverse(i):
    x, y, d = extendedEuclideanAlgorithm(i, p)
    return x


def extendedEuclideanAlgorithm( a, b):
    if abs(b) > abs(a):
        (x, y, d) = extendedEuclideanAlgorithm(b, a)
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

def add(x1,y1,x2,y2,p):

    if (x2 == "ideal" and y2 == "ideal"):
        return x1,y1

    if (x1,y1) == (x2,y2):
        inv = inverse(2 * y1)
        m = ((3 * x1 * x1) * inv) % p
    else:
        if (x2-x1) < 0:
            inv = inverse (x1-x2)
            m = (-(y2-y1) * inv) % p
        else:
            inv = inverse(x2 - x1)
            m = ((y2 - y1) * inv) % p

    x3 = (m * m - x2 - x1) % p
    y3 = (m * (x3 - x1) + y1) % p
    return (x3, y3)


def mul(x,y,n,p):
            Qx = x
            Qy = y

            if n & 1 == 1 :
                Rx = x
                Ry = y
            else:
                Rx = ideal(x)
                Ry = ideal (y)
            # This will iterate n-1 times
            i = 2
            while i <= n:
                Qx, Qy = add (Qx, Qy, Qx, Qy, p)
                if n & i == i:
                    Rx, Ry = add(Qx, Qy, Rx, Ry, p)
                i = i << 1

            return (Rx, Ry)

def ideal (x):
    return "ideal"

def sign(msg):

    # 0) Encode the message into a form which can be hashed
    msg_bytes = bytes(msg, 'utf8')
    print ("msg_bytes: ", msg_bytes)

    # 1)  e = hash(msg)
    e = sha256(msg_bytes)
    print ("e: ", e)

    # 2) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
    z = e.hexdigest()[int(-bl / 4):]
    print ("z: ",z)
    z_int = int(z, 16)

    # 3) Select a cryptographically secure random integer k from [1,n-1]
    k = 465407

    # 4) Calculate the curve point (x1,y1) = k x G
    kGx, kGy = mul(Gx, Gy, k, p)

    # 5) Calculate r = Pubkey_x mod n, if r = 0 go  back to step 3)
    if kGx % n == 0:
        raise ("kGx_x mod n is equal to 0!!! Just generate another k and kGx")
    else:
        r = kGx

    # 6) Calculate s = (k^-1)*(z + r*da) mod n
    k_inv = inverse(k)
    rda = r * pri_key
    zrda = z_int + rda
    kzrda = k_inv * zrda
    s = kzrda % n
    if s == 0:
        raise ("s is equal to 0!!! Just generate another k and kGx")
    return r, s

def verify  (msg,r,s,p):
    # 0) Encode the message into a form which can be hashed
    msg_bytes = bytes(msg, 'utf8')

    # 1) Skipping step 1 since we checked in sign that both r & s are in [1,n-1]
    # TODO: Need to implement this later on

    # 2)  e = hash(msg)
    e = sha256(msg_bytes)

    # 3) Let z be the bl leftmost bits of e, where bl is the bit length of the curve
    z = e.hexdigest()[int(-bl / 4):]
    z_int = int(z, 16)
    print ("z in verify: ", z)

    # 4) Calculate s^-1 mod n
    s_inv = inverse(s)
    print ("s_inv", s_inv)
    w = s_inv % n
    print ("w: ", w)

    # 5) Calculate u1 = zw mod n and u2 = rw mod n
    u1 = (z_int * w) % n
    u2 = (r * w) % n
    print ("u2: ", u2)
    # Calculating u1Gx
    PubKey_x, PubKey_y = mul(Gx, Gy, pri_key, p)
    u1Gx, u1Gy = mul(Gx, Gy, u1, p)
    # Calculating u2Qx
    Qx = PubKey_x
    Qy = PubKey_y
    u2Qx, u2Qy = mul(Qx, Qy, u2, p)
    print ("u2Qx: ", u2Qx)
    print ("u2Qy: ", u2Qy)
    # Calculating u1G + u2Q
    x1, y1 = add(u1Gx, u1Gy, u2Qx, u2Qy, p)

    # 6) Check if r = x1 mod n
    if (r % n) == (x1 % n):
        print("OMG! (r % n) == (x1 % n)")
    else:
        print("Sigh....(r % n) != (x1 % n)")

    #*********Correctness of Verification*******************
    i = u2*pri_key
    u2dagx, u2dagy = mul(Gx, Gy, i, p)
    print ("u2dagx: ", u2dagx)
    print ("u2dagy: ", u2dagy)
    a = (u1 + (u2 * pri_key))
    b = (u1 + (r * w) * pri_key)
    c = (z_int + (r * pri_key))*w
    print ("a: ",a)
    print ("b", b)
    print ("c", c)


# *********************************TEST*************************************************************

msg = "Hello World"
r, s = sign (msg)
print ("r: ", r)
print ("s: ",s)
verify (msg,r,s,p)



