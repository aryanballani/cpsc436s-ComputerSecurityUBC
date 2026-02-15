iv_base = '72 dd 6c f5 76 85 98 3f 3f 40 a7 0f 7e 1d 2b f3'

# for i in range(256):
#     print("654a515b4005a24f5a474440f888bfb3")

incorrect_pad_val = 0x07
padding_val = 0x10
intermediate_val = incorrect_pad_val ^ padding_val
print(f"Intermediate byte value: {intermediate_val:02x}")

l = [0xe8, 0x0a, 0x91, 0x41, 0xb4, 0xaa, 0x59, 0x59, 0x79, 0x97, 0x3f, 0x1a, 0x2a, 0x4d, 0xca]
l.insert(0, intermediate_val)

for i in range(len(l)):
    l[i] ^= len(l) + 1
    l[i] = f"{l[i]:02x}"
    
# Print new IV candidates
for i in range(256):
    print("00"*(15 - len(l)) + format(i, "02x") + "".join(l))
