hex_key = []    # construct key here 
len_key = 20

# ========= signature part for key ==============
png_signature = '89504e470d0a1a0a'  # 8 byte signature in hex 
bytes_png_signature = bytes.fromhex(png_signature)

with open('flag2.png.enc', 'rb') as f:
    for i in range(8):
        bytes = f.read(1)
        key_byte = bytes[0] ^ bytes_png_signature[i]
        hex_key.append(key_byte)
        

print("First 8 bytes of key are:", hex_key)

# ========= IHDR length part for key ==============
# next 4 bytes tells how long the next chunk is. Since the first chunk is IHDR, we can use that to get next 4 bytes of key
# IHDR length is always 13 bytes, so next 4 bytes should be 00 00 00 0D
next_bytes = '0000000d'  # 4 bytes
hex_next_bytes = bytes.fromhex(next_bytes)

with open('flag2.png.enc', 'rb') as f:
    f.seek(8)   # skip first 8 bytes (png signature)
    for i in range(4):
        bytes = f.read(1)
        key_byte = bytes[0] ^ hex_next_bytes[i]
        hex_key.append(key_byte)

print("First 12 bytes of key are:", hex_key)

# ========= IHDR chunk type part for key ==============
bytes_ihd = [] # construct next 4 bytes of key here
ihdr_png = "49484452"   # 'IHDR' in hex 
bytes_ihdr_png = bytes.fromhex(ihdr_png)
with open('flag2.png.enc', 'rb') as f:
    f.seek(12)   # skip first 12 bytes (png signature + IHDR length)
    for i in range(4):
        bytes = f.read(1)
        key_byte = bytes[0] ^ bytes_ihdr_png[i]
        hex_key.append(key_byte)

# ========= Next 8 bytes of the key from image dimensions ==============
bytes_dim = [] # construct next 8 bytes of key here
# Image dimensions are 655x32 pixels, so next 4 bytes should be:
dim_png = "0000028F"   # in hex
bytes_dim_png = bytes.fromhex(dim_png)

with open('flag2.png.enc', 'rb') as f:
    f.seek(16)   # skip first 16 bytes (png signature + IHDR length + IHDR chunk type)
    for i in range(4):
        bytes = f.read(1)
        key_byte = bytes[0] ^ bytes_dim_png[i]
        hex_key.append(key_byte)

print("First 16 bytes of key are:", hex_key)

# Final key contruction since it is only 20 bytes long
key = "".join([f"{byte:02x}" for byte in hex_key])
print("Full key in hex is:", key)


# ========= Now decrypt the image using the found key =========
decrypted = []
with open('./flag2.png.enc', 'rb') as f:
    ind = 0
    while True:
        byte = f.read(1)
        if not byte:
            break
        decrypted_byte = byte[0] ^ hex_key[ind % len_key]
        ind += 1        
        decrypted.append(decrypted_byte)

with open('./flag2.png', 'wb') as f:
    # print(decrypted)
    f.write(bytearray(decrypted))

