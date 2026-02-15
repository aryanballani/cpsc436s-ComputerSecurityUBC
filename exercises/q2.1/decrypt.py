key = 'ffffffffffffffffffffffffffffffffffffffff' # 20 bytes
hex_key = bytearray.fromhex(key)
len_key = len(hex_key)
print(f"length of key is: {len_key}")

png_signature = '89504e470d0a1a0a'  # 8 bytes - got this from link in exercise description and converted to hex
hex_png_signature = bytes.fromhex(png_signature)
len_sig = len(hex_png_signature)
print(f"length of png signature is: {len_sig}")

with open('./flag2.png.enc', 'rb') as f:
    # get first 8 bytes and xor with png signature to get first 8 bytes of the key
    ind = 0
    while ind < len_sig:
        byte = f.read(1)
        
        if not byte:
            break
        key_byte = byte[0] ^ hex_png_signature[ind]
        hex_key[ind] = key_byte
        print(f"byte is {byte.hex()} and byte of png signature is {hex_png_signature[ind]:02x}. Thus, key byte is: {key_byte:02x}")
        ind += 1
    print(f"key after first 8 bytes: {hex_key.hex()}")

    # ----------------------------------------------------------------
    # next 4 bytes tells how long the next chunk is. Since the first chunk is IHDR, we can use that to get next 4 bytes of key
    # IHDR length is always 13 bytes, so next 4 bytes should be 00 00 00 0D
    next_bytes = '0000000d'  # 4 bytes
    hex_next_bytes = bytes.fromhex(next_bytes)
    len_next = len(hex_next_bytes)
    print(f"length of next bytes is: {len_next}")

    stop = ind + len_next
    i = 0
    while ind < stop:
        byte = f.read(1)
        
        if not byte:
            break
        key_byte = byte[0] ^ hex_next_bytes[i]
        hex_key[ind] = key_byte
        print(f"byte is {byte.hex()} and byte of next bytes is {hex_next_bytes[i]:02x}. Thus, key byte is: {key_byte:02x}")
        ind += 1
        i += 1
    print(f"key after next 4 bytes: {hex_key.hex()}")

    # ----------------------------------------------------------------
    # Next chunk tells us the next 13 bytes since IHDR chunk is always 13 bytes long.
    # However since the key is only 20 bytes long, we only need to check the next 8 bytes of the key
    # The first 4 bytes of the IHDR chunk is always '49484452' (IHDR in ASCII) - In decimal: 73 72 68 82 (also from link in exercise description)
    ihdr_bytes = '49484452'  # 4 bytes
    hex_ihdr_bytes = bytes.fromhex(ihdr_bytes)
    len_ihdr = len(hex_ihdr_bytes)
    print(f"length of IHDR bytes is: {len_ihdr}")

    stop = ind + len_ihdr
    i = 0
    while ind < stop:
        byte = f.read(1)
        
        if not byte:
            break
        key_byte = byte[0] ^ hex_ihdr_bytes[i]
        hex_key[ind] = key_byte
        print(f"byte is {byte.hex()} and byte of IHDR bytes is {hex_ihdr_bytes[i]:02x}. Thus, key byte is: {key_byte:02x}")
        ind += 1
        i += 1
    print(f"key after next 4 bytes: {hex_key.hex()}")

    # The next 13 bytes are the chunk data. The first 4 bytes of the IHDR chunk are the width of the image.
    # From the question description, we know the width is 655 pixels (0x028f).
    width_bytes = '0000028f'  # 4 bytes
    hex_width_bytes = bytes.fromhex(width_bytes)
    len_width = len(hex_width_bytes)
    print(f"length of width bytes is: {len_width}")

    stop = ind + len_width
    i = 0
    while ind < stop:
        byte = f.read(1)
        
        if not byte:
            break
        key_byte = byte[0] ^ hex_width_bytes[i]
        hex_key[ind] = key_byte
        print(f"byte is {byte.hex()} and byte of width bytes is {hex_width_bytes[i]:02x}. Thus, key byte is: {key_byte:02x}")
        ind += 1
        i += 1
    print(f"key after next 4 bytes: {hex_key.hex()}")


# ----------------------------------------------------------------
# Now we have the full key, we can decrypt the rest of the file

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