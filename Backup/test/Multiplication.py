p = 2 ** 256 - 2 ** 32 - 977


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
    print ("m: ",m)
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

if __name__ == '__main__':


    x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    u2 = 24656904712057171826465467884208612159843667514232756640156499757907197986708
    pri_key = 7230495730459

    # Assume for understanding: Q = d * G
    #PubKey_x, PubKey_y = mul(x,y,pri_key,p)

    PubKey_x, PubKey_y = mul(x, y, 30, p)

    print ("x: ",PubKey_x)
    print ("y: ",PubKey_y)
    z = ((PubKey_x * PubKey_x * PubKey_x) + 7)
    print ('both side mod p is same (i.e. point is on curve): ', (PubKey_y * PubKey_y)%p == z%p)

    # Assume then C = u * Q
    #x_double, y_double = mul(PubKey_x, PubKey_y, u2, p)
    x_double, y_double = mul(PubKey_x, PubKey_y, 5, p)
    print ("x_double: ", x_double)
    print ("y_double: ", y_double)

    # Then C should also be equal to (d * u) * G
    prod = u2 * pri_key
    #x_result, y_result = mul (x,y,prod,p)
    x_result, y_result = mul(x, y, 150, p)

    print ("x_result: ", x_result)
    print ("y_result: ", y_result)