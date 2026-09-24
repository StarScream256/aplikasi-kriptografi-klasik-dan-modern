def encrypt_xor(plaintext: str, key: str) -> str:
    """
    Enkripsi XOR sederhana. Untuk setiap karakter dalam plaintext, lakukan operasi XOR dengan karakter kunci yang sesuai.

    Args:
        plaintext (str): Plaintext yang akan dienkripsi.
        key (str): Kunci untuk enkripsi.

    Returns:
        str: Ciphertext.
    """
    ciphertext = []
    key_length = len(key)
    
    for i, char in enumerate(plaintext):
        # Dapatkan karakter kunci yang sesuai
        key_char = key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        ciphertext.append(encrypted_char)
    
    return ''.join(ciphertext)

def decrypt_xor(ciphertext: str, key: str) -> str:
    """
    Dekripsi XOR sederhana. Untuk setiap karakter dalam ciphertext, lakukan operasi XOR dengan karakter kunci yang sesuai.

    Args:
        ciphertext (str): Ciphertext yang akan didekripsi.
        key (str): Kunci untuk dekripsi.

    Returns:
        str: Plaintext.
    """
    plaintext = []
    key_length = len(key)
    
    for i, char in enumerate(ciphertext):
        # Dapatkan karakter kunci yang sesuai
        key_char = key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        plaintext.append(decrypted_char)
    
    return ''.join(plaintext)