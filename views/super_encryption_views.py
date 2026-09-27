# views/super_encryption_views.py
import streamlit as st
from algorithms.super_encryption import SuperEncryptionCipher
from algorithms.rsa import rsa_keygen
from utils.math_utils import is_prime


def render_key_generation():
    st.markdown("### Generate Kunci RSA")
    st.write(
        "Kunci RSA dipakai pada tahap terakhir pipeline Super Enkripsi. "
        "Dapatkan angka prima besar [link](https://bigprimes.org/)"
    )

    if "super_rsa_keys" not in st.session_state:
        st.session_state.super_rsa_keys = None

    cols = st.columns(2)
    with cols[0]:
        p_input = st.text_input("Masukkan bilangan prima p", key="super_p")
    with cols[1]:
        q_input = st.text_input("Masukkan bilangan prima q", key="super_q")
    if st.button("Generate Key Pair", key="super_keygen_button"):
        if not p_input or not q_input:
            st.error("Input p dan q wajib diisi.")
        else:
            try:
                p = int(p_input)
                q = int(q_input)
            except ValueError:
                st.error("p dan q harus berupa bilangan bulat.")
                return

            if is_prime(p) and is_prime(q) and p != q:
                st.session_state.super_rsa_keys = rsa_keygen(p, q)
                st.success("Kunci RSA berhasil dibuat.")
            else:
                st.error("Masukkan dua bilangan prima yang berbeda.")

    if st.session_state.super_rsa_keys:
        keys = st.session_state.super_rsa_keys
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Public Key (e, n):**\n`{keys['public_key']}`")
        with col2:
            st.warning(f"**Private Key (d, n):**\n`{keys['private_key']}`")
    else:
        st.info("RSA key belum di-generate.")


def render_super_enkripsi_view():
    st.title("Super Enkripsi")
    st.badge("Algoritma Gabungan")
    st.write(
        "Super Enkripsi menggabungkan 4 algoritma secara berurutan: "
        "**Caesar → Vigenère → XOR → RSA**. Hasil akhirnya dikodekan "
        "menjadi huruf A-Z."
    )

    st.divider()
    render_key_generation()
    st.divider()

    keys = st.session_state.get("super_rsa_keys")

    tabs = st.tabs(["Enkripsi", "Dekripsi"])

    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):", key="super_enc_text")
        c1, c2, c3 = st.columns(3)
        with c1:
            caesar_shift = st.number_input("Shift Caesar", value=3, step=1, key="super_enc_caesar")
        with c2:
            vigenere_key = st.text_input("Kunci Vigenère", value="KEY", key="super_enc_vigenere")
        with c3:
            xor_key = st.text_input("Kunci XOR", value="KEY", key="super_enc_xor")

        if keys:
            st.badge(f"Public key (e, n): **{keys['public_key']}**")
            if st.button("Enkripsi", key="super_encrypt_button"):
                if not plaintext:
                    st.error("Teks asli harus diisi.")
                elif not vigenere_key or not xor_key:
                    st.error("Kunci Vigenère dan XOR harus diisi.")
                else:
                    try:
                        cipher = SuperEncryptionCipher(
                            caesar_shift=int(caesar_shift),
                            vigenere_key=vigenere_key,
                            xor_key=xor_key,
                        )
                        result, steps = cipher.encrypt(plaintext, keys["public_key"])
                        st.text_area("Hasil enkripsi (ciphertext A-Z):", result, height=100, key="super_enc_result")
                        with st.expander("Lihat langkah proses"):
                            st.code("\n".join(steps))
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("Generate RSA key pair terlebih dahulu.")

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area("Masukkan ciphertext (A-Z):", key="super_dec_text")
        c1, c2, c3 = st.columns(3)
        with c1:
            caesar_shift = st.number_input("Shift Caesar", value=3, step=1, key="super_dec_caesar")
        with c2:
            vigenere_key = st.text_input("Kunci Vigenère", value="KEY", key="super_dec_vigenere")
        with c3:
            xor_key = st.text_input("Kunci XOR", value="KEY", key="super_dec_xor")

        if keys:
            st.badge(f"Private key (d, n): **{keys['private_key']}**")
            if st.button("Dekripsi", key="super_decrypt_button"):
                if not ciphertext:
                    st.error("Ciphertext harus diisi.")
                elif not vigenere_key or not xor_key:
                    st.error("Kunci Vigenère dan XOR harus diisi.")
                else:
                    try:
                        cipher = SuperEncryptionCipher(
                            caesar_shift=int(caesar_shift),
                            vigenere_key=vigenere_key,
                            xor_key=xor_key,
                        )
                        result, steps = cipher.decrypt(ciphertext, keys["private_key"])
                        st.text_area("Hasil dekripsi (plaintext):", result, height=100, key="super_dec_result")
                        with st.expander("Lihat langkah proses"):
                            st.code("\n".join(steps))
                    except ValueError as error:
                        st.error(str(error))
        else:
            st.info("Generate RSA key pair terlebih dahulu.")


if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi", layout="wide")
    render_super_enkripsi_view()
