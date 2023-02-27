from BitVector import *
from PrimeGenerator import PrimeGenerator
import sys

e = 65537
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
        if p != q and p > mask and q > mask and gcd_modified(p,e) == 1 and gcd_modified(q, e) == 1:
            break
    POUT = open(f1, 'w')
    QOUT = open(f2, 'w')
    POUT.write(str(p))
    QOUT.write(str(q))
    POUT.close()
    QOUT.close()


if __name__ == "__main__":
    if sys.argv[1] == '-g':
        genkey(sys.argv[2],sys.argv[3])