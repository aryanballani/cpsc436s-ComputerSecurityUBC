from Crypto.Util import number

e = 65537
n = 0xa082497e8eb9b8b329270511d0aa0333bfd10c3888c6a47949d61a8dfcf1a3f2489ab595747daa922f147f56d355098b6238c17b77a8c20f007a25b5f1ddf63b3efb53c9300016db51ed711d7d6dab39b89f108f7a78ac2e6b0c52030a9137ae79bb9d3d57af53b1193025662a5189357b6918a9d974bf9f04aaefe9d7a641b128ef81a852eb3588d7d6a49eb81724ff014f436d6efc0b110d5a0e74ead443158b2979a29b348153c35cf127cdbb3b83d4d6a454f432f75ac3601ea997964d7216c6e2a3acd52f632278d94357c837dde261e4421a26c9bc535f94ad41ca4292fc1c380a69eb7b0fbc99aa8eacd2710d45c80cfa5f3111c8f111f7343aec9459

def encrypt(plaintext, e, n):
    m = int(plaintext.encode().hex(), 16)
    c = pow(m, e, n)
    return f"{c:x}"


flag = 0x6aaecfb5f74784b4ee32bd9f755c5d70b2504a2f7fff09315f69898e4ef4969fb4cd673cf413eb55cd0ed2b4ab0c63f389b23c4ab8e853da5e2016e705619fbb2f13e99432c948643b466415548f34295465c2bd5ec8f29c9642db14c60de425028245cac7140c0343e27fb08f1442903c121ef37a55100a5099d795e3d03fb471fb0b4945480c192bd621a04c0b84fd5e8739475fa929c389de4a58c12d90c32160966bbbef613bbf9c5aa81cd944e4391122da8294d79c13b411829ec8910b2d1fc1bdc188e63c49b181ca770a32444addf05021f75485b90150748d5e8574e16daa9b1e991d7b02b588eb44dd357159f9e0e4f315436f0eb70250d0b1adca

# last 12 bits missing 
# we will brute force the last 12 bits of p and q, and check if the resulting n is correct
partial_p = 0xfa9220b783c800b7169da6dea8c0018741679eed7e393b23e18c3e4400783c6ca64852b59e180ca755b2f3600a6027104fe03fe8d9b7411bf310f545e8aaa5948c46bbcf069c5b8327cd1e9abf1607bdc6536e83a29df17e3df682a56fe4a1f3d9ab95ac553e11c15e7901c1a6a5f6dd16552ba8639ff00a22c9250a9bcef000

for bits in range(2**12):
    i = hex(bits)[2:]  # Get the hexadecimal representation of the bits
    print(f"Trying with hex: {i}")
    p = partial_p + bits
    if n % p != 0:  # skip most iterations where p is not a factor of n
        continue
    q = n // p
    phi_n = (p-1) * (q-1)
    d = pow(e, -1, phi_n)
    decrypted_flag = pow(flag, d, n)
    decryted_flag_hex = hex(decrypted_flag)[2:]
    try:
        plaintext = bytes.fromhex(decryted_flag_hex).decode(errors='ignore')
        # print(f"Decrypted plaintext: {plaintext}")
        if plaintext[0:4] == "cpsc":
            print(f"Found the flag: {bytes.fromhex(hex(decrypted_flag)[2:]).decode()}")
            break
    except Exception:
        continue
    

