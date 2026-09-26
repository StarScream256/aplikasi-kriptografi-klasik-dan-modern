def encode_message(message: str) -> dict[str, bytes | int]:
    """
    Encode pesannya menjadi representasi byte dan integer.
    
    Args:
        message (str): Pesan yang akan diencode.

    Returns:
        dict[str, bytes | int]: Dictionary yang berisi representasi byte dan integer dari pesan.
    """

    message_bytes = message.encode("utf-8")
    message_value = int.from_bytes(message_bytes, byteorder="big")
    return message_bytes, message_value

def decode_message(message_value: int) -> str:
    """
    Decode representasi integer menjadi pesan UTF-8.

    Args:
        message_value (int): Representasi integer dari pesan.

    Returns:
        str: Pesan yang didecode.
    """

    byte_length = max(1, (message_value.bit_length() + 7) // 8)
    decoded_bytes = message_value.to_bytes(byte_length, byteorder="big").decode("utf-8")
    return byte_length, decoded_bytes

def plaintext_to_binary(plaintext: str):
    c_bins = []
    for char in plaintext:
        c_bins.append(format(ord(char), '08b'))
    binary_sequence = ''.join(c_bins)
    return c_bins, binary_sequence

def binary_to_decimal(binary_sequence: str):
    decimal_value = int(binary_sequence, 2)
    return decimal_value

def decimal_to_binary(decimal_value: str) -> str:
    """
    Convert decimal value to binary string with leading zeros to make it a multiple of 8 bits.
    """
    binary_sequence = bin(decimal_value)[2:]
    padding_length = (8 - len(binary_sequence) % 8) % 8
    return '0' * padding_length + binary_sequence
