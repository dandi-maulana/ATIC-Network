# ATIC Network (Anugrah Teknik Informatika Coin)
---

```markdown
# ATIC Network (Anugrah Teknik Informatika Coin)

![ATIC Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**ATIC Network** adalah platform simulasi Blockchain dan Cryptocurrency berbasis *Peer-to-Peer* (P2P) yang dikembangkan untuk tujuan edukasi di lingkungan **Universitas Medan Area**. 

Proyek ini mendemonstrasikan bagaimana teknologi Blockchain bekerja di balik layar, mulai dari hashing, kriptografi dompet digital, mekanisme konsensus *Proof-of-Work*, hingga propagasi data antar node.

---

## 🔥 Fitur Unggulan

* **⛏️ Smart Mining System:** Simulasi penambangan menggunakan algoritma SHA-256 dengan tingkat kesulitan (difficulty) yang dinamis. Tersedia mode manual dan otomatis.
* **🔐 Secure Wallet:** Pembuatan pasangan kunci (*Public & Private Key*) menggunakan kurva eliptik **SECP256k1** (standar yang sama digunakan oleh Bitcoin).
* **📊 Liquid Block Visualization:** Dashboard visual yang unik untuk melihat blok terisi transaksi layaknya cairan dalam wadah.
* **🌐 P2P Auto-Discovery:** Node dapat saling menemukan dan terhubung secara otomatis menggunakan daftar sentral (`peers.json`) di GitHub.
* **💰 Halving Mechanism:** Simulasi pengurangan hadiah blok (reward) setiap periode tertentu untuk menjaga inflasi koin.

---

## 📂 Struktur Folder (WAJIB)

Agar aplikasi dapat berjalan tanpa error, susunan folder di komputer Anda harus **persis** seperti ini:

```text
ATIC-Network/
│
├── templates/
│   └── index.html       <-- File HTML Dashboard (Wajib di dalam folder ini)
│
├── mesin_atic.py        <-- Script Python Utama (Backend Server)
├── peers.json           <-- Daftar Alamat Node (Untuk P2P)
├── requirements.txt     <-- Daftar Library Python
└── README.md            <-- Dokumentasi ini

```

---

##🛠️ Instalasi & Persiapan###1. Kloning RepositoryBuka terminal/CMD dan unduh kode program:

```bash
git clone [https://github.com/dandi-maulana/ATIC-Network.git](https://github.com/dandi-maulana/ATIC-Network.git)
cd ATIC-Network

```

###2. Instal DependensiPastikan Python 3.x sudah terinstal. Kemudian instal pustaka yang dibutuhkan:

```bash
pip install flask requests ecdsa uuid

```

###3. Jalankan AplikasiJalankan server node:

```bash
python mesin_atic.py

```

Jika berhasil, terminal akan menampilkan log sistem ATIC.

---

##📖 Panduan Penggunaan (User Guide)Setelah aplikasi berjalan, buka browser dan akses: **`http://localhost:5000`**

###A. Membuat Dompet (Wallet)1. Klik tombol **"BUAT DOMPET BARU"** di halaman utama.
2. Sistem akan memberikan dua kode:
* **Public Key:** Alamat rekening Anda (Boleh disebar).
* **Private Key:** Kunci rahasia untuk tanda tangan transaksi (JANGAN DISEBAR).


3. **Penting:** Salin Private Key Anda ke tempat aman. Jika hilang, saldo tidak bisa digunakan.

###B. Cara Menambang (Mining)1. Login menggunakan Public Key Anda.
2. Gulir ke bagian **"Area Pertambangan"**.
3. Pilih Mode:
* **Tambang Manual:** Menggali 1 blok lalu berhenti.
* **Tambang Otomatis:** Sistem akan terus mencari blok secara looping.


4. Lihat Terminal/CMD Anda untuk melihat proses perhitungan hash secara visual.
5. Jika sukses, Anda mendapat hadiah koin ATIC.

###C. Melakukan Transaksi1. Pastikan Anda memiliki saldo.
2. Masuk ke menu **"Kirim Koin"**.
3. Masukkan **Alamat Penerima** (Public Key teman).
4. Masukkan **Jumlah** koin.
5. Masukkan **Private Key** Anda untuk memvalidasi transaksi.
6. Klik Kirim. Transaksi akan masuk antrian (*Mempool*) dan baru akan valid setelah proses Mining berikutnya selesai.

---

##🌐 Cara Online (Menghubungkan Node / P2P)Agar bisa bermain dengan teman yang berbeda jaringan internet:

###Langkah 1: Gunakan NgrokKarena `localhost` hanya untuk komputer sendiri, gunakan Ngrok untuk membuat alamat publik.

1. Download & Instal [Ngrok](https://ngrok.com).
2. Jalankan perintah:
```bash
ngrok http 5000

```


3. Salin URL HTTPS yang muncul (Contoh: `https://abcd-123.ngrok-free.app`).

###Langkah 2: Daftarkan Node (Peering)Agar node lain tahu Anda sedang online:

1. Buka file **`peers.json`** di repository GitHub ini.
2. Edit file tersebut (Klik ikon Pensil).
3. Tambahkan URL Ngrok Anda ke dalam daftar.
*Contoh:*
```json
[
   "[https://url-teman-anda.ngrok-free.app](https://url-teman-anda.ngrok-free.app)",
   "[https://url-ngrok-anda.ngrok-free.app](https://url-ngrok-anda.ngrok-free.app)"
]

```


4. Simpan perubahan (**Commit Changes**).
5. **Restart** script `python mesin_atic.py`. Node Anda otomatis akan sinkronisasi dengan teman.

---

##📚 API EndpointsUntuk pengembang yang ingin mengakses sistem via kode:

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/info_chain` | Mengambil seluruh data blockchain & status node |
| `GET` | `/api/buat_dompet` | Generate key pair baru |
| `POST` | `/api/gali` | Perintah mining (Body: `{"alamat": "PUB_KEY"}`) |
| `POST` | `/api/kirim` | Kirim koin (Body: `{"penerima": "...", "jumlah": 10, "priv_key": "..."}`) |
| `GET` | `/api/cek_saldo/<addr>` | Cek saldo alamat tertentu |

---

**© 2025 ATIC Network Project - Universitas Medan Area**

```

```
