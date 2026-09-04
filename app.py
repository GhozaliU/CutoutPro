"""
CutOut Pro - Background Remover App
=====================================
Aplikasi web untuk menghapus latar belakang gambar secara otomatis
menggunakan AI (pustaka rembg), dibangun dengan Streamlit.
Tema visual mengikuti template "CutOut Pro" (cream & gold).

Cara menjalankan:
    streamlit run app.py

Author: Senior Full-Stack Engineer & AI Integration Specialist
"""

import io
import base64

import streamlit as st
from PIL import Image, ImageDraw
from rembg import remove

# ----------------------------------------------------------------------------
# Konfigurasi Halaman
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="CutOut Pro - Hapus Latar Belakang",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Design Tokens (mengikuti referensi: cream background + gold accent)
# ----------------------------------------------------------------------------
CREAM_BG = "#FBF5EA"
CARD_BG = "#FFFFFF"
BORDER = "#E7DFCF"
GOLD = "#E3A857"
GOLD_DARK = "#CC9440"
INK = "#2A2420"
MUTED = "#7A7168"

# ----------------------------------------------------------------------------
# Styling Kustom (CSS)
# ----------------------------------------------------------------------------
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {CREAM_BG};
        background-image:
            linear-gradient(90deg, rgba(0,0,0,0.025) 1px, transparent 1px),
            linear-gradient(rgba(0,0,0,0.025) 1px, transparent 1px);
        background-size: 64px 64px;
    }}

    .block-container {{
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* ---------- Header / Navbar ---------- */
    .navbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.1rem;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 2.4rem;
        flex-wrap: wrap;
        gap: 1rem;
    }}
    .navbar-logo {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        color: {INK};
    }}
    .navbar-logo .icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: {GOLD};
        color: white;
        font-size: 1.1rem;
    }}
    .navbar-links {{
        display: flex;
        gap: 1.8rem;
        font-size: 0.95rem;
        color: {INK};
    }}
    .navbar-links span {{
        cursor: default;
        opacity: 0.85;
    }}
    .navbar-cta {{
        background: {GOLD};
        color: white;
        padding: 0.55rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        white-space: nowrap;
    }}

    /* ---------- Hero ---------- */
    .hero {{
        text-align: center;
        margin-bottom: 2.2rem;
    }}
    .hero h1 {{
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.7rem;
        line-height: 1.15;
        color: {INK};
        margin-bottom: 0.9rem;
    }}
    .hero p {{
        color: {MUTED};
        font-size: 1.05rem;
        max-width: 640px;
        margin: 0 auto;
        line-height: 1.55;
    }}

    /* ---------- Showcase panels (Asli / Upload / Hasil) ---------- */
    .panel {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 0.6rem;
        height: 340px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }}
    .panel img {{
        max-height: 100%;
        max-width: 100%;
        border-radius: 12px;
        object-fit: contain;
    }}
    .panel-placeholder {{
        color: {MUTED};
        text-align: center;
        font-size: 0.9rem;
        padding: 1rem;
    }}
    .panel-label {{
        text-align: center;
        margin-top: 0.7rem;
        font-weight: 600;
        color: {INK};
        font-size: 0.95rem;
    }}

    /* ---------- File uploader restyle ---------- */
    [data-testid="stFileUploaderDropzone"] {{
        background: {CARD_BG} !important;
        border: 2px dashed {GOLD} !important;
        border-radius: 16px !important;
    }}
    [data-testid="stFileUploaderDropzoneInstructions"] svg {{
        display: none;
    }}
    [data-testid="stFileUploader"] section > button {{
        background-color: {GOLD} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    [data-testid="stFileUploader"] section > button:hover {{
        background-color: {GOLD_DARK} !important;
    }}
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small {{
        color: {MUTED} !important;
    }}

    /* ---------- Buttons ---------- */
    div.stButton > button {{
        border-radius: 10px !important;
        border: 1px solid {BORDER} !important;
        background: {CARD_BG} !important;
        color: {INK} !important;
        font-weight: 600 !important;
        padding: 0.5rem 0 !important;
    }}
    div.stButton > button:hover {{
        border-color: {GOLD} !important;
        color: {GOLD_DARK} !important;
    }}
    div.stDownloadButton > button {{
        background-color: {GOLD} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.65rem 0 !important;
    }}
    div.stDownloadButton > button:hover {{
        background-color: {GOLD_DARK} !important;
    }}

    /* ---------- Feature section ---------- */
    .features-title {{
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.9rem;
        color: {INK};
        margin: 3rem 0 1.6rem 0;
    }}
    .feature-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 1.5rem 1.4rem;
        height: 100%;
    }}
    .feature-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: #FCEFD9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-bottom: 0.9rem;
    }}
    .feature-card h4 {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: {INK};
        margin-bottom: 0.4rem;
    }}
    .feature-card p {{
        color: {MUTED};
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }}

    .footer-note {{
        text-align: center;
        color: {MUTED};
        font-size: 0.85rem;
        margin-top: 2.5rem;
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Fungsi Bantuan (Helper Functions)
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def remove_background(image_bytes: bytes) -> bytes:
    """Menghapus latar belakang dari gambar menggunakan pustaka rembg."""
    return remove(image_bytes, model_name="u2net")


def load_image(file_like) -> Image.Image:
    """Membuka file menjadi objek PIL Image (RGB) untuk ditampilkan."""
    image = Image.open(file_like)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    return image


def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Mengonversi objek PIL Image menjadi bytes."""
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


@st.cache_data(show_spinner=False)
def make_demo_image(kind: str) -> bytes:
    """
    Membuat gambar contoh sintetis (mobil / produk) secara lokal dengan PIL,
    dipakai untuk tombol "Coba Contoh" tanpa memerlukan aset eksternal.
    """
    img = Image.new("RGB", (600, 450), "#CFEAF5")
    draw = ImageDraw.Draw(img)

    if kind == "mobil":
        draw.rectangle([0, 320, 600, 450], fill="#B8B2A6")
        draw.rectangle([0, 300, 600, 320], fill="#8F8A7E")
        draw.rounded_rectangle([90, 210, 470, 300], radius=20, fill="#D33F3F")
        draw.rounded_rectangle([150, 150, 400, 215], radius=25, fill="#B93333")
        draw.rounded_rectangle([170, 165, 390, 210], radius=12, fill="#CFEAF5")
        draw.ellipse([120, 275, 200, 355], fill="#1E1E1E")
        draw.ellipse([145, 300, 175, 330], fill="#8A8A8A")
        draw.ellipse([370, 275, 450, 355], fill="#1E1E1E")
        draw.ellipse([395, 300, 425, 330], fill="#8A8A8A")
    else:  # "produk"
        draw.rectangle([0, 300, 600, 450], fill="#EDE6D6")
        draw.rounded_rectangle([250, 90, 350, 130], radius=10, fill="#3E6E5E")
        draw.rounded_rectangle([220, 130, 380, 340], radius=24, fill="#4A8570")
        draw.rounded_rectangle([245, 170, 355, 260], radius=10, fill="#F4EFE3")

    return pil_to_bytes(img, fmt="PNG")


def render_panel(image, placeholder_text: str, label: str, container):
    """Merender satu panel kotak (Asli / Hasil) dengan gaya kartu sesuai referensi."""
    with container:
        if image is not None:
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            st.markdown(
                f'<div class="panel"><img src="data:image/png;base64,{b64}" /></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="panel"><div class="panel-placeholder">{placeholder_text}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<div class="panel-label">{label}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# State awal
# ----------------------------------------------------------------------------
if "active_bytes" not in st.session_state:
    st.session_state.active_bytes = None
    st.session_state.active_name = None

# ----------------------------------------------------------------------------
# Header / Navbar
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-logo"><span class="icon">✂️</span> CutOut Pro</div>
        <div class="navbar-links">
            <span>Features</span><span>Pricing</span><span>How it Works</span><span>Blog</span>
        </div>
        <div class="navbar-cta">Login/Sign Up</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Hapus Latar Belakang<br>Secara Instan &amp; Otomatis</h1>
        <p>Hapus latar belakang dari foto produk, mobil, dan orang dengan mudah hanya
        dalam hitungan detik. Presisi tinggi, gratis 100% untuk pratinjau.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Showcase: Asli | Upload | Hasil
# ----------------------------------------------------------------------------
col_left, col_mid, col_right = st.columns([1, 1.05, 1], gap="medium")

with col_mid:
    st.markdown(
        '<div class="panel" style="height:auto; padding:1.6rem 1rem; flex-direction:column;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="text-align:center; font-size:2rem; margin-bottom:0.4rem;">🖼️➕</div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Unggah Gambar Anda",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="visible",
        help="Seret & lepas gambar di sini, atau klik untuk mengunggah (JPG, PNG, WebP, maks 15MB)",
    )
    st.markdown(
        f'<div style="text-align:center; color:{MUTED}; font-size:0.82rem; margin-top:0.3rem;">'
        f"Seret &amp; lepas gambar di sini atau klik untuk mengunggah<br>(JPG, PNG, WebP, maks 15MB)</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Tentukan sumber gambar aktif: file yang diunggah > contoh yang dipilih
if uploaded_file is not None:
    st.session_state.active_bytes = uploaded_file.getvalue()
    st.session_state.active_name = uploaded_file.name

original_image = None
result_image = None

if st.session_state.active_bytes is not None:
    try:
        original_image = load_image(io.BytesIO(st.session_state.active_bytes))
    except Exception as e:
        st.error(f"Gagal membuka gambar. Detail error: {e}")
        st.session_state.active_bytes = None

    if original_image is not None:
        with st.spinner("Sedang memproses gambar dengan AI... ⏳"):
            try:
                result_bytes = remove_background(st.session_state.active_bytes)
                result_image = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")

render_panel(original_image, "Belum ada gambar yang diunggah", "Asli", col_left)
render_panel(result_image, "Hasil akan muncul di sini", "Tanpa Latar Belakang", col_right)

# ----------------------------------------------------------------------------
# Tombol Contoh & Unduh
# ----------------------------------------------------------------------------
ex1, ex2, ex3 = st.columns([1, 1, 1.3], gap="small")
with ex1:
    if st.button("Coba Contoh Mobil", use_container_width=True):
        st.session_state.active_bytes = make_demo_image("mobil")
        st.session_state.active_name = "contoh_mobil.png"
        st.rerun()
with ex2:
    if st.button("Coba Contoh Produk", use_container_width=True):
        st.session_state.active_bytes = make_demo_image("produk")
        st.session_state.active_name = "contoh_produk.png"
        st.rerun()
with ex3:
    if result_image is not None:
        final_png_bytes = pil_to_bytes(result_image, fmt="PNG")
        base_name = (st.session_state.active_name or "hasil").rsplit(".", 1)[0]
        st.download_button(
            "⬇️ Unduh Hasil (PNG)",
            data=final_png_bytes,
            file_name=f"{base_name}_no_bg.png",
            mime="image/png",
            use_container_width=True,
        )
    else:
        st.button("⬇️ Unduh Hasil (PNG)", use_container_width=True, disabled=True)

# ----------------------------------------------------------------------------
# Fitur Unggulan
# ----------------------------------------------------------------------------
st.markdown('<div class="features-title">Fitur Unggulan</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="medium")
features = [
    ("⏱️", "Otomatis & Cepat", "Proses otomatis dan cepat, hasil didapat hanya dalam hitungan detik tanpa perlu keahlian desain."),
    ("🎭", "Presisi Tinggi", "Model AI mendeteksi tepi objek dengan presisi tinggi, termasuk detail rambut dan bagian yang rumit."),
    ("🏷️", "Bebas Biaya untuk Pratinjau", "Coba dan lihat hasilnya secara gratis 100% sebelum memutuskan untuk mengunduh."),
]
for col, (icon, title, desc) in zip([f1, f2, f3], features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="footer-note">Dibangun dengan ❤️ menggunakan Streamlit &amp; rembg</div>',
    unsafe_allow_html=True,
)
