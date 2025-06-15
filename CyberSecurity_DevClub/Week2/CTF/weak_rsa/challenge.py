#!/usr/bin/env python3
import random
from math import gcd

def is_prime(n, k=128):
    """Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number with specified bit length"""
    while True:
        # Generate random odd number
        n = random.getrandbits(bits) | 1
        # Ensure n has exactly 'bits' bits
        n |= (1 << (bits-1))
        if is_prime(n):
            return n

def mod_inverse(e, phi):
    """Calculate modular inverse using extended Euclidean algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def main():
    # Generate two prime numbers (256 bits each)
    print("Generating primes...")
    p = generate_prime(128)
    q = generate_prime(128)
    
    # Calculate RSA parameters
    n = p * q
    e = 65537  # Common RSA public exponent
    phi = (p - 1) * (q - 1)
    
    # Ensure e and phi are coprime
    while gcd(e, phi) != 1:
        p = generate_prime(256)
        q = generate_prime(256)
        n = p * q
        phi = (p - 1) * (q - 1)
    
    # Calculate private key
    d = mod_inverse(e, phi)
    
    # Convert flag to number
    flag = "dcCTF{W34k_RSA_1s_N0_G00D}"
    flag_bytes = flag.encode()
    flag_int = int.from_bytes(flag_bytes, 'big')
    
    # Encrypt flag
    encrypted_flag = pow(flag_int, e, n)
    
    # Write challenge file
    with open("rsa_challenge.txt", "w") as f:
        f.write(f"n = {n}\n")
        f.write(f"e = {e}\n\n")
        f.write(f"c = {encrypted_flag}\n")
    
    print("Challenge file created: rsa_challenge.txt")
    print("\nSolution parameters (for verification):")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"d = {d}")

if __name__ == "__main__":
    main()