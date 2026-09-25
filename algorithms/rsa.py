import math
from utils.math_utils import is_prime


def rsa_keygen(p: int, q: int):
    """
    Generate RSA keys based on two prime numbers p and q.

    Args:
        p (int): Angka prima pertama.
        q (int): Angka prima kedua.

    Returns:
        dict: Dictionary yang berisi kunci publik, kunci privat, n, dan phi.
    """

    if not(is_prime(p) and is_prime(q)):
        raise ValueError("p dan q harus berupa bilangan prima.")
    elif p == q:
        raise ValueError("p dan q harus berupa bilangan prima yang berbeda.")

    n_key = p * q
    phi = (p - 1) * (q - 1)

    e_key = 65537  # Nilai umum untuk e
    if phi <= e_key or math.gcd(e_key, phi) != 1:
        e_key = 3
        while math.gcd(e_key, phi) != 1:
            e_key += 2

    d_key = pow(e_key, -1, phi) # inverse modulo phi

    public_key = (e_key, n_key)
    private_key = (d_key, n_key)
    return {
        "p": p,
        "q": q,
        "n": n_key,
        "phi": phi,
        "public_key": public_key,
        "private_key": private_key,
    }

def encrypt_rsa(plaintext: str, public_key: tuple[int, int]) -> str:
    """
    Enkripsi RSA sederhana.Untuk setiap karakter dalam plaintext, konversi ke nilai ASCII, lalu enkripsi menggunakan kunci publik (e_key, n_key).

    Args:
        plaintext (str): Plaintext yang akan dienkripsi.
        public_key (tuple[int, int]): Kunci publik (e, n).

    Returns:
        str: Ciphertext.
    """

    e_key, n_key = public_key
    ciphertext = []
    for char in plaintext:
        ascii_value = ord(char)
        # Enkripsi dengan rumus RSA: c = (m^e) mod n
        encrypted_value = pow(ascii_value, e_key, n_key)
        ciphertext.append(str(encrypted_value))
    
    return ' '.join(ciphertext)



def decrypt_rsa(ciphertext: str, private_key: tuple[int, int]):
    """
    Dekripsi RSA sederhana. Untuk setiap nilai dalam ciphertext, dekripsi menggunakan kunci privat (d_key, n_key), lalu konversi kembali ke karakter.

    Args:
        ciphertext (str): Ciphertext yang akan didekripsi.
        private_key (tuple[int, int]): Kunci privat (d, n).

    Returns:
        str: Plaintext.
    """

    d_key, n_key = private_key
    plaintext = []
    for value in ciphertext.split():
        encrypted_value = int(value)
        # Dekripsi dengan rumus RSA: m = (c^d) mod n
        decrypted_value = pow(encrypted_value, d_key, n_key)
        plaintext.append(chr(decrypted_value))
    
    return ''.join(plaintext)