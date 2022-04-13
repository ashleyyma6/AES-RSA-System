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

N = p∙q
ϕ (N) = (p - 1)∙(q - 1)
ϕ (N): gcd(e,ϕ(N)) = 1
(d ∙ e) mod ϕ (N) = 1

Public key: (e, N)
Private key is (d, N)

"""
from math import sqrt
import math
import sys
import random

# 2
def gen_odd(size):
    # prime is odd, except 2
    r = random.getrandbits(size)
    if r%2==0:
        r+=1
    # print("M - get a random: ",r)
    return r

# (x^y)%p in O(log y)
def mod_exp(x,y,p):
    result = 1
    x %= p
    while(y>0):
        if((y&1)==1): 
            # y is odd
            result = (result * x) % p
            y -= 1
        else: 
            # y is even
            x = (x**2) % p
            y = y // 2
    return result % p

def fermat(num, iter):
    # gcd (a,n)！= 1, false
    # a^(n-1) != 1 (mod n), false
    for i in range(iter):
        random_num = random.SystemRandom().randrange(2, num-2)
        if(mod_exp(random_num,num-1,num) != 1):
            return False
    return True

# 3
def is_prime(num, prime_arr):
    # prime is odd, except 2
    if(num%2==0):
        return False
    for i in prime_arr:
        if(num%i == 0) :
            return False
    if(fermat(num,8) == False):
        return False
    return True

def check_prime(num):
     for i in range (2, int(sqrt(num))): 
        if((num%i)==0): 
            return False 

def gen_prime_arr(start,end):
    # start should be odd, reduce unnecessary calculation
    if(start%2 == 0):
        start+=1
    arr = []
    for num in range(start,end,2):
        if(check_prime(num)):
            arr.append(num)
    return arr

# 1
def gen_prime(size):
    # prime is odd, except 2
    find_prime = False
    num = 0
    prime_arr = gen_prime_arr(2,2**16)
    while(not find_prime):
        num = gen_odd(size)
        find_prime = is_prime(num, prime_arr)
    # print("M - get a prime: ",r)
    return num

def gen_ran(size):
    # less than (p − 1)(q − 1)
    start = 2 # e must be greater than 1
    stop = size
    r = random.SystemRandom().randrange(start, stop)
    # print("M - get a random: ",r)
    return r

#5
def find_gcd_extend_iter(a,b):
    # ax+by = gcd(a,b)
    # return (g,x,y)
    x0,x1,y0,y1 = 1, 0, 0, 1
    while (b!=0):
        q = a//b
        x0, x1 = x1, x0-q*x1
        y0, y1 = y1,y0-q*y1
        a, b = b, a - q*b
    # a is e, x0 is d
    return [abs(x0),y0] 
    
#4    
def gen_e(phi_n):
    # loop
    # generate a number, find if it is rel prime with phiN, is, return
    find_e = False
    num = 0
    while(not find_e):
        num = gen_ran(phi_n)
        if(math.gcd(phi_n,num)==1):
            find_e = True
    return num

'''
N = p∙q
ϕ (N) = (p - 1)∙(q - 1)
ϕ (N): gcd(e,ϕ(N)) = 1

(d ∙ e) mod ϕ (N) = 1

Public key: (e, N)
Private key is (d, N)
'''
def gen_key_pair():
    key_size = 1024 # test only

    prime_p = gen_prime(key_size)
    prime_q = prime_p
    # in case p = q, regenerate if euqal
    while(prime_q == prime_p):
        prime_q = gen_prime(key_size)
    n = prime_p*prime_q
    phi_n = (prime_p-1)*(prime_q-1)
    print("M - get p: ",prime_p," q: ", prime_q," n: ", n," phi n: ", phi_n)
    
    rel_prime_e = gen_e(phi_n)
    print("M - get e: ", rel_prime_e)
    public_key = [rel_prime_e,n]

    # 4 find d (inverse, using Pulverizer)
    gcd_ex = find_gcd_extend_iter(rel_prime_e,phi_n)
    # print(gcd_ex)
    eInverse_d = gcd_ex[0]
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
# python ./genkeys.py alice