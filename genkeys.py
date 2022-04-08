"""
generate RSA public and private keys.
- 1. The program takes a single command line argument: 
    the name of the user for whom the keys will be generated. 
    For test purposes, use the user names alice and bob.
- 2. The program must be runnable directly from the command shell, 
    e.g., ./genkeys.py alice
3. The program must generate an RSA public/private key pair using your own code 
    (you cannot import RSA code from another module such as PyCrypto). 
    It must use random.SystemRandom or os.urandom() as the source of pseudo-random bytes. 
    The keys must be of practical cryptographic size (e.g., 1024 bits).
4. The program must produce two output files, 
    one containing the RSA private key (e.g., alice.prv) 
    and the other one containing the RSA public key (e.g., alice.pub). 
    The format of the key files is up to you.
5. The program must produce two output files, 
    one containing the RSA private key (e.g., alice.prv) 
    and the other one containing the RSA public key (e.g., alice.pub). 
    The format of the key files is up to you.
6. To achieve the latter, you can implement the Miller-Rabin primality test
"""
from math import sqrt
import sys
import random

def gen_odd(size):
    # print("gen_odd")
    # prime is odd, except 2
    start = pow(2, size-1)+1
    stop = pow(2,size)
    r = random.SystemRandom().randrange(start, stop, 2)
    # print("M - get a random: ",r)
    return r

def is_prime(num):
    # prime is odd, except 2
    if(num%2==0):
        return False
    for i in range (2, int(sqrt(num))):
        if((num%i)==0):
            return False
    return True

def gen_prime(size):
    # prime is odd, except 2
    find_prime = False
    r = 0
    while(not find_prime):
        r = gen_odd(size)
        find_prime = is_prime(r)
    # print("M - get a prime: ",r)
    return r

def gen_ran(size):
    # less than (p − 1)(q − 1)
    start = 2 # e must be greater than 1
    stop = size
    r = random.SystemRandom().randrange(start, stop)
    # print("M - get a random: ",r)
    return r

def find_gcd(num1,num2):
    # assume num1 > num2
    if(num1 == 0):
        return num2
    if(num2 == 0):
        return num1
    return find_gcd(num2,num1%num2)
    
def find_gcd_extend(num1,num2):
    if(num1 == 0):
        return [num2,0,1]
    result = find_gcd_extend(num2%num1,num1)
    gcd = result[0]
    x = result[2] + (num2//num1)*result[1]
    y = result[1]
    return [gcd,x,y]

def is_rel_prime(num1,num2):
    gcd = find_gcd(num1,num2)
    # print("M - find gcd: ",gcd)
    return (gcd == 1)
    
def gen_e(phi_n):
    # loop
    # generate a number, find if it is rel prime with phiN, is, return
    find_e = False
    result = []
    while(not find_e):
        r = gen_ran(phi_n)
        # find_e = is_rel_prime(phi_n, r)
        result = find_gcd_extend(phi_n,r)
        if(result[0]==1):
            find_e = True
            result.insert(0,r)
    return result

def gen_key_pair():
    # 1 find large prime p, q
    # use random.SystemRandom or os.urandom() as the source of pseudo-random bytes
    # 2 check if is prime
    key_size = 10
    prime_p = gen_prime(key_size)
    prime_q = prime_p
    # in case p = q, regenerate if euqal
    while(prime_q == prime_p):
        prime_q = gen_prime(key_size)
    n = prime_p*prime_q
    phi_n = (prime_p-1)*(prime_q-1)
    print("M - get p: ",prime_p," q: ", prime_q," n: ", n," phi n: ", phi_n)
    # 3 find e rel. prime to (p-1)(q-1)
    get_gcd_e_d = gen_e(phi_n)
    print("M - get gcd_e_d: ", get_gcd_e_d[0], " ", get_gcd_e_d[1], " ",get_gcd_e_d[2], " ",get_gcd_e_d[3])
    rel_prime_e = get_gcd_e_d[0]
    # print("M - get e: ", rel_prime_e)
    public_key = [rel_prime_e,n]
    # 4 find d (inverse, using Pulverizer)
    eInverse_d = get_gcd_e_d[3]
    private_key = [eInverse_d,n]
    return public_key,private_key
    
def output_key_pair(public_key,private_key,file_name):
    pub_file = file_name+'.pub'
    prv_file = file_name+'.prv'
    with open(pub_file,'w') as f:
        for item in public_key:
            f.write(str(item))
            f.write('\n')
    with open(prv_file,'w') as f:
        for item in private_key:
            f.write(str(item))
            f.write('\n')

def main():
    input_name = ''
    if(len(sys.argv)>1):
        input_name = sys.argv[1]
        # print("M - get input: ",input_name)
    public_key, private_key = gen_key_pair()
    output_key_pair(public_key,private_key,input_name)
    
main()
