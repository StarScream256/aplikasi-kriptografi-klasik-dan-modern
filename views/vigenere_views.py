# views/vigenere_views.py
from algorithms.vigenere import VigenereCipher

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