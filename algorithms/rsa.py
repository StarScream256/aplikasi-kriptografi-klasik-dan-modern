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