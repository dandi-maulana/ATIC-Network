import hashlib
import json
import time
import os
import requests
import logging
import random
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from uuid import uuid4
from ecdsa import SigningKey, SECP256k1

# ==========================================
# 1. KONFIGURASI SISTEM ATIC
# ==========================================
NAMA_KOIN = "ATIC (Anugrah Teknik Informatika Coin)"
KESULITAN = 4           # Jumlah nol di depan Hash (Target Mining)
HADIAH_AWAL = 50        # Hadiah koin per blok
TOTAL_SUPPLY = 11500000 # Batas maksimal koin
INTERVAL_HALVING = 115000 
LINK_BUKU_TELEPON = "https://raw.githubusercontent.com/dandi-maulana/ATIC-Network/refs/heads/main/peers.json"

# ==========================================
# 2. SISTEM LOGGING CANGGIH (Terminal UI)
# ==========================================
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Matikan log bawaan yang jelek

# Kode Warna ANSI
HIJAU = "\033[92m"
KUNING = "\033[93m"
MERAH = "\033[91m"
BIRU = "\033[94m"
UNGU = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def cetak_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BIRU}╔{'═'*60}╗{RESET}")
    print(f"{BIRU}║ {BOLD}{HIJAU}ATIC BLOCKCHAIN NODE SYSTEM{RESET}{BIRU}{' '*27}║{RESET}")
    print(f"{BIRU}║ {CYAN}Teknik Informatika - Universitas Medan Area{RESET}{BIRU}{' '*16}║{RESET}")
    print(f"{BIRU}╚{'═'*60}╝{RESET}\n")

def cetak_log(judul, pesan, tipe="info"):
    waktu = datetime.now().strftime("%H:%M:%S")
    
    if tipe == "sukses":
        ikon, warna = "✅", HIJAU
    elif tipe == "proses":
        ikon, warna = "⚙️ ", CYAN
    elif tipe == "mining":
        ikon, warna = "⛏️ ", KUNING
    elif tipe == "transaksi":
        ikon, warna = "💸", UNGU
    elif tipe == "network":
        ikon, warna = "📡", BIRU
    elif tipe == "warning":
        ikon, warna = "⚠️ ", MERAH
    else:
        ikon, warna = "ℹ️ ", RESET

    print(f"[{waktu}] {ikon} {warna}{BOLD}[{judul}]{RESET} {pesan}")

def simulasi_matematika_mining(target_difficulty):
    """Efek visual menghitung hash di terminal"""
    print(f"\n{KUNING}--- MEMULAI PROSES PROOF-OF-WORK (SHA-256) ---{RESET}")
    print(f"{KUNING}TARGET: Hash harus diawali dengan {target_difficulty} angka nol{RESET}")
    
    chars = "abcdef0123456789"
    for i in range(5): # Tampilkan 5 baris sampel perhitungan
        nonce_sample = random.randint(1000, 999999)
        hash_sample = "".join(random.choice(chars) for _ in range(64))
        print(f"   ├─ Mencoba Nonce: {nonce_sample} | Hash: {hash_sample} {MERAH}[GAGAL]{RESET}")
        time.sleep(0.2)
    print(f"   └─ Melanjutkan pencarian brute force di latar belakang...\n")

# ==========================================
# 3. LOGIKA BLOCKCHAIN (BACKEND)
# ==========================================
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaksi_pending = []
        self.teman_network = set()
        
        cetak_header()
        cetak_log("SISTEM", "Menginisialisasi Node...", "proses")
        
        if os.path.exists('data_chain.json'):
            self.muat_data()
        else:
            self.buat_blok_baru(proof=100, hash_sebelumnya='1', genesis=True)
            
        self.cari_teman_di_github()

    def hitung_saldo(self, alamat):
        saldo = 0
        for blok in self.chain:
            for tx in blok['transaksi']:
                if tx['penerima'] == alamat: saldo += tx['jumlah']
                if tx['pengirim'] == alamat: saldo -= tx['jumlah']
        return saldo

    def hitung_sirkulasi(self):
        total = 0
        for blok in self.chain:
            if 'hadiah' in blok: total += blok['hadiah']
        return total

    def hitung_hadiah(self):
        """Menghitung Halving agar supply terbatas dan desimal rapi"""
        tinggi_blok = len(self.chain)
        jumlah_halving = tinggi_blok // INTERVAL_HALVING
        
        # Hitung pembagian
        hadiah_mentah = HADIAH_AWAL / (2 ** jumlah_halving)
        
        # PERBAIKAN: Batasi 8 angka di belakang koma (Standar Crypto)
        hadiah_bulat = round(hadiah_mentah, 8)
        
        # Mencegah nilai terlalu kecil (Debu/Dust)
        if hadiah_bulat < 0.00000001:
            return 0
            
        return hadiah_bulat

    def buat_blok_baru(self, proof, hash_sebelumnya=None, genesis=False):
        hadiah = 0 if genesis else self.hitung_hadiah()
        
        blok = {
            'index': len(self.chain) + 1,
            'waktu': time.time(),
            'transaksi': self.transaksi_pending,
            'proof': proof,
            'hash_sebelumnya': hash_sebelumnya or self.buat_hash(self.chain[-1]),
            'hadiah': hadiah
        }
        
        # Log Detail Blok
        if not genesis:
            cetak_log("BLOCKCHAIN", f"Blok #{blok['index']} berhasil divalidasi!", "sukses")
            print(f"      ├─ Waktu  : {datetime.fromtimestamp(blok['waktu'])}")
            print(f"      ├─ Hash   : {blok['hash_sebelumnya'][:20]}...")
            print(f"      ├─ Reward : {hadiah} ATIC")
            print(f"      └─ Jumlah Transaksi: {len(self.transaksi_pending)}")

        self.transaksi_pending = []
        self.chain.append(blok)
        self.simpan_data()
        return blok

    def tambah_transaksi(self, pengirim, penerima, jumlah):
        self.transaksi_pending.append({
            'pengirim': pengirim, 
            'penerima': penerima, 
            'jumlah': jumlah,
            'waktu': time.time()
        })
        return self.blok_terakhir['index'] + 1

    @staticmethod
    def buat_hash(blok):
        return hashlib.sha256(json.dumps(blok, sort_keys=True).encode()).hexdigest()

    @property
    def blok_terakhir(self): return self.chain[-1]

    def kerja_mining(self, proof_terakhir):
        simulasi_matematika_mining(KESULITAN) # Tampilkan efek visual
        
        start = time.time()
        time.sleep(3) # Delay agar user di web sempat melihat animasi
        
        proof = 0
        while self.cek_valid(proof_terakhir, proof) is False:
            proof += 1
            
        durasi = time.time() - start
        cetak_log("MINING", f"Solusi Matematika Ditemukan! Nonce: {proof} ({durasi:.2f} detik)", "sukses")
        return proof

    @staticmethod
    def cek_valid(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        return hashlib.sha256(guess).hexdigest()[:KESULITAN] == "0" * KESULITAN

    def simpan_data(self):
        with open('data_chain.json', 'w') as f:
            json.dump({'chain': self.chain, 'panjang': len(self.chain)}, f, indent=4)

    def muat_data(self):
        try:
            with open('data_chain.json', 'r') as f:
                data = json.load(f)
                self.chain = data['chain']
                cetak_log("DATABASE", f"Berhasil memuat {len(self.chain)} blok dari penyimpanan lokal.", "proses")
        except:
            self.buat_blok_baru(100, '1', True)

    def cari_teman_di_github(self):
        cetak_log("JARINGAN", "Mengunduh daftar node dari GitHub...", "network")
        try:
            res = requests.get(LINK_BUKU_TELEPON, timeout=5)
            if res.status_code == 200:
                peers = res.json()
                for p in peers:
                    self.teman_network.add(p.strip().rstrip('/'))
                cetak_log("JARINGAN", f"Terhubung dengan {len(self.teman_network)} node aktif.", "sukses")
        except:
            cetak_log("JARINGAN", "Gagal koneksi ke GitHub. Berjalan dalam mode Offline.", "warning")

    def sinkronisasi_data(self):
        max_len = len(self.chain)
        new_chain = None
        for node in self.teman_network:
            try:
                if 'localhost' in node: continue
                res = requests.get(f'{node}/api/info_chain', timeout=3)
                if res.status_code == 200:
                    data = res.json()
                    if data['panjang'] > max_len:
                        max_len = data['panjang']
                        new_chain = data['chain']
                        cetak_log("JARINGAN", f"Mendeteksi rantai blok lebih panjang dari {node}", "network")
            except: continue
            
        if new_chain:
            self.chain = new_chain
            self.simpan_data()
            cetak_log("DATABASE", "Data berhasil diperbarui (Sinkronisasi P2P).", "sukses")

# ==========================================
# 4. API SERVER (FLASK)
# ==========================================
app = Flask(__name__)
atic = Blockchain()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/buat_dompet')
def buat_dompet():
    cetak_log("WALLET", "Membuat pasangan kunci kriptografi baru (ECC SECP256k1)...", "proses")
    k = SigningKey.generate(curve=SECP256k1)
    return jsonify({'priv': k.to_string().hex(), 'pub': k.verifying_key.to_string().hex()})

@app.route('/api/kirim', methods=['POST'])
def kirim_koin():
    data = request.get_json()
    priv = data.get('priv_key')
    penerima = data.get('penerima')
    
    try: jumlah = int(data.get('jumlah'))
    except: return jsonify({'status':'gagal', 'pesan':'Jumlah harus angka'}), 400

    if jumlah <= 0:
        return jsonify({'status':'gagal', 'pesan':'Jumlah tidak valid'}), 400

    try:
        sk = SigningKey.from_string(bytes.fromhex(priv), curve=SECP256k1)
        pengirim = sk.verifying_key.to_string().hex()
    except:
        cetak_log("KEAMANAN", "Gagal verifikasi tanda tangan digital (Private Key Salah)", "warning")
        return jsonify({'status':'gagal', 'pesan':'Private Key Salah'}), 400

    if atic.hitung_saldo(pengirim) < jumlah:
        return jsonify({'status':'gagal', 'pesan':'Saldo Tidak Cukup'}), 400

    atic.tambah_transaksi(pengirim, penerima, jumlah)
    cetak_log("TRANSAKSI", f"Permintaan transfer {jumlah} ATIC dari {pengirim[:10]}...", "transaksi")
    return jsonify({'status':'sukses', 'pesan':'Masuk Antrian'}), 200

@app.route('/api/gali', methods=['POST'])
def gali():
    data = request.get_json()
    miner_addr = data.get('alamat')
    
    cetak_log("MINING", f"Menerima perintah mining dari {miner_addr[:10]}...", "proses")
    
    atic.sinkronisasi_data()
    proof = atic.kerja_mining(atic.blok_terakhir['proof'])
    
    hadiah = atic.hitung_hadiah()
    if hadiah > 0:
        atic.tambah_transaksi("SISTEM_PENCETAK_UANG", miner_addr, hadiah)
    
    blok = atic.buat_blok_baru(proof, atic.buat_hash(atic.blok_terakhir))
    return jsonify({'pesan': 'Sukses', 'blok': blok, 'hadiah': hadiah})

@app.route('/api/info_chain')
def info():
    return jsonify({
        'chain': atic.chain, 
        'panjang': len(atic.chain), 
        'sisa_supply': TOTAL_SUPPLY - atic.hitung_sirkulasi(),
        'peers': len(atic.teman_network)
    })

@app.route('/api/cek_saldo/<addr>')
def saldo(addr): return jsonify({'saldo': atic.hitung_saldo(addr)})

if __name__ == '__main__':
    # Tidak perlu print disini karena sudah ada di header
    app.run(host='0.0.0.0', port=5000)