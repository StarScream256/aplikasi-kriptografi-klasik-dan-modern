def encrypt_rsa(plaintext: str, e_key: int, n_key: int):
    """
    Enkripsi RSA sederhana.Untuk setiap karakter dalam plaintext, konversi ke nilai ASCII, lalu enkripsi menggunakan kunci publik (e_key, n_key).

    Args:
        plaintext (str): Plaintext yang akan dienkripsi.
        e_key (int): Public exponent key.
        n_key (int): Modulus key.

    Returns:
        str: Ciphertext.
    """
    ciphertext = []
    for char in plaintext:
        ascii_value = ord(char)
        # Enkripsi dengan rumus RSA: c = (m^e) mod n
        encrypted_value = pow(ascii_value, e_key, n_key)
        ciphertext.append(str(encrypted_value))
    
    return ' '.join(ciphertext)

def decrypt_rsa(ciphertext: str, d_key: int, n_key: int):
    """
    Dekripsi RSA sederhana. Untuk setiap nilai dalam ciphertext, dekripsi menggunakan kunci privat (d_key, n_key), lalu konversi kembali ke karakter.

    Args:
        ciphertext (str): Ciphertext yang akan didekripsi.
        d_key (int): Private exponent key.
        n_key (int): Modulus key.

    Returns:
        str: Plaintext.
    """
    plaintext = []
    for value in ciphertext.split():
        encrypted_value = int(value)
        # Dekripsi dengan rumus RSA: m = (c^d) mod n
        decrypted_value = pow(encrypted_value, d_key, n_key)
        plaintext.append(chr(decrypted_value))
    
    return ''.join(plaintext)