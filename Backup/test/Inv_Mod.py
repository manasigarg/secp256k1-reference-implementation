# --------------------------------------------------------------------------------------------------
#                                           CORE FUNCTIONS
# --------------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------------
#                                             TEST CODE
# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    print("EEA(a,b): (mul inv of a mod b, mul inv of b mod a, gcd(a,b)\n")

    a = [4, 19, 6, 23, 7]
    b = [6,  7, 7,  7, 7]

    for i in range(0,len(a)):

        print("EEA({},{}): {}".format(a[i],b[i],extendedEuclideanAlgorithm(a[i], b[i])))
        print("EEA({},{}): {}".format(-a[i],b[i],extendedEuclideanAlgorithm(-a[i], b[i])))
        print("EEA({},{}): {}".format(a[i],-b[i],extendedEuclideanAlgorithm(a[i], -b[i])))
        print("EEA({},{}): {}\n".format(-a[i],-b[i],extendedEuclideanAlgorithm(-a[i], -b[i])))

        tmp = a[i]
        a[i] = b[i]
        b[i] = tmp

        print("EEA({},{}): {}".format(a[i], b[i], extendedEuclideanAlgorithm(a[i], b[i])))
        print("EEA({},{}): {}".format(-a[i], b[i], extendedEuclideanAlgorithm(-a[i], b[i])))
        print("EEA({},{}): {}".format(a[i], -b[i], extendedEuclideanAlgorithm(a[i], -b[i])))
        print("EEA({},{}): {}\n".format(-a[i], -b[i], extendedEuclideanAlgorithm(-a[i], -b[i])))



