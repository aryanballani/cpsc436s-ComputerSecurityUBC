from Crypto.Util import number

e = 3
n = 0xc4af6feb8833d1684611b539cb8e0c538597c0898e3cc8cd6dec5e54c57d382db782530401e3cb8ea04f8fd2cde6f0ce79039bd4fa86139d49209f266db4302d1c8ba6a8cfd23a3249cbae203e8fc19ede17a90a01016c69f0fe6cd82560cde64e419fd681441879a7796ecaf94f77ba9a3ad086b8b142f6cd0e73504f

flag = 0x67e2aa7932312dd126939b2263f953aa50a8ee84048f10445a8cbf93fb8fc66c94863a1eccfa5d496f4ec754a2533d95d7e109bd47bb1a3a4c8a0a7f2ec1073759748e42fa9743e34800d20b4da701048bfdfd4d663075ca8908892b3c6f6849b135322418605f3e006c440fe845c4c16807b17f871d2011423e2c5388


# ======== Sanity check for cube root attack ========
m_len = 42 # in bytes
n_len = 125 # in bytes since p and q are 500 bits each

max_m = "0x" + "".join(["ff" for _ in range(m_len)]) # max message in hex
# print(max_m)

max_m_cube = hex(pow(int(max_m, 16), e))
# print(max_m_cube)
# check max_m**3 is < n_len bytes 
if len(max_m_cube[2:]) < n_len*2:
    print("Since max_m**3 is less than n, we can directly compute the cube root to get the plaintext")
else:
    print("max_m**3 is", len(max_m_cube[2:])//2, "bytes which is greater than n_len", n_len, "bytes. We can try diff values of k to see if we can get a valid plaintext")
# ===========================

# ==== we try the cube root attack anyway 
def integer_cube_root(a):
    """Returns the integer cube root of a."""
    x = a
    y = (2 * x + a // (x * x)) // 3
    while y < x:
        x = y
        y = (2 * x + a // (x * x)) // 3
    return x

# max value of k can be 2^8, since the max number possible for m^3 is a 126 byte number, 
# and n is a 125 byte number, so the flag can only loop around a max of 256 times 
# before we get a valid plaintext
# since m = cube_root(ciphertext + k*n), we can try a few values of k to see if we get a valid plaintext
for k in range(256):  # we can try a few values of k to see if we get a valid plaintext
    decrypted_flag = integer_cube_root(flag + k*n)      # try a random k to see if we get a valid plaintext
    try:
        plaintext = bytes.fromhex(hex(decrypted_flag)[2:]).decode(errors='ignore')
        if plaintext[0:4] == "cpsc":
            print(f"Decrypted plaintext: {plaintext}", f"with k={k}")
    except Exception:
        continue