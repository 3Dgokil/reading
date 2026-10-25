import streamlit as st
from openai import OpenAI
import os

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Ekstraktor & Penata Teks Terstruktur",
    page_icon="📑",
    layout="wide"
)

# Cek apakah API Key sudah ada di Streamlit Secrets atau Environment
default_api_key = ""
if "CLARIO_API_KEY" in st.secrets:
    default_api_key = st.secrets["CLARIO_API_KEY"]
elif "CLARIO_API_KEY" in os.environ:
    default_api_key = os.environ["CLARIO_API_KEY"]

# Judul Utama
st.title("📑 Otomasi Penata Teks Sesuai Struktur")
st.caption("Aplikasi otomatisasi untuk membedah, mencari, dan menata teks sesuai format struktur yang ditentukan.")

# --- SIDEBAR: Konfigurasi API & Model ---
with st.sidebar:
    st.header("🔑 Pengaturan ClarioHub API")
    base_url = st.text_input(
        "Base URL:",
        value="https://clariohub.id/v1",
        help="Base URL API ClarioHub"
    )
    
    # Otomatis terisi jika ada di secrets/env, atau bisa diisi manual jika kosong
    api_key = st.text_input(
        "ClarioHub API Key:", 
        value=default_api_key,
        type="password",
        placeholder="sk-clario-...",
        help="Otomatis diambil dari Secrets jika sudah dikonfigurasi di Streamlit Cloud."
    )
    
    if default_api_key:
        st.success("✅ API Key otomatis terdeteksi dari Secrets!")
    
    st.markdown("---")
    st.header("⚙️ Konfigurasi Model")
    model_name = st.selectbox(
        "Pilih Model Clario:",
        options=[
            "clario/gemini-3.7-flash",
            "clario/gemini-3.7-flash-auto",
            "clario/deepseek-v4.1-flash",
            "clario/deepseek-v4.1-flash-auto",
            "clario/deepseek-v4-flash",
            "clario/deepseek-v4-pro",
            "clario/gpt-5.6-sol",
            "clario/glm-5.3",
            "clario/glm-5.3-flash",
            "clario/opus-5"
        ],
        index=0,
        help="Pilih model dari katalog ClarioHub."
    )
    temperature = st.slider("Kreativitas (Temperature):", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

# --- AREA UTAMA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Data")
    
    structure_template = st.text_area(
        "Definisi Struktur Dokumen Target:",
        value="""1. Judul / Topik Utama
2. Ringkasan Eksekutif / Abstrak
3. Poin-Poin Utama / Temuan Kunci
4. Analisis & Pembahasan Mendalam
5. Kesimpulan & Rekomendasi""",
        height=150,
        help="Sesuaikan urutan dan struktur sesuai kebutuhan format Anda."
    )
    
    source_text = st.text_area(
        "Teks Sumber / Bahan Mentah (atau instruksi topik):",
        placeholder="Tempelkan draf teks mentah, artikel, transkrip, atau catatan kasar di sini...",
        height=260
    )
    
    process_btn = st.button("🚀 Ekstrak & Format Sekarang", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Hasil Sesuai Struktur")
    
    if process_btn:
        if not api_key:
            st.error("⚠️ Mohon masukkan API Key ClarioHub (sk-clario-...) di sidebar.")
        elif not source_text.strip():
            st.warning("⚠️ Mohon masukkan teks sumber atau topik yang ingin diproses.")
        else:
            with st.spinner(f"Sedang memproses teks via {model_name}..."):
                try:
                    # Inisialisasi OpenAI client dengan Base URL ClarioHub
                    client = OpenAI(
                        base_url=base_url,
                        api_key=api_key
                    )
                    
                    system_prompt = (
                        "Anda adalah asisten editor profesional dan analis dokumen tingkat lanjut. "
                        "Tugas utama Anda adalah mengekstrak, membedah, dan menata informasi dari teks sumber "
                        "agar PERSIS mengikuti format/struktur yang diminta pengguna.\n"
                        "- Pertahankan keakuratan fakta dan substansi asli.\n"
                        "- Jika ada bagian struktur yang tidak memiliki data dalam sumber, berikan analisis logis yang relevan "
                        "atau beri catatan '(Data tidak tersedia dalam teks sumber)'.\n"
                        "- Gunakan gaya bahasa profesional dan format Markdown yang rapi."
                    )

                    user_prompt = f"""--- STRUKTUR TARGET ---
{structure_template}

--- TEKS SUMBER ---
{source_text}

Tolong susun teks di atas agar mengikuti urutan struktur target secara presisi."""

                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=temperature
                    )
                    
                    # Ambil hasil
                    result_text = response.choices[0].message.content
                    st.session_state["result_text"] = result_text
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memanggil API ClarioHub: {str(e)}")

    # Menampilkan hasil jika tersimpan di session state
    if "result_text" in st.session_state:
        st.markdown(st.session_state["result_text"])
        st.markdown("---")
        st.download_button(
            label="💾 Unduh Hasil (.md)",
            data=st.session_state["result_text"],
            file_name="hasil_terstruktur.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("Hasil pemrosesan akan muncul di sini setelah Anda mengklik tombol proses.")