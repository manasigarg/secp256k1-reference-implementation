x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
p = 2 ** 256 - 2 ** 32 - 977

print ('y^2 is: ', y*y)
z = ((x * x * x) + 7)
print ('z is: ',z)
print ('is y and z equal: ', y==z)
print ('(y^2 - (x^3 +7)) % p is: ', ((y * y) - z) % p)
print ('y^2 % p is: ', (y*y)%p)
print ('z % p is: ', z%p)
print ('both side mod p is same (i.e. point is on curve): ', (y*y)%p == z%p)