from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

shared_key = "5517884560197983135869892901579348204787724654473775012698264817211381680355336937007985374377047933819001620978764107629700463062829023894579024606480381922155981796526088366548077108245830792432301807361261131096422792307699143237957930687286261207699792527694145172898299152760742674424718054768916738305"
bytes_key = int(shared_key).to_bytes((int(shared_key).bit_length() + 7) // 8, 'big')

aes_key = bytes_key[-16:]  # Use the last 128 bits for AES-128 key
print(aes_key.hex())  # Print the AES key in hexadecimal format
iv= bytes.fromhex("8e908d01c6abb2c3732fa0f595f86e16")
encrypted_message = bytes.fromhex("25deee8c810ee92a545edf18840d388bd2107c212e05eb3d645cacc78828110c32ce3e47f0990703cb6047f3d6904621")

aes = AES.new(aes_key, AES.MODE_ECB)

# since this is AES 128 encryption, block size is 16 bytes
cipher_blocks = [encrypted_message[i:i+16] for i in range(0, len(encrypted_message), 16)]
prev = iv
pt = b''

for c in cipher_blocks:
    d = aes.decrypt(c)
    p = bytes(x ^ y for x, y in zip(d, prev))
    pt += p
    prev = c

pt = unpad(pt, 16)
print(pt)
