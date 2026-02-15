m1 = {"protected": true, "data": <FLAG>} \
m2 = {"protected": false, "data": <FLAG>}

Also from prev tutorials we know that \
let m2 $\equiv$ m1 + x mod n \
so, m2 - m1 $\equiv$ x mod n 



E(m2) = E(m1 + x) = E(D(E(m1)E(x))) = E(m1)E(x)

now the only catch is finding the additive inverse of m1 that flips the `true` to `false` which is x. We use a trick for that -> 

i ran an experiment first:
```
# ===== experiment =======
# use flags to simulate from prev questions
m1 = "{\"protected\": true, \"data\": \"cpsc436s{acc4c9769ab832942a3d3f56fd935db9}\"}"  
m2 = "{\"protected\": false, \"data\": \"cpsc436s{acc4c9769ab832942a3d3f56fd935db9}\"}"
m3 = "{\"protected\": true, \"data\": \"cpsc436s{26519cb394d2caadfbf0f25702d1ca6f}\"}"
m4 = "{\"protected\": false, \"data\": \"cpsc436s{26519cb394d2caadfbf0f25702d1ca6f}\"}"

print("Diff btw true and false strings with flag1 as data", int.from_bytes(m2.encode(), 'big') - int.from_bytes(m1.encode(), 'big'))
print("Diff btw true and false strings with flag2 as data", int.from_bytes(m4.encode(), 'big') - int.from_bytes(m3.encode(), 'big'))
```

`Diff btw true and false strings with flag1 as data 7766002641839691383578911736931355187460913150939253324404400677034740542591695375121159605413481068245423699477771258100531556486288214698711277194499925446809546750215994736640
Diff btw true and false strings with flag2 as data 7766002641839691383578911736931355187460913150939253324404400677034740542591695375121159605413481068245423699477771258100531556486288214698711277194499925446809546750215994736640
`

this observation should be more or less consistent as long as data is 42 bytes. so we know that to change the `true` to `false` the additive inverse in the mod n field should be this number (atleast for the 42 bit flag), since the int diff is a result of changing `true` to `false` when everything else remains the same. 

Here is the rest of the script

```
def encrypt(m):
    c = pow(g, m, n**2) * pow(r, n, n**2) % (n**2)
    return c

# ===== experiment =======
m1 = "{\"protected\": true, \"data\": \"cpsc436s{acc4c9769ab832942a3d3f56fd935db9}\"}"
m2 = "{\"protected\": false, \"data\": \"cpsc436s{acc4c9769ab832942a3d3f56fd935db9}\"}"
m3 = "{\"protected\": true, \"data\": \"cpsc436s{26519cb394d2caadfbf0f25702d1ca6f}\"}"
m4 = "{\"protected\": false, \"data\": \"cpsc436s{26519cb394d2caadfbf0f25702d1ca6f}\"}"

print("Diff btw true and false strings with flag1 as data", int.from_bytes(m2.encode(), 'big') - int.from_bytes(m1.encode(), 'big'))
print("Diff btw true and false strings with flag2 as data", int.from_bytes(m4.encode(), 'big') - int.from_bytes(m3.encode(), 'big'))

x = int.from_bytes(m2.encode(), 'big') - int.from_bytes(m1.encode(), 'big')
ex = encrypt(x)
print("Encryption of x:", ex)
# let us try to multiply the encrypted message with the encryption of x, which should give us 
# the encryption of the json by changing true to false 
encrypted_protected_false = encrypted_flag * ex % (n**2)
print("flipped protected encrypted message", encrypted_protected_false)
```


