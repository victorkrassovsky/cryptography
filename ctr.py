import numpy as np
import aes128
import os

#xors two 16 byte blocks
def xor_blocks(b1,b2):
    return bytes(a^b for a,b in zip(b1,b2))

#converts an array of bytes to a single byte string
def array_to_string(arr):
    return b''.join(arr)

#takes any string, 16 byte key and an optional nonce, and encrypts using aes128 ctr mode
#returns a string of bytes corresponding to the cipher text
#note: if the end of the plaintext ends in \x00, it will be removed due to padding
def aes_128_ctr_encrypt(plaintext, key, nonce=os.urandom(8)):
    pt = bytes(plaintext, 'utf-8')
    pad = 16 - (len(pt) % 16)
    pt = pt + bytes(pad)
    pt_array = [pt[i:i+16] for i in range(0,len(pt),16)]
    ct_array = [None]*len(pt_array)
    for i in range(0,len(pt_array)):
        counter = i.to_bytes(8,'big')
        ct_array[i] = xor_blocks(aes128.encrypt(nonce + counter,key),pt_array[i])
    return nonce + array_to_string(ct_array)


#takes a string of bytes returned from encrypt method and returns corresponding plaintext
def aes_128_ctr_decrypt(ct, key):
    nonce = ct[0:8]
    ct = ct[8:]
    ct_array = [ct[i:i+16] for i in range(0,len(ct), 16)]
    pt_array = [None]*len(ct_array)
    for i in range(0,len(pt_array)):
        counter = i.to_bytes(8,'big')
        pt_array[i] = xor_blocks(aes128.encrypt(nonce + counter,key),ct_array[i])
    pt = array_to_string(pt_array)
    return pt.decode('utf-8').rstrip('\x00')



    
