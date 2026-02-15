from Crypto.Util import number
import math

e = 65537
n = 0x87a985ec5133747a82cd17de68ab83c0f5766ae7b3336ca432ff91d7271b1afdb4a2515bad8ac431d20d87fce5faeb5e0eaf757154d2213037109b3e9f2678a164c2453df140b5ad5bb78a71349ca843f5bc51e1edc073ee87f115df7f4b7d83ebdade0bff9b8c366fd488a29bf9d80ae91ab547b009651a22cc9b953a50ff0141b40e14f0f9c8e6e0f4fc235fc59c4f0f8e9fee1b14331a0cd056834d1ced5d2661ef01b222d6ed168fbb72d34aeb52e113d5514e91c87dc07b5253cdaabfd939b296f9d27f13d9f441b97c599b5086ddac5e1a91bba8f9a46abd4f7a437ff654c4aca52cf713ca5461ab5ee81b7d5e342689cb4da36809fa5fc18356a2d7b3
flag = 0x7ad27404f189b12838e91c4af8a0766299af402d9f9ccfcc32cd0a1fec9a9efddd52680a5a65e84338a23322044c7d38d58b64b74e72532dac63b384f7dd2f322494767eade65499b5f9d387cd4c16d5fe5747f3bfef5db2e7c03eb34947860f5eb9362bc5935c1191d2d468c632657ba17cda19ea2049268b651dbe0edccff1bd9e71309a712aa626ecbf28476040706edaca69f4132bcabed0a186b36ae9b905e99717f83e436f30d65cc020ed45487e5fd61051ce8555108a76810c201aeb57b33403964a686f3fa971c50bee957933e3aa38c81f4236d30a84124ffdd2bb21cca8bf5441e54451cef552e5326464ad120d4ea9287c469715096960ac759e
# since p and q are 1024 bit primes that are close to each other 
# so we take the square root of n and try to check nearby primes as potential candidates for p and q
cnt = 0

# calculate the sqrt of n 
p = math.isqrt(n)


while not number.isPrime(p):
    p += 1
    cnt += 1
    if n % p != 0:
        continue
    q = n // p
    phi_n = (p-1) * (q-1)
    d = pow(e, -1, phi_n)
    decrypted_flag = pow(flag, d, n)
    try:
        plaintext = bytes.fromhex(hex(decrypted_flag)[2:]).decode(errors='ignore')
        if plaintext[0:4] == "cpsc":
            print(f"Decrypted plaintext: {plaintext}")
            break
    except Exception:
        continue

    if cnt > 10000: # we can try a few values of p and q to see if we get a valid plaintext
        print("Tried 10000 values of p and q, but couldn't find the correct plaintext. Exiting...")
        break