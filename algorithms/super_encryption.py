from algorithms.caesar import CaesarCipher
from algorithms.rsa import decrypt_rsa, encrypt_rsa
from algorithms.vigenere import VigenereCipher
from algorithms.xor import decrypt_xor, encrypt_xor


_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _encode_rsa_ciphertext(ciphertext: str) -> str:
    letters = []
    for value in ciphertext.encode("utf-8"):
        high, low = divmod(value, len(_ALPHABET))
        letters.extend((_ALPHABET[high], _ALPHABET[low]))
    return "".join(letters)


def _decode_rsa_ciphertext(ciphertext: str) -> str:
    if not ciphertext or len(ciphertext) % 2:
        raise ValueError("Ciphertext super enkripsi memiliki format yang tidak valid.")
    if any(character not in _ALPHABET + _ALPHABET.lower() for character in ciphertext):
        raise ValueError("Ciphertext super enkripsi harus berupa huruf A-Z.")

    normalized = ciphertext.upper()
    values = bytearray()
    for index in range(0, len(normalized), 2):
        value = (
            _ALPHABET.index(normalized[index]) * len(_ALPHABET)
            + _ALPHABET.index(normalized[index + 1])
        )
        if value > 255:
            raise ValueError("Ciphertext super enkripsi memiliki format yang tidak valid.")
        values.append(value)

    try:
        return values.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Ciphertext super enkripsi memiliki format yang tidak valid.") from error


class SuperEncryptionCipher:
    """Gabungan Caesar, Vigenere, XOR, dan RSA dengan ciphertext akhir A-Z."""

    def __init__(self, caesar_shift: int = 3, vigenere_key: str = "KEY", xor_key: str = "KEY"):
        if not xor_key:
            raise ValueError("Kunci XOR wajib diisi.")
        if not xor_key.isascii():
            raise ValueError("Kunci XOR harus menggunakan karakter ASCII.")

        self.caesar = CaesarCipher(shift=caesar_shift)
        self.vigenere = VigenereCipher(key=vigenere_key)
        self.xor_key = xor_key

    def encrypt(self, plaintext: str, public_key: tuple[int, int]) -> tuple[str, list[str]]:
        if not plaintext:
            return "", ["Plaintext kosong; tidak ada data untuk dienkripsi."]

        caesar_text, caesar_steps = self.caesar.encrypt(plaintext)
        vigenere_text, vigenere_steps = self.vigenere.encrypt(caesar_text)
        xor_text = encrypt_xor(vigenere_text, self.xor_key)
        rsa_ciphertext = encrypt_rsa(xor_text, public_key)
        ciphertext = _encode_rsa_ciphertext(rsa_ciphertext)

        steps = ["=== SUPER ENKRIPSI ==="]
        steps.extend(caesar_steps)
        steps.extend(vigenere_steps)
        steps.append(f"XOR selesai memproses {len(xor_text)} karakter.")
        steps.append("RSA mengenkripsi data dalam blok, lalu ciphertext dikodekan menjadi huruf A-Z.")
        steps.append(f"Ciphertext akhir: {ciphertext}")
        return ciphertext, steps

    def decrypt(self, ciphertext: str, private_key: tuple[int, int]) -> tuple[str, list[str]]:
        if not ciphertext:
            return "", ["Ciphertext kosong; tidak ada data untuk didekripsi."]

        rsa_ciphertext = _decode_rsa_ciphertext(ciphertext)
        xor_text = decrypt_rsa(rsa_ciphertext, private_key)
        vigenere_text = decrypt_xor(xor_text, self.xor_key)
        caesar_text, vigenere_steps = self.vigenere.decrypt(vigenere_text)
        plaintext, caesar_steps = self.caesar.decrypt(caesar_text)

        steps = ["=== DEKRIPSI SUPER ENKRIPSI ==="]
        steps.append("Ciphertext A-Z dikembalikan ke format blok RSA.")
        steps.append("RSA dan XOR berhasil dibalik.")
        steps.extend(vigenere_steps)
        steps.extend(caesar_steps)
        return plaintext, steps