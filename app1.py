import streamlit as st
from openai import OpenAI
import os
import json

st.set_page_config(
    page_title="AI Teleprompter Script Generator (Reading Challenge)",
    page_icon="🎙️",
    layout="wide"
)

# Deteksi API Key ClarioHub dari Secrets atau Environment
default_api_key = ""
if "CLARIO_API_KEY" in st.secrets:
    default_api_key = st.secrets["CLARIO_API_KEY"]
elif "CLARIO_API_KEY" in os.environ:
    default_api_key = os.environ["CLARIO_API_KEY"]

st.title("🎙️ AI Reading Challenge Script Generator")
st.caption("Generator naskah Teleprompter otomatis untuk video vertikal Shorts/TikTok (Siap Copy-Paste ke HTML Renderer).")

# --- SIDEBAR PENGATURAN ---
with st.sidebar:
    st.header("🔑 ClarioHub API")
    base_url = st.text_input("Base URL:", value="https://clariohub.id/v1")
    api_key = st.text_input(
        "API Key:",
        value=default_api_key,
        type="password",
        placeholder="sk-clario-..."
    )
    if default_api_key:
        st.success("✅ Terkoneksi via Streamlit Secrets")

    st.markdown("---")
    st.header("⚙️ Model & Kreativitas")
    model_name = st.selectbox(
        "Model:",
        options=[
            "clario/gemini-3.7-flash",
            "clario/gemini-3.7-flash-auto",
            "clario/deepseek-v4.1-flash",
            "clario/gpt-5.6-sol",
            "clario/opus-5"
        ],
        index=0
    )
    temperature = st.slider("Kreativitas (Temperature):", 0.0, 1.0, 0.4, 0.05)

# --- AREA INPUT FORM ---
col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader("1. Konfigurasi Challenge")

    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        category = st.selectbox(
            "Kategori Naskah:",
            [
                "Tongue Twister & Fast Flow (Paling Viral)",
                "English Accent & Pronunciation Test (ESL)",
                "One Breath Challenge (Ego Test)",
                "Stoic / Deep Motivation Quote",
                "2-Sentence Horror / Mystery Twist"
            ]
        )
    with col_sub2:
        target_duration = st.selectbox(
            "Target Durasi Baca:",
            ["20 Detik (Sangat Cepat / Hard)", "30 Detik (Ideal / Medium)", "45 Detik (Story / Normal)", "60 Detik (Full Story)"],
            index=1
        )

    difficulty = st.select_slider(
        "Tingkat Kesulitan:",
        options=["Easy (Beginner)", "Medium (Fluent)", "Hard (Speed Test)", "Insane (God Level)"],
        value="Hard (Speed Test)"
    )

    custom_topic = st.text_input(
        "Ide Topik / Kata Kunci Tertentu (Opsional):",
        placeholder="Contoh: Kata 'Worcestershire' dan 'Colonel', atau tentang 'Discipline vs Motivation'..."
    )

    cta_option = st.selectbox(
        "Template Tombol Subscribe:",
        [
            "🔴 SUBSCRIBE FOR LEVEL 2",
            "👉 SUBSCRIBE IF YOU PASSED!",
            "⚡ SUBSCRIBE FOR MORE TESTS",
            "🎙️ DUET THIS & SUBSCRIBE"
        ]
    )

    generate_btn = st.button("🚀 Buat Naskah Challenge", type="primary", use_container_width=True)

# --- PROSES GENERASI ---
with col_out:
    st.subheader("2. Hasil Format HTML Renderer")

    if generate_btn:
        if not api_key:
            st.error("⚠️ Masukkan API Key ClarioHub terlebih dahulu di sidebar.")
        else:
            with st.spinner("Meracik script teleprompter siap pakai..."):
                try:
                    client = OpenAI(base_url=base_url, api_key=api_key)

                    system_prompt = (
                        "You are an expert viral YouTube Shorts & TikTok content creator specializing in "
                        "'Reading Challenge' and 'Speed Reading Teleprompter' videos.\n"
                        "Your job is to generate a challenge formatted EXACTLY to be pasted into a vertical HTML teleprompter renderer.\n\n"
                        "Rules:\n"
                        "1. Language must be 100% natural, idiomatic English.\n"
                        "2. Format the body reading script so that each line contains only 3 to 6 words. "
                        "Short phrases are critical for vertical teleprompter readability as the text rolls up.\n"
                        "3. Group 3-4 short lines into a paragraph, separated by a blank line.\n"
                        "4. The title should be a high-ego hook challenge (e.g. 'Can you read this in 30 seconds?').\n"
                        "5. Output must be strictly valid JSON without any markdown wrapping (no ```json code blocks)."
                    )

                    user_prompt = f"""Generate a reading challenge script with the following details:
- Category: {category}
- Difficulty Level: {difficulty}
- Target Duration: {target_duration}
- Custom Instructions/Topic: {custom_topic if custom_topic else 'Pick the best viral concept for this category'}
- Subscribe CTA: {cta_option}

Return JSON with exactly these keys:
{{
  "title": "Short catchy challenge title for header (max 6 words)",
  "body_script": "The reading lines. Each line 3-6 words. Separate paragraphs with double newline (\\n\\n).",
  "closing": "Short closing text (e.g. 'Did you make it? Thank you for reading.')",
  "suggested_duration_seconds": 30,
  "suggested_theme": "dark or mountain or forest or sunset or sage",
  "shorts_caption": "Title + hashtags for upload (e.g., #readingchallenge #teleprompter #fyp)"
}}"""

                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=temperature
                    )

                    raw_resp = response.choices[0].message.content.strip()
                    # Bersihkan jika LLM masih membungkus dengan backticks
                    if raw_resp.startswith("```"):
                        raw_resp = raw_resp.split("\n", 1)[1]
                        if raw_resp.endswith("```"):
                            raw_resp = raw_resp.rsplit("```", 1)[0]
                    
                    data = json.loads(raw_resp.strip())
                    st.session_state["challenge_data"] = data

                except json.JSONDecodeError:
                    # Fallback jika model mengembalikan teks mentah
                    st.session_state["raw_output"] = response.choices[0].message.content
                except Exception as e:
                    st.error(f"Error memanggil API: {str(e)}")

    # Tampilkan hasil terpisah per kotak input HTML
    if "challenge_data" in st.session_state:
        d = st.session_state["challenge_data"]

        st.success("✨ Naskah siap! Tinggal copy-paste ke kotak masing-masing di aplikasi HTML:")

        st.markdown("**1. Judul Header** *(Salin ke `titleInput`)*")
        st.code(d.get("title", ""), language=None)

        st.markdown("**2. Isi Teks Bacaan** *(Salin ke `scriptInput`)*")
        st.code(d.get("body_script", ""), language=None)

        st.markdown("**3. Teks Penutup** *(Salin ke `closingInput`)*")
        st.code(d.get("closing", ""), language=None)

        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.info(f"⏱️ **Set Durasi Slider:** `{d.get('suggested_duration_seconds', 30)} detik`")
        with col_meta2:
            st.info(f"🎨 **Rekomendasi Tema:** `{d.get('suggested_theme', 'mountain')}`")

        with st.expander("📱 Caption & Hashtag untuk Upload ke Shorts/TikTok"):
            st.code(d.get("shorts_caption", ""), language=None)

    elif "raw_output" in st.session_state:
        st.markdown(st.session_state["raw_output"])
    else:
        st.info("Pilih kategori di sebelah kiri lalu klik tombol merah untuk menghasilkan naskah teleprompter.")