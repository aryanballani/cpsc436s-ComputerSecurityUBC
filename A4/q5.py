import hashlib

flag = "cpsc436s{cc8bd368d11f5580ed9bd031dfb60000}"
hash_flag = "028ab1932dd1fbd6dabe7143c3625372"  # hex 

# only 2^16 = 65536 possibilities for the next character, so we can brute-force it
for i in range(2**16):
    # print(i)
    # hex should always be 4 characters long (0x0000 to 0xffff)
    next_char = hex(i)[2:].rjust(4, "0")
    # print("Trying next character:", next_char)
    flag_candidate = flag[:-5] + next_char + "}"
    # print("Trying flag candidate:", flag_candidate)
    if hashlib.md5(flag_candidate.encode()).hexdigest() == hash_flag:
        print("Found the flag:", flag_candidate)
        break
