from BitVector import *
from PrimeGenerator import PrimeGenerator
import sys

ee = 65537
mask = 1 << 126

def gcd_modified(a,b):
    a -= 1
    while b:
        a,b = b, a % b
    return a

def genkey(f1, f2):
    generator = PrimeGenerator(bits = 128)
    print(mask)
    while True:
        p = generator.findPrime()
        q = generator.findPrime()
        if p != q and p > mask and q > mask and gcd_modified(p,ee) == 1 and gcd_modified(q, ee) == 1:
            break
    POUT = open(f1, 'w')
    QOUT = open(f2, 'w')
    POUT.write(str(p))
    QOUT.write(str(q))
    POUT.close()
    QOUT.close()

def encrypt(mfile, pfile, qfile, outfile):
    mbv = BitVector(filename=mfile)
    qbv = BitVector(filename=qfile)
    pbv = BitVector(filename=pfile)

    q = qbv.read_bits_from_file(128)
    p = pbv.read_bits_from_file(128)
    n = int(p) * int(q)
    totient = BitVector(intVal=((int(p)-1)*(int(q)-1)))
    e = BitVector(intVal=ee)
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
    pass

if __name__ == "__main__":
    if sys.argv[1] == '-g':
        genkey(sys.argv[2],sys.argv[3])
    elif sys.argv[1] == '-e':
        encrypt(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == '-d':
        decrypt(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("Please enter valid arguments")