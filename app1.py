import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import base64

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Prediksi Risiko Diabetes",
    page_icon="🩺",
    layout="wide"
)

# ======================================================
# LOAD MODEL
# ======================================================

model = joblib.load("rf_diabetes_model2.pkl")
encoders = joblib.load("label_encoders2.pkl")

# ======================================================
# SESSION STATE
# ======================================================

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

menu = st.session_state.menu

# ======================================================
# BACKGROUND GLOBAL
# ======================================================

def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("BC MEDIS.png")

page_bg = f"""
<style>

[data-testid="stAppViewContainer"] {{

    background-image:
    linear-gradient(
        rgba(235,242,250,0.45),
        rgba(235,242,250,0.45)
    ),

    url("data:image/png;base64,{img}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

.main {{
    background: transparent;
}}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ======================================================
# CUSTOM CSS
# ======================================================

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 20px !important;
}
.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1500px;
    margin: auto;
}

/* =====================================================
   HEADER
===================================================== */

.title-box {

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #3b82f6,
        #60a5fa
    );

    padding: 90px 60px;

    border-radius: 35px;

    color: white;

    margin-bottom: 55px;

    box-shadow:
        0 15px 40px rgba(37,99,235,0.35);

    text-align: center;
}
.title-box h1 {

    font-size: 64px !important;

    font-weight: 800 !important;

    margin-bottom: 25px !important;

    line-height: 1.2;

    text-align: center !important;

    width: 100%;
}

.title-box p {

    font-size: 26px !important;

    font-weight: 400;

    line-height: 2;

    max-width: 900px;

    margin: auto;

    text-align: center !important;

    color: rgba(255,255,255,0.95);
}
.title-box:hover {

    transform: translateY(-4px);

    box-shadow:
        0 20px 50px rgba(37,99,235,0.45);
}
/* =====================================================
   BUTTON
===================================================== */

.stButton > button {

    width: 100%;

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    border-radius: 22px;

    height: 72px;

    font-size: 22px;

    font-weight: 700;

    border: none;

    transition: 0.3s ease;

    letter-spacing: 0.4px;

    box-shadow:
        0px 8px 22px rgba(37,99,235,0.30);
}

.stButton > button:hover {

    transform:
        translateY(-3px)
        scale(1.02);

    background:
    linear-gradient(
        135deg,
        #1d4ed8,
        #1e40af
    );

    color: white;

    box-shadow:
        0px 15px 30px rgba(37,99,235,0.35);
}
/* =====================================
   LABEL FORM CLEAN
===================================== */

div[data-testid="stNumberInput"] label p,
div[data-testid="stSelectbox"] label p {

    font-size: 21px !important;

    font-weight: 600 !important;

    color: #111827 !important;

    line-height: 1.4 !important;

    letter-spacing: 0px !important;

    opacity: 1 !important;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {

    opacity: 1 !important;
}
/* =====================================================
   ALERT
===================================================== */

.stSuccess,
.stWarning,
.stInfo,
.stError {

    border-radius: 20px !important;

    padding: 20px !important;

    font-size: 20px !important;
}

/* =====================================================
   CARD
===================================================== */

.diabetes-card{
    background:white;
    border-radius:30px;
    padding:50px;
    box-shadow:0px 6px 20px rgba(0,0,0,0.08);
    margin-top:20px;
}

.section-title{
    font-size:42px;
    font-weight:800;
    color:#1e293b;
    margin-bottom:20px;
}

.section-text{
    font-size:24px;
    line-height:2;
    color:#334155;
}

.type-card{
    border-radius:24px;
    padding:30px;
    margin-top:25px;
    display:flex;
    align-items:center;
    gap:25px;
}

.type-number{
    width:85px;
    height:85px;
    border-radius:22px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:42px;
    font-weight:800;
    color:white;
    flex-shrink:0;
}

.type-title{
    font-size:34px;
    font-weight:700;
    margin-bottom:10px;
}

.type-desc{
    font-size:22px;
    color:#334155;
    line-height:1.8;
}

.info-box{
    background:#eef4ff;
    border-radius:24px;
    padding:35px;
    margin-top:40px;
}

.info-title{
    font-size:32px;
    font-weight:700;
    color:#2563eb;
    margin-bottom:15px;
}

.info-text{
    font-size:22px;
    line-height:1.9;
    color:#334155;
}
/* =====================================================
   RAPIIKAN KOLOM
===================================================== */

div[data-testid="column"] {

    padding-left: 10px;
    padding-right: 10px;
}
.main .block-container {

    background:
    rgba(255,255,255,0.72);

    backdrop-filter: blur(14px);

    border-radius: 35px;

    padding: 40px;

    box-shadow:
        0 10px 35px rgba(0,0,0,0.10);

    margin-top: 20px;

    margin-bottom: 30px;
}
.block-container {

    padding-top: 1rem !important;
}
/* Hilangkan background putih streamlit */
.main {
    background: transparent;
}

/* Container utama */
.block-container {
    padding-top: 2rem;  
    padding-bottom: 2rem;
}

/* =========================
   HERO SECTION
========================= */
.hero-box {

    background: linear-gradient(
        135deg,
        #2563eb 0%,
        #5fb5ff 100%
    );

    border-radius: 35px;

    padding:
    60px
    40px
    60px
    40px;

    text-align: center;

    box-shadow:
    0 10px 35px rgba(0,0,0,0.18);

    margin-bottom: 40px;
}

/* Judul */
.hero-title {

    color: white;

    font-size: 58px;

    font-weight: 800;

    margin-bottom: 18px;

    letter-spacing: -1px;
}

/* Subtitle */
.hero-subtitle {

    color: rgba(255,255,255,0.95);

    font-size: 24px;

    line-height: 1.8;
}


/* =========================
   CARD STATISTIK
========================= */
.stats-card {

    background: rgba(255,255,255,0.82);

    backdrop-filter: blur(10px);

    border-radius: 24px;

    padding: 30px;

    text-align: center;

    box-shadow:
    0 8px 24px rgba(0,0,0,0.10);

    border:
    1px solid rgba(255,255,255,0.25);

    transition: 0.3s ease;
}

/* Hover card */
.stats-card:hover {

    transform: translateY(-5px);

    box-shadow:
    0 12px 30px rgba(0,0,0,0.14);
}

/* Label statistik */
.stats-label {

    font-size: 22px;

    color: #374151;

    margin-bottom: 12px;

    font-weight: 500;
}

/* Angka statistik */
.stats-value {

    font-size: 64px;

    font-weight: 700;

    color: #111827;
}

/* =========================
   BUTTON
========================= */
.stButton > button {

    width: 100%;

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    border: none;

    border-radius: 20px;

    padding: 18px 25px;

    font-size: 24px;

    font-weight: 600;

    transition: all 0.3s ease;

    box-shadow:
    0 8px 20px rgba(37,99,235,0.35);
}

/* Hover tombol */
.stButton > button:hover {

    transform: translateY(-3px);

    background:
    linear-gradient(
        135deg,
        #1d4ed8,
        #2563eb
    );

    box-shadow:
    0 12px 28px rgba(37,99,235,0.45);
}

/* =========================
   SIDEBAR
========================= */
[data-testid="stSidebar"] {

    background:
    rgba(255,255,255,0.78);

    backdrop-filter: blur(12px);
}

/* =========================
   TEXT GLOBAL
========================= */
h1,h2,h3,h4,h5,h6,p,span,label {

    font-family: 'Segoe UI', sans-serif;
}
/* =========================
   METRIC BACKGROUND PREMIUM
========================= */

[data-testid="metric-container"] {

    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,0.92),
        rgba(240,248,255,0.82)
    ) !important;

    border-radius: 30px !important;

    padding: 40px 25px !important;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.12) !important;

    border:
        1px solid rgba(255,255,255,0.45) !important;

    backdrop-filter: blur(12px) !important;

    min-height: 230px !important;

    transition: 0.3s ease !important;
}

/* Hover */
[data-testid="metric-container"]:hover {

    transform: translateY(-6px);

    box-shadow:
        0 18px 35px rgba(37,99,235,0.18);
}

/* Label */
[data-testid="metric-container"] label {

    font-size: 28px !important;

    font-weight: 700 !important;

    color: #1e293b !important;

    justify-content: center !important;

    text-align: center !important;
}

/* Value */
[data-testid="metric-container"] [data-testid="stMetricValue"] {

    font-size: 80px !important;

    font-weight: 800 !important;

    color: #2563eb !important;

    justify-content: center !important;

    text-align: center !important;
}
/* =====================================
   CUSTOM METRIC CARD
===================================== */

.custom-metric-card {

    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,0.90),
        rgba(240,248,255,0.80)
    );

    border-radius: 24px;

    padding: 25px 15px;

    text-align: center;

    backdrop-filter: blur(10px);

    box-shadow:
        0 8px 22px rgba(0,0,0,0.10);

    border:
        1px solid rgba(255,255,255,0.45);

    transition: 0.3s ease;

    min-height: 140px;

    display: flex;

    justify-content: center;

    align-items: center;

    flex-direction: column;
}

/* Hover */
.custom-metric-card:hover {

    transform: translateY(-4px);

    box-shadow:
        0 12px 28px rgba(37,99,235,0.16);
}

/* Label */
.metric-label {

    font-size: 20px;

    font-weight: 700;

    color: #1e293b;

    margin-bottom: 10px;
}

/* Value */
.metric-value {

    font-size: 52px;

    font-weight: 800;

    color: #2563eb;

    line-height: 1;
}
/* =====================================
   WARNING BOX
===================================== */

.warning-box{

    background:#fef2f2;

    border-left:8px solid #dc2626;

    border-radius:18px;

    padding:24px;

    margin-bottom:25px;

    box-shadow:0 6px 18px rgba(220,38,38,0.12);

}

.warning-box h3{

    color:#b91c1c;

    font-size:30px;

    font-weight:800;

    margin-bottom:12px;

}

.warning-box p{

    color:#7f1d1d;

    font-size:20px;

    line-height:1.8;

    margin-bottom:10px;

}

.warning-box h3{
    display:flex;
    align-items:center;
    gap:12px;
}

/* =====================================
   HASIL PREDIKSI CARD
===================================== */

.prediction-card {

    background: white;

    border-radius: 24px;

    padding: 28px;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.12);

    margin-top: 20px;

    margin-bottom: 25px;
}

/* Judul */
.prediction-title {

    font-size: 34px;

    font-weight: 800;

    color: #1e3a8a;

    margin-bottom: 25px;
}

/* Status */
.prediction-status {

    font-size: 58px;

    font-weight: 900;

    margin-bottom: 10px;
}

/* Persentase */
.prediction-percent {

    font-size: 38px;

    font-weight: 800;

    margin-top: 10px;
}

/* Warna positif */
.risk-high {

    color: #dc2626;
}

/* Warna rendah */
.risk-low {

    color: #16a34a;
}

/* =====================================
   FAKTOR RISIKO
===================================== */

.factor-card {

    background: #eef5ff;

    border-radius: 20px;

    padding: 20px;

    margin-bottom: 15px;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.08);
}

.factor-title {

    font-size: 26px;

    font-weight: 800;

    color: #1e40af;

    margin-bottom: 15px;
}

.factor-text {

    font-size: 20px;

    line-height: 1.8;

    color: #334155;
}

/* =====================================
   SARAN KESEHATAN
===================================== */

.health-card {

    background: #f0fdf4;

    border-left: 8px solid #22c55e;

    border-radius: 22px;

    padding: 24px;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.08);

    margin-top: 15px;
}

.health-title {

    font-size: 28px;

    font-weight: 800;

    color: #166534;

    margin-bottom: 15px;
}

.health-text {

    font-size: 21px;

    line-height: 1.8;

    color: #14532d;
}
/* =====================================
   BESARKAN TEXT ALERT
===================================== */

.stWarning,
.stSuccess,
.stInfo {

    font-size: 28px !important;

    font-weight: 600 !important;

    line-height: 1.9 !important;

    padding: 28px !important;
}

/* Judul markdown di alert */
.stWarning p,
.stSuccess p,
.stInfo p {

    font-size: 28px !important;

    line-height: 1.9 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# FEATURE ORDER
# ======================================================

feature_order = [
    "Age",
    "Gender",
    "Polyuria",
    "Polydipsia",
    "sudden weight loss",
    "weakness",
    "Polyphagia",
    "Genital thrush",
    "visual blurring",
    "Itching",
    "Irritability",
    "delayed healing",
    "partial paresis",
    "muscle stiffness",
    "Alopecia",
    "Obesity"
]

# ======================================================
# FEATURE TRANSLATE
# ======================================================

feature_translate = {
    "Age": "Umur (Age)",
    "Gender": "Jenis Kelamin (Gender)",
    "Polyuria": "Sering Buang Air Kecil (Polyuria)",
    "Polydipsia": "Sering Haus (Polydipsia)",
    "sudden weight loss": "Penurunan Berat Badan Drastis (Sudden Weight Loss)",
    "weakness": "Tubuh Lemah / Mudah Lelah (Weakness)",
    "Polyphagia": "Nafsu Makan Berlebih (Polyphagia)",
    "Genital thrush": "Infeksi Jamur Kelamin (Genital Thrush)",
    "visual blurring": "Penglihatan Kabur (Visual Blurring)",
    "Itching": "Gatal-gatal (Itching)",
    "Irritability": "Mudah Marah / Sensitif (Irritability)",
    "delayed healing": "Luka Sulit Sembuh (Delayed Healing)",
    "partial paresis": "Kelemahan Otot Sebagian (Partial Paresis)",
    "muscle stiffness": "Kaku Otot (Muscle Stiffness)",
    "Alopecia": "Kerontokan Rambut (Alopecia)",
    "Obesity": "Obesitas (Obesity)"
}

# ======================================================
# BERANDA
# ======================================================

if menu == "Beranda":

    st.markdown("""
    <div class="title-box">
        <h1>🩺 Sistem Prediksi Risiko Diabetes</h1>
        <p>
            Aplikasi Machine Learning untuk Prediksi Risiko Diabetes
            Menggunakan Algoritma Random Forest
        </p>
    </div>
    """, unsafe_allow_html=True)

    left_space, col1, col2, col3, right_space = st.columns(
        [1, 1.2, 1.2, 1.2, 1]
    )

    with col1:
        st.markdown("""
        <div class="custom-metric-card">
            <div class="metric-label">📊 Dataset</div>
            <div class="metric-value">520</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-metric-card">
            <div class="metric-label">🧠 Jumlah Fitur</div>
            <div class="metric-value">16</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="custom-metric-card">
            <div class="metric-label">🎯 Akurasi Model</div>
            <div class="metric-value">97%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    center_col = st.columns([0.7, 4, 0.7])[1]

    with center_col:

        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            if st.button(
                "🔍 Mulai Prediksi",
                use_container_width=True
            ):
                st.session_state.menu = "Prediksi Diabetes"
                st.rerun()

        with btn2:
            if st.button(
                "📚 Tentang Diabetes",
                use_container_width=True
            ):
                st.session_state.menu = "Tentang Diabetes"
                st.rerun()

        with btn3:
            if st.button(
                "ℹ️ Informasi Model",
                use_container_width=True
            ):
                st.session_state.menu = "Informasi Model"
                st.rerun()
# ======================================================
# TENTANG DIABETES
# ======================================================

elif menu == "Tentang Diabetes":

    st.markdown("""
    <div class="title-box">
        <h1>📚 Tentang Diabetes</h1>
        <p>
            Informasi dan Edukasi Mengenai Penyakit Diabetes
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.menu = "Beranda"
        st.rerun()

    st.write("")

    import streamlit.components.v1 as components

    components.html("""

    <style>

    body{
        background:#f5f7fa;
        font-family:Inter,sans-serif;
    }

    .main-card{
        background:white;
        border-radius:30px;
        padding:50px;
        margin:20px;
        box-shadow:0px 8px 25px rgba(0,0,0,0.08);
    }

    .section-title{
        font-size:38px;
        font-weight:800;
        color:#0f172a;
        margin-bottom:20px;
    }

    .section-text{
        font-size:22px;
        line-height:2;
        color:#334155;
    }

    .type-grid{
        display:grid;
        grid-template-columns:1fr;
        gap:25px;
        margin-top:30px;
    }

    .type-card{
        padding:30px;
        border-radius:24px;
        display:flex;
        align-items:flex-start;
        gap:25px;
        transition:0.3s ease;
    }

    .type-card:hover{
        transform:translateY(-5px);
    }

    .type-number{
        min-width:85px;
        height:85px;
        border-radius:22px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-size:38px;
        font-weight:800;
    }

    .type-title{
        font-size:30px;
        font-weight:800;
        margin-bottom:10px;
    }

    .type-desc{
        font-size:21px;
        line-height:1.8;
        color:#334155;
    }

    .info-box{
        margin-top:45px;
        background:linear-gradient(135deg,#2563eb,#3b82f6);
        padding:35px;
        border-radius:25px;
        color:white;
    }

    .info-title{
        font-size:30px;
        font-weight:800;
        margin-bottom:15px;
    }

    .info-text{
        font-size:21px;
        line-height:1.9;
    }

    hr{
        border:none;
        height:2px;
        background:#e2e8f0;
        margin-top:45px;
        margin-bottom:45px;
    }

    </style>

    <div class="main-card">

        <div class="section-title">
            🩺 Apa Itu Diabetes?
        </div>

        <div class="section-text">
            Diabetes adalah penyakit kronis yang menyebabkan kadar gula darah
            dalam tubuh menjadi terlalu tinggi. Penyakit ini terjadi ketika tubuh
            tidak dapat memproduksi insulin dengan baik atau tidak mampu menggunakan
            insulin secara efektif.
        </div>

        <hr>

        <div class="section-title">
            📌 Jenis-Jenis Diabetes
        </div>

        <div class="type-grid">

            <!-- CARD 1 -->
            <div class="type-card"
                 style="background:#eff6ff; border-left:8px solid #2563eb;">

                <div class="type-number"
                     style="background:#2563eb;">
                     1
                </div>

                <div>

                    <div class="type-title"
                         style="color:#2563eb;">
                         Diabetes Tipe 1
                    </div>

                    <div class="type-desc">
                        Sistem imun menyerang sel penghasil insulin sehingga tubuh
                        tidak dapat memproduksi insulin dengan normal.
                    </div>

                </div>

            </div>

            <!-- CARD 2 -->
            <div class="type-card"
                 style="background:#f0fdf4; border-left:8px solid #16a34a;">

                <div class="type-number"
                     style="background:#16a34a;">
                     2
                </div>

                <div>

                    <div class="type-title"
                         style="color:#16a34a;">
                         Diabetes Tipe 2
                    </div>

                    <div class="type-desc">
                        Tubuh tidak mampu menggunakan insulin secara efektif sehingga
                        kadar gula darah meningkat.
                    </div>

                </div>

            </div>

            <!-- CARD 3 -->
            <div class="type-card"
                 style="background:#fff7ed; border-left:8px solid #ea580c;">

                <div class="type-number"
                     style="background:#ea580c;">
                     3
                </div>

                <div>

                    <div class="type-title"
                         style="color:#ea580c;">
                         Diabetes Gestasional
                    </div>

                    <div class="type-desc">
                        Diabetes yang terjadi selama masa kehamilan dan perlu
                        pengawasan medis secara rutin.
                    </div>

                </div>

            </div>

        </div>

        <div class="info-box">

            <div class="info-title">
                💡 Penting Untuk Diketahui
            </div>

            <div class="info-text">
                Diabetes dapat dikontrol dengan pola hidup sehat,
                olahraga teratur, menjaga pola makan,
                dan melakukan pemeriksaan kesehatan secara rutin.
            </div>

        </div>

    </div>

    """, height=1000, scrolling=True)
# ======================================================
# INFORMASI MODEL
# ======================================================

elif menu == "Informasi Model":

    st.markdown("""
    <div class="title-box">
        <h1>ℹ️ Informasi Model</h1>
        <p>
            Informasi Mengenai Model Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.menu = "Beranda"
        st.rerun()

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
        ### 🤖 Algoritma
        Random Forest Classifier
        """)

        st.info("""
        ### 📊 Dataset
        Early Stage Diabetes Risk Prediction
        """)

    with col2:

        st.info("""
        ### 🧠 Jumlah Fitur
        16 Fitur
        """)

        st.info("""
        ### 🎯 Akurasi
        97%
        """)

# ======================================================
# PREDIKSI DIABETES
# ======================================================

elif menu == "Prediksi Diabetes":

    st.markdown("""
    <div class="title-box">
        <h1>🔍 Prediksi Risiko Diabetes</h1>
        <p>
            Masukkan data pasien untuk melakukan prediksi
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.menu = "Beranda"
        st.rerun()

    st.markdown("""
    <div class="warning-box">

    <h3>⚠️ PERINGATAN</h3>

    <p>
    Hasil prediksi yang ditampilkan oleh sistem ini hanya digunakan sebagai
    alat skrining awal berdasarkan gejala klinis dan bukan merupakan
    diagnosis medis.
    Untuk memperoleh diagnosis yang akurat serta penanganan yang tepat,
    pengguna disarankan berkonsultasi dengan dokter atau tenaga kesehatan
    profesional.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ==================================================
    # LEFT
    # ==================================================

    with col1:
        
        age = st.number_input(
            "Umur (Age)",
            min_value=1,
            max_value=120,
            value=30
        )
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Masukkan umur Anda saat ini dalam satuan tahun.
        </div>
        """, unsafe_allow_html=True)
        gender_ui = st.selectbox(
            "Jenis Kelamin (Gender)",
            ["Laki-laki", "Perempuan"]
        )
        gender = "Male" if gender_ui == "Laki-laki" else "Female"
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Pilih jenis kelamin sesuai dengan identitas biologis Anda.
        </div>
        """, unsafe_allow_html=True)
        
        def convert_yes_no(value):
            return "Yes" if value == "Iya" else "No"
        
        polyuria = st.selectbox(
            "Sering Buang Air Kecil (Polyuria)",
            ["Iya", "Tidak"]
        )
        polyuria = convert_yes_no(polyuria)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Buang air kecil lebih sering dari biasanya, terutama pada malam hari, meskipun tidak sedang banyak minum.
        </div>
        """, unsafe_allow_html=True)

        polydipsia = st.selectbox(
            "Sering Haus (Polydipsia)",
            ["Iya", "Tidak"]
        )
        polydipsia = convert_yes_no(polydipsia)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Merasa haus berlebihan dan ingin minum terus-menerus meskipun sudah cukup minum.
        </div>
        """, unsafe_allow_html=True)
    
        weight_loss = st.selectbox(
            "Penurunan Berat Badan Drastis (Sudden Weight Loss)",
            ["Iya", "Tidak"]
        )
        weight_loss = convert_yes_no(weight_loss)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Mengalami penurunan berat badan yang cukup signifikan tanpa melakukan diet atau olahraga khusus.
        </div>
        """, unsafe_allow_html=True)

        weakness = st.selectbox(
            "Tubuh Lemah / Mudah Lelah (Weakness)",
            ["Iya", "Tidak"]
        )
        weakness = convert_yes_no(weakness)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Sering merasa lemas, kurang bertenaga, atau mudah lelah saat melakukan aktivitas sehari-hari.
        </div>
        """, unsafe_allow_html=True)

        polyphagia = st.selectbox(
            "Nafsu Makan Berlebih (Polyphagia)",
            ["Iya", "Tidak"]
        )
        polyphagia = convert_yes_no(polyphagia)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Nafsu makan meningkat atau merasa lapar lebih sering dibandingkan biasanya.
        </div>
        """, unsafe_allow_html=True)
       
        genital_thrush = st.selectbox(
            "Infeksi Jamur Kelamin (Genital Thrush)",
            ["Iya", "Tidak"]
        )
        genital_thrush = convert_yes_no(genital_thrush)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Mengalami infeksi jamur pada area kelamin yang ditandai dengan gatal, kemerahan, atau rasa tidak nyaman.
        </div>
        """, unsafe_allow_html=True)

    # ==================================================
    # RIGHT
    # ==================================================

    with col2:
         
        visual_blurring = st.selectbox(
            "Penglihatan Kabur (Visual Blurring)",
            ["Iya", "Tidak"]
        )
        visual_blurring = convert_yes_no(visual_blurring)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Penglihatan menjadi kabur atau tidak sejelas biasanya saat melihat objek.
        </div>
        """, unsafe_allow_html=True)  
    
        itching = st.selectbox(
            "Gatal-gatal (Itching)",
            ["Iya", "Tidak"]
        )
        itching = convert_yes_no(itching)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Mengalami rasa gatal pada kulit yang sering muncul tanpa penyebab yang jelas.
        </div>
        """, unsafe_allow_html=True)
        
        irritability = st.selectbox(
            "Mudah Marah / Sensitif (Irritability)",
            ["Iya", "Tidak"]
        )
        irritability = convert_yes_no(irritability)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Lebih mudah marah, sensitif, atau merasa emosional dibandingkan biasanya.
        </div>
        """, unsafe_allow_html=True)
        
        delayed_healing = st.selectbox(
            "Luka Sulit Sembuh (Delayed Healing)",
            ["Iya", "Tidak"]
        )
        delayed_healing = convert_yes_no(delayed_healing)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Luka kecil atau goresan membutuhkan waktu lebih lama untuk sembuh dibandingkan biasanya.
        </div>
        """, unsafe_allow_html=True)
        
        partial_paresis = st.selectbox(
            "Kelemahan Otot Sebagian (Partial Paresis)",
            ["Iya", "Tidak"]
        )
        partial_paresis = convert_yes_no(partial_paresis)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Mengalami kelemahan pada sebagian anggota tubuh sehingga gerakan terasa tidak sekuat biasanya.
        </div>
        """, unsafe_allow_html=True)
        
        muscle_stiffness = st.selectbox(
            "Kaku Otot (Muscle Stiffness)",
            ["Iya", "Tidak"]
        )
        muscle_stiffness = convert_yes_no(muscle_stiffness)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Otot terasa kaku atau sulit digerakkan, terutama setelah beristirahat atau bangun tidur.
        </div>
        """, unsafe_allow_html=True)
        
        alopecia = st.selectbox(
            "Kerontokan Rambut (Alopecia)",
            ["Iya", "Tidak"]
        )
        alopecia = convert_yes_no(alopecia)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Mengalami kerontokan rambut yang lebih banyak dari biasanya hingga menyebabkan penipisan rambut.
        </div>
        """, unsafe_allow_html=True)
        
        obesity = st.selectbox(
            "Obesitas (Obesity)",
            ["Iya", "Tidak"]
        )
        obesity = convert_yes_no(obesity)
        st.markdown("""
        <div style="
        font-size:15px;
        font-weight:600;
        color:#334155;
        margin-top:-10px;
        margin-bottom:8px;
        line-height:1.5;
        ">
        ℹ️ Memiliki berat badan berlebih yang dapat meningkatkan risiko berbagai penyakit, termasuk diabetes.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    # ==================================================
    # BUTTON
    # ==================================================

    if st.button("🔍 Prediksi Risiko Diabetes"):

        input_dict = {
            "Age": age,
            "Gender": gender,
            "Polyuria": polyuria,
            "Polydipsia": polydipsia,
            "sudden weight loss": weight_loss,
            "weakness": weakness,
            "Polyphagia": polyphagia,
            "Genital thrush": genital_thrush,
            "visual blurring": visual_blurring,
            "Itching": itching,
            "Irritability": irritability,
            "delayed healing": delayed_healing,
            "partial paresis": partial_paresis,
            "muscle stiffness": muscle_stiffness,
            "Alopecia": alopecia,
            "Obesity": obesity
        }

        input_df = pd.DataFrame([input_dict])

        input_df = input_df[feature_order]

        # ==================================================
        # ENCODING
        # ==================================================

        for col in input_df.columns:
            if col in encoders:
                input_df[col] = encoders[col].transform(
                    input_df[col]
                )

        # ==================================================
        # PREDICTION
        # ==================================================

        prediction = model.predict(input_df)[0]

        probabilities = model.predict_proba(input_df)[0]

        predicted_label = encoders['class'].inverse_transform(
            [prediction]
        )[0]

        class_labels = encoders['class'].classes_

        positive_index = list(class_labels).index("Positive")

        positive_probability = probabilities[positive_index]

        st.markdown("---")

        st.subheader("📊 Hasil Prediksi")

        if predicted_label == "Positive":

            st.markdown(f"""
            <div style="
            background:white;
            padding:25px;
            border-radius:20px;
            box-shadow:0 5px 20px rgba(0,0,0,0.10);
            border-left:8px solid #ef4444;
            margin-bottom:20px;
            ">

            <h3 style="
            color:#ef4444;
            font-size:34px;
            font-weight:800;
            margin-bottom:15px;
            ">
            ⚠️ Pasien Memiliki Risiko Diabetes
            </h3>

            <p style="
            font-size:28px;
            font-weight:700;
            color:#111827;
            ">
            Tingkat Risiko: {positive_probability * 100:.2f}%
            </p>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div style="
            background:white;
            padding:25px;
            border-radius:20px;
            box-shadow:0 5px 20px rgba(0,0,0,0.10);
            border-left:8px solid #22c55e;
            margin-bottom:20px;
            ">

            <h3 style="color:#16a34a;">
            ✅ Risiko Diabetes Rendah
            </h3>

            <p style="
            font-size:20px;
            font-weight:600;
            color:#111827;
            ">
            Tingkat Risiko: {positive_probability * 100:.2f}%
            </p>

            </div>
            """, unsafe_allow_html=True)

        # ==================================================
        # GAUGE
        # ==================================================

        st.subheader("📌 Persentase Risiko Diabetes")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=positive_probability * 100,
            title={'text': "Risiko Diabetes (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgreen"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ]
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=18)
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={'displayModeBar': False}
)

        # ==================================================
        # FEATURE IMPORTANCE
        # ==================================================


        importance_df = pd.DataFrame({
            "Fitur": [
                feature_translate[f]
                for f in feature_order
            ],
            "Importance": model.feature_importances_
        })

        importance_df = importance_df.sort_values(
            by="Importance",
            ascending=True
        )

        # ==================================================
        # TOP FEATURE
        # ==================================================

        st.subheader("🧠 Faktor Risiko Utama")

        top_feature = importance_df.sort_values(
            by="Importance",
            ascending=False
        ).head(3)

        for i, row in top_feature.iterrows():

            st.markdown(f"""
            <div style="
                background:#eef5ff;
                padding:22px;
                border-radius:18px;
                margin-bottom:15px;
                box-shadow:0 4px 15px rgba(0,0,0,0.08);
                border-left:7px solid #2563eb;
            ">

            <div style="
                font-size:30px;
                font-weight:700;
                color:#1e3a8a;
                margin-bottom:8px;
            ">
                🧠 {row['Fitur']}
            </div>

            <div style="
                font-size:24px;
                color:#334155;
            ">
                Tingkat Pengaruh:
                <b>{row['Importance']:.3f}</b>
            </div>

            </div>
            """, unsafe_allow_html=True)

        # ==================================================
        # RECOMMENDATION
        # ==================================================

        st.subheader("💡 Saran Kesehatan")

        if positive_probability >= 0.7:

            st.markdown("""
            <div style="
            background:#fef2f2;
            padding:24px;
            border-radius:20px;
            border-left:8px solid #ef4444;
            box-shadow:0 5px 15px rgba(0,0,0,0.08);
            margin-top:15px;
            ">

            <div style="
            font-size:34px;
            font-weight:700;
            color:#b91c1c;
            margin-bottom:10px;
            ">
            ⚠️ Saran Kesehatan
            </div>

            <div style="
            font-size:24px;
            color:#374151;
            line-height:1.8;
            ">
            Risiko diabetes cukup tinggi.
            Disarankan segera melakukan pemeriksaan medis
            dan menjaga pola hidup sehat.
            </div>

            </div>
            """, unsafe_allow_html=True)

        elif positive_probability >= 0.4:

            st.markdown("""
            <div style="
            background:#fffbeb;
            padding:24px;
            border-radius:20px;
            border-left:8px solid #f59e0b;
            box-shadow:0 5px 15px rgba(0,0,0,0.08);
            margin-top:15px;
            ">

            <div style="
            font-size:34px;
            font-weight:700;
            color:#92400e;
            margin-bottom:10px;
            ">
            ⚠️ Saran Kesehatan
            </div>

            <div style="
            font-size:18px;
            color:#374151;
            line-height:1.8;
            ">
            Risiko diabetes sedang.
            Mulailah menjaga pola makan dan rutin berolahraga.
            </div>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div style="
            background:#f0fdf4;
            padding:24px;
            border-radius:20px;
            border-left:8px solid #22c55e;
            box-shadow:0 5px 15px rgba(0,0,0,0.08);
            margin-top:15px;
            ">

            <div style="
            font-size:34px;
            font-weight:700;
            color:#166534;
            margin-bottom:10px;
            ">
            ✅ Saran Kesehatan
            </div>

            <div style="
            font-size:24px;
            font-weight:500;
            color:#374151;
            line-height:1.9;
            ">
            Risiko diabetes rendah.
            Tetap pertahankan pola hidup sehat,
            konsumsi makanan bergizi seimbang,
            dan lakukan aktivitas fisik secara rutin.
            </div>

            </div>
            """, unsafe_allow_html=True)
        # ==================================================
        # GENERATE PDF
        # ==================================================

        st.subheader("📄 Download Hasil Prediksi PDF")

        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 16)
                self.cell(0, 10, 'HASIL PREDIKSI RISIKO DIABETES', ln=True, align='C')
                self.ln(10)

        pdf = PDF()
        pdf.add_page()

        # =========================
        # HASIL PREDIKSI
        # =========================

        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 10, "Hasil Prediksi", ln=True)

        pdf.set_font("Arial", '', 12)

        pdf.cell(
            0,
            10,
            f"Status Prediksi : {predicted_label}",
            ln=True
        )

        pdf.cell(
            0,
            10,
            f"Tingkat Risiko : {positive_probability * 100:.2f}%",
            ln=True
        )

        pdf.ln(5)

        # =========================
        # DATA INPUT PASIEN
        # =========================

        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 10, "Data Pasien", ln=True)

        pdf.set_font("Arial", '', 11)

        for key, value in input_dict.items():

            nama_fitur = feature_translate.get(key, key)

            pdf.multi_cell(
                0,
                8,
                f"{nama_fitur} : {value}"
            )

        pdf.ln(5)

        # =========================
        # FAKTOR RISIKO
        # =========================

        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 10, "Faktor Risiko Utama", ln=True)

        pdf.set_font("Arial", '', 11)

        for i, row in top_feature.iterrows():

            pdf.multi_cell(
                0,
                8,
                f"- {row['Fitur']} ({row['Importance']:.3f})"
            )

        pdf.ln(5)

        # =========================
        # SARAN
        # =========================

        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 10, "Saran Kesehatan", ln=True)

        pdf.set_font("Arial", '', 11)

        if positive_probability >= 0.7:

            saran = (
                "Risiko diabetes cukup tinggi. "
                "Disarankan segera melakukan pemeriksaan medis "
                "dan menjaga pola hidup sehat."
            )

        elif positive_probability >= 0.4:

            saran = (
                "Risiko diabetes sedang. "
                "Mulailah menjaga pola makan dan rutin berolahraga."
            )

        else:

            saran = (
                "Risiko diabetes rendah. "
                "Tetap pertahankan pola hidup sehat."
            )

        pdf.multi_cell(0, 8, saran)

        # =========================
        # SAVE PDF
        # =========================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            pdf.output(tmp_file.name)

            with open(tmp_file.name, "rb") as file:

                st.download_button(
                    label="⬇️ Download PDF",
                    data=file,
                    file_name="hasil_prediksi_diabetes.pdf",
                    mime="application/pdf"
                )
