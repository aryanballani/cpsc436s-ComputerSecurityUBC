from Crypto.Util import number
import hashlib

message = "qwertyuiasdfghjkwertyui436sSIG{6639af226df1e93b7cf98d710998bff1}"
e = 49939

p = number.getPrime(1024)
q = number.getPrime(1024)

n = p*q
print("n is", n)
phi_n = (p-1) * (q-1)
print("phi_n is", phi_n.bit_length(), "bits long")
# check how many bits d is 
d = pow(e, -1, phi_n)
print("d is", d)
print("d is", d.bit_length(), "bits long")

# =====
# how to hash 
hash_message = hashlib.sha256(message.encode()).digest()
h_m = int.from_bytes(hash_message, "big")

# print(h_m)

signature = pow(h_m, d, n)
print("signature is", signature)