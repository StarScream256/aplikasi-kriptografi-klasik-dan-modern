import math
import random

def is_prime(num: int, k: int = 5) -> bool:
    """
    Memeriksa bilangan prima menggunakan algoritma cepat Miller-Rabin.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    
    d = num - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # pengujian akurasi sebanyak k kali putaran
    for _ in range(k):
        a = random.randint(2, num - 2)
        x = pow(a, d, num)
        
        if x == 1 or x == num - 1:
            continue
            
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
            
    return True
