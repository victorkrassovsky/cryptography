# pads a byte array to be a multiple of 512 bits in preperation for hashing
def pad_to_512(b):
    binary = b+(1).to_bytes(1,'little')
    pad = 64 - (len(binary) % 64)
    binary = binary + b'\x00'*pad
    return binary

# xors two 4 byte words
def xor_words(b1,b2):
    return b''.joint([(x^y).to_bytes(1,'big') for x,y in zip(b1,b2)])

#xors three 4 byte words
def xor_three_words(b1,b2,b3):
    return xor_words(b1,xor_words(b2,b3))

# right rotates a 4 byte word n times
def right_rotate_words(word, n):
    b = int.from_bytes(word,'big')
    n = n%32
    new_word = (b >> n) ^ ((b%(1<<n)) << (32-n))
    return  new_word.to_bytes(4,'big')

#right shifts a 4 byte word n times
def right_shift_word(word, n):
    b = int.from_bytes(word,'big')
    n=n%32
    new_word = b >> n
    return new_word.to_bytes(4,'big')

#ands two 4 byte words
def and_words(b1,b2):
    return b''.join([x & y for x,y in zip(b1,b2)])

#nots a 4 byte word
def not_word(by):
    return b''.join([~x for x in by])

#sums a list of 4 byte words
def add_words(b_list):
    total = 0
    for b in b_list:
        total += int.from_bytes(b,'big')
    return (total % (1 << 32)).to_bytes(4)

def sha256 (b):
    binary = pad_to_512(b)
    chunks = [binary[i:i+64] for i in range(0,len(binary),64)]
    
    h = "6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19".split(' ')
    h = [bytes.fromhex(x) for x in h]
    k ="""428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
    27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85
    a2bfe8a1 a81a664b c24b8b70 c76c51a3 d192e819 d6990624 f40e3585 106aa070
    19a4c116 1e376c08 2748774c 34b0bcb5 391c0cb3 4ed8aa4a 5b9cca4f 682e6ff3
    748f82ee 78a5636f 84c87814 8cc70208 90befffa a4506ceb bef9a3f7 c67178f2""".split(" ")
    k = [bytes.fromhex(x) for x in k]
    
    for block in chunks:
        w = [bytes(4)]*64
        for i in range(16):
            w[i] = block[4*i:4*i+4]
        for i in range(16, 64):
            s0 = xor_three_words(right_rotate_word(w[i-15],7), right_rotate_word(w[i-15],18), right_shift_word(w[i-15],3))
            s1 = xor_three_words(right_rotate_word(w[i-2], 17), right_rotate_word(w[i-2],19), right_shift_word(w[i-2],10))
            w[i] = add_words([int.from_bytes(w[i-16], 'big') + int.from_bytes(s0,'big') + int.from_bytes(w[i-7],'big') + int.from_bytes(s1,'big')])
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for i in range(64):
            s1 = xor_three_words(right_rotate_word(e,6),right_rotate_word(e, 11), right_rotate_word(e, 25))
            ch = xor_words(and_words(e,f), xor_words(not_word(e),g))
            temp1 = add_words([h,s1,ch,k[i],w[i]])
            s0 = xor_three_words(right_rotate_word(a,2),right_rotate_word(a,13), right_rotate_word(a,22))
            maj = xor_three_words(and_words(a,b), and_words(a,c), and_words(b,c))
            temp2 = add_words([S0, maj])


