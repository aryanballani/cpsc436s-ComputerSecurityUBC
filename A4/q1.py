def hash_djb2(s):
    h = 5381
    for x in s.encode():
        h = ((h * 33) + x) & 0xFFFFFFFF_FFFFFFFF
    return h

start_s = "d17794nwvz"
s1 = "d17794nwvzb"
s2 = "d17794nwvza"

# added `b` to s1 and `a` to s2 because the diff in bytes is 1, 
# now the next character in the strings should be different by -33 (s1-s2)
s1_next = "("
s2_next = chr(ord(s1_next) + 33)

s1 += s1_next
s2 += s2_next

print(s1, "->", hash_djb2(s1))
print(s2, "->", hash_djb2(s2))