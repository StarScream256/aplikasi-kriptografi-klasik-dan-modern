# untuk development rsa_views.py, dengan run langsung file ini dari root folder (streamlit run views/rsa_views.py)
# hapus kalau function render_rsa_view() sudah diimport ke main.py
#===========================
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
#=========================== 


import streamlit as st
from algorithms.rsa import decrypt_rsa, encrypt_rsa, rsa_keygen
from utils.math_utils import is_prime
from utils.rsa_utils import encode_message, decode_message, plaintext_to_binary, binary_to_decimal, decimal_to_binary


def render_key_generation():
    st.markdown("### Generate Kunci RSA")
    st.write("Generate kunci publik (untuk enkripsi) dan privat (untuk dekripsi) untuk algoritma RSA. Dapatkan angka prima besar [link](https://bigprimes.org/)")
    
    if "rsa_keys" not in st.session_state:
        st.session_state.rsa_keys = None

    cols = st.columns(2)
    with cols[0]:
        p_input = st.text_input("Masukkan bilangan prima p")
        p = int(p_input) if p_input else 0
    with cols[1]:
        q_input = st.text_input("Masukkan bilangan prima q")
        q = int(q_input) if q_input else 0
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

        with st.expander("Lihat detail pembuatan kunci"):
            key_generation_process(keys)
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


def encryption_process():
    st.write("### Proses Enkripsi RSA")
    p_text = [x for x in st.session_state.rsa_plaintext]
    c_bins, binary_sequence = plaintext_to_binary(st.session_state.rsa_plaintext)
    decimal_value = binary_to_decimal(binary_sequence)
    st.markdown("##### 1. Encode plaintext ke UTF-8")
    st.dataframe({
        "Karakter": p_text,
        "Binary (8-bit)": c_bins,
    })
    
    st.markdown("##### 2. Gabungkan semua binary menjadi satu dan konversi ke desimal")
    st.latex(rf"\text{{Binary sequence = }} {' + '.join(c_bins)}")
    st.latex(rf"\text{{Binary sequence = }} {binary_sequence}")
    st.latex(rf"\text{{Decimal value = }} {decimal_value}")

    e, n = st.session_state.rsa_keys['public_key']
    st.markdown("##### 3. Enkripsi dengan kunci publik")
    st.latex(rf"\text{{Rumus }} c = m^e \pmod n")
    st.latex(rf"\text{{Message ($m$) = }} {decimal_value}")
    st.latex(rf"\text{{Public key ($e, n$) = }} ({e}, {n})")
    st.latex(rf"\text{{Ciphertext ($c$) = }} {decimal_value}^{{ {e} }} \pmod {{ {n} }}")
    st.latex(rf"\text{{Ciphertext ($c$) = }} {pow(decimal_value, e, n)}")


def decryption_process():
    st.write("### Proses Dekripsi RSA")
    ciphertext = st.session_state.rsa_ciphertext.strip()
    encrypted_value = int(ciphertext)
    d, n = st.session_state.rsa_keys["private_key"]
    decrypted_value = pow(encrypted_value, d, n)
    binary_values = decimal_to_binary(decrypted_value)
    p_bins = [binary_values[i:i+8] for i in range(0, len(binary_values), 8)]
    plaintext = decode_message(decrypted_value)[1]
    message_bytes = plaintext.encode("utf-8")

    st.markdown("##### 1. Ciphertext yang diterima")
    st.latex(rf"\text{{Ciphertext ($c$) = }} {encrypted_value}")

    st.markdown("##### 2. Dekripsi dengan kunci privat")
    st.latex(rf"\text{{Rumus }} m = c^d \pmod n")
    st.latex(rf"\text{{Private key ($d, n$) = }} ({d}, {n})")
    st.latex(rf"\text{{Message ($m$) = }} {encrypted_value}^{{ {d} }} \pmod {{ {n} }}")
    st.latex(rf"\text{{Message ($m$) = }} {decrypted_value}")

    st.markdown("##### 3. Decode nilai desimal menjadi plaintext UTF-8")
    st.latex(rf"\text{{Binary sequence = }} {''.join(p_bins)}")
    st.latex(rf"\text{{Binary (8-bit) = }} [{', '.join(p_bins)}]")
    st.dataframe({
        "Binary (8-bit)": p_bins,
        "Byte": list(message_bytes),
        "Karakter": list(plaintext),
    })
    st.latex(rf"\text{{Plaintext = }} \text{{{plaintext}}}")


def render_rsa_view():
    st.title("Algoritma RSA")
    st.divider()
    render_key_generation()
    st.divider()

    keys = st.session_state.get("rsa_keys")
    tabs = st.tabs(["Enkripsi", "Dekripsi"])

    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan pesan (plaintext):", key="rsa_plaintext")

        if keys:
            st.badge(f"Public key (e, n): **{keys['public_key']}**")
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
                        encryption_process()
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("Generate RSA key pair terlebih dahulu.")

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area(
            "Masukkan ciphertext (satu bilangan utuh):",
            key="rsa_ciphertext",
        )

        if keys:
            st.badge(f"Private key (d, n): **{keys['private_key']}**")
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
                        decryption_process()
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("Generate RSA key pair terlebih dahulu.")


if __name__ == "__main__":
    st.set_page_config(page_title="RSA Encryption/Decryption", layout="wide")
    render_rsa_view()