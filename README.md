Siap! Berikut versi `README.md` yang sudah diperbarui, bagian setup database diubah agar menggunakan file `fitnessmanagementsystem.sql`:

---

# 💪 FitReserve - Aplikasi Pemesanan Fasilitas Olahraga

FitReserve adalah aplikasi berbasis web yang dibuat dengan Python dan Streamlit untuk membantu pengguna mencari dan memesan fasilitas olahraga seperti gym, kolam renang, dan lapangan.

---

## 🚀 Fitur Utama

- 🔐 Login dan Registrasi pengguna  
- 🔍 Pencarian fasilitas berdasarkan jenis, lokasi, dan tanggal  
- 📅 Melihat daftar booking yang telah dilakukan  
- 🧾 Kode QR untuk bukti booking  
- 🧑‍💼 Profil pengguna dan edit data  
- 🎨 Antarmuka yang modern dan responsif  

---

## 🧰 Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/)  
- [MySQL](https://www.mysql.com/) sebagai basis data  
- [Pillow](https://pillow.readthedocs.io/) untuk manipulasi gambar  
- [qrcode](https://pypi.org/project/qrcode/) untuk membuat kode QR  
- [extra-streamlit-components](https://github.com/ChrisDelClea/extra-streamlit-components) dan [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) untuk navigasi dan UI tambahan  

---

## 🛠️ Instalasi

1. **Clone repositori**
```bash
git clone https://github.com/username/fitreserve.git
cd fitreserve
```

2. **Buat environment virtual (opsional tapi direkomendasikan)**
```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
venv\Scripts\activate     # Untuk Windows
```

3. **Install dependensi**
```bash
pip install -r requirements.txt
```

4. **Impor file SQL ke MySQL**

Pastikan MySQL sudah berjalan, lalu impor file `fitnessmanagementsystem.sql`:
```bash
mysql -u root -p < fitnessmanagementsystem.sql
```

> 📌 Gantilah `root` dan masukkan password sesuai konfigurasi lokal Anda.

5. **Konfigurasi koneksi database**

Pastikan konfigurasi berikut sesuai di dalam file `.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fitnessmanagementsystem',
    'port': 3306
}
```

---

## ▶️ Menjalankan Aplikasi

```bash
streamlit run app.py
```

---

## 📁 Struktur Folder

```
fitreserve/
│
├── app.py                         # File utama aplikasi
├── requirements.txt               # Dependensi Python
├── fitnessmanagementsystem.sql   # File SQL untuk setup database
├── image.png                      # Logo aplikasi (opsional)
├── avatar.png                     # Gambar profil default (opsional)
└── README.md
```
