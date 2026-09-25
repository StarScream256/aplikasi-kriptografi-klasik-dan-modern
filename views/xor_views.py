import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass
import pandas as pd
import streamlit as st
from algorithms.xor import encrypt_xor, decrypt_xor
from algorithms.rsa import encrypt_rsa, decrypt_rsa
from utils.xor_formats import (
    binary_to_ciphertext,
    ciphertext_to_binary,
    ciphertext_to_hex,
    hex_to_ciphertext,
)


@dataclass
class XORProcessData:
    index: int
    p_char: str
    k_char: str
    c_char: str
    p_bin: str
    k_bin: str
    c_bin: str
    c_hex: str
    is_decryption: bool = False

    @property
    def is_printable(self) -> bool:
        # mengubah nilai hex/int kembali menjadi karakter untuk dicek
        char_value = chr(int(self.c_hex, 16))
        return char_value.isprintable()


def create_process_data(
    plaintext: str,
    key: str,
    ciphertext: str,
    is_decryption: bool = False,
) -> list[XORProcessData]:
    process_data = []
    for index, (p_char, c_char) in enumerate(zip(plaintext, ciphertext), start=1):
        k_char = key[(index - 1) % len(key)]
        bit_width = max(8, ord(p_char).bit_length(), ord(k_char).bit_length(), ord(c_char).bit_length())
        process_data.append(
            XORProcessData(
                index=index,
                p_char=p_char,
                k_char=k_char,
                c_char=c_char,
                p_bin=f"{ord(p_char):0{bit_width}b}",
                k_bin=f"{ord(k_char):0{bit_width}b}",
                c_bin=f"{ord(c_char):0{bit_width}b}",
                c_hex=f"{ord(c_char):X}",
                is_decryption=is_decryption,
            )
        )
    return process_data


def render_process_card(data: XORProcessData):
    with st.container(border=True):
        st.badge(f"Character {data.index}")
        if data.is_decryption:
            if data.c_char.isprintable():
                st.markdown(f"#### Ciphertext `Raw` {data.c_char} ⊕ Key `Raw` {data.k_char}")
            else:
                st.markdown(f"#### Ciphertext `Hex` {data.c_hex} ⊕ Key `Raw` {data.k_char}")
            result_char = data.p_char
            result_bin = data.p_bin
            result_hex = f"{ord(data.p_char):X}"
            result_label = "Plaintext"
            input_bin = data.c_bin
            input_label = f"Ciphertext Bit ({'Raw' if data.c_char.isprintable() else 'Hex'} {data.c_char if data.c_char.isprintable() else data.c_hex})"
        else:
            st.markdown(f"#### Plaintext `{data.p_char}` ⊕ Key `{data.k_char}`")
            result_char = data.c_char
            result_bin = data.c_bin
            result_hex = data.c_hex
            result_label = "Ciphertext"
            input_bin = data.p_bin
            input_label = f"Plaintext Bit ({'Raw' if data.p_char.isprintable() else 'Hex'} {data.p_char if data.p_char.isprintable() else data.p_hex})"

        st.markdown("#### Result")
        st.table({
            "Raw": result_char if result_char.isprintable() else "Non-printable",
            "Hex": result_hex,
            "Binary": result_bin,
        })

        st.markdown("#### XOR Process")
        input_bins = list(input_bin)
        k_bins = list(data.k_bin)
        result_bins = list(result_bin)
        st.dataframe({
            input_label: input_bins,
            f"Key Bit ({data.k_char})": k_bins,
            f"{result_label} Bit ({result_char})": result_bins,
        })


# panggil fungsi ini jika diimport dari file lain untuk visualisasi
def render_xor_view():
    st.title("Algoritma XOR")
    st.badge("Algoritma Kriptografi Modern")
    st.write("Algoritma XOR adalah algoritma enkripsi sederhana yang menggunakan operasi logika XOR untuk mengubah data asli menjadi bentuk terenkripsi. Algoritma ini sering digunakan dalam berbagai aplikasi keamanan data.")

    tabs = st.tabs(["Enkripsi", "Dekripsi"])
    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):")
        key = st.text_input("Masukkan kunci (key):")
        output_format = st.selectbox(
            "Format ciphertext:",
            ["Raw", "Hex", "Binary"],
            key="xor_encrypt_format",
        )
        if output_format == "Raw":
            st.warning("Format Raw mungkin tidak akan terlihat dengan baik di text area karena dapat berisi karakter non-printable.")
        if st.button("Enkripsi"):
            if plaintext and key:
                ciphertext = encrypt_xor(plaintext, key)
                raw_ciphertext = ciphertext
                if output_format == "Hex":
                    ciphertext = ciphertext_to_hex(ciphertext)
                elif output_format == "Binary":
                    ciphertext = ciphertext_to_binary(ciphertext)
                st.text_area("Hasil enkripsi:", ciphertext, height=150)

                st.subheader("Langkah proses XOR")
                for data in create_process_data(plaintext, key, raw_ciphertext):
                    render_process_card(data)
            else:
                st.error("Teks asli dan kunci harus diisi.")

    with tabs[1]:
        st.subheader("Dekripsi")
        input_format = st.selectbox(
            "Format ciphertext:",
            ["Raw", "Hex", "Binary"],
            key="xor_decrypt_format",
        )
        if input_format == "Raw":
            st.warning("Format Raw mungkin tidak akan terlihat dengan baik di text area karena berisi karakter non-printable.")
        ciphertext = st.text_area("Masukkan ciphertext:")
        key = st.text_input("Masukkan kunci dekripsi (key):")
        if st.button("Dekripsi"):
            if ciphertext and key:
                try:
                    if input_format == "Hex":
                        ciphertext = hex_to_ciphertext(ciphertext)
                    elif input_format == "Binary":
                        ciphertext = binary_to_ciphertext(ciphertext)
                    raw_ciphertext = ciphertext
                    plaintext = decrypt_xor(raw_ciphertext, key)
                    st.text_area("Hasil dekripsi:", plaintext, height=150)

                    st.subheader("Langkah proses XOR")
                    for data in create_process_data(plaintext, key, raw_ciphertext, is_decryption=True):
                        render_process_card(data)
                except ValueError as error:
                    st.error(str(error))
            else:
                st.error("Ciphertext dan kunci harus diisi.")

if __name__ == "__main__":
    st.set_page_config(page_title="XOR Encryption/Decryption", layout="wide")
    render_xor_view()