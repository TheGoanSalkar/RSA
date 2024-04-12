import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator
import solve_pRoot

class RSA ():
    def __init__ (self , e) -> None :
        self .e = e

    
    def key_generator(self):
        generator = PrimeGenerator(bits = 128)
        p_list = []
        q_list = []
        
        for _ in range(3):
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
                elif p in p_list or q in q_list:
                    continue
                else:
                    p_list.append(p)
                    q_list.append(q)
                    break
        return p_list, q_list


    def encrypt (self , plaintext :str , ciphertexts :str , n_keyfile :str) -> None :
        # your implemenation goes here
        p_list, q_list = self.key_generator()
        n_list = [p * q for p,q in zip(p_list, q_list)]

        f = open(n_keyfile, 'w')
        f.write(str(n_list[0]) + '\n' + str(n_list[1]) + '\n' + str(n_list[2]))
        f.close()

        for i in range(3):
            n = n_list[i]            
            bv_plaintxt = BitVector(filename = plaintext)
            f = open(ciphertexts[i], "a")
            while (bv_plaintxt.more_to_read):
                bitvec = bv_plaintxt.read_bits_from_file( 128 )
                if len(bitvec) != 128:
                    bitvec.pad_from_right(128 - len(bitvec))
                bitvec.pad_from_left(128)
                int_block = int(bitvec)
                cipher_block = (int_block ** self.e) % n
                cipher_bv = BitVector(intVal = cipher_block, size = 256)
                cipher_hex = cipher_bv.get_bitvector_in_hex()
                f.write(cipher_hex)
            f.close()


    def decrypt (self , ciphertexts :str , n_keyfile :str , recovered_plaintext :str ) -> None :
        # your implemenation goes here
        encs = []
        for ciphertext in ciphertexts:
            f = open(ciphertext, "r")
            text = f.readlines()[0]
            encs.append(text)
            f.close()
        enc1 = encs[0]
        enc2 = encs[1]
        enc3 = encs[2]

        n_list = []
        f = open(n_keyfile, "r")
        for i in range(3):
            if i != 2:
                n_list.append(f.readline()[:-1])
            else:
                n_list.append(f.readline())
        f.close()
        n1 = int(n_list[0])
        n2 = int(n_list[1])
        n3 = int(n_list[2])
        N = n1 * n2 * n3

        n1_partial = N // n1
        n2_partial = N // n2
        n3_partial = N // n3

        n1_modulus = BitVector(intVal = n1)
        n2_modulus = BitVector(intVal = n2)
        n3_modulus = BitVector(intVal = n3)

        n1_partial_bv = BitVector(intVal = n1_partial)
        n2_partial_bv = BitVector(intVal = n2_partial)
        n3_partial_bv = BitVector(intVal = n3_partial)

        # xi is the inverse of ni_partial in ni
        x1 = int(n1_partial_bv.multiplicative_inverse(n1_modulus))
        x2 = int(n2_partial_bv.multiplicative_inverse(n2_modulus))
        x3 = int(n3_partial_bv.multiplicative_inverse(n3_modulus))
        
        bv1 = BitVector(hexstring = enc1)
        bv2 = BitVector(hexstring = enc2)
        bv3 = BitVector(hexstring = enc3)

        f = open(recovered_plaintext, "a", encoding = 'utf-8')
        for i in range(len(bv1) // 256):
            bitvec1 = bv1[256*i: 256*(i + 1)]
            bitvec2 = bv2[256*i: 256*(i + 1)]
            bitvec3 = bv3[256*i: 256*(i + 1)]

            m_cube = (((int(bitvec1)) * n1_partial * x1) + ((int(bitvec2)) * n2_partial * x2) + ((int(bitvec3)) * n3_partial * x3)) % N
            m = solve_pRoot.solve_pRoot(3, m_cube)
            m_bv = BitVector(intVal = m, size = 256)
            _, m_bv = m_bv.divide_into_two()
            m_str = m_bv.get_bitvector_in_ascii()
            f.write(m_str)
        f.close()


if __name__ == "__main__":
    cipher = RSA (e=3)
    if sys.argv [1] == "-e":
        cipher.encrypt(plaintext = sys.argv[2], ciphertexts = sys.argv[3:6], n_keyfile=sys.argv[6])
    elif sys.argv [1] == "-c":
        cipher.decrypt(ciphertexts = sys.argv[2:5], n_keyfile = sys.argv[5], recovered_plaintext =sys.argv[6])