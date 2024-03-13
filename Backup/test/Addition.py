
# ***************************************************************************************************************
# Below commented are some other example points on the curve y^2 = x^3 +7 for testing
# Reference website for these examples: https://crypto.stackexchange.com/questions/784/are-there-any-secp256k1-ecdsa-test-examples-available

# x_hex = "34F9460F0E4F08393D192B3C5133A6BA099AA0AD9FD54EBCCFACDFA239FF49C6"
# y_hex = "0B71EA9BD730FD8923F6D25A7A91E7DD7728A960686CB5A901BB419E0F2CA232"

# x_hex = "E8AECC370AEDD953483719A116711963CE201AC3EB21D3F3257BB48668C6A72F"
# y_hex = "C25CAF2F0EBA1DDB2F0F3F47866299EF907867B7D27E95B3873BF98397B24EE1"

# x_hex = "F73C65EAD01C5126F28F442D087689BFA08E12763E0CEC1D35B01751FD735ED3"
# y_hex = "F449A8376906482A84ED01479BD18882B919C140D638307F0C0934BA12590BDE"

# x = int(x_hex,16)
# y = int(y_hex, 16)
# ***************************************************************************************************************

x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
p = 2 ** 256 - 2 ** 32 - 977

def extendedEuclideanAlgorithm(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


def inverse(a, m=p):
	g, x, y = extendedEuclideanAlgorithm(a, m)
	if g != 1:
		raise ValueError
	return x % m


def add(x1,y1,x2,y2,p):
    if (x1,y1) == (x2,y2):
        inv = inverse(2 * y1)
        m = ((3 * x1 * x1) * inv) % p
        m2 = ((3 * x1 * x1) * inv) % p
    else:
        # if (x2-x1) < 0:
        #     inv = inverse (x1-x2)
        #     m = (-(y2-y1) * inv) % p
        #     m2 = (-(y2 - y1) * inv) % p
        # else:
        inv = inverse(x2 - x1)
        inv2 = abs(inverse (x1-x2))
        m = ((y2 - y1) * inv) % p
        m2 = ((y2 - y1) * inv2) % p

    x3 = (m * m - x2 - x1) % p
    y3 = (m * (x3 - x1) + y1) % p
    x3_check = (m2 * m2 - x2 - x1) % p
    z = (x3 - x1) + y1
    y3_check = (m2 * (x3 - x1) + y1) % p
    # print ('m: ',m)
    return (x3, y3)


def PointOnCurve (x,y,p):
    z = ((x*x*x) + 7)
    return ((y*y)%p == z%p)

# *********************************TEST*************************************************************

# If Point P is (x,y), then in below examples:

if __name__ == '__main__':

    # G = (x,y)

    # A = (Ax,Ay) = G + G = 2G
    Ax,Ay = add (x,y,x,y,p)
    print ('Ax:', Ax)
    print ('Ay:', Ay)
    # print ('Is A on curve?: ', PointOnCurve(Ax,Ay,p))

    # B = (Bx,By) = A + G = 2G + G = 3G
    Bx, By = add(Ax, Ay, x, y, p)
    print('Bx:', Bx)
    print('By:', By)
    # print('Is B on curve?: ', PointOnCurve(Bx, By, p))

    # C = (Cx,Cy) = A + A = 2G + 2G = 4G
    Cx, Cy = add(Ax, Ay, Ax, Ay, p)
    print('Cx:', Cx)
    print('Cy:', Cy)
    # print('Is C on curve?: ', PointOnCurve(Cx, Cy, p))

    # D = (Dx,Dy) = B + G = 3G + G = 4G
    Dx, Dy = add(Bx, By, x, y, p)
    print('Dx:', Dx)
    print('Dy:', Dy)
    # print('Is D on curve?: ', PointOnCurve(Dx, Dy, p))







