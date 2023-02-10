import sys

#This code borrows from the provided FindMI.py given to us in the lecture code

def MIB(num, mod):
    num = int(num)
    mod = int(mod)
    sn = num
    sm = mod
    x, xo = 0, 1
    y, yo = 1, 0
    while mod:
        #print('Num: ' + str(num) + ' Mod: ' + str(mod) + ' = ' + str(bin_div(num,mod)) + ' Should be: ' + str(num // mod))

        q = bin_div(num, mod)
        num, mod = mod, num % mod
        #print('Q: ' + str(q) + ' X: ' + str(x) + ' = ' + str(bin_mult(q,x)) + ' Should be: ' + str(q * x))
        x, xo = xo - bin_mult(q, x), x
        #print('Q: ' + str(q) + ' X: ' + str(x) + ' = ' + str(bin_mult(q,y)) + ' Should be: ' + str(q * y))
        y, yo = yo - bin_mult(q, y), y
    if num != 1:
        pass
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (sn, sm, num))
    else:
        mi = (xo + sm) % sm
        print("\nMI of %d modulo %d is: %d\n" % (sn, sm, mi))

def bin_mult(a, b):
    if(a < 0) ^ (b < 0):
        sign = 1
    else:
        sign = 0   
    a = abs(int(bin(a), 2))
    b = bin(b)
    res = 0
    for i in range(len(b) - 1, -1, -1):
        if b[i] == '1':
            res += a << (len(b) - 1 - i)
    if sign:
        sres = res
        res -= sres
        res -= sres
    return res


def bin_div(a, b):
    if(a < 0) ^ (b < 0):
        sign = 1
    else:
        sign = 0   
    a = abs(a)
    b = abs(b)
    res = 0
    s = 0
    while b <= a:
        b = b << 1
        s +=1
    while s >= 0:
        if b <= a:
            res += 1 << s
            a -= b
        b = b >> 1
        s -= 1
    return res
    
if __name__ == "__main__":
    MIB(sys.argv[1], sys.argv[2])
    #print(bin_mult(int(sys.argv[1]), int(sys.argv[2])))
    #print(bin_div(int(sys.argv[1]), int(sys.argv[2])))