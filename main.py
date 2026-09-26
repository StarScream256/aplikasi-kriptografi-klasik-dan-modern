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

def goto(kategori: str, item: str | None = None):
    """Callback tombol di Beranda: pindahkan sidebar ke kategori/item ini."""
    st.session_state["kategori_radio"] = kategori
    if item is not None:
        st.session_state["algoritma_radio"] = item

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
    
            st.button(
                "Caesar Cipher", use_container_width=True,
                on_click=goto, args=("Algoritma Klasik", "Caesar Cipher"),
            )
            st.write("Transformasi alfabet A-Z, cocok untuk memahami dasar kriptografi.")
            st.button(
                "Vigenère Cipher", use_container_width=True,
                on_click=goto, args=("Algoritma Klasik", "Vigenère Cipher"),
            )
            st.write("Sandi Vigenère adalah metode enkripsi teks alfabet klasik menggunakan deretan sandi Caesar berdasarkan huruf-huruf pada kata kunci")
    with cols[1]:
        with st.container(border=True):
            st.markdown("## Algoritma Kriptografi Modern")
            st.button(
                "RSA", use_container_width=True,
                on_click=goto, args=("Algoritma Modern", "RSA"),
            )
            st.write("kriptografi asimetris yang menggunakan dua kunci berbeda, yaitu kunci publik untuk mengenkripsi data dan kunci privat untuk mendekripsinya")
            st.button(
                "XOR", use_container_width=True,
                on_click=goto, args=("Algoritma Modern", "XOR"),
            )
            st.write("algoritma enkripsi simetris sederhana yang menggunakan operator logika Exclusive OR (XOR) untuk mengenkripsi dan mendekripsi data")

    with cols[2]:
        with st.container(border=True):
            st.markdown("## Algoritma Gabungan")
            st.button(
                "Super Enkripsi", use_container_width=True,
                on_click=goto, args=("Gabungan", "Super Enkripsi"),
            )
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
    kategori = st.sidebar.radio(
        "Kategori:", list(MENU_ITEMS.keys()), key="kategori_radio"
    )
    if kategori == "Beranda":
        pilihan = "Beranda"
    else:
        daftar_item = MENU_ITEMS[kategori]
        # Jaga-jaga: kalau kategori baru saja diganti dan item lama tidak ada
        # di kategori ini, reset ke item pertama supaya radio tidak error.
        if st.session_state.get("algoritma_radio") not in daftar_item:
            st.session_state["algoritma_radio"] = daftar_item[0]
 
        pilihan = st.sidebar.radio(
            "Pilih algoritma:", daftar_item, key="algoritma_radio"
        )
        tersedia = STATUS_TERSEDIA.get(pilihan, False)
        badge = "🟢 Siap dipakai" if tersedia else "🟡 Belum tersedia"
        st.sidebar.caption(badge)
 
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
        render_placeholder("Super Enkripsi")


if __name__ == "__main__":
    main()