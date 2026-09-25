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
    # jika 65537 gagal, mulai dari bilangan 3 dan cari bilangan ganjil yang relatif prima dengan phi
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
    Enkripsi seluruh plaintext UTF-8 sebagai satu bilangan RSA.

    Args:
        plaintext (str): Plaintext yang akan dienkripsi.
        public_key (tuple[int, int]): Kunci publik (e, n).

    Returns:
        str: Ciphertext.
    """

    e_key, n_key = public_key
    if not plaintext:
        return ""

    message_bytes = plaintext.encode("utf-8")
    message_value = int.from_bytes(message_bytes, byteorder="big")
    if message_value >= n_key:
        raise ValueError("Plaintext terlalu besar untuk modulus n. Gunakan p dan q yang lebih besar.")

    encrypted_value = pow(message_value, e_key, n_key)
    return str(encrypted_value)



def decrypt_rsa(ciphertext: str, private_key: tuple[int, int]):
    """
    Dekripsi satu bilangan RSA menjadi seluruh plaintext UTF-8.

    Args:
        ciphertext (str): Ciphertext yang akan didekripsi.
        private_key (tuple[int, int]): Kunci privat (d, n).

    Returns:
        str: Plaintext.
    """

    if not ciphertext.strip():
        return ""

    d_key, n_key = private_key
    values = ciphertext.split()
    if len(values) != 1:
        raise ValueError("Ciphertext RSA harus berupa satu bilangan.")

    encrypted_value = int(values[0])
    if not 0 <= encrypted_value < n_key:
        raise ValueError("Nilai ciphertext harus berada di antara 0 dan n - 1.")

    decrypted_value = pow(encrypted_value, d_key, n_key)
    byte_length = max(1, (decrypted_value.bit_length() + 7) // 8)
    try:
        return decrypted_value.to_bytes(byte_length, byteorder="big").decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Ciphertext tidak menghasilkan plaintext UTF-8 yang valid.") from error