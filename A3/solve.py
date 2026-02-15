import math
from Crypto.Util import number

# Returns the unique solution x such that
# x = a[0] (mod m[0])
# x = a[1] (mod m[1])
# ...
def solve_crt(a, m):
    out = 0
    M = math.prod(m)
    for i in range(len(m)):
        ai = a[i]
        mi = m[i]
        bi = M // mi
        out += ai * bi * pow(bi, -1, mi)

    return out % M

# Brute-forces the discrete log for small x
# (finds x such that y = g**x (mod p))
def brute_dlog(y, g, p):
    y = y % p
    print(f"y: {y}")
    for i in range(1, p):
        gi = pow(g, i, p)
        if gi == y:
            return i

    print(f"brute_dlog: No solution found for {y} = {g}**x mod {p}")

# Source - https://stackoverflow.com/a/22808285
# Posted by Stefan, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-13, License - CC BY-SA 3.0

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def solve_pohlig_hellman(g, p, A):
    # Step 1: Factor p-1 into its prime factors
    n = p - 1
    factors = prime_factors(n)
    

    # complicated case bypass
    if len(factors) != len(set(factors)):
        return None

    print(f"Factors of p-1: {factors}")

    a = []
    m = []

    for p_i in set(factors):
        # Step 2: Compute A_i = A**((p-1)//p_i) mod p
        A_i = pow(A, n // p_i, p)

        # Step 3: Compute g_i = g**((p-1)//p_i) mod p
        g_i = pow(g, n // p_i, p)

        # Step 4: Solve for x_i such that A_i = g_i**x_i mod p
        x_i = brute_dlog(A_i, g_i, p)

        a.append(x_i)
        m.append(p_i)
    
    return solve_crt(a, m)

# Tests
ans = solve_pohlig_hellman(3, 463, 102)
assert ans == 331
print("Test 1 passed")
ans = solve_pohlig_hellman(5, 315002056831958905306372021250145722463340695973775431729822986878966540913388934373852910641288819944555277276599477341667, 148104241291803927705494459855491407409967644577848232945026200172193136671478792583141788506521503966837957396366375972330)
assert ans == 78750514207989726326593005312536430615835173993443857932455746719741635228347233593463227660322204986138819319149869335416
print("Test 2 passed")