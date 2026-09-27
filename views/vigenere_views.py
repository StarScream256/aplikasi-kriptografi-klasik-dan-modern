# views/vigenere_views.py
import streamlit as st
from algorithms.vigenere import VigenereCipher

def render_vigenere_view():
    st.title("Vigenère Cipher")
    st.badge("Algoritma Kriptografi Klasik")
    st.write(
        "Vigenère Cipher mengenkripsi teks menggunakan deretan sandi Caesar "
        "berdasarkan huruf-huruf pada kata kunci."
    )

    tabs = st.tabs(["Enkripsi", "Dekripsi"])

    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):", key="vigenere_enc_text")
        key = st.text_input("Masukkan kata kunci:", key="vigenere_enc_key")
        if st.button("Enkripsi", key="vigenere_encrypt_button"):
            if not plaintext or not key:
                st.error("Teks asli dan kunci harus diisi.")
            else:
                cipher = VigenereCipher(key=key)
                result, steps = cipher.encrypt(plaintext)
                st.text_area("Hasil enkripsi (ciphertext):", result, height=100, key="vigenere_enc_result")
                with st.expander("Lihat langkah proses"):
                    st.code("\n".join(steps))

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area("Masukkan ciphertext:", key="vigenere_dec_text")
        key = st.text_input("Masukkan kata kunci:", key="vigenere_dec_key")
        if st.button("Dekripsi", key="vigenere_decrypt_button"):
            if not ciphertext or not key:
                st.error("Ciphertext dan kunci harus diisi.")
            else:
                cipher = VigenereCipher(key=key)
                result, steps = cipher.decrypt(ciphertext)
                st.text_area("Hasil dekripsi (plaintext):", result, height=100, key="vigenere_dec_result")
                with st.expander("Lihat langkah proses"):
                    st.code("\n".join(steps))



def render_vigenere_menu():
    print("\n==============================")
    print("     MENU VIGENERE CIPHER     ")
    print("==============================")
    print("1. Enkripsi")
    print("2. Dekripsi")
    choice = input("Pilih menu (1/2): ")
    
    if choice not in ['1', '2']:
        print("Pilihan tidak valid.")
        return

    text = input("Masukkan teks: ")
    key = input("Masukkan Kata Kunci (Kunci Teks): ")
    
    if not key:
        print("Kunci tidak boleh kosong!")
        return

    cipher = VigenereCipher(key=key)
    
    if choice == '1':
        result, steps = cipher.encrypt(text)
        print("\n--- LANGKAH PROSES ---")
        for step in steps:
            print(step)
        print(f"\nHasil Ciphertext: {result}")
    else:
        result, steps = cipher.decrypt(text)
        print("\n--- LANGKAH PROSES ---")
        for step in steps:
            print(step)
        print(f"\nHasil Plaintext: {result}")