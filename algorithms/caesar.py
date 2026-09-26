# algorithms/caesar.py

class CaesarCipher:
    def __init__(self, shift=3):
        self.shift = shift

    def _generate_mapping_table(self):
        # Membuat baris abjad asli dan abjad tergeser A-Z
        asli = [chr(i + ord('A')) for i in range(26)]
        tergeser = [chr((i + self.shift) % 26 + ord('A')) for i in range(26)]
        
        str_asli = " ".join(asli)
        str_tergeser = " ".join(tergeser)
        
        table_log = (
            f"--- TABEL PEMETAAN ALFABET (Shift: {self.shift:+d}) ---\n"
            f"Abjad Asli  : {str_asli}\n"
            f"Pergeseran  : {str_tergeser}\n"
        )
        return table_log

    def encrypt(self, plaintext: str):
        ciphertext = ""
        steps = []
        
        clean_text = "".join([c.upper() for c in plaintext if c.isalpha()])
        
        steps.append("--- PREPROCESSING CAESAR CIPHER ---")
        steps.append(f"Teks Awal  : '{plaintext}'")
        steps.append(f"Teks Bersih: '{clean_text}'\n")
        
        # Tambahkan tabel pemetaan alfabet penuh di awal
        steps.append(self._generate_mapping_table())
        steps.append(f"--- DETAIL PROSES ENKRIPSI ---")

        for i, char in enumerate(clean_text):
            p_val = ord(char) - ord('A')
            c_val = (p_val + self.shift) % 26
            c_char = chr(c_val + ord('A'))
            ciphertext += c_char

            if self.shift >= 0:
                char_range = [chr((p_val + s) % 26 + ord('A')) for s in range(abs(self.shift) + 1)]
                deretan_str = "  ".join(char_range)
                panah_str = "|" + "-" * (len(deretan_str) - 2) + f"> (Shift +{self.shift})"
            else:
                char_range = [chr((p_val - s) % 26 + ord('A')) for s in range(abs(self.shift), -1, -1)]
                deretan_str = "  ".join(char_range)
                panah_str = "<" + "-" * (len(deretan_str) - 2) + f"| (Shift {self.shift})"

            steps.append(
                f"[{i+1}] Karakter: '{char}' (Posisi {p_val})\n"
                f"    Deretan : {deretan_str}\n"
                f"              {panah_str}\n"
                f"    Hasil   : '{c_char}' (Posisi {c_val})\n"
                f"    Detail  : ({p_val} + ({self.shift})) mod 26 = {c_val} -> '{c_char}'\n"
            )

        return ciphertext, steps

    def decrypt(self, ciphertext: str):
        plaintext = ""
        steps = []
        
        clean_text = "".join([c.upper() for c in ciphertext if c.isalpha()])
        
        steps.append("--- PREPROCESSING DEKRIPSI CAESAR CIPHER ---")
        steps.append(f"Teks Bersih: '{clean_text}'\n")
        
        # Tabel pemetaan untuk dekripsi
        steps.append(self._generate_mapping_table())
        steps.append(f"--- DETAIL PROSES DEKRIPSI ---")

        for i, char in enumerate(clean_text):
            c_val = ord(char) - ord('A')
            p_val = (c_val - self.shift) % 26
            p_char = chr(p_val + ord('A'))
            plaintext += p_char

            dec_shift = -self.shift
            if dec_shift >= 0:
                char_range = [chr((c_val + s) % 26 + ord('A')) for s in range(abs(dec_shift) + 1)]
                deretan_str = "  ".join(char_range)
                panah_str = "|" + "-" * (len(deretan_str) - 2) + f"> (Shift +{dec_shift})"
            else:
                char_range = [chr((c_val - s) % 26 + ord('A')) for s in range(abs(dec_shift), -1, -1)]
                deretan_str = "  ".join(char_range)
                panah_str = "<" + "-" * (len(deretan_str) - 2) + f"| (Shift {dec_shift})"

            steps.append(
                f"[{i+1}] Karakter: '{char}' (Posisi {c_val})\n"
                f"    Deretan : {deretan_str}\n"
                f"              {panah_str}\n"
                f"    Hasil   : '{p_char}' (Posisi {p_val})\n"
                f"    Detail  : ({c_val} - ({self.shift})) mod 26 = {p_val} -> '{p_char}'\n"
            )

        return plaintext, steps