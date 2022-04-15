import math
import random
from string import ascii_letters
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def gen_aes_key(size):
    # size = bytes
    key = ''
    for i in range(size):
        key+=random.choice(ascii_letters)
    return key.encode()
    
def encryption(RSA_key,txt_input):
    AES_KEY = gen_aes_key(16) # 128 bits = 16 bytes
    IV = get_random_bytes(16)
    #print("AES_KEY: ",AES_KEY)
    ciphertext = AES_encrypt(AES_KEY,txt_input,IV)
    encrypted_AES_key = RSA_encrypt(RSA_key,AES_KEY)
    #print(len(ciphertext))
    #print(len(IV))
    #print(len(encrypted_AES_key))
    return [ciphertext,IV,encrypted_AES_key]

def decryption(RSA_key,input):
    AES_KEY = RSA_decrypt(RSA_key,input[2])
    #print(AES_KEY)
    plaintext = AES_decrypt(AES_KEY,input[0],input[1])
    #print(plaintext)
    return plaintext.decode()

def AES_encrypt(key, message,IV):
    pad_m = pad(message.encode(),16)
    cipher = AES.new(key, AES.MODE_CBC, IV=IV)
    ciphertext = cipher.encrypt(pad_m)
    return ciphertext

def AES_decrypt(key, ciphertext,IV):
    decipher = AES.new(key, AES.MODE_CBC, IV=IV)
    pad_p = decipher.decrypt(ciphertext)
    unpad_p = unpad(pad_p,16)
    return unpad_p

def RSA_encrypt(pub_key,aes_key):
    # key = pub key [e,n]
    int_key = int.from_bytes(aes_key,'big')
    # print(int_key)
    encrypted_key = pow(int_key,pub_key[0],pub_key[1])
    encrypted_key_byte = encrypted_key.to_bytes(math.ceil(encrypted_key.bit_length()/ 8),'big')
    return encrypted_key_byte

def RSA_decrypt(prv_key,ciphertext):
    # key = prv key [d,n]
    # print(ciphertext)
    int_key = int.from_bytes(ciphertext,'big')
    decrypted_key = pow(int_key,prv_key[0],prv_key[1])
    str_key = decrypted_key.to_bytes(math.ceil(decrypted_key.bit_length() / 8),'big')
    return str_key

def load_key(key_file):
    key = []
    with open(key_file,'r') as f:
        lines = f.readlines()
        for line in lines:
            key.append(int(line))
    return key

def load_plaintxt_file(input_file):
    with open(input_file,'r') as f:
        input = f.read()
        return input

def load_ciphertxt_file(input_file):
    input = []
    with open(input_file,'rb') as f:
        ciphertext = f.read()
        #print(ciphertext)
        IV_index = len(ciphertext)-16-256
        key_index = len(ciphertext)-256
        input.append(ciphertext[:IV_index])
        input.append(ciphertext[IV_index:key_index])
        input.append(ciphertext[key_index:])
        return input

def write_to_file(output_file,output):
    with open(output_file,'wb') as f:
        for item in output:
            f.write(item)

def write_pt_to_file(output_file,output):
    with open("check_"+output_file,'w') as f:
            f.write(output.decode())

def main():
    if(len(sys.argv)<5):
        return
    mode = sys.argv[1]
    key_file = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    key = load_key(key_file) # pub[e,n]/prv[d,n]
    # plaintext[text] / ciphertext[ciphertext,encrypted key]
    #print(key)

    if(mode == '-e'):
        # encryption: pub key [e,n], plaintext
        # input [plaintext] assume one line
        # output ciphertext[ciphertext,encrypted key]
        input = load_plaintxt_file(input_file)
        #print(input)
        encryption_output = encryption(key,input)
        #print(encryption_output)
        write_to_file(output_file,encryption_output)
    else:
        # decryption: prv key, ciphertext
        # input [ciphertext,encrypted AES key]
        # output [plaintext]
        input = load_ciphertxt_file(input_file)
        #print(input)
        decryption_output = decryption(key,input)
        write_pt_to_file(output_file,decryption_output)
   
main()
# python ./crypt.py -e alice.pub message2.txt message2.cip
# python ./crypt.py -d alice.prv message2.cip message2.txt
# python ./crypt.py -e bob.pub message.txt message.cip
# python ./crypt.py -d bob.prv message.cip message.txt