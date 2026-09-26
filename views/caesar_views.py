# views/caesar_views.py
from algorithms.caesar import CaesarCipher

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