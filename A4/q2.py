import random 

def hash_djb2(s):
    h = 5381
    for x in s.encode():
        h = ((h * 33) + x) & 0xFFFFFFFF
    return h

# =============
flag_hash = 0x53b65f37

s = "cpsc436s{e15"

# for r in range(10):
#     for i in range(2**(4*r)):
#         # print(i)
#         # hex should always be r characters long (0x0 to 0xffff for r=4, 0x00 to 0xff for r=2, etc.)
#         next_char = hex(i)[2:].rjust(r, "0")
#         candidate = s + next_char
#         if hash_djb2(candidate) == flag_hash:
#             print("Found the flag:", candidate)
#             exit(0)

#     print("Done searching appending", r, "characters, haven't found the flag yet")
# ==============

def reverse_step(h, x):
    return ((h - x) * pow(33, -1, 2**32)) % 2**32

prefix_hash = hash_djb2(s)

suffix_inv = ""

def dfs(h, depth, path):
    if depth == 0:
        return h == prefix_hash, path
    
    for x in range(32, 127):  # printable ASCII
        prev = reverse_step(h, x)
        found, res = dfs(prev, depth - 1, chr(x) + path)
        if found:
            return True, res
    
    return False, None

found, suffix = dfs(flag_hash, 8, "")
if found:
    print("Found:", s + suffix)