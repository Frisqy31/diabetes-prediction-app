import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 20px !important;
}

.stApp {
    background-color: #f5f7fa;
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
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    padding: 65px 40px;
    border-radius: 28px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.18);

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.title-box h1 {
    font-size: 52px !important;
    font-weight: 800 !important;
    margin-bottom: 18px !important;
    text-align: center !important;
}

.title-box p {
    font-size: 24px !important;
    font-weight: 400;
    text-align: center !important;
    line-height: 1.8;
    max-width: 900px;
}

/* =====================================================
   BUTTON
===================================================== */

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 22px;
    height: 72px;
    font-size: 24px;
    font-weight: 600;
    border: none;
    transition: 0.3s ease;
    box-shadow:
        0px 5px 16px rgba(37,99,235,0.3);
}

.stButton > button:hover {
    transform: scale(1.02);

    background: linear-gradient(
        135deg,
        #1d4ed8,
        #1e40af
    );

    color: white;
}

/* =====================================================
   METRIC
===================================================== */

[data-testid="metric-container"] {

    background: white;

    border-radius: 30px;

    padding: 45px 25px;

    box-shadow:
        0px 5px 20px rgba(0,0,0,0.08);

    border: none;

    min-height: 240px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    transition: 0.3s ease;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    box-shadow:
        0px 10px 30px rgba(0,0,0,0.12);
}

[data-testid="metric-container"] label {

    width: 100% !important;

    display: flex !important;

    justify-content: center !important;

    align-items: center !important;

    text-align: center !important;

    font-size: 28px !important;

    font-weight: 600 !important;

    color: #0f172a !important;

    margin-bottom: 25px !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {

    width: 100% !important;

    display: flex !important;

    justify-content: center !important;

    align-items: center !important;

    text-align: center !important;

    font-size: 78px !important;

    font-weight: 700 !important;

    color: #2563eb !important;

    line-height: 1 !important;
}

[data-testid="stMetricDelta"] {
    display: none;
}

/* =====================================================
   FORM
===================================================== */

.stSelectbox label,
.stNumberInput label {

    font-size: 24px !important;

    font-weight: 700 !important;

    color: #111827 !important;

    line-height: 1.8 !important;
}

.stSelectbox div[data-baseweb="select"] {

    min-height: 65px !important;

    border-radius: 18px !important;
}

.stSelectbox div[data-baseweb="select"] span {

    font-size: 24px !important;

    font-weight: 600 !important;

    color: #111827 !important;
}

.stNumberInput input {

    height: 65px !important;

    font-size: 24px !important;

    font-weight: 500 !important;

    border-radius: 18px !important;
}

.stSelectbox,
.stNumberInput {

    margin-bottom: 15px;
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
        st.metric(label="📊 Dataset", value="520")

    with col2:
        st.metric(label="🧠 Jumlah Fitur", value="16")

    with col3:
        st.metric(label="🎯 Akurasi Model", value="97%")

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

    st.warning("""
    Hasil prediksi ini bukan diagnosis medis final.
    Silakan konsultasikan dengan tenaga kesehatan profesional.
    """)

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

        gender = st.selectbox(
            "Jenis Kelamin (Gender)",
            ["Male", "Female"]
        )

        polyuria = st.selectbox(
            "Sering Buang Air Kecil (Polyuria)",
            ["Yes", "No"]
        )

        polydipsia = st.selectbox(
            "Sering Haus (Polydipsia)",
            ["Yes", "No"]
        )

        weight_loss = st.selectbox(
            "Penurunan Berat Badan Drastis (Sudden Weight Loss)",
            ["Yes", "No"]
        )

        weakness = st.selectbox(
            "Tubuh Lemah / Mudah Lelah (Weakness)",
            ["Yes", "No"]
        )

        polyphagia = st.selectbox(
            "Nafsu Makan Berlebih (Polyphagia)",
            ["Yes", "No"]
        )

        genital_thrush = st.selectbox(
            "Infeksi Jamur Kelamin (Genital Thrush)",
            ["Yes", "No"]
        )

    # ==================================================
    # RIGHT
    # ==================================================

    with col2:

        visual_blurring = st.selectbox(
            "Penglihatan Kabur (Visual Blurring)",
            ["Yes", "No"]
        )

        itching = st.selectbox(
            "Gatal-gatal (Itching)",
            ["Yes", "No"]
        )

        irritability = st.selectbox(
            "Mudah Marah / Sensitif (Irritability)",
            ["Yes", "No"]
        )

        delayed_healing = st.selectbox(
            "Luka Sulit Sembuh (Delayed Healing)",
            ["Yes", "No"]
        )

        partial_paresis = st.selectbox(
            "Kelemahan Otot Sebagian (Partial Paresis)",
            ["Yes", "No"]
        )

        muscle_stiffness = st.selectbox(
            "Kaku Otot (Muscle Stiffness)",
            ["Yes", "No"]
        )

        alopecia = st.selectbox(
            "Kerontokan Rambut (Alopecia)",
            ["Yes", "No"]
        )

        obesity = st.selectbox(
            "Obesitas (Obesity)",
            ["Yes", "No"]
        )

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

            st.error(
                f"""
                ⚠️ Pasien memiliki risiko diabetes

                Tingkat Risiko:
                {positive_probability * 100:.2f}%
                """
            )

        else:

            st.success(
                f"""
                ✅ Risiko diabetes rendah

                Tingkat Risiko:
                {positive_probability * 100:.2f}%
                """
            )

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

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={'displayModeBar': False}
)

        # ==================================================
        # FEATURE IMPORTANCE
        # ==================================================

        st.subheader("📈 Grafik Tingkat Pengaruh Fitur")

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

        st.dataframe(
            importance_df,
            use_container_width=True
        )

        # ==================================================
        # CHART
        # ==================================================

        fig2, ax = plt.subplots(figsize=(12, 8))

        bars = ax.barh(
            importance_df["Fitur"],
            importance_df["Importance"]
        )

        for bar in bars:

            width = bar.get_width()

            ax.text(
                width + 0.003,
                bar.get_y() + bar.get_height()/2,
                f"{width:.3f}",
                va='center'
            )

        ax.set_title(
            "Grafik Tingkat Pengaruh Fitur",
            fontsize=16,
            fontweight='bold'
        )

        ax.grid(
            axis='x',
            linestyle='--',
            alpha=0.5
        )

        plt.tight_layout()

        st.pyplot(fig2)

        # ==================================================
        # TOP FEATURE
        # ==================================================

        st.subheader("🧠 Faktor Risiko Utama")

        top_feature = importance_df.sort_values(
            by="Importance",
            ascending=False
        ).head(3)

        for i, row in top_feature.iterrows():

            st.info(
                f"✅ {row['Fitur']} "
                f"({row['Importance']:.3f})"
            )

        # ==================================================
        # RECOMMENDATION
        # ==================================================

        st.subheader("💡 Saran Kesehatan")

        if positive_probability >= 0.7:

            st.warning("""
            Risiko diabetes cukup tinggi.
            Disarankan segera melakukan pemeriksaan medis
            dan menjaga pola hidup sehat.
            """)

        elif positive_probability >= 0.4:

            st.info("""
            Risiko diabetes sedang.
            Mulailah menjaga pola makan dan rutin berolahraga.
            """)

        else:

            st.success("""
            Risiko diabetes rendah.
            Tetap pertahankan pola hidup sehat.
            """)