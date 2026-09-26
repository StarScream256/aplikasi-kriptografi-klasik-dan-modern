from views.caesar_views import render_caesar_menu
from views.vigenere_views import render_vigenere_menu

def main():
    while True:
        print("\n==========================================")
        print("   TESTING MODUL ALGORITMA KLASIK (ZEN)   ")
        print("==========================================")
        print("1. Tes Caesar Cipher (Algo Klasik 1)")
        print("2. Tes Vigenere Cipher (Algo Klasik 2)")
        print("0. Keluar")
        
        pilihan = input("\nPilih menu (0-2): ")
        
        if pilihan == '1':
            render_caesar_menu()
        elif pilihan == '2':
            render_vigenere_menu()
        elif pilihan == '0':
            print("Selesai testing.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()