import numpy as np
import aes128
import os

#takes a string, a 16 byte key and an optional iv and applies the cbc mode aes cipher to it
def aes_128_cbc_encrypt(plaintext, key, iv=os.urandom(16)):
    pt = bytes(plaintext,'utf-8')
    pad = 8-(len(pt)%8)
    pt = iv + pt + pad.to_bytes(1,'big')*pad
    pt_array = [pt[i:i+16] for i in range(0,len(pt),16)]
    ct_array = [None]*len(pt_array)
    ct_array[0] = pt_array[0]
    for i in range(1, len(pt_array)):
        ct_array[i] = aes128.encrypt(bytes(a^b for a,b in zip(pt_array[i-1],pt_array[i])),key)
    return b''.join([bytearray(x) for x in np.array(ct_array).T.tolist()])

def aes_128_cbc_decrypt(ciphertext, key):
    ct_array = [ciphertext[i:i+16] for i in range(0,len(ciphertext),16)]
    pt_array = [None]*(len(ct_array)-1)
    for i in range(0, len(pt_array)):
        pt_array[i] = bytes(a^b for a,b in zip(aes128.decrypt(ct_array[i+1],key), ct_array[i]))
    pt = b''.join([bytearray(x) for x in np.array(pt_array).T.tolist()])
    pt = pt[:-pt[-1]]
    return pt.decode('utf-8')
    
