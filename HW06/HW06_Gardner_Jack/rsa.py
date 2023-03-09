#Homework Number: 06
#Name: Jack Gardner
#ECN Login: gardne97
#Due Date: 3/1/23

from BitVector import *
from PrimeGenerator import PrimeGenerator
import sys

ee = 65537

def gcd_modified(a,b):
    a -= 1
    while b:
        a,b = b, a % b
    return a

def genkey(f1, f2):
    generator = PrimeGenerator(bits = 128)
    while True:
        p = generator.findPrime()
        q = generator.findPrime()
        if p != q and p >> 126 == 0b11 and q >> 126 == 0b11 and gcd_modified(p,ee) == 1 and gcd_modified(q, ee) == 1:
            break
    POUT = open(f1, 'w')
    QOUT = open(f2, 'w')
    POUT.write(str(p))
    QOUT.write(str(q))
    POUT.close()
    QOUT.close()

def crt(p,q,c,d):
    qbv = BitVector(intVal=q,size=128)
    pbv = BitVector(intVal=p,size=128)
    vp = pow(c,d,p)
    vq = pow(c,d,q)
    qinv = qbv.multiplicative_inverse(pbv)
    pinv = pbv.multiplicative_inverse(qbv)
    xp = q * int(qinv)
    xq = p * int(pinv)
    return (vp * xp + vq * xq) % (p * q)

def encrypt(mfile, pfile, qfile, outfile):
    mbv = BitVector(filename=mfile)
    QIN = open(qfile,'r')
    PIN = open(pfile,'r')
    q = int(QIN.read())
    p = int(PIN.read())
    n = int(p) * int(q)
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

def decrypt(cfile, pfile, qfile, outfile):
    cbv = BitVector(filename=cfile)
    e = BitVector(intVal=ee)
    QIN = open(qfile,'r')
    PIN = open(pfile,'r')
    CIN = open(cfile,'r')
    q = int(QIN.read())
    p = int(PIN.read())
    tbv = BitVector(intVal=((p - 1) * (q - 1)))
    d = int(e.multiplicative_inverse(tbv))
    hs = CIN.read()
    FOUT = open(outfile,'w')
    i = 0
    while i < len(hs):
        bits = hs[i: i + 64]
        i += 64

        temp = BitVector(hexstring=bits)
        if len(temp) < 256:
            temp.pad_from_right(256 - len(temp))
        
        textout = crt(p,q,int(temp),d)
        bvt = BitVector(intVal=textout,size=256)
        bvt = BitVector(intVal=int(bvt),size=128)
        '''for i in range(len(fluffy)):
            print(fluffy[i],end = '')
        print('\n')'''

        FOUT.write(bvt.get_text_from_bitvector())
    FOUT.close()

if __name__ == "__main__":
    if sys.argv[1] == '-g':
        genkey(sys.argv[2],sys.argv[3])
    elif sys.argv[1] == '-e':
        encrypt(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == '-d':
        decrypt(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("Please enter valid arguments")