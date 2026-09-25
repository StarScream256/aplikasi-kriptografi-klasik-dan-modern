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
        p = st.number_input("Masukkan bilangan prima p (contoh: 17)", step=1, min_value=2)
    with cols[1]:
        q = st.number_input("Masukkan bilangan prima q (contoh: 19)", step=1, min_value=2, value=3)
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
            st.write(f"Totient Euler (phi) φ(n): `{keys['phi']}`")
    else:
        st.info("RSA key belum di-generate")


def key_generation_process(rsa_keys):
    st.write("### Proses Key Generation RSA")
    st.write(f"1. Diberikan dua bilangan prima $p = {rsa_keys['p']}$ dan $q = {rsa_keys['q']}$")
    st.write(f"2. Hitung modulus $$n = p \\times q = {rsa_keys['p']} \\times {rsa_keys['q']} = {rsa_keys['p'] * rsa_keys['q']}$$")
    st.write(r"3. Hitung fungsi Totient Euler")
    st.latex(r"\phi(n) = (p - 1)(q - 1)")
    st.latex(rf"\phi(n) = ({rsa_keys['p']} - 1)({rsa_keys['q']} - 1)")
    st.latex(rf"\phi(n) = {rsa_keys['p'] - 1} \times {rsa_keys['q'] - 1} = {(rsa_keys['p'] - 1) * (rsa_keys['q'] - 1)}")
    st.write(f"4. Pilih bilangan bulat $e$ sebagai kunci publik yang relatif prima terhadap $\\phi(n)$ dan $1 < e < \\phi(n)$. Umumnya, $e = 65537$ digunakan.")
    st.write(r"5. Hitung kunci privat $d$ sebagai invers modular dari $e$ modulo $\phi(n)$, yaitu:")
    st.latex(r"d = e^{-1} \pmod{\phi(n)}")
    st.latex(rf"d = {rsa_keys['n']}^{{-1}} \pmod{{{rsa_keys['phi']}}} = {rsa_keys['private_key'][0]}")
    st.write("6. Maka didapatkan kunci publik dan kunci privat.")
    st.latex(rf"\text{{Public Key (e, n)}} = ({rsa_keys['public_key'][0]}, {rsa_keys['public_key'][1]})")
    st.latex(rf"\text{{Private Key (d, n)}} = ({rsa_keys['private_key'][0]}, {rsa_keys['private_key'][1]})")


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
                else:
                    try:
                        ciphertext = encrypt_rsa(plaintext, keys["public_key"])
                        st.text_area(
                            "Hasil enkripsi (satu angka ciphertext):",
                            ciphertext,
                            height=150,
                            key="rsa_encryption_result",
                        )
                    except ValueError as error:
                        st.error(str(error))

                    key_generation_process(keys)
        else:
            st.info("Generate RSA key pair terlebih dahulu.")

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area(
            "Masukkan ciphertext (satu angka):",
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
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("Generate RSA key pair terlebih dahulu.")


if __name__ == "__main__":
    st.set_page_config(page_title="RSA Encryption/Decryption", layout="wide")
    render_rsa_view()