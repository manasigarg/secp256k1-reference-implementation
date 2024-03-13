from ec import Elliptic_Curve
from logger import *
from point import Point

Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
p = 2 ** 256 - 2 ** 32 - 977

ec = Elliptic_Curve()
G = Point(Gx,Gy,ec)

k = 3457898
u = 6783577

# This is the originial base point G
print("Gx: ", G.x)
print("Gy: ", G.y)

# Point A = k * G
A = k * G
print ("\nThis is ",k," * G:")
print ("Ax: ", A.x)
print ("Ay: ", A.y)
print ("Point on curve: ", ec.is_on_curve(A))

# Point B = u * A
B = u * A
print ("\nThis is ",u," * A:")
print ("Bx: ", B.x)
print ("By: ", B.y)
print ("Point on curve: ", ec.is_on_curve(B))

# Point C = (k * u) * G
C = (k*u) * G
print ("\nThis is ",(k*u)," * G")
print ("Cx: ", C.x)
print ("Cy: ", C.y)
print ("Point on curve: ", ec.is_on_curve(C))

# Points B and C should be equal
print ("\n",u," * (",k," * G) == (",(k*u)," * G) ?")
print ("X coordinate same: ", B.x == C.x)
print ("Y coordinate same: ", B.y == C.y)
