from Crypto.Hash import SHA1

def sign(plaintext, p, q, g, x, k):
    m = plaintext.encode()
    h = int(SHA1.new(m).hexdigest(), 16)

    r = pow(g, k, p) % q
    if r == 0:
        raise Exception
    s = (pow(k, -1, q) * (h + x * r)) % q
    if s == 0:
        raise Exception

    return (r, s)

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

k = 0xea5e9ada33e46afc7c1b62a749a083598df4258c # nonce 

g = 0xbc9b56e61620851fec96975075c79d2aaee1ca66931783923ddf93c45047d3c62e3317264aa6a50d6b0bc4dffa6dcb7a217aafe58570c3ca531078e42ca9950117edb13d9747f00f31ca24acaffee519409ae5a537b73e661bf47d707724d9e78a2a19b358f7cc1251b969559895bbd01568b5c776460f205b70e831970c1853
p = 0xd2c37f97e96e5bee77805d32731037bc630752c7223c07d4dccabed5ec287832aca3aafcf4e46c9b295e041330e372aa985b37ce828854f817aa9c2334a267b6ec4eaccdcedf53176d1bd5313f18072615edea8ea6bb061c1c2c9200fe5990a00786d8ae5fc56059c38ddcdcf59805f40d5377c9d42dfcb240a774e28e025881
q = 0xfc68cfb0405ab92cd0baa41fe82bb114f190643f
y = 0x2194e5d9d569bfd28d53dd03aa850891d367c635fbc697170485eab1c2867d543a93f1809936ab29416367501ce67c8ca87ff8c33f026460c692a0698c1dbefb1f3e3ad79e19a61e26ce05737b6ae08c22d05ca6150b12c9e2d991bf5715ca3eb03479bd7ff02d533ff429d3833d8335d25a8581228a4c1116b7b3787fcc0bbb

r = 0x53dddc47bd03bce1dc87d6157a9a53036ed0b339

m1 = "flag{this_is_an_example}"
s1 = 0x81360a4e2d8c9dff819e9f76e694b0b23dfa70b5
print(verify(m1, p, q, g, r, s1))

m2 = "cpsc436s{4d8be444febe2a230ef53d6867ae7338}"
k_inv = pow(k, -1, q)
s2 = (s1 + k_inv * (int(SHA1.new(m2.encode()).hexdigest(), 16) - int(SHA1.new(m1.encode()).hexdigest(), 16))) % q
print(verify(m2, p, q, g, r, s2), s2.to_bytes(20, "big").hex())
