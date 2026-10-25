# ðŸš€ Panduan Cepat: Deploy ke Streamlit Cloud lewat GitHub

Dengan cara ini, aplikasi Anda langsung aktif di browser (bisa dibuka dari HP/Laptop) tanpa perlu install Python di perangkat lokal.

---

### Langkah 1: Buat Repository di GitHub
1. Buka [GitHub.com](https://github.com) dan login.
2. Klik tombol **New** (Repository baru).
3. Beri nama repository (misal: `struktur-teks-clario`).
4. Pilih **Public** (atau **Private**).
5. Klik **Create repository**.
6. Unggah dua file ini ke dalam repository:
   - `app.py`
   - `requirements.txt`

---

### Langkah 2: Deploy di Streamlit Community Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io) dan login menggunakan akun GitHub Anda.
2. Klik tombol **"Create app"** / **"New app"**.
3. Pilih repository yang baru saja dibuat (`struktur-teks-clario`).
4. Pastikan `Main file path` tertulis: `app.py`.
5. **Sebelum klik Deploy**, klik bagian **Advanced settings...**:
   - Di kolom **Secrets**, ketikkan:
     ```toml
     CLARIO_API_KEY = "sk-clario-MASUKKAN_KEY_ANDA_DISINI"
     ```
   - Klik **Save**.
6. Klik tombol **Deploy!** ðŸš€

---

### Hasilnya:
- Aplikasi akan otomatis berjalan dalam 1-2 menit.
- Anda akan mendapatkan URL publik (misal: `https://struktur-teks-clario.streamlit.app`).
- **Otomatis aman:** API Key sudah otomatis tersimpan di server Streamlit dan tidak perlu diketik ulang setiap kali membuka web!
