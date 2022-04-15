from math import sqrt
import math
import sys
import random

# 2
def gen_odd(size):
    # prime is odd, except 2
    r = random.getrandbits(size)
    while(r%2==0):
        r = random.getrandbits(size)
    return r

def witness(n, d, k):
    a = random.SystemRandom().randrange(2, n-1)
    x = pow(a, d, n)
    if((x == 1) or (x==(n-1))):
        return True
    for i in range(k-1):
        x = x**2 % n
        if (x == 1): return False
        if (x == (n-1)): return True
    return False

# reference: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
def miller_rabin(num, iter):
    # no need to handle small corner case, even in this func
    # odd d, n-1 = d*2^r
    d = num-1
    r = 0
    while(d%2 == 0):
        d >>= 1
        r += 1
    for i in range(iter):
        if (witness(num,d,r)==False):
            return False
    return True

# 3
def is_prime(num):
    # prime is odd, except 2
    if(num%2==0):
        return False
    if(miller_rabin(num,2**6) == False):
        return False
    return True

def check_prime(num):
     for i in range (2, int(sqrt(num))): 
        if((num%i)==0): 
            return False

# 1
def gen_prime(size):
    # prime is odd, except 2
    find_prime = False
    num = 0
    while(not find_prime):
        num = gen_odd(size)
        find_prime = is_prime(num)
    return num

def gen_ran(phi_n, size):
    # less than (p − 1)(q − 1)
    r = random.getrandbits(size)
    while(r >= phi_n):
        r = random.getrandbits(size)
    return r

#5 Extend Euclid
# reference: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def find_gcd_extend_iter(a,b):
    x0, x1, y0, y1 = 0, 1, b, a
    while y1:
        q = y0//y1
        x0,x1 = x1, x0-q*x1
        y0,y1 = y1, y0-q*y1
    # to get a positive number
    if (x0 < 0):
        x0 += b
    return x0
    
#4    
def gen_e(phi_n,key_size):
    # loop
    # generate a number, find if it is rel prime with phiN, is, return
    find_e = False
    e = 0
    while(not find_e):
        e = gen_ran(phi_n,key_size)
        if(math.gcd(phi_n,e)==1):
            find_e = True
    return e

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
    # print("M - get p: ",prime_p," q: ", prime_q," n: ", n," phi n: ", phi_n)
    rel_prime_e = gen_e(phi_n,key_size)
    # print("M - get e: ", rel_prime_e)
    public_key = [rel_prime_e,n]

    # 4 find d (inverse, using Pulverizer)
    eInverse_d = find_gcd_extend_iter(rel_prime_e,phi_n)
    # print("M - get d: ", eInverse_d)
    private_key = [eInverse_d,n]
    return public_key, private_key
    
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
    public_key, private_key = gen_key_pair()
    # print("public_key: ")
    # print(public_key)
    # print("private_key: ")
    # print(private_key)
    output_key_pair(public_key,private_key,input_name)
    
main()
# python ./genkeys.py alice