line1_enc = "3e4765d3884e9b36a63deb1c923091"
line3_enc = "6d9c8e1a2b4f5c7d8e9f0a1b2c3d4e"
s = "Congratulations"

for i in range(15):
    l1_byte = bytes.fromhex(line1_enc[i*2:(i+1)*2])
    l3_byte = bytes.fromhex(line3_enc[i*2:(i+1)*2])
    s_byte = bytes(s[i], 'utf-8')

    print(chr(l1_byte[0]^l3_byte[0]^s_byte[0]))
