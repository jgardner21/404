import sys
from BitVector import *
AES_modulus = BitVector(bitstring='100011011')

encryption_S_box = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]


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

def get_key(keyfile):
    FO = open(keyfile, 'r')
    key = FO.read()
    key = BitVector(textstring = key)
    return key

def encrypt(key, fin):
    out = []
    keys = gen_key_schedule_256( key )
    bv = BitVector( filename = fin )
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128 )
        #print(bitvec)
        if len(bitvec) > 0:
            if len(bitvec) < 128:
                bitvec.pad_from_right(128 - len(bitvec))
            out1 = bitvec[0:32].__xor__(keys[0])
            out2 = bitvec[32:64].__xor__(keys[1])
            out3 = bitvec[64:96].__xor__(keys[2])
            out4 = bitvec[96:128].__xor__(keys[3])
            out.append(out1 + out2 + out3 + out4)
    for i in range(len(out)):
        for j in range(16):
            print(out[i].get_hex_string_from_bitvector())
            #out[i][(j*8):(j*8)+8].permute(encryption_S_box)
            print(out[i][(j*8):(j*8)+8].size)

    #statearray = [[0 for x in range(4)] for x in range(4)]
    '''for k in range(len(out)):
        for i in range(4):
            for j in range(4):
                statearray[j][i] = out[k][8*j + 32 * i:8*j + 32 * i + 8]
                statearray[j][i] = BitVector(intVal = encryption_S_box[to_int(statearray[j][i])])
                print(statearray[j][i])
        out[k] = statearray'''

    return(out)
            #print(len(bitvec))
            #print(len(keys[0]))


def to_int(bs):
        integer = 0
        for i in range(len(bs)):
            if bs[i] == '1':
                integer += 2**(len(bs) - 1 - i)
        return integer

def decrypt():
    pass

if __name__ == "__main__":
    keyfile = sys.argv[3]
    key = get_key(keyfile)
    if(sys.argv[1] == '-e'):
        FILEOUT = open(sys.argv[4], 'w')
        out = encrypt(key, sys.argv[2])
        for i in range(len(out)):
            FILEOUT.write(out[i].get_hex_string_from_bitvector())
        FILEOUT.close
    #print('\n\n\n')
    else:
        FO2 = open(sys.argv[4], 'w')
        out = decrypt(key, sys.argv[2])
        for i in range(len(out)):
            FO2.write(out[i])