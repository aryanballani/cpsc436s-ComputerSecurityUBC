from Crypto.Hash import SHA1

def verify(plaintext, p, q, g, r, s):
    m = plaintext.encode()
    h = int(SHA1.new(m).hexdigest(), 16)

    if r == 0:
        return False

    if s == 0:
        return False

    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    return v == r
    
g = 0x86dea8bbff08ba709dd83020801281622e545884e8679facafd49e78671f95fa2d6b41df9e386b183779171c6a6fa74dc992aae2f6ea483effbac63ea8bf1969e0302222eb4e0e64eac8738fac485fb1cd7611183b0cb44427b77365163e10cb835b8b9a74e208ba164f8bce7a83caf682ce347b1e769134959ba5002b77b1e8
p = 0xd4bf158b187b88587a1560e803127d20c7c9ab317622af5cff5aa204e50f684fdf72febef404c783efde2f958b5eb7c6d6e715f4d286e487e9b56e092f9715bc6b0edbc7c992e5cd1029a39f77bc4df820d25fdb44be8791c088c8034bf51746a23026bd75f2f0a3f607c60cb84578ba90e98a6d209589d83339b3d00b6e4ddd
q = 0x9a2259f0378bb20aa8c9459d4353c1f7a2250f05
y = 0x1c7b55209c15ae038a68df89b6491291dcaeac78c27166c22c362b4d71b44c5a2303dc4c2e2a672a1112b7187393cf54874cb9b0432f74d2bd4c8a5316125a31bb95c1c99b379fb7a56979eb790cb0edf7916bd71dccd980ef3e1e20a41eef7edeb8b042ac1d76fdfbf90320c56a14ff9a7716c984b141f48bc9b4ce3963e62a

r = 0x737afb39dbe5a4fc7713159abc79159bd24daa68

m1 = "flag{this_is_an_example}"
s1 = 0x2e38bc9cbae499d004c6dfd3e13f4566a283ac6d

m2 = "flag{this_is_another_example}"
s2 = 0x70a52497953b3aa2b6623395ae7c80709adeccc5

m3 = "cpsc436s{90cec3f864c8a03a1c8d64a02fc3e85a}"

m1_int = (int(SHA1.new(m1.encode()).hexdigest(), 16))
m2_int = (int(SHA1.new(m2.encode()).hexdigest(), 16))
m3_int = (int(SHA1.new(m3.encode()).hexdigest(), 16))

k_inv = (pow((m1_int - m2_int), -1, q) * (s1 - s2)) % q

s3 = (s1 + k_inv * (m3_int - m1_int)) % q
print(verify(m3, p, q, g, r, s3), s3.to_bytes(20, "big").hex())