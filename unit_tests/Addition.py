from ec import Elliptic_Curve
from logger import *
from point import Point


Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
p = 2 ** 256 - 2 ** 32 - 977

ec = Elliptic_Curve()
G = Point(Gx,Gy,ec)

# This is the originial base point G
print("Gx: ", G.x)
print("Gy: ", G.y)

# Point 2G = G + G
A = G + G
print("\n2G_x: ", A.x)
print("2G_y: ", A.y)

# Point 3G = 2G + G
B = A + G
print("\n(3G = 2G+G)_x: ", B.x)
print("(3G = 2G+G)_y: ", B.y)

# Point 3G = G + 2G
C = G + A
print("(3G = G+2G)_x: ", C.x)
print("(3G = G+2G)_Y: ", C.y)

# Point 4G = 2G + 2G
D = A + A
print("\n(4G = 2G + 2G)_x: ", D.x)
print("(4G = 2G + 2G)_y: ", D.y)

# Point 4G = 3G + G
E = C + G
print("(4G = 3G + G)_x: ", E.x)
print("(4G = 3G + G)_y: ", E.y)

# Point 4G = G + 3G
F = G + C  # 4G
print("(4G = G + 3G)_x: ", F.x)
print("(4G = G + 3G)_y: ", F.y)

# Point 5G = 4G + G
H = D + G
print("\n(5G = 4G + G)_x: ", H.x)
print("(5G = 4G + G)_y: ", H.y)

# Point 5G = 3G + 2G
I = B + A
print("(5G = 3G + 2G)_x: ", I.x)
print("(5G = 3G + 2G)_y: ", I.y)

#********* COMMUTATIVE CHECK *****************

# Check for 3G
print ("\nChecking if this is commutative -- 2G+G = G+2G ?")
print ("X coordinate same: ", B.x == C.x)
print ("Y coordinate same: ", B.y == C.y)

#Check for 4G
print ("Checking if this is commutative -- 3G+G = G+3G ?")
print ("X coordinate same: ", E.x == F.x)
print ("Y coordinate same: ", E.y == F.y)

#********* ASSOCIATIVE CHECK *****************

# Check for 4G
print ("\nChecking if this is associative -- 4G = 2G+2G = 3G+G ?")
print ("X coordinate same: ", D.x == E.x)
print ("Y coordinate same: ", D.y == E.y)

# Check for 5G
print ("Checking if this is associative -- 5G = 4G+2G = 3G+2G ?")
print ("X coordinate same: ", H.x == I.x)
print ("Y coordinate same: ", H.y == I.y)