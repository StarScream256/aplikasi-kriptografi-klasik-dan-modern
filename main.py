import streamlit as st

from views.rsa_views import render_rsa_view
from views.xor_views import render_xor_view

# TODO: caesar_views.py & vigenere_views.py masih versi CLI (print/input),
# belum ada render_xxx_view() ala Streamlit seperti rsa_views/xor_views.
# Ganti placeholder di bawah begitu sudah dikonversi.

MENU_ITEMS = {
    "Beranda": [],
    "Algoritma Klasik": ["Caesar Cipher","Vigenère Cipher"],
    "Algoritma Moderen": ["RSA","XOR"],
    "Gabungan": ["Super Enkripsi"],
}

STATUS_TERSEDIA = {
    "Caesar Cipher": False,
    "Vigenère Cipher": False,
    "RSA": True,
    "XOR": True,
    "Super Enkripsi": False,
}

def render_beranda():
    st.title("Aplikasi Kriptografi Klasik dan Modern")
    st.write(
        "Pilih algoritma di sidebar untuk mulai eksplorasi proses enkripsi "
        "dan dekripsi secara interaktif."
    )
    cols = st.columns(3)
    with cols[0]:
        with st.container(border = True):
            st.markdown("## Algoritma Kriptografi Klasik")
            st.caption("## Caesar Cipher")
            st.caption("## Vigenère Cipher")
            st.write("Transformasi alfabet A-Z, cocok untuk memahami dasar kriptografi.")

    with cols[1]:
        with st.container(border=True):
            st.markdown("## Algoritma Kriptografi Modern")
            st.caption("RSA")
            st.caption("XOR")
            st.write("Kriptografi asimetris dan operasi logika sederhana namun kuat")

    with cols[2]:
        with st.container(border=True):
            st.markdown("## Algoritma Gabungan")
            st.caption("Super Enkripsi")
            st.write("Gabungan dari berbagai algoritma kriptografi dalam satu alur.")

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
        page_icon="",
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