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
    with cols[1]:
        q_input = st.text_input("Masukkan bilangan prima q")
    if st.button("Generate Key Pair"):
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
    plaintext = st.session_state.rsa_plaintext
    message_bytes = plaintext.encode("utf-8")
    e, n = st.session_state.rsa_keys['public_key']
    block_size = (n.bit_length() - 1) // 8
    blocks = [message_bytes[i:i + block_size] for i in range(0, len(message_bytes), block_size)]
    message_values = [int.from_bytes(block, byteorder="big") for block in blocks]
    cipher_values = [pow(value, e, n) for value in message_values]
    ciphertext_blocks = [
        f"{len(block)}:{cipher_value}"
        for block, cipher_value in zip(blocks, cipher_values)
    ]
    character_ranges = []
    byte_position = 0
    for character in plaintext:
        character_size = len(character.encode("utf-8"))
        character_ranges.append((byte_position, byte_position + character_size, character))
        byte_position += character_size

    st.markdown("##### 1. Encode plaintext dan bagi menjadi blok byte")
    st.info(
        f"Batas blok: {block_size} byte per blok. "
        f"Nilai maksimum mᵢ = 256^{block_size} - 1 = {256 ** block_size - 1}, "
        f"dan harus lebih kecil dari n = {n}."
    )
    st.write("Setiap blok diubah dari byte UTF-8 menjadi biner 8-bit, lalu seluruh biner digabungkan menjadi mᵢ.")
    for index, (block, message_value) in enumerate(zip(blocks, message_values), start=1):
        binary_bytes = [format(byte, "08b") for byte in block]
        binary_value = "".join(binary_bytes)
        block_start = (index - 1) * block_size
        block_end = block_start + len(block)
        position = f"{block_start + 1}-{block_end}"
        characters = []
        for character_start, character_end, character in character_ranges:
            if character_start < block_end and character_end > block_start:
                is_complete = character_start >= block_start and character_end <= block_end
                characters.append(character if is_complete else f"{character} (UTF-8 terpotong)")
        character_text = f"[{', '.join(characters)}]" if characters else "-"

        with st.container(border=True):
            st.markdown(f"**Blok {index}** · posisi byte {position}")
            st.table({
                "Karakter yang diproses": character_text,
                "UTF-8 byte": f"[{', '.join(str(byte) for byte in block)}]",
                "Biner per byte": f"[{', '.join(binary_bytes)}]",
                "Biner yang digabungkan": binary_value,
                "Nilai desimal mᵢ": str(message_value),
            })

    st.markdown("##### 2. Enkripsi setiap blok dengan kunci publik")
    st.latex(r"c_i = m_i^e \pmod n")
    st.latex(rf"\text{{Public key (e, n) = }} ({e}, {n})")
    st.dataframe({
        "Blok": list(range(1, len(blocks) + 1)),
        "Nilai mᵢ": [str(value) for value in message_values],
        "Nilai cᵢ": ciphertext_blocks,
    })


def decryption_process():
    st.write("### Proses Dekripsi RSA")
    ciphertext = st.session_state.rsa_ciphertext.strip()
    d, n = st.session_state.rsa_keys["private_key"]
    block_size = (n.bit_length() - 1) // 8
    encrypted_tokens = ciphertext.split()
    encrypted_values = []
    block_lengths = []
    for token in encrypted_tokens:
        if ":" in token:
            length_text, value_text = token.split(":", 1)
            block_lengths.append(int(length_text))
        else:
            value_text = token
            block_lengths.append(None)
        encrypted_values.append(int(value_text))
    decrypted_values = [pow(value, d, n) for value in encrypted_values]
    decrypted_blocks = [
        value.to_bytes(
            block_lengths[index]
            if block_lengths[index] is not None
            else block_size if index < len(decrypted_values) - 1
            else max(1, (value.bit_length() + 7) // 8),
            byteorder="big",
        )
        for index, value in enumerate(decrypted_values)
    ]
    message_bytes = b"".join(decrypted_blocks)
    plaintext = message_bytes.decode("utf-8")

    st.markdown("##### 1. Ciphertext yang diterima")
    st.table({
        "Ciphertext": encrypted_tokens,
        "Panjang byte": [str(length) if length is not None else "legacy" for length in block_lengths],
        "Nilai cᵢ": [str(value) for value in encrypted_values],
    })

    st.markdown("##### 2. Dekripsi dengan kunci privat")
    st.latex(r"m_i = c_i^d \pmod n")
    st.latex(rf"\text{{Private key ($d, n$) = }} ({d}, {n})")
    st.dataframe({
        "Blok": list(range(1, len(encrypted_values) + 1)),
        "Panjang byte": [str(length) if length is not None else "legacy" for length in block_lengths],
        "Nilai cᵢ": [str(value) for value in encrypted_values],
        "Nilai mᵢ": [str(value) for value in decrypted_values],
    })

    block_characters = []
    for block in decrypted_blocks:
        try:
            block_characters.append(block.decode("utf-8"))
        except UnicodeDecodeError:
            block_characters.append("bagian karakter UTF-8")

    st.markdown("##### 3. Konversi nilai desimal mᵢ menjadi byte dan karakter")
    st.write("Setiap mᵢ dikembalikan ke byte sesuai panjang blok, lalu seluruh byte digabungkan dan di-decode sebagai UTF-8.")
    st.table({
        "Blok": list(range(1, len(decrypted_values) + 1)),
        "Nilai mᵢ": [str(value) for value in decrypted_values],
        "Byte": [list(block) for block in decrypted_blocks],
        "Karakter": block_characters,
    })
    st.info(f"Plaintext gabungan: **{plaintext}**")


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
                            "Hasil enkripsi (blok ciphertext dipisahkan spasi):",
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
            "Masukkan ciphertext (blok dipisahkan spasi):",
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