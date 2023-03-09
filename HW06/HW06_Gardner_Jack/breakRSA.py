#Homework Number: 06
#Name: Jack Gardner
#ECN Login: gardne97
#Due Date: 3/1/23

import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator
from solve_pRoot import solve_pRoot

ee = 3

def gcd_modified(a,b):
    a -= 1
    while b:
        a,b = b, a % b
    return a

def genkey():
    generator = PrimeGenerator(bits = 128)
    while True:
        p = generator.findPrime()
        q = generator.findPrime()
        if p != q and p >> 126 == 0b11 and q >> 126 == 0b11 and gcd_modified(p,ee) == 1 and gcd_modified(q, ee) == 1:
            break
    return p, q

def encrypt(mfile, outfile):
    mbv = BitVector(filename=mfile)
    p,q = genkey()
    n = p * q
    FOUT = open(outfile,'w')
    while mbv.more_to_read:
        temp = mbv.read_bits_from_file(128)
        if len(temp) < 128:
            temp.pad_from_right(128 - len(temp))
        textout = pow(int(temp), ee, n)
        fluffy = BitVector(intVal=int(textout),size=256)
        '''for i in range(len(fluffy)):
            print(fluffy[i],end = '')
        print('\n')'''
        FOUT.write(fluffy.get_hex_string_from_bitvector())
    FOUT.close()
    return n

def crt(ns, cs):
    total = 0
    N = ns[0] * ns[1] * ns[2]
    tuples = [(ns[0],cs[0]),(ns[1],cs[1]),(ns[2],cs[2])]
    for n,c in tuples:
        p = N // n 
        total += c * p * int(BitVector(intVal=p).multiplicative_inverse(BitVector(intVal=n)))
    return total % N

def crack(fe1,fe2,fe3,fn,fout):
    NS = open(fn,'r')
    n1 = int(NS.readline())
    n2 = int(NS.readline())
    n3 = int(NS.readline())
    bign = n1 * n2 * n3
    IN1 = open(fe1,'r')
    IN2 = open(fe2,'r')
    IN3 = open(fe3,'r')
    hs1 = IN1.read()
    hs2 = IN2.read()
    hs3 = IN3.read()
    i = 0
    FOUT = open(fout,'w')
    while i < len(hs1):
        m1 = BitVector(hexstring=hs1[i : i + 64])
        m2 = BitVector(hexstring=hs2[i : i + 64])
        m3 = BitVector(hexstring=hs3[i : i + 64])
        i += 64
        a = crt([n1,n2,n3],[int(m1),int(m2),int(m3)])
        out = BitVector(intVal=solve_pRoot(3,a),size=128)
        FOUT.write(out.get_text_from_bitvector())
    FOUT.close()

if __name__ == "__main__":
    if sys.argv[1] == '-e':
        ns = []
        temp = encrypt(sys.argv[2], sys.argv[3])
        ns.append(temp)
        temp = encrypt(sys.argv[2], sys.argv[4])
        ns.append(temp)
        temp = encrypt(sys.argv[2], sys.argv[5])
        ns.append(temp)
        FOUT = open(sys.argv[6],'w')
        for i in ns:
            FOUT.write(str(i))
            FOUT.write('\n')
    elif sys.argv[1] == '-c':
        crack(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
