import random
import string
import math
import collections

def key_to_binary(key):
    if isinstance(key, str):
        key = key.encode('utf-8')
    # Kiểm tra độ dài của key
    if len(key) > 8:
        key = key[:8]
    else:
        key = key.ljust(8, b'\0')
    return bin(int.from_bytes(key, 'big'))[2:].zfill(64)


def circular_shift(bits, amount):
    return bits[amount:] + bits[:amount]


def generate_subkeys(key):
    pc1_table = [57, 49, 41, 33, 25, 17, 9,
             1,  58, 50, 42, 34, 26, 18,
             10, 2,  59, 51, 43, 35, 27,
             19, 11, 3,  60, 52, 44, 36,
             63, 55, 47, 39, 31, 23, 15,
             7,  62, 54, 46, 38, 30, 22,
             14, 6,  61, 53, 45, 37, 29,
             21, 13, 5,  28, 20, 12, 4]


    pc2_table = [14, 17, 11, 24, 1,  5,
             3,  28, 15, 6,  21, 10,
             23, 19, 12, 4,  26, 8,
             16, 7,  27, 20, 13, 2,
             41, 52, 31, 37, 47, 55,
             30, 40, 51, 45, 33, 48,
             44, 49, 39, 56, 34, 53,
             46, 42, 50, 36, 29, 32]


    # convert the key to binary
    key_binary = key_to_binary(key)
    print(key_binary)
    # convert the key to a list of characters
    key_list = list(key_binary)
    print(key_list)
    key = [key_list[i - 1] for i in pc1_table]
    # apply PC-1 permutation to the key

   # split the key into two 28-bit halves
    L_key = key[:28]
    R_key = key[28:]

    subs = []
    for i in range(1, 17):
        # determine the shift amount based on the current round
        if i in [1, 2, 9, 16]:
            shift_amount = 1
        else:
            shift_amount = 2

        # perform a circular L shift on each key of the key
        L_key = circular_shift(L_key, shift_amount)
        R_key = circular_shift(R_key, shift_amount)

        # combine the two halves and apply PC-2 permutation
        combined_key = L_key + R_key
        sub = [combined_key[i - 1] for i in pc2_table]
        subs.append(sub)

    return subs


def BangGhiNgauNhien():
    key = []
    for x in range(16):
        k = random.randint(0,9)
        key.append(k)
    string = ''.join(map(str,key))
    return string
    

# string = 'REPIYDBA'
# subkes = generate_subkeys(string)
# print(subkes)


# Generate a random sequence of 64 bits
bits = [random.randint(0, 1) for i in range(64)]

# Convert the bits to a binary string
bit_str = ''.join(map(str, bits))


def binary_to_char (bit_str):

    # Convert the binary string to an ASCII string
    ascii_str = ''.join(chr(int(bit_str[i:i+8], 2)) for i in range(0, len(bit_str), 8))

    # Convert the ASCII string to an alphabet string
    offset = ord('A')
    string = ''.join(chr((ord(c) + offset) % 26 + offset) for c in ascii_str)

    return string

key_str = binary_to_char (bit_str)
subkeys = generate_subkeys(key_str)
print(subkeys)
# convert the key to binary
key_binary = key_to_binary(key_str)


with open('./PC2_key_10times.txt', 'w') as f:
    f.write("key: " + key_str)
    f.write("\nPC-1:\n" + key_binary + "\nPC-2:")
    for x, subkeys in enumerate(subkeys):
        f.write(f"\n{''.join(subkeys)}")

# ====================================== #
def split_64bit_array_to_8_blocks(s):
    return [s[i:i+8] for i in range(0, len(s), 8)]

def get_val_Sboxes(i,row,col):
    #S_BOXES =   
    S1 =[   [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
            [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
            [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
            [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
        ]
    S2 =[   [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
            [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
            [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
            [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
        ]
    S3 =[   [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
            [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
            [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
            [ 1, 10, 13,  0, 11,  8,  3,  4,  9,  5,  6,  7, 12,  2, 14, 15],
        ]
    S4 =[   [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
            [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
            [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
            [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
        ]
    S5 =[   [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
            [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
            [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
            [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
        ]
    S6 =[   [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
            [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
            [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
            [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
        ]
    S7 =[   [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5,  10, 6,  1],
            [15, 12,  1, 10,  6,  9, 11,  3, 14,  5,  0,  8, 12,  7, 13,  2],
            [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
            [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
            [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
        ]
    S8 =[   [12,  9,  0,  7,  9,  2, 14,  1, 10, 15,  3,  4,  6, 12,  5, 11],
            [10, 14,  1,  5,  3,  8,  9,  6, 15, 12,  0, 13, 11,  7,  2,  4],
            [ 3,  2, 12, 13,  6,  9,  5, 15, 10, 11, 14,  0,  8,  4,  7,  1],
            [13, 10, 11,  6,  7,  0,  8,  1,  4, 15,  3,  5, 12,  2, 14,  9],
        ]
    
    S = [S1, S2, S3, S4, S5, S6, S7, S8]
    return S[i-1][row][col]

def find_row_column(array_list):
    rc = []
    for i, item in enumerate(array_list):
        row = int(item[0] + item[5:], 2)
        col = int(item[1:5], 2)
        rc.append([i+1, row, col])
    return rc

def PofTypings(bgnn):
    # Bảng hoán vị IP
    PoT_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    # Bảng hoán vị IP ngược
    ip_table_inv = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]

    # Bảng hoán vị P
    p_table = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]

    # Bảng hoán vị E
    Exp_table = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    pot_bit = key_to_binary(bgnn)
    print(pot_bit)

    pot_list = list(pot_bit)
    Pote = [pot_list[i - 1] for i in PoT_table]
    print(Pote)
    # split the Pote into two 28-bit halves
    L_Pote = Pote[:32]
    R_Pote = Pote[32:]
    print(R_Pote)
    
    Exp_Pote = [R_Pote[i - 1] for i in Exp_table]
    print(Exp_Pote)
    string_Exp_Pote = ''.join(map(str,Exp_Pote))
    R6bit_SBoxes = split_64bit_array_to_8_blocks(string_Exp_Pote)
    print(R6bit_SBoxes)
    frc = find_row_column(R6bit_SBoxes)
    print(frc)
    res_per_IP = []
    for it in frc:
        res_tb = get_val_Sboxes(it[0],it[1],it[2])
        print(res_tb)
        res_bit = format(res_tb, '04b')
        print(res_bit)
        res_per_IP.append(res_bit)
    L_per_IP = ''.join(map(str,res_per_IP))
    lpIP = [i for i in L_per_IP]
    
    L_Pote = [lpIP[i - 1] for i in p_table]

    L_Pote = ''.join(map(str,L_Pote))
    R_Pote = ''.join(map(str,R_Pote))
    end_Pot = R_Pote + L_Pote
    print(end_Pot)
    new_Pot = binary_to_char(end_Pot)
    print(new_Pot)

# born random M
bgnn = BangGhiNgauNhien()
print(bgnn)

PofTypings(bgnn)
