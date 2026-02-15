key = 'ed9d11792571f337dcaa368b'
len_key = len(key) // 2
print(len_key)

decrypted = []
byte_key = bytes.fromhex(key)
with open('./flag1.png.enc', 'rb') as f:
    ind = 0
    while True:
        byte = f.read(1)
        if not byte:
            break
        decrypted_byte = byte[0] ^ byte_key[ind % len_key]
        ind += 1        
        decrypted.append(decrypted_byte)

with open('./flag1.png', 'wb') as f:
    # print(decrypted)
    f.write(bytearray(decrypted))

print(decrypted[:8])