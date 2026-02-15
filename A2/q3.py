import struct

# Parameters matching how the original image was generated
WIDTH = 512 * 8  # 4096
HEIGHT = 32 * 8  # 256
BPP = 32  # RGBA -> 32 bits per pixel
PIXEL_OFFSET = 64  # choose 64 so pixel data starts at a 16-byte boundary (helps ECB block alignment)


with open('A2/flag.bmp.enc', 'rb') as f:
    ciphertext = f.read()

# Calculate expected raw image size
raw_img_size = WIDTH * HEIGHT * (BPP // 8)

# We'll use ciphertext as the pixel bytes (truncated or padded to raw_img_size)
pixel_bytes = ciphertext[:raw_img_size]
if len(pixel_bytes) < raw_img_size:
    pixel_bytes = pixel_bytes + b"\x00" * (raw_img_size - len(pixel_bytes))

# Build BMP file header (14 bytes)
bfType = b'BM'
bfSize = PIXEL_OFFSET + raw_img_size
bfReserved1 = 0
bfReserved2 = 0
bfOffBits = PIXEL_OFFSET
file_header = struct.pack('<2sIHHI', bfType, bfSize, bfReserved1, bfReserved2, bfOffBits)

# Build DIB header (BITMAPINFOHEADER, 40 bytes)
biSize = 40
biWidth = WIDTH
biHeight = HEIGHT
biPlanes = 1
biBitCount = BPP
biCompression = 0  # BI_RGB (no compression)
biSizeImage = raw_img_size
biXPelsPerMeter = 0
biYPelsPerMeter = 0
biClrUsed = 0
biClrImportant = 0

dib_header = struct.pack('<IIIHHIIIIII', biSize, biWidth, biHeight, biPlanes, biBitCount,
                         biCompression, biSizeImage, biXPelsPerMeter, biYPelsPerMeter,
                         biClrUsed, biClrImportant)

# Compose final BMP: header + (PIXEL_OFFSET - len(header)) padding + pixel bytes
header = file_header + dib_header

padding_between = PIXEL_OFFSET - len(header)

OUT_PATH = 'A2/valid_flag.bmp'
with open(OUT_PATH, 'wb') as out:
    out.write(header)
    out.write(b"\x00" * padding_between)
    out.write(pixel_bytes)

print('Wrote', OUT_PATH, 'file_size=', bfSize)
