# algorithms/vigenere.py

class VigenereCipher:
    def __init__(self, key: str):
        # Cleaning kunci di awal
        self.key = "".join([c.upper() for c in key if c.isalpha()])
        if not self.key:
            self.key = "KEY"

    def encrypt(self, plaintext: str):
        ciphertext = ""
        steps = []
        
        # Preprocessing: Hapus spasi dan semua karakter non-huruf
        clean_text = "".join([c.upper() for c in plaintext if c.isalpha()])
        key_length = len(self.key)
        
        steps.append("--- PREPROCESSING VIGENERE CIPHER ---")
        steps.append(f"Plaintext Awal   : '{plaintext}'")
        steps.append(f"Plaintext Bersih : '{clean_text}' (Spasi & non-huruf dihapus)")
        steps.append(f"Kunci            : '{self.key}'\n")

        # Visualisasi Penyelarasan Kunci
        key_aligned = "".join([self.key[i % key_length] for i in range(len(clean_text))])
        steps.append("--- PENYELARASAN KUNCI & TEKS ---")
        steps.append(f"Plaintext : {' '.join(clean_text)}")
        steps.append(f"Kunci     : {' '.join(key_aligned)}")
        steps.append("            " + "| " * len(clean_text) + "\n")

        steps.append("--- DETAIL PROSES ENKRIPSI ---")
        for i, char in enumerate(clean_text):
            k_char = self.key[i % key_length]
            p_val = ord(char) - ord('A')
            k_val = ord(k_char) - ord('A')
            
            c_val = (p_val + k_val) % 26
            c_char = chr(c_val + ord('A'))
            ciphertext += c_char
            
            steps.append(
                f"Posisi [{i+1}] P='{char}' ({p_val:2d}) + K='{k_char}' ({k_val:2d}) "
                f"mod 26 = {c_val:2d} -> C='{c_char}'"
            )
            
        return ciphertext, steps

    def decrypt(self, ciphertext: str):
        plaintext = ""
        steps = []
        
        # Preprocessing untuk dekripsi
        clean_text = "".join([c.upper() for c in ciphertext if c.isalpha()])
        key_length = len(self.key)
        
        steps.append("--- PREPROCESSING DEKRIPSI VIGENERE ---")
        steps.append(f"Ciphertext Bersih : '{clean_text}'")
        steps.append(f"Kunci             : '{self.key}'\n")

        key_aligned = "".join([self.key[i % key_length] for i in range(len(clean_text))])
        steps.append("--- PENYELARASAN KUNCI & TEKS ---")
        steps.append(f"Ciphertext : {' '.join(clean_text)}")
        steps.append(f"Kunci      : {' '.join(key_aligned)}")
        steps.append("             " + "| " * len(clean_text) + "\n")

        steps.append("--- DETAIL PROSES DEKRIPSI ---")
        for i, char in enumerate(clean_text):
            k_char = self.key[i % key_length]
            c_val = ord(char) - ord('A')
            k_val = ord(k_char) - ord('A')
            
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('A'))
            plaintext += p_char
            
            steps.append(
                f"Posisi [{i+1}] C='{char}' ({c_val:2d}) - K='{k_char}' ({k_val:2d}) "
                f"mod 26 = {p_val:2d} -> P='{p_char}'"
            )
            
        return plaintext, steps