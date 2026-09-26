# Aplikasi Kriptografi Klasik dan Modern

Aplikasi ini adalah project Python untuk mempelajari, mengeksplorasi, dan menampilkan berbagai teknik kriptografi dalam satu platform yang interaktif. Project ini dirancang untuk menampilkan algoritma klasik, algoritma modern, serta sistem super enkripsi yang menggabungkan beberapa konsep keamanan data dalam satu alur kerja.

Tujuan utama dari project ini adalah:
- memahami cara kerja algoritma kriptografi dari sisi teori dan praktik,
- memvisualisasikan proses enkripsi dan dekripsi secara edukatif,
- menyediakan UI yang menarik dan mudah dipahami,
- membuat pengalaman belajar kriptografi terasa lebih hidup dan interaktif.

---

## Fitur Utama

- 2 algoritma klasik yang akan dikembangkan (misalnya Caesar dan Vigenere, atau dapat disesuaikan sesuai kebutuhan)
- 2 algoritma modern yang sudah dirancang dalam project ini: RSA dan XOR
- Sistem super enkripsi yang menggabungkan 4 algoritma dalam satu pipeline
- Visualisasi proses per karakter secara detail
- Antarmuka berbasis Streamlit yang ramah pengguna
- Desain UI yang sederhana, fokus pada pembelajaran dan kemudahan penggunaan

---

## Gambaran Project

Project ini akan menjadi aplikasi edukasi yang menampilkan:

1. Algoritma Klasik
   - teknik enkripsi tradisional yang lebih sederhana
   - cocok untuk memahami dasar kriptografi
   - biasanya lebih mudah diajarkan melalui proses per langkah

2. Algoritma Modern
   - RSA untuk kriptografi asimetris
   - XOR untuk operasi logika sederhana namun powerful

3. Super Enkripsi
   - gabungan beberapa algoritma menjadi satu mekanisme keamanan
   - proses dilakukan berurutan agar pesan lebih aman dan lebih menarik untuk dipelajari

4. Visual Interaktif
   - tampilan antarmuka dibuat lebih modern dan menarik
   - karakter anime berperan sebagai narator/panduan yang menjelaskan alur enkripsi

---

## Algoritma yang Akan Dikembangkan

### 1. Algoritma Klasik

Saat ini project ini masih dalam tahap pengembangan untuk menentukan 2 algoritma klasik yang akan dipakai. Beberapa pilihan yang mungkin digunakan:

- Caesar Cipher
- Vigenere Cipher
- Affine Cipher
- Playfair Cipher

### 2. Algoritma Modern

#### RSA
RSA adalah algoritma kriptografi asimetris yang menggunakan pasangan kunci publik dan kunci privat.

Fitur utama:
- key generation berdasarkan dua bilangan prima
- enkripsi dengan kunci publik
- dekripsi dengan kunci privat
- cocok untuk pembelajaran konsep modulus, phi, dan inverse modulo

#### XOR
XOR adalah operasi logika yang sangat sederhana namun populer dalam kriptografi modern untuk pembelajaran dasar.

Fitur utama:
- XOR dengan key yang sama panjang atau cycle key
- mudah dipahami
- sangat cocok untuk visualisasi bit per bit

### 3. Super Enkripsi

Konsep super enkripsi di project ini adalah menggabungkan 4 algoritma menjadi satu pipeline, misalnya:

Plaintext
  -> Algoritma Klasik 1
  -> Algoritma Klasik 2
  -> XOR
  -> RSA
  -> Ciphertext Final

Untuk dekripsi, proses dilakukan secara terbalik:

Ciphertext Final
  -> RSA decrypt
  -> XOR decrypt
  -> Algoritma Klasik 2 decrypt
  -> Algoritma Klasik 1 decrypt
  -> Plaintext

Tujuan dari konsep ini adalah:
- menampilkan bahwa keamanan data dapat ditingkatkan dengan mengkombinasikan beberapa metode
- memberi gambaran real-world tentang layered security
- meningkatkan nilai edukasi project secara visual dan teknis

---

## Konsep UI yang Sederhana

Project ini fokus pada pengalaman belajar yang mudah dipahami dan tidak berlebihan secara visual.

### Struktur UI

- Sidebar: daftar algoritma dan langkah-langkah
- Main Panel: area enkripsi dan dekripsi utama
- Panel Keterangan: penjelasan singkat tentang proses yang sedang berjalan
- Output: hasil cipher, key, dan langkah logika yang mudah dibaca

Tujuan dari desain ini adalah menjaga aplikasi tetap edukatif, bersih, dan mudah digunakan oleh pengguna pemula.

---

## Struktur Project

```text
aplikasi-kriptografi-klasik-dan-modern/
├── main.py
├── README.md
├── algorithms/
│   ├── __init__.py
│   ├── rsa.py
│   └── xor.py
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   ├── rsa_utils.py
│   └── xor_formats.py
└── views/
    ├── __init__.py
    ├── rsa_views.py
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

Jika project nanti dikembangkan lebih lanjut, dapat ditambahkan:
- fitur perbandingan algoritma
- chart visualisasi keamanan
- mode demo langkah demi langkah
- mode super enkripsi interaktif

---

## Roadmap Pengembangan

### Tahap 1: Dasar aplikasi
- [x] Menyiapkan project struktur dasar
- [x] Menambahkan RSA
- [x] Menambahkan XOR
- [ ] Menambahkan 2 algoritma klasik
- [ ] Menyempurnakan UI

### Tahap 2: Visualisasi edukasi
- [ ] Menambahkan panel penjelasan per tahap
- [ ] Menyempurnakan tampilan agar lebih rapi dan mudah dipahami

### Tahap 3: Super enkripsi
- [ ] Menggabungkan 4 algoritma dalam satu pipeline
- [ ] Menambah mode enkripsi dan dekripsi multi-langkah
- [ ] Menyediakan output yang mudah dipahami pengguna

### Tahap 4: Polishing
- [ ] Desain lebih modern dan menarik
- [ ] Peningkatan UX
- [ ] Dokumentasi penggunaan yang lebih lengkap

---

## Catatan Pengembangan

Project ini sangat cocok untuk:
- belajar kriptografi secara visual,
- membuat demo pembelajaran algoritma,
- menyusun portfolio Python berbasis aplikasi interaktif,
- menampilkan kombinasi ilmu keamanan dan desain UI.

Dengan pendekatan UI yang sederhana dan rapi, project ini tetap menjadi alat pembelajaran yang informatif dan mudah dipahami.

---

## Kesimpulan

Project ini adalah kombinasi antara
- teori kriptografi,
- aplikasi interaktif Python,
- visualisasi proses algoritma,
- dan pengalaman belajar yang lebih immersive.

Dengan dua algoritma klasik, dua algoritma modern, serta super enkripsi, aplikasi ini diharapkan menjadi proyek edukatif yang kuat dan memiliki nilai visual yang tinggi.