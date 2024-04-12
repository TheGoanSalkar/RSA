import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator

class RSA ():
    def __init__ (self , e) -> None :
        self .e = e
        self .n = None
        self .d = None
        self .p = None
        self .q = None

    
    def key_generator(self):
        generator = PrimeGenerator(bits = 128)
        
        while True:
            p = generator.findPrime()
            bv_p = BitVector(intVal = p)
            bv_p1 = BitVector(intVal = p - 1)
            q = generator.findPrime()
            bv_q = BitVector(intVal = q)
            bv_q1 = BitVector(intVal = q - 1)
            bv_e = BitVector(intVal = self.e)

            if bv_p[0] == 0 or bv_p[1] == 0 or bv_q[0] == 0 or bv_q[1] == 0:
                continue
            elif p == q:
                continue
            elif int(bv_p1.gcd(bv_e)) != 1 or int(bv_q1.gcd(bv_e)) != 1:
                continue
            else:
                break
        
        fp = open('p_test.txt', 'w')
        fp.write(str(p))
        fp.close()
        fq = open('q_test.txt', 'w')
        fq.write(str(q))
        fq.close()


    def set_primes(self, fp :str, fq :str) -> None :
        self.p = int(open(fp, "r").readlines()[0])
        self.q = int(open(fq, "r").readlines()[0])


    def encrypt (self , plaintext :str , ciphertext :str ) -> None :
        # your implemenation goes here
        self.n = self.p * self.q
        totient = (self.p - 1) * (self.q - 1)
        
        bv_modulus = BitVector(intVal = totient)
        bv_e = BitVector(intVal = self.e)
        bv_d = bv_e.multiplicative_inverse(bv_modulus)
        self.d = int(bv_d)

        bv_plaintxt = BitVector(filename = plaintext)
        f = open(ciphertext, "a")
        while (bv_plaintxt.more_to_read):
            bitvec = bv_plaintxt.read_bits_from_file( 128 )
            if len(bitvec) != 128:
                bitvec.pad_from_right(128 - len(bitvec))
            bitvec.pad_from_left(128)
            int_block = int(bitvec)
            cipher_block = (int_block ** self.e) % self.n
            cipher_bv = BitVector(intVal = cipher_block, size = 256)
            cipher_hex = cipher_bv.get_bitvector_in_hex()
            f.write(cipher_hex)
        f.close()


    def decrypt (self , ciphertext :str , recovered_plaintext :str ) -> None :
        # your implemenation goes here
        hex_str = open(ciphertext, "r").readlines()[0]
        bv = BitVector(hexstring = hex_str)

        FILEOUT = open('temp.bin', 'wb')
        bv.write_to_file(FILEOUT)
        FILEOUT.close()

        self.n = self.p * self.q
        totient = (self.p - 1) * (self.q - 1)
        bv_modulus = BitVector(intVal = totient)
        bv_e = BitVector(intVal = self.e)
        bv_d = bv_e.multiplicative_inverse(bv_modulus)
        self.d = int(bv_d)

        f = open(recovered_plaintext, "a", encoding='utf-8')
        bv = BitVector(filename = 'temp.bin')
        i = 0
        while (bv.more_to_read):
            bitvec = bv.read_bits_from_file( 256 )
            cipher_int = int(bitvec)

            v_p = pow(cipher_int, self.d, self.p)
            v_q = pow(cipher_int, self.d, self.q)
            
            bv_modulus = BitVector(intVal = self.p)
            bv_q = BitVector(intVal = self.q)
            bv_qInv = bv_q.multiplicative_inverse(bv_modulus)
            qInv = int(bv_qInv)

            bv_modulus = BitVector(intVal = self.q)
            bv_p = BitVector(intVal = self.p)
            bv_pInv = bv_p.multiplicative_inverse(bv_modulus)
            pInv = int(bv_pInv)

            x_p = self.q * qInv
            x_q = self.p * pInv

            plaintext_block = (v_p*x_p + v_q*x_q) % self.n
            bv_plaintext = BitVector(intVal = plaintext_block, size=256)
            [_, bv_plaintext] = bv_plaintext.divide_into_two()
                        
            plaintext_str = bv_plaintext.get_bitvector_in_ascii()
            f.write(plaintext_str)
        f.close()


if __name__ == "__main__":
    cipher = RSA (e= 65537 )
    if sys.argv[1] == "-g":
        cipher.key_generator()
    elif sys.argv [1] == "-e":
        cipher.set_primes(fp = sys.argv[3], fq = sys.argv[4])
        cipher.encrypt(plaintext = sys.argv[2], ciphertext = sys.argv[5])
    elif sys.argv [1] == "-d":
        cipher.set_primes(fp = sys.argv[3], fq = sys.argv[4])
        cipher.decrypt(ciphertext = sys.argv[2], recovered_plaintext =sys.argv[5])