def ciphertext_to_hex(ciphertext: str) -> str:
    """Convert character-based XOR ciphertext to readable hexadecimal."""
    return " ".join(f"{ord(char):X}" for char in ciphertext)


def hex_to_ciphertext(value: str) -> str:
    """Convert space-separated hexadecimal ciphertext back to characters."""
    try:
        return "".join(chr(int(token, 16)) for token in value.split())
    except ValueError as error:
        raise ValueError("Format hex tidak valid.") from error


def ciphertext_to_binary(ciphertext: str) -> str:
    """Convert character-based XOR ciphertext to readable binary."""
    return " ".join(f"{ord(char):b}" for char in ciphertext)


def binary_to_ciphertext(value: str) -> str:
    """Convert space-separated binary ciphertext back to characters."""
    try:
        return "".join(chr(int(token, 2)) for token in value.split())
    except ValueError as error:
        raise ValueError("Format biner tidak valid.") from error
