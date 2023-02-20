#Homework Number: 04
#Name: Jack Gardner
#ECN Login: gardne97
#Due Date: 2/16/23

import sys
from BitVector import *
AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []  
one = BitVector(intVal=1, size=128)

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words   

#The above functions are all borrowed from the lecture code

def get_key(keyfile):
    #read key from file
    FO = open(keyfile, 'r')
    key = FO.read()
    key = BitVector(textstring = key)
    return key

def substitute(bv):
    #inverse sub bytes step
    for i in range(16):
        n = to_int(bv[i*8:i*8+8])
        n = subBytesTable[n]
        bv[i*8:i*8+8] = BitVector(intVal=n, size=8)
    return bv


def shift_rows(statearray):
    #shift rows step
    statearray_copy = [[0 for x in range(4)] for x in range(4)]
    statearray_copy[0] = [statearray[0][0], statearray[0][1], statearray[0][2], statearray[0][3]]
    statearray_copy[1] = [statearray[1][1], statearray[1][2], statearray[1][3], statearray[1][0]]
    statearray_copy[2] = [statearray[2][2], statearray[2][3], statearray[2][0], statearray[2][1]]
    statearray_copy[3] = [statearray[3][3], statearray[3][0], statearray[3][1], statearray[3][2]]


    return(statearray_copy)


def mix_columns(statearray):
    bs2 = BitVector(intVal = 2)
    bs3 = BitVector(intVal = 3)
    #mix columns step
    statearray_copy = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
        statearray_copy[0][i] = statearray[0][i].gf_multiply_modular(bs2, AES_modulus, 8) ^ statearray[1][i].gf_multiply_modular(bs3, AES_modulus, 8) ^ statearray[2][i] ^ statearray[3][i]
        statearray_copy[1][i] = statearray[1][i].gf_multiply_modular(bs2, AES_modulus, 8) ^ statearray[2][i].gf_multiply_modular(bs3, AES_modulus, 8) ^ statearray[3][i] ^ statearray[0][i]
        statearray_copy[2][i] = statearray[2][i].gf_multiply_modular(bs2, AES_modulus, 8) ^ statearray[3][i].gf_multiply_modular(bs3, AES_modulus, 8) ^ statearray[0][i] ^ statearray[1][i]
        statearray_copy[3][i] = statearray[3][i].gf_multiply_modular(bs2, AES_modulus, 8) ^ statearray[0][i].gf_multiply_modular(bs3, AES_modulus, 8) ^ statearray[1][i] ^ statearray[2][i]
    return statearray_copy


def decomp_sa(statearray):
    bv = BitVector(size=0)
    for j in range(4):
        for k in range(4):
            bv += statearray[k][j]
    return(bv)

def create_sa(bv):
    statearray = [[0 for x in range(4)] for x in range(4)]
    for j in range(4):
        for k in range(4):
            statearray[k][j] = bv[8*k + 32 * j:8*k + 32 * j + 8]
    return statearray

def print_sa(statearray):
    #testing function to print statearray
    for j in range(4):
        print(statearray[j][0].get_hex_string_from_bitvector() + statearray[j][1].get_hex_string_from_bitvector() + statearray[j][2].get_hex_string_from_bitvector() + statearray[j][3].get_hex_string_from_bitvector())        


        
    #statearray = [[0 for x in range(4)] for x in range(4)]
    '''for k in range(len(out)):
        for i in range(4):
            for j in range(4):
                statearray[j][i] = out[k][8*j + 32 * i:8*j + 32 * i + 8]
                statearray[j][i] = BitVector(intVal = encryption_S_box[to_int(statearray[j][i])])
                print(statearray[j][i])
        out[k] = statearray'''
            #print(len(bitvec))
            #print(len(keys[0]))


def to_int(bs):
    bs = bs.get_hex_string_from_bitvector()
    return(int(bs, 16))

def encrypt(keys, FI, iv):
    out = []
    pt = []
    bs = FI.read(16)
    #generate key schedule and tables
    while bs:
        pt.append(BitVector(rawbytes = bs))
        bitvec = iv
        #print(bitvec)
        if len(bitvec) > 0:
            if len(bitvec) < 128:
                bitvec.pad_from_right(128 - len(bitvec))
            #initial key xoring
            out1 = bitvec[0:32].__xor__(keys[0])
            out2 = bitvec[32:64].__xor__(keys[1])
            out3 = bitvec[64:96].__xor__(keys[2])
            out4 = bitvec[96:128].__xor__(keys[3])
            out.append(out1 + out2 + out3 + out4)
        iv.set_value(intVal = to_int(iv) + 1, size = 128)
        bs = FI.read(16)
    print("out")
    for n in range(14):
        for i in range(len(out)):
            # 4 steps: substitute, shift rows, mix columns, add key
            out[i] = substitute(out[i])
            statearray = create_sa(out[i])
            statearray = shift_rows(statearray)
            #skip on last iteration
            if(n != 13):
                statearray = mix_columns(statearray)
            out[i] = decomp_sa(statearray)
            out[i][0:32] = out[i][0:32] ^ keys[4 *(n + 1)]
            out[i][32:64] = out[i][32:64] ^ keys[4 * (n + 1) + 1]
            out[i][64:96] = out[i][64:96] ^ keys[4 * (n + 1) + 2]
            out[i][96:128] = out[i][96:128] ^ keys[4 * (n + 1) + 3]
    for n in range(len(pt)):
        if len(pt[n]) < 128:
            pt[n].pad_from_right(128 - len(bitvec))
        out[n] = out[n] ^ pt[n]

    return out

def ctr_aes_image(iv, fin, fout, fkey):
    key = get_key(fkey)
    genTables()
    keys = gen_key_schedule_256( key )
    FILEOUT = open(fout, 'wb')
    FIN = open(fin, 'rb')
    for k in range(3):
        FILEOUT.write(FIN.readline())
    out = encrypt(keys, FIN, iv)
    for i in range(len(out)):
        out[i].write_to_file(FILEOUT)
    FILEOUT.close
    #print('\n\n\n')

if __name__ == "__main__":
    iv = BitVector(textstring='computersecurity')
    ctr_aes_image(iv,'image.ppm','out_image.ppm','keyCTR.txt')