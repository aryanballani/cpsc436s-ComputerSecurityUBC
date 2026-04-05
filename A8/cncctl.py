
char_map = [0xff] * 256
# Filling char_map based on your provided data
mapping = {48: 19, 49: 11, 50: 4, 51: 13, 52: 9, 53: 8, 54: 21, 55: 6, 56: 24, 57: 27, 65: 0, 66: 23, 67: 18, 68: 29, 69: 7, 70: 31, 71: 30, 72: 10, 74: 15, 75: 26, 77: 16, 78: 2, 80: 1, 81: 3, 82: 20, 83: 25, 84: 14, 86: 5, 87: 22, 88: 17, 89: 28, 90: 12}
for k, v in mapping.items(): char_map[k] = v

# Create a reverse lookup: value -> character
rev_map = {v: chr(k) for k, v in mapping.items()}

key_table = [0x18A242CACBCF, 0x1FA7AF4D66F9, 0x19DBD1219329]

# Mask used in the C code: 0x1fffffffffff
MASK = 0x1FFFFFFFFFFF

# Initial uVar4 and final expected value from the C code
BASE = 0x87848A98784
TARGET = 0x19FF0C535E68

# multiple possible license keys in format chunk0-chunk1-chunk2
# each chunk is 9 chars
c0 = "000000000"        # i'll set as anything random
c1 = "000000000"        # same anything random, now we calc chunk2
c2 = ""

def inner_loop(chunk):
    uVar1 = 0
    # it can index based on the char values provided as input
    # valid ones (not ff are 48-57, 65-90) basically 0-9 and A-Z
    for c in chunk:
        uVar1 = ((uVar1 << 5) | char_map[ord(c)]) & MASK
    return uVar1

def decode_uvar(val):
    """Converts the uVar1 sum back into 9 characters using base-32"""
    chars = []
    for _ in range(9):
        five_bits = val & 0x1F
        if five_bits not in rev_map: return None
        chars.append(rev_map[five_bits])
        val >>= 5
    return "".join(reversed(chars))

'''
TARGET = (BASE + 
        (inner_loop(chunk0) * key_table[0]) + 
        (inner_loop(chunk1) * key_table[1]) + 
        (inner_loop(chunk2) * key_table[2])
        ) & MASK

=> TARGET - BASE - (inner_loop(chunk0) * key_table[0]) - (inner_loop(chunk1) * key_table[1]) = (inner_loop(chunk2) * key_table[2])

=> (TARGET - BASE - (inner_loop(chunk0) * key_table[0]) - (inner_loop(chunk1) * key_table[1])) * pow(key_table[2], -1, MASK) = inner_loop(chunk2)

'''

# rhs current sum 
current_sum = (BASE + (inner_loop(c0) * key_table[0]) + (inner_loop(c1) * key_table[1])) & MASK

# now we solve for the needed difference to reach TARGET
needed_diff = (TARGET - current_sum) & MASK

# mod inverse to find the final chunk
# pow(a, -1, m) available in Python 3.8+
try:
    inv_key2 = pow(key_table[2], -1, MASK + 1)
    target_uVar1 = (needed_diff * inv_key2) & MASK
    
    c2 = decode_uvar(target_uVar1)
    if c2:
        print(f"Success! License Key: {c0}{c1}{c2}")
    else:
        print("Resulting bits don't map to valid characters. Try different c0/c1.")
except ValueError:
    print("key_table[2] is not invertible. Logic requires a different approach.")
