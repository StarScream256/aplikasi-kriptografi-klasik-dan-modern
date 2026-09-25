import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from dataclasses import dataclass
from algorithms.xor import decrypt_xor, encrypt_xor
from utils.xor_formats import (
    ascii_to_ciphertext,
    binary_to_ciphertext,
    ciphertext_to_ascii,
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


def create_process_data(
    plaintext: str,
    key: str,
    ciphertext: str,
    is_decryption: bool = False,
) -> list[XORProcessData]:
    process_data = []
    for index, (p_char, c_char) in enumerate(zip(plaintext, ciphertext), start=1):
        k_char = key[(index - 1) % len(key)]
        bit_width = max(
            8,
            ord(p_char).bit_length(),
            ord(k_char).bit_length(),
            ord(c_char).bit_length(),
        )
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


def character_display(character: str) -> str:
    if character.isprintable():
        return f"Raw {character}"
    return f"ASCII Number {ord(character)}"


def render_process_card(data: XORProcessData):
    with st.container(border=True):
        st.badge(f"Character {data.index}")
        if data.is_decryption:
            input_character = data.c_char
            input_binary = data.c_bin
            input_label = "Ciphertext"
            result_character = data.p_char
            result_binary = data.p_bin
            result_label = "Plaintext"
        else:
            input_character = data.p_char
            input_binary = data.p_bin
            input_label = "Plaintext"
            result_character = data.c_char
            result_binary = data.c_bin
            result_label = "Ciphertext"

        st.markdown(
            f"#### {input_label} ({character_display(input_character)}) "
            f"XOR Key ({character_display(data.k_char)})"
        )

        st.markdown("#### Result")
        st.table(
            {
                "Raw": (
                    result_character
                    if result_character.isprintable()
                    else "Non-printable"
                ),
                "ASCII Number": ord(result_character),
                "Hex": f"{ord(result_character):X}",
                "Binary": result_binary,
            }
        )

        st.markdown("#### XOR Process")
        st.dataframe(
            {
                f"{input_label} Bit ({character_display(input_character)})": list(
                    input_binary
                ),
                f"Key Bit ({character_display(data.k_char)})": list(data.k_bin),
                f"{result_label} Bit ({character_display(result_character)})": list(
                    result_binary
                ),
            },
            hide_index=True,
        )


def render_xor_view():
    st.title("Algoritma XOR")
    st.badge("Algoritma Kriptografi Modern")
    st.write(
        "Algoritma XOR adalah algoritma enkripsi sederhana yang menggunakan operasi "
        "logika XOR untuk mengubah data asli menjadi bentuk terenkripsi."
    )

    tabs = st.tabs(["Enkripsi", "Dekripsi"])
    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):")
        key = st.text_input("Masukkan kunci (key):")
        output_format = st.selectbox(
            "Format ciphertext:",
            ["Raw", "ASCII Number", "Hex", "Binary"],
            key="xor_encrypt_format",
        )
        if output_format == "Raw":
            st.warning(
                "Format Raw mungkin tidak akan terlihat dengan baik di text area "
                "karena dapat berisi karakter non-printable."
            )
        if st.button("Enkripsi"):
            if plaintext and key:
                raw_ciphertext = encrypt_xor(plaintext, key)
                ciphertext = raw_ciphertext
                if output_format == "ASCII Number":
                    ciphertext = ciphertext_to_ascii(ciphertext)
                elif output_format == "Hex":
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
            ["Raw", "ASCII Number", "Hex", "Binary"],
            key="xor_decrypt_format",
        )
        if input_format == "Raw":
            st.warning(
                "Format Raw mungkin tidak akan terlihat dengan baik di text area "
                "karena dapat berisi karakter non-printable."
            )
        ciphertext = st.text_area("Masukkan ciphertext:")
        key = st.text_input("Masukkan kunci dekripsi (key):")
        if st.button("Dekripsi"):
            if ciphertext and key:
                try:
                    if input_format == "ASCII Number":
                        ciphertext = ascii_to_ciphertext(ciphertext)
                    elif input_format == "Hex":
                        ciphertext = hex_to_ciphertext(ciphertext)
                    elif input_format == "Binary":
                        ciphertext = binary_to_ciphertext(ciphertext)

                    raw_ciphertext = ciphertext
                    plaintext = decrypt_xor(raw_ciphertext, key)
                    st.text_area("Hasil dekripsi:", plaintext, height=150)

                    st.subheader("Langkah proses XOR")
                    for data in create_process_data(
                        plaintext,
                        key,
                        raw_ciphertext,
                        is_decryption=True,
                    ):
                        render_process_card(data)
                except ValueError as error:
                    st.error(str(error))
            else:
                st.error("Ciphertext dan kunci harus diisi.")


if __name__ == "__main__":
    st.set_page_config(page_title="XOR Encryption/Decryption", layout="wide")
    render_xor_view()