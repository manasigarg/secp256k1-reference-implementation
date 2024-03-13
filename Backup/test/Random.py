x2 = 89565891926547004231252920425935692360644145829622209833684329913297188986597
y2 = 103633689937622365100603176395974509217114616778598935862658712053120463017733
p = 2 ** 256 - 2 ** 32 - 977
x1 = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y1 = 32670510020758816978083085130507043184471273380659243275938904335757337482424

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

'''def add(x1,y1,x2,y2,p):
    if (x1,y1) == (x2,y2):
        inv = inverse(2 * y1)
        m = ((3 * x1 * x1) * inv) % p
    else:
        inv = inverse(x2 - x1)
        m = ((y2 - y1) * inv) % p

    x3 = (m * m - x2 - x1) % p
    y3 = (m * (x3 - x1) + y1) % p
    print ('m: ',m)
    return (x3, y3) '''

def add(x1,y1,x2,y2,p):
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
    print ('m: ',m)
    print ('y2-y1: ',y2-y1)
    return (x3, y3)

def PointOnCurve (x,y,p):
    z = ((x*x*x) + 7)
    return ((y*y)%p == z%p)

print ('inverse of x1-x2: ', inverse(x1-x2))
print ('inverse of x2-x1: ', inverse(x2-x1))

x3,y3 = add (x1,y1,x2,y2,p)
print ('Point on curve: ', PointOnCurve(x3,y3,p))



