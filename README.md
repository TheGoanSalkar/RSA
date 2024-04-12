# RSA
My implementation of the RSA (Rivest-Shamir-Adleman) Algorithm. I also showcase the drawbacks of using a low value for e (e = 3 in this case) by cracking it.

# message.txt
The message to be encrypted.

# p.txt, q.txt
The primes used in RSA encryption. They can also be generated via the PrimeGenerator.py code.

# encrypted.txt
The encrypted message using the RSA algorithm.

# enc1.txt, enc2.txt, enc3.txt
Three different encryptions of the message using three different self-generated public keys and e = 3 with the RSA algorithm.

# n_1_2_3.txt
The moduli used for encrypting the message 3 different ways.

# cracked.txt
The decrypted text, that was cracked using the three different encyrptions, and the three different moduli.

# solve_pRoot.py
The Python code to find the pth root of a number in an efficient and accurate way.

# PrimeGenerator.py
The Python code to generate a prime number.

# rsa.py
The Python code implementing the RSA algorithm.

# breakRSA.py
The Python code that breaks RSA using an application of the Chinese Remainder Theorem, and the fact that e has a low value (e = 3), which makes it easier to find the eth root of a number.
