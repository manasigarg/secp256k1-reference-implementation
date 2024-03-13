import math

x1 = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y1 = 32670510020758816978083085130507043184471273380659243275938904335757337482424
x2 = 89565891926547004231252920425935692360644145829622209833684329913297188986597
y2 = 103633689937622365100603176395974509217114616778598935862658712053120463017733
m = 91914383230618135761690975197207778399550061809281766160147273830617914855857
#m2 = 23877706006698059661880009811480129453719922856358797879310310177290919815806
p = p = 2 ** 256 - 2 ** 32 - 977

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

print ("x2 - x1: ", x2-x1)
print ("p: ",p)
x3 = (m * m - x2 - x1) % p
print ("m * m: ", m*m)
print ("x2 + x1: ", x2+x1)
print ("x3: ", x3)
print ("x3 % p: ", x3%p)

y3 = (m * (x3 - x1) + y1) % p
print ("x3 - x1: ", x3-x1)
print ("m * (x3 - x1): ", m * (x3 - x1))
print ("y3: ", y3)
print ("y3 % p: ", y3%p)

print ("inv (x2-x1): ", inverse(x2-x1))

print ("2*y1:", 2*y1)
print ("inv(2*y1): ", inverse(2*y1))

m_first = ((3 * x1 * x1) * inverse(2*y1))
#rem_first = m_first - (math.floor(m_first/p) * p)
rem_first = divmod(m_first,p)


m_second = ((y2 - y1) * inverse(x2-x1))
#rem_second = m_second - (math.floor(m_second/p) * p)
rem_second = divmod(m_second,p)

print ("m_first % p: ",m_first % p)
print ("m_second % p: ",m_second % p)

print ("rem_first: ",rem_first)
print ("rec_second: ",rem_second)

#print (rem_first > p)
