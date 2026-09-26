# Aplikasi Kriptografi Klasik dan Modern

Aplikasi ini adalah project Python untuk mempelajari, mengeksplorasi, dan menampilkan berbagai teknik kriptografi dalam satu platform yang interaktif. Project ini dirancang untuk menampilkan algoritma klasik, algoritma modern, serta sistem super enkripsi yang menggabungkan beberapa konsep keamanan data dalam satu alur kerja.

Tujuan utama dari project ini adalah:
- memahami cara kerja algoritma kriptografi dari sisi teori dan praktik,
- memvisualisasikan proses enkripsi dan dekripsi secara edukatif,
- menyediakan UI yang menarik dan mudah dipahami,
- membuat pengalaman belajar kriptografi terasa lebih hidup dan interaktif.

---

## Fitur Utama

- Caesar Cipher dan Vigenere Cipher untuk transformasi alfabet A-Z.
- RSA yang memproses pesan UTF-8 dalam beberapa blok byte.
- XOR dengan kunci berulang dan pilihan representasi ciphertext Raw, ASCII Number, Hex, atau Binary.
- Modul super-enkripsi yang menggabungkan Caesar, Vigenere, XOR, dan RSA.
- Antarmuka Streamlit untuk RSA dan XOR. Menu Caesar, Vigenere, dan Super Enkripsi masih berupa placeholder di `main.py`.

---

## Gambaran Project

Project ini adalah aplikasi edukasi yang menyediakan:

1. Algoritma Klasik
   - Caesar Cipher dan Vigenere Cipher
   - cocok untuk memahami dasar kriptografi
   - biasanya lebih mudah diajarkan melalui proses per langkah

2. Algoritma Modern
   - RSA untuk kriptografi asimetris
   - XOR untuk operasi logika sederhana namun powerful

3. Super Enkripsi
   - modul algoritma yang menggabungkan empat algoritma secara berurutan
   - pipeline untuk pembelajaran; penggabungan ini tidak menjadikan algoritma klasik atau XOR aman untuk penggunaan nyata

4. Antarmuka
   - Streamlit saat ini menyediakan tampilan untuk RSA dan XOR
   - tampilan Caesar, Vigenere, dan Super Enkripsi belum diintegrasikan ke Streamlit

---

## Algoritma

### 1. Algoritma Klasik

1. **Caesar Cipher**
   - Mendukung pergeseran positif (maju) dan negatif (mundur).
   - Membersihkan input menjadi huruf sebelum enkripsi atau dekripsi.
   - Mengembalikan hasil dan daftar langkah proses.

2. **Vigenère Cipher**
   - Pemrosesan alfabet A–Z (Modulo 26).
   - Mengulang kunci sepanjang teks dan membersihkan spasi serta karakter non-huruf.
   - Mengembalikan hasil dan detail proses per karakter.

### 2. Algoritma Modern

#### RSA
RSA adalah algoritma kriptografi asimetris yang menggunakan pasangan kunci publik dan kunci privat.

Fitur utama:
- Pembangkitan pasangan kunci dari dua bilangan prima.
- Pesan UTF-8 dibagi menjadi blok byte sesuai ukuran modulus.
- Setiap blok ciphertext ditulis sebagai `panjang_byte:nilai`, dipisahkan spasi.
- Cocok untuk mempelajari modulus, phi, invers modulo, dan pemrosesan blok.

#### XOR
XOR adalah operasi logika yang sangat sederhana namun populer dalam kriptografi modern untuk pembelajaran dasar.

Fitur utama:
- Kunci diulang sepanjang pesan dan wajib diisi.
- Tampilan menyediakan format Raw, ASCII Number, Hex, dan Binary.
- XOR di sini adalah implementasi edukatif, bukan enkripsi aman untuk data nyata.

### 3. Super Enkripsi

`SuperEncryptionCipher` di `algorithms/super_encryption.py` menjalankan pipeline berikut:

Plaintext -> Caesar -> Vigenere -> XOR -> RSA -> encoding huruf A-Z

RSA menghasilkan ciphertext blok berupa teks dengan angka, titik dua, dan spasi. Modul super-enkripsi mengodekan setiap byte ciphertext tersebut menjadi dua huruf A-Z, sehingga ciphertext akhirnya hanya berisi huruf. Dekripsi mengembalikan encoding ini lalu membalik setiap tahap:

Ciphertext A-Z -> decode -> RSA decrypt -> XOR decrypt -> Vigenere decrypt -> Caesar decrypt -> plaintext

Contoh pemakaian modul:

```python
from algorithms.rsa import rsa_keygen
from algorithms.super_encryption import SuperEncryptionCipher

keys = rsa_keygen(1009, 1013)
cipher = SuperEncryptionCipher(caesar_shift=3, vigenere_key="KEY", xor_key="XOR")

ciphertext, encryption_steps = cipher.encrypt("Pesan rahasia", keys["public_key"])
plaintext, decryption_steps = cipher.decrypt(ciphertext, keys["private_key"])
```

Caesar dan Vigenere menghapus spasi serta karakter non-huruf, sehingga plaintext hasil dekripsi berupa huruf kapital A-Z. Kunci prima pada contoh hanya untuk demonstrasi dan tidak aman untuk penggunaan nyata. Pipeline ini belum memiliki tampilan Streamlit dan belum dihubungkan ke menu aplikasi.

---

## Konsep UI yang Sederhana

Antarmuka Streamlit tersedia untuk RSA dan XOR. Caesar dan Vigenere juga memiliki menu berbasis CLI. Di Streamlit, menu Caesar, Vigenere, dan Super Enkripsi masih menampilkan placeholder.

### Struktur UI

- Sidebar: navigasi algoritma.
- RSA dan XOR: area enkripsi/dekripsi dan detail proses.
- Super Enkripsi: kelas algoritma sudah tersedia, tetapi belum memiliki view.

---

## Struktur Project

```text
aplikasi-kriptografi-klasik-dan-modern/
├── main.py
├── README.md
├── algorithms/
│   ├── __init__.py
│   ├── caesar.py
│   ├── rsa.py
│   ├── super_encryption.py
│   ├── vigenere.py
│   └── xor.py
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   ├── rsa_utils.py
│   └── xor_formats.py
└── views/
    ├── __init__.py
    ├── caesar_views.py
    ├── rsa_views.py
    ├── vigenere_views.py
    └── xor_views.py
```

---

## Cara Menjalankan Project

Pastikan Anda sudah memiliki Python dan dependency yang dibutuhkan.

1. Masuk ke folder project
2. Instal dependency utama jika diperlukan
3. Jalankan aplikasi Streamlit

Contoh:

```bash
cd aplikasi-kriptografi-klasik-dan-modern
streamlit run main.py
```

Pengembangan berikutnya dapat mencakup integrasi view Caesar, Vigenere, dan Super Enkripsi ke menu Streamlit.

---

## Roadmap Pengembangan

### Tahap 1: Algoritma dasar
- [x] Menyiapkan project struktur dasar
- [x] Menambahkan RSA
- [x] Menambahkan XOR
- [x] Menambahkan Caesar dan Vigenere
- [x] Membuat modul super-enkripsi dan dekripsi

### Tahap 2: Integrasi UI
- [ ] Membuat view Streamlit Caesar dan Vigenere
- [ ] Membuat view Streamlit Super Enkripsi
- [ ] Menghubungkan view tersebut ke navigasi aplikasi

### Tahap 3: Polishing
- [ ] Desain lebih modern dan menarik
- [ ] Peningkatan UX
- [ ] Dokumentasi penggunaan yang lebih lengkap

---

## Catatan Keamanan

Implementasi RSA pada project ini menggunakan RSA textbook tanpa padding standar, sedangkan Caesar, Vigenere, dan XOR berulang tidak dirancang untuk melindungi data nyata. Gunakan project ini untuk pembelajaran dan demonstrasi, bukan untuk menyimpan atau mengirim informasi sensitif.