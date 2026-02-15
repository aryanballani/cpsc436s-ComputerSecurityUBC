'''
Returns d, x, y such that a*x + b*y = d = gcd(a,b)
'''
def xgcd(a, b):
    if b == 0:
       d = a; x = 1; y = 0 
       return d, x, y
    else:
       d, x1, y1 = xgcd(b, a % b)
       q = a // b
       x = y1
       y  = x1-y1*q
       assert a*x + b*y == d
       return d, x, y
    
'''
Returns modular inverse of a mod m if it exists; exception otherwise
'''
def modinv(a, m):
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m