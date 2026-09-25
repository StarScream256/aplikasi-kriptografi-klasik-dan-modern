import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from algorithms.rsa import decrypt_rsa, encrypt_rsa, rsa_keygen
from utils.math_utils import is_prime


def render_key_generation():
    st.markdown("### Generate Kunci RSA")
    st.write("Generate kunci publik (untuk enkripsi) dan privat (untuk dekripsi) untuk algoritma RSA.")
    
    if "rsa_keys" not in st.session_state:
        st.session_state.rsa_keys = None

    cols = st.columns(2)
    with cols[0]:
        p = st.number_input("Masukkan bilangan prima p", step=1, min_value=2)
    with cols[1]:
        q = st.number_input("Masukkan bilangan prima q", step=1, min_value=2, value=3)
    if st.button("Generate Key Pair"):
        if is_prime(p) and is_prime(q) and p != q:
            rsa_keys = rsa_keygen(p, q)
            st.session_state.rsa_keys = rsa_keys
            st.success("Kunci RSA berhasil dibuat.")
        else:
            st.error("Masukkan dua bilangan prima yang berbeda.")

    if st.session_state.rsa_keys:
        keys = st.session_state.rsa_keys
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Public Key (e, n):**\n`{keys['public_key']}`")
        with col2:
            st.warning(f"**Private Key (d, n):**\n`{keys['private_key']}`")

        with st.expander("Lihat detail kunci"):
            st.write(f"Prime p: `{keys['p']}`")
            st.write(f"Prime q: `{keys['q']}`")
            st.write(f"Modulus n: `{keys['n']}`")
            st.write(f"Totient φ(n): `{keys['phi']}`")
    else:
        st.info("RSA key belum di-generate")


def render_rsa_view():
    st.title("Algoritma RSA")
    st.divider()
    render_key_generation()
    st.divider()

    keys = st.session_state.get("rsa_keys")
    tabs = st.tabs(["Enkripsi", "Dekripsi"])

    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):", key="rsa_plaintext")

        if keys:
            st.caption(f"Public key (e, n): `{keys['public_key']}`")
            if st.button("Enkripsi", key="rsa_encrypt_button"):
                if not plaintext:
                    st.error("Teks asli harus diisi.")
                elif any(ord(char) >= keys["n"] for char in plaintext):
                    st.error("Setiap nilai karakter plaintext harus lebih kecil dari modulus n.")
                else:
                    ciphertext = encrypt_rsa(plaintext, keys["public_key"])
                    st.text_area(
                        "Hasil enkripsi (angka ciphertext):",
                        ciphertext,
                        height=150,
                        key="rsa_encryption_result",
                    )
        else:
            st.info("Generate RSA key pair terlebih dahulu.")

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area(
            "Masukkan ciphertext (angka dipisahkan spasi):",
            key="rsa_ciphertext",
        )

        if keys:
            st.caption(f"Private key (d, n): `{keys['private_key']}`")
            if st.button("Dekripsi", key="rsa_decrypt_button"):
                if not ciphertext:
                    st.error("Ciphertext harus diisi.")
                else:
                    try:
                        plaintext = decrypt_rsa(ciphertext, keys["private_key"])
                        st.text_area(
                            "Hasil dekripsi (plaintext):",
                            plaintext,
                            height=150,
                            key="rsa_decryption_result",
                        )
                    except ValueError:
                        st.error("Ciphertext harus berisi angka yang dipisahkan spasi.")
        else:
            st.info("Generate RSA key pair terlebih dahulu.")

        # TODO: tambah visualisasi, nyusul


if __name__ == "__main__":
    st.set_page_config(page_title="RSA Encryption/Decryption", layout="wide")
    render_rsa_view()