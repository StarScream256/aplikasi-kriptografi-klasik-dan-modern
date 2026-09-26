import streamlit as st

from views.rsa_views import render_rsa_view
from views.xor_views import render_xor_view

# TODO: caesar_views.py & vigenere_views.py masih versi CLI (print/input),
# belum ada render_xxx_view() ala Streamlit seperti rsa_views/xor_views.
# Ganti placeholder di bawah begitu sudah dikonversi.

MENU_ITEMS = [
    "Beranda",
    "Caesar Cipher",
    "Vigenère Cipher",
    "RSA",
    "XOR",
    "Super Enkripsi",
]


def render_beranda():
    st.title("Aplikasi Kriptografi Klasik dan Modern")
    st.write(
        "Pilih algoritma di sidebar untuk mulai eksplorasi proses enkripsi "
        "dan dekripsi secara interaktif."
    )
    st.markdown(
        """
        - **Algoritma Klasik**: Caesar Cipher, Vigenère Cipher
        - **Algoritma Modern**: RSA, XOR
        - **Super Enkripsi**: gabungan beberapa algoritma dalam satu pipeline
        """
    )


def render_placeholder(nama: str):
    st.title(nama)
    st.info(
        f"Tampilan {nama} masih dalam bentuk command-line, "
        "belum dikonversi ke Streamlit."
    )


def render_super_enkripsi():
    st.title("Super Enkripsi")
    st.info("Pipeline gabungan 4 algoritma belum diimplementasikan.")


def main():
    st.set_page_config(
        page_title="Aplikasi Kriptografi Klasik dan Modern",
        layout="wide",
    )

    st.sidebar.title("Menu Algoritma")
    pilihan = st.sidebar.radio("Pilih algoritma:", MENU_ITEMS)

    if pilihan == "Beranda":
        render_beranda()
    elif pilihan == "Caesar Cipher":
        render_placeholder("Caesar Cipher")
    elif pilihan == "Vigenère Cipher":
        render_placeholder("Vigenère Cipher")
    elif pilihan == "RSA":
        render_rsa_view()
    elif pilihan == "XOR":
        render_xor_view()
    elif pilihan == "Super Enkripsi":
        render_super_enkripsi()


if __name__ == "__main__":
    main()