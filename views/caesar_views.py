# views/caesar_views.py
import steamlit as st
from algorithms.caesar import CaesarCipher

def render_caesar_view():
    st.title("Caesar Cipher")
    st.badge("Algoritma Kriptografi Klasik")
    st.write(
        "Caesar Cipher menggeser setiap huruf pada teks sejauh nilai shift "
        "tertentu di sepanjang alfabet A-Z."
    )

    tabs = st.tabs(["Enkripsi", "Dekripsi"])

    with tabs[0]:
        st.subheader("Enkripsi")
        plaintext = st.text_area("Masukkan teks asli (plaintext):", key="caesar_enc_text")
        shift = st.number_input(
            "Nilai shift (contoh: 5 untuk maju, -3 untuk mundur):",
            value=3, step=1, key="caesar_enc_shift",
        )
        if st.button("Enkripsi", key="caesar_encrypt_button"):
            if not plaintext:
                st.error("Teks asli harus diisi.")
            else:
                cipher = CaesarCipher(shift=int(shift))
                result, steps = cipher.encrypt(plaintext)
                st.text_area("Hasil enkripsi (ciphertext):", result, height=100, key="caesar_enc_result")
                with st.expander("Lihat langkah proses"):
                    st.code("\n".join(steps))

    with tabs[1]:
        st.subheader("Dekripsi")
        ciphertext = st.text_area("Masukkan ciphertext:", key="caesar_dec_text")
        shift = st.number_input(
            "Nilai shift yang dipakai saat enkripsi:",
            value=3, step=1, key="caesar_dec_shift",
        )
        if st.button("Dekripsi", key="caesar_decrypt_button"):
            if not ciphertext:
                st.error("Ciphertext harus diisi.")
            else:
                cipher = CaesarCipher(shift=int(shift))
                result, steps = cipher.decrypt(ciphertext)
                st.text_area("Hasil dekripsi (plaintext):", result, height=100, key="caesar_dec_result")
                with st.expander("Lihat langkah proses"):
                    st.code("\n".join(steps))


def render_caesar_menu():
    print("\n==============================")
    print("      MENU CAESAR CIPHER      ")
    print("==============================")
    print("1. Enkripsi")
    print("2. Dekripsi")
    choice = input("Pilih menu (1/2): ")
    
    if choice not in ['1', '2']:
        print("Pilihan tidak valid.")
        return

    text = input("Masukkan teks: ")
    try:
        shift = int(input("Masukkan nilai shift (contoh: 5 untuk maju, -3 untuk mundur): "))
    except ValueError:
        print("Shift harus berupa angka bulat!")
        return

    cipher = CaesarCipher(shift=shift)
    
    if choice == '1':
        result, steps = cipher.encrypt(text)
        print("\n" + "="*50)
        for step in steps:
            print(step)
        print("="*50)
        print(f"Hasil Akhir Ciphertext: {result}\n")
    else:
        result, steps = cipher.decrypt(text)
        print("\n" + "="*50)
        for step in steps:
            print(step)
        print("="*50)
        print(f"Hasil Akhir Plaintext: {result}\n")