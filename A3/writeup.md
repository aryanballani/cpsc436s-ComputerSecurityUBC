just followed the flow of the example on slides, the discrete log of \
y = g^x mod p \
is a difficult one , but mathematically we can take p-1 and calculate it's prime factors (if it is not very big this will be easy) \ 
and after we have all the prime factors for p-1 we can solve a smaller discrete log problem to obtain x. \
(the math works 🥳 and i am not very good at proves 🙏)

in the end we have a bunch of mod equations with x and all the primes factors as mod fields and we can use the chineese remainder theorem to solve the system of equations to obtain `x`. 


