import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit.components.v1 as components


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit.components.v1 as components

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA DARK SPOTIFY
# ==========================================
st.set_page_config(page_title="Spotify Analytics Dashboard", page_icon="🎵", layout="wide")

# Palet warna Spotify
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_GREEN_LIGHT = "#1ED760"
BG_DARK = "#121212"
BG_CARD = "#181818"
BG_ELEVATED = "#282828"
TEXT_PRIMARY = "#FFFFFF"
TEXT_MUTED = "#B3B3B3"

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

        /* ===== GLOBAL DARK BACKGROUND ===== */
        .stApp {{
            background: radial-gradient(ellipse at top, #1a1a1a 0%, {BG_DARK} 50%, #000000 100%) !important;
            color: {TEXT_PRIMARY} !important;
        }}
        
        /* PERBAIKAN DI SINI: Menghapus selektor tag universal 'div' agar tidak memicu teks hantu undefined */
        html, body, .stMarkdown, p, span, label, .stMetric, .stSelectbox, .stRadio {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: {TEXT_PRIMARY};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_PRIMARY} !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }}
        h1 {{
            background: linear-gradient(135deg, #FFFFFF 0%, {SPOTIFY_GREEN_LIGHT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* ===== SIDEBAR DARK & LOCK PERMANEN ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #000000 0%, #0a0a0a 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }}
        [data-testid="stSidebar"] * {{
            color: {TEXT_PRIMARY} !important;
        }}
        [data-testid="stSidebar"] .stMarkdown p {{
            color: {TEXT_MUTED} !important;
        }}

        /* SEMBUNYIKAN TOMBOL COLLAPSE SECARA AMAN (Tanpa Merusak Komponen Lain) */
        [data-testid="stSidebarCollapseButton"],
        button[data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] button,
        button[aria-label="Close sidebar"],
        button[aria-label="Open sidebar"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0px !important;
            height: 0px !important;
            pointer-events: none !important;
        }}

        /* ===== TOMBOL ===== */
        .stButton>button {{
            border-radius: 500px !important;
            background: {SPOTIFY_GREEN} !important;
            color: #000000 !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            transition: all 0.2s ease !important;
            padding: 12px 32px !important;
            box-shadow: 0 4px 20px rgba(29, 185, 84, 0.3) !important;
        }}
        .stButton>button:hover {{
            background: {SPOTIFY_GREEN_LIGHT} !important;
            transform: scale(1.04) !important;
            box-shadow: 0 8px 30px rgba(29, 185, 84, 0.5) !important;
        }}

        /* ===== MENU RADIO SIDEBAR (Pill Style Spotify) ===== */
        div[role="radiogroup"] [data-testid="stRadioButtonCustomizedOption"] div:first-child,
        div[role="radiogroup"] label > div:first-child {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }}
        div[role="radiogroup"] label {{
            background: transparent !important;
            border: none !important;
            padding: 12px 16px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            margin-bottom: 4px !important;
            width: 100% !important;
            display: block !important;
        }}
        div[role="radiogroup"] label p {{
            color: {TEXT_MUTED} !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin: 0 !important;
        }}
        div[role="radiogroup"] label:hover {{
            background: rgba(255,255,255,0.07) !important;
        }}
        div[role="radiogroup"] label:hover p {{
            color: {TEXT_PRIMARY} !important;
        }}
        div[role="radiogroup"] [data-checked="true"] label {{
            background: linear-gradient(135deg, {SPOTIFY_GREEN} 0%, #169c46 100%) !important;
            box-shadow: 0 4px 20px rgba(29, 185, 84, 0.4) !important;
        }}
        div[role="radiogroup"] [data-checked="true"] label p {{
            color: #000000 !important;
            font-weight: 800 !important;
        }}

        /* ===== METRIC CARDS (Glassmorphism) ===== */
        [data-testid="stMetric"] {{
            background: linear-gradient(135deg, {BG_CARD} 0%, {BG_ELEVATED} 100%) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
            transition: all 0.3s ease !important;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-4px) !important;
            border-color: {SPOTIFY_GREEN} !important;
            box-shadow: 0 12px 40px rgba(29, 185, 84, 0.2) !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {TEXT_MUTED} !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            font-size: 12px !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 36px !important;
            font-weight: 800 !important;
            color: {SPOTIFY_GREEN} !important;
        }}

        /* ===== TABEL ===== */
        .stTable, .stDataFrame {{
            background: {BG_CARD} !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
        }}
        .stTable table {{
            background: {BG_CARD} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .stTable thead th {{
            background: linear-gradient(135deg, {SPOTIFY_GREEN} 0%, #169c46 100%) !important;
            color: #000000 !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            font-size: 12px !important;
            padding: 14px !important;
        }}
        .stTable tbody td {{
            background: {BG_CARD} !important;
            color: {TEXT_PRIMARY} !important;
            border-bottom: 1px solid rgba(255,255,255,0.05) !important;
            padding: 12px 14px !important;
        }}
        .stTable tbody tr:hover td {{
            background: {BG_ELEVATED} !important;
        }}

        /* ===== ALERT BOXES ===== */
        .stAlert {{
            background: {BG_CARD} !important;
            border-left: 4px solid {SPOTIFY_GREEN} !important;
            border-radius: 8px !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .stAlert * {{ color: {TEXT_PRIMARY} !important; }}

        /* ===== SELECTBOX / SLIDER ===== */
        .stSelectbox > div > div, .stMultiSelect > div > div {{
            background: {BG_ELEVATED} !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background: {SPOTIFY_GREEN} !important;
        }}

        /* ===== DIVIDER ===== */
        hr {{ border-color: rgba(255,255,255,0.1) !important; }}

        /* ===== TARGET ANTI UNDEFINED ===== */
        .element-container:has(iframe[title="plotly"]) + div:empty,
        div[data-testid="stVerticalBlock"] > div[class*="st-emotion-cache"]:empty {{
            display: none !important;
            height: 0px !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.hero-box{
    background:
        radial-gradient(circle at top left,
        rgba(29,185,84,.35),
        rgba(0,0,0,0) 60%),
        linear-gradient(
        135deg,
        #012b14 0%,
        #00150a 40%,
        #000000 100%);
    border-radius:32px;
    padding:70px;
    border:1px solid rgba(255,255,255,.05);
    margin-bottom:40px;
    position:relative;
    overflow:hidden;
}

.hero-badge{
    position:absolute;
    top:30px;
    right:30px;
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    padding:12px 20px;
    border-radius:999px;
    color:white;
    font-weight:600;
}

.hero-small{
    color:#47d764;
    letter-spacing:5px;
    font-size:14px;
    font-weight:700;
    text-transform:uppercase;
}

.hero-title{
    font-size:82px;
    line-height:0.95;
    font-weight:900;
    margin-top:25px;
    margin-bottom:10px;
    color:white;
}

.hero-title-green{
    background:linear-gradient(
        90deg,
        #4ade80,
        #166534);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-desc{
    font-size:24px;
    color:#b3b3b3;
    max-width:850px;
    margin-top:30px;
    line-height:1.7;
}

.hero-btn{
    display:inline-block;
    background:#57e368;
    color:black !important;
    padding:18px 36px;
    border-radius:999px;
    font-weight:700;
    text-decoration:none;
    margin-top:40px;
    margin-right:15px;
}

.hero-btn-secondary{
    display:inline-block;
    background:transparent;
    border:1px solid rgba(255,255,255,.1);
    color:white !important;
    padding:18px 36px;
    border-radius:999px;
    text-decoration:none;
    margin-top:40px;
}

.metric-card{
    background:linear-gradient(
        135deg,
        #101916 0%,
        #09100d 100%);
    border:1px solid rgba(255,255,255,.05);
    border-radius:24px;
    padding:32px;
}

.metric-title{
    color:#cfcfcf;
    font-size:14px;
    letter-spacing:2px;
    text-transform:uppercase;
}

.metric-value{
    color:white;
    font-size:58px;
    font-weight:800;
    margin-top:15px;
}

.metric-sub{
    color:#57e368;
    font-size:22px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)
# ==========================================
# 2. LOAD DATA
# ==========================================

def kalkulasi_manual_valence(dataframe, mode_pilihan):
    """
    Fungsi kustom untuk memfilter mode, menghitung total SUM valence,
    menghitung total lagu (COUNT), dan membagi keduanya untuk mencari rata-rata.
    """
    df_filter = dataframe[dataframe['mode'] == mode_pilihan]
    seri_valence = df_filter['valence_%'].dropna()
    
    total_sum = seri_valence.sum()
    total_count = seri_valence.count()
    
    if total_count > 0:
        rata_rata = total_sum / total_count
    else:
        rata_rata = 0.0
        
    return total_sum, total_count, rata_rata

def format_miliar_juta(angka):
    """Fungsi pembantu untuk memformat angka besar (Digunakan di Menu 3)"""
    if angka >= 1_000_000_000:
        return f"{angka / 1_000_000_000:.2f} Miliar"
    elif angka >= 1_000_000:
        return f"{angka / 1_000_000:.2f} Juta"
    return f"{angka:,.0f}"

def apply_custom_theme(fig):
    """Fungsi pembantu untuk tema grafik Plotly (Digunakan di Menu 3 & 4)"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#ffffff",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    
@st.cache_data
def load_data():
    df = pd.read_csv("spotify-2023.csv", delimiter=";", encoding='latin-1')
    if 'streams' in df.columns:
        df['streams'] = df['streams'].astype(str).str.replace(r'[^\d]', '', regex=True)
        df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    cols_numeric = [
        'released_year', 'released_month', 'released_day', 'artist_count',
        'in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts',
        'in_spotify_playlists', 'in_apple_playlists', 'in_deezer_playlists',
        'bpm', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%',
        'instrumentalness_%', 'liveness_%', 'speechiness_%'
    ]
    for col in cols_numeric:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['streams', 'track_name', 'artist(s)_name'])
    df = df[df['streams'] <= 4000000000]
    return df

df = load_data()


def format_miliar_juta(angka):
    if pd.isna(angka): return "0"
    if angka >= 1e9: return f"{angka / 1e9:.2f} Miliar"
    elif angka >= 1e6: return f"{angka / 1e6:.2f} Juta"
    return f"{angka:,.0f}"


# ===== TEMA PLOTLY DARK SPOTIFY =====
def apply_custom_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Plus Jakarta Sans",
        font_color=TEXT_PRIMARY,
        title_font_color=SPOTIFY_GREEN_LIGHT,
        title_font_size=18,
        title_font_family="Plus Jakarta Sans",
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
        legend=dict(bgcolor="rgba(24,24,24,0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
    )
    return fig


# ==========================================
# 3. SIDEBAR
# ==========================================
st.sidebar.markdown(f"<h2 style='color:{SPOTIFY_GREEN}; margin-bottom:0;'>🎵 Spotify Analitycs</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:{TEXT_MUTED}; font-size:13px; margin-top:4px;'>Haris Sandy Setiawan- 09020624033</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:{TEXT_MUTED}; font-size:13px; margin-top:4px;'>M. Resa Alfarizi - 09010624011</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:{TEXT_MUTED}; font-size:13px; margin-top:4px;'>Hafidz Arkaan Syauqi - 09020624032</p>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.markdown("""
    <style>
        /* 1. Mengubah font untuk teks di sidebar (Kode asli Anda) */
        [data-testid="stSidebar"] .st-emotion-cache-174383l, 
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] span {
            font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            transition: color 0.3s ease, background-color 0.3s ease;
        }

        /* 2. Efek untuk menu yang SEDANG AKTIF / DIPILIH */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] + div [aria-checked="true"] {
            background-color: rgba(30, 215, 96, 0.15) !important; /* Latar hijau transparan */
            border-left: 4px solid #1ED760 !important; /* Garis vertikal hijau di kiri */
            border-radius: 4px;
        }
        
        /* Mengubah warna teks pilihan yang aktif menjadi Hijau Spotify */
        [data-testid="stSidebar"] [aria-checked="true"] p {
            color: #1ED760 !important;
            font-weight: 600 !important;
        }

        /* 3. Efek HOVER saat kursor mendekati/menyentuh menu */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] + div [role="radiogroup"] div[data-testid="stMarkdownContainer"]:hover {
            background-color: rgba(30, 215, 96, 0.1) !important; /* Sorot hijau tipis */
            cursor: pointer;
            border-radius: 4px;
        }
        
        /* Teks berubah agak terang saat di-hover */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:hover p {
            color: #1ED760 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- DAFTAR MENU ---
list_menu = [
    "Welcome Screen",
    "Top 10 Lagu Terpopuler",
    "Platform Battleground",
    "Collaboration ROI Calculator",
    "Anatomi Sebuah Lagu Global Hit",
    "Pola Rilis Musik Musiman",
    "Distribusi Kecepatan Musik (BPM)"
]

# Inisialisasi session state untuk navigasi jika belum ada
if 'nav_menu' not in st.session_state:
    st.session_state.nav_menu = "Welcome Screen"

# Cari indeks menu saat ini agar posisi radio button sinkron secara dinamis
indeks_sekarang = list_menu.index(st.session_state.nav_menu) if st.session_state.nav_menu in list_menu else 0

menu_pilihan = st.sidebar.radio(
    "Navigasi:",
    list_menu,
    index=indeks_sekarang, # Menjaga posisi radio button sesuai state terbaru
    label_visibility="collapsed"
)

# Sinkronisasi balik jika user mengklik langsung di sidebar radio
st.session_state.nav_menu = menu_pilihan

st.sidebar.markdown("---")
st.sidebar.caption("⚡ Powered by Streamlit & Plotly")

# ==========================================
# 📊 4. LOGIKA HALAMAN UTAMA (100% LENGKAP TANPA POTONGAN)
# ==========================================

# --- MENU: WELCOME SCREEN ---
if menu_pilihan == "Welcome Screen":
    
    # 1. HERO BOX UTAMA
    st.markdown(f"""
        <div class="hero-box">
            <div class="hero-small">Music Intelligence Hub</div>
            <div class="hero-title" style="margin-top:15px; margin-bottom:0px;">
                Spotify Global Hits<br>
                <span class="hero-title-green">Analytics</span>
            </div>
            <div class="hero-desc">
                Membongkar rahasia di balik musik populer dunia — dari 
                mood, tempo, hingga kolaborasi yang melahirkan hit.
            </div>
            <div style="margin-bottom: -25px;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tombol Mulai Eksplorasi dengan style kustom Streamlit
    st.markdown("""
        <style>
            div.stButton > button:first-child {
                margin-top: -65px !important;
                margin-left: 70px !important;
                position: relative;
                z-index: 999;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # KETIKA TOMBOL DIKLIK:
    if st.button("Mulai Eksplorasi"):
        st.session_state.nav_menu = "Top 10 Lagu Terpopuler" # Harus sama persis dengan teks menu
        st.rerun() # Memaksa streamlit merender ulang dengan state menu yang baru
        
    st.markdown(" ") # Spacer jembatan antar komponen
    
    # Hitung nilai asli dari DataFrame agar dinamis
    total_lagu = len(df)
    total_artis = df['artist(s)_name'].str.split(', ').explode().dropna().unique()
    total_artis_count = len(total_artis) if len(total_artis) > 0 else df['artist(s)_name'].nunique()
    modus_bpm = int(df['bpm'].mode()[0]) if 'bpm' in df.columns and not df['bpm'].mode().empty else 123

    # --- Tambahan CSS: Efek Hover Glow yang Lebih Tebal & Menyala Pekat ---
    st.markdown("""
        <style>
            /* Efek transisi halus dan pergerakan kartu saat di-hover */
            .metric-card {
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
                position: relative;
            }
            
            /* Animasi naik sedikit lebih tinggi saat di-hover */
            .metric-card:hover {
                transform: translateY(-6px) !important;
                filter: brightness(1.15); /* Membuat seluruh isi kartu ikut memancarkan cahaya */
            }

            /* Efek Nyala Tebal Kartu 1 (Hijau Spotify) */
            .glow-green:hover {
                border-color: #1ED760 !important;
                box-shadow: 0 0 25px rgba(30, 215, 96, 0.45), 
                            0 0 50px rgba(30, 215, 96, 0.2) !important;
            }

            /* Efek Nyala Tebal Kartu 2 (Cyan/Sian) */
            .glow-cyan:hover {
                border-color: #00bcd4 !important;
                box-shadow: 0 0 25px rgba(0, 188, 212, 0.45), 
                            0 0 50px rgba(0, 188, 212, 0.2) !important;
            }

            /* Efek Nyala Tebal Kartu 3 (Oranye) */
            .glow-orange:hover {
                border-color: #ff9800 !important;
                box-shadow: 0 0 25px rgba(255, 152, 0, 0.45), 
                            0 0 50px rgba(255, 152, 0, 0.2) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # # 2. 3 KARTU METRIK UTAMA DENGAN EFEK HOVER NYALA TEBAL
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown(f"""
            <div class="metric-card glow-green">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="metric-title">Total Lagu</div>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1ED760" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"></circle><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"></path></svg>
                </div>
                <div class="metric-value">{total_lagu}</div>
                <div class="metric-sub" style="color: #47d764;">Lagu Hits</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_w2:
        st.markdown(f"""
            <div class="metric-card glow-cyan">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="metric-title">Total Musisi</div>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                </div>
                <div class="metric-value">{total_artis_count}</div>
                <div class="metric-sub" style="color: #00bcd4;">Artis</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_w3:
        st.markdown(f"""
            <div class="metric-card glow-orange">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="metric-title">Tempo Dominan</div>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff9800" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path></svg>
                </div>
                <div class="metric-value">{modus_bpm}</div>
                <div class="metric-sub" style="color: #ff9800;">BPM</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.success("📊 Dashboard ini menyajikan berbagai visualisasi interaktif untuk mengeksplorasi pola, tren, dan karakteristik data Spotify 2023. Gunakan menu navigasi di sebelah kiri untuk melakukan analisis pada setiap aspek data yang tersedia.") 
# --- MENU 1: TOP 10 LAGU TERPOPULER & GARIS WAKTU ---
elif menu_pilihan == "Top 10 Lagu Terpopuler":
    st.title("Popularity Metrics & Time Series Dispersion")
    
    st.sidebar.subheader("⚙️ Filter Parameter")
    daftar_tahun = sorted(df['released_year'].dropna().unique().astype(int).tolist(), reverse=True)
    daftar_tahun.insert(0, "Semua Tahun")
    tahun_terpilih = st.sidebar.selectbox("Pilih Tahun Rilis:", daftar_tahun)
    
    st.subheader("📅 Garis Waktu Tren Rilis Musik Hits")
    df_timeline = df.groupby('released_year').size().reset_index(name='Jumlah Lagu Rilis Tahun Tersebut')
    
    if tahun_terpilih == "Semua Tahun":
        df_timeline_plot = df_timeline[df_timeline['released_year'] >= 2000]
        judul_timeline = "Distribusi Umur Musik Hits Dunia (Sejak Era 2000)"
    else:
        df_timeline_plot = df_timeline[df_timeline['released_year'] == tahun_terpilih]
        judul_timeline = f"Jumlah Musik Hits yang Dirilis pada Tahun {tahun_terpilih}"
        
    if not df_timeline_plot.empty:
        fig_timeline_bar = px.bar(
            df_timeline_plot, x='released_year', y='Jumlah Lagu Rilis Tahun Tersebut',
            labels={'released_year': 'Tahun Rilis Lagu', 'Jumlah Lagu Rilis Tahun Tersebut': 'Jumlah Lagu Rilis'},
            title=judul_timeline,
            color='Jumlah Lagu Rilis Tahun Tersebut', color_continuous_scale='Greens'
        )
        apply_custom_theme(fig_timeline_bar)
        fig_timeline_bar.update_layout(coloraxis_showscale=False, height=400, xaxis=dict(type='category'))
        st.plotly_chart(fig_timeline_bar, use_container_width=True)
    
    st.subheader("🏆 Hall of Fame: 10 Lagu Terpopuler")
    if tahun_terpilih == "Semua Tahun":
        data_top10 = df.nlargest(10, 'streams')
        judul_grafik = "Top 10 Lagu Terpopuler"
    else:
        data_top10 = df[df['released_year'] == tahun_terpilih].nlargest(10, 'streams')
        judul_grafik = f"Top 10 Lagu Rilisan {tahun_terpilih}"
        
    if not data_top10.empty:
        data_top10_plot = data_top10.iloc[::-1]
        fig_bar = px.bar(
            data_top10_plot, x='streams', y='track_name',
            orientation='h', text='streams',
            hover_data=['artist(s)_name'],
            labels={'streams': 'Total Streams', 'track_name': 'Judul Lagu'},
            title=judul_grafik,
            color='streams', color_continuous_scale='YlGn'
        )
        fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        apply_custom_theme(fig_bar)
        fig_bar.update_layout(coloraxis_showscale=False, height=500)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("#### 📋 Tabel Detail Peringkat")
        tabel_tampil = data_top10[['track_name', 'artist(s)_name', 'streams']].copy()
        tabel_tampil['Total Putaran'] = tabel_tampil['streams'].apply(format_miliar_juta)
        tabel_tampil = tabel_tampil.drop(columns=['streams']).reset_index(drop=True)
        tabel_tampil.columns = ['Judul Lagu', 'Nama Artis', 'Total Putaran (Streams)']
        st.table(tabel_tampil)

        lagu_puncak = data_top10.iloc[0]['track_name']
        artis_puncak = data_top10.iloc[0]['artist(s)_name']
        streams_puncak = data_top10.iloc[0]['streams']
        
        st.markdown("### 💡 Kesimpulan Analisis Tren Pasar & Leaderboard:")
        st.info(
            f"Berdasarkan parameter kurasi filter **{tahun_terpilih}**, data menunjukkan dominasi absolut dipegang oleh lagu "
            f"**'{lagu_puncak}'** karya **{artis_puncak}** dengan akumulasi performa menembus **{format_miliar_juta(streams_puncak)} streams**.\n\n"
            f"**Analisis Tren Waktu (Time Series Analysis):** Analisis grafik ini menunjukkan terjadinya ledakan streaming, "
            f" di mana tangga lagu hits dunia saat ini didominasi oleh lagu-lagu baru yang rilis beberapa tahun belakangan."
            f" Hal ini menjadi bukti nyata bahwa jumlah pengguna internet dan aplikasi musik digital di seluruh dunia meningkat sangat pesat, sehingga memudahkan lagu-lagu baru untuk langsung populer dalam waktu singkat."
        )

# --- MENU 2: PLATFORM BATTLEGROUND ---
elif menu_pilihan == "Platform Battleground":
    st.title("⚔️ Platform Battleground & Cross-App Analytics")
    
    st.sidebar.subheader("⚙️ Filter Target")
    tipe_pencarian = st.sidebar.radio("Cari Berdasarkan:", ["Judul Lagu", "Nama Artis"])
    
    if tipe_pencarian == "Judul Lagu":
        list_lagu = sorted(df['track_name'].dropna().unique())
        pilihan_user = st.sidebar.selectbox("Pilih Judul Lagu:", list_lagu)
        data_filtered = df[df['track_name'] == pilihan_user]
    else:
        list_artis = df['artist(s)_name'].str.split(', ').explode().dropna().unique()
        list_artis = sorted(list_artis)
        pilihan_user = st.sidebar.selectbox("Pilih Nama Artis:", list_artis)
        data_filtered = df[df['artist(s)_name'].str.contains(pilihan_user, case=False, na=False)]

    if not data_filtered.empty:
        if tipe_pencarian == "Nama Artis":
            st.markdown(f"### 📋 Daftar Lagu Populer oleh **{pilihan_user}**")
            lagu_spesifik = st.selectbox("Pilih salah satu lagu untuk dilihat perbandingan tangga lagunya:", data_filtered['track_name'].unique())
            data_plot_final = data_filtered[data_filtered['track_name'] == lagu_spesifik].iloc[0]
            judul_grafik = f"Posisi Tangga Lagu: {lagu_spesifik} ({pilihan_user})"
        else:
            lagu_spesifik = pilihan_user  # Definisikan agar variabel tetap terbaca di bawah
            data_plot_final = data_filtered.iloc[0]
            judul_grafik = f"Posisi Tangga Lagu untuk '{pilihan_user}'"

        st.markdown(f"### 📊 {judul_grafik}")
        
        # Konversi super aman untuk menghindari galat objek kosong/None
        def dapatkan_nilai_numerik(kolom):
            nilai = data_plot_final.get(kolom, 0)
            if pd.isna(nilai) or nilai is None:
                return 0
            try:
                return int(float(str(nilai).replace(',', '').strip()))
            except:
                return 0

        val_spotify = dapatkan_nilai_numerik('in_spotify_charts')
        val_apple = dapatkan_nilai_numerik('in_apple_charts')
        val_deezer = dapatkan_nilai_numerik('in_deezer_charts')
        val_shazam = dapatkan_nilai_numerik('in_shazam_charts')
        
        # =====================================================================
        # LOGIKA PROSES GRAFIK LEADERBOARD (Makin Kecil Peringkat, Makin Tinggi Bar)
        # =====================================================================
        BATAS_ATAS_CHART = 100  # Menjadi acuan tinggi maksimal chart (Top 100)

        # Fungsi hitung tinggi batang
        def hitung_skor_grafik(peringkat):
            if peringkat == 0:
                return 0
            if peringkat > BATAS_ATAS_CHART:
                return 1  # Tetap muncul batang sangat pendek jika di luar top 100
            return (BATAS_ATAS_CHART + 1) - peringkat

        # Fungsi penulisan label teks di atas batang
        def buat_label_teks(peringkat):
            return "-" if peringkat == 0 else f"#{peringkat}"

        # Eksekusi logika untuk masing-masing platform
        df_chart_compare = pd.DataFrame({
            'Platform Aplikasi': ['Spotify Charts', 'Apple Music Charts', 'Deezer Charts', 'Shazam Charts'],
            'Tinggi Batang': [
                hitung_skor_grafik(val_spotify), 
                hitung_skor_grafik(val_apple), 
                hitung_skor_grafik(val_deezer), 
                hitung_skor_grafik(val_shazam)
            ],
            'Peringkat Asli': [
                buat_label_teks(val_spotify), 
                buat_label_teks(val_apple), 
                buat_label_teks(val_deezer), 
                buat_label_teks(val_shazam)
            ]
        })
        
        # Gambar grafik menggunakan kolom bayangan 'Tinggi Batang' dan teks 'Peringkat Asli'
        fig_battle = px.bar(
            df_chart_compare, 
            x='Platform Aplikasi', 
            y='Tinggi Batang',
            text='Peringkat Asli', 
            color='Platform Aplikasi',
            color_discrete_map={
                'Spotify Charts': '#1DB954', 
                'Apple Music Charts': '#FA243C', 
                'Deezer Charts': '#EF5466', 
                'Shazam Charts': '#0088FF'
            }
        )
        
        # Modifikasi layout dasar: Sembunyikan angka sumbu Y agar tidak membingungkan
        fig_battle.update_layout(
            showlegend=False, 
            height=400,
            yaxis=dict(
                title="Posisi Tangga Lagu",
                showticklabels=False,  # Sembunyikan angka skor buatan matematika
                showgrid=False         # Bersihkan garis horizontal belakang
            )
        )
        
        # Paksa posisi teks peringkat selalu berada tepat di luar/atas batang
        fig_battle.update_traces(textposition='outside')
        # =====================================================================
        
        try:
            fig_battle = apply_custom_theme(fig_battle)
        except:
            pass
            
        fig_battle_html = pio.to_html(fig_battle, full_html=False, include_plotlyjs='cdn')
        components.html(fig_battle_html, height=450, scrolling=False)

        # --- POTONGAN KODE SETELAH components.html(fig_battle_html, height=450, scrolling=False) ---

        st.markdown("---")
        st.markdown("### 📝 Kesimpulan Analisis Platform")

        # Buat dictionary untuk mempermudah pemetaan nilai valid (bukan 0)
        peta_posisi = {
            'Spotify': val_spotify,
            'Apple Music': val_apple,
            'Deezer': val_deezer,
            'Shazam': val_shazam
        }

        # Filter platform tempat lagu ini benar-benar masuk chart (posisi > 0)
        chart_aktif = {k: v for k, v in peta_posisi.items() if v > 0}

        if chart_aktif:
            # Cari posisi terbaik (angka terkecil, misal peringkat 1 lebih bagus dari 50)
            platform_terbaik = min(chart_aktif, key=chart_aktif.get)
            posisi_terbaik = chart_aktif[platform_terbaik]
            
            # Hitung total platform yang berhasil ditembus
            total_platform = len(chart_aktif)

            # Siapkan teks narasi dinamis
            nama_lagu = lagu_spesifik
            
            st.success(f"🎵 Lagu **{nama_lagu}** menunjukkan performa yang menarik di berbagai platform streaming!")
            
            # Tampilkan kesimpulan berbasis poin agar scannable
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="🏆 Performa Terbaik", value=f"#{posisi_terbaik}", delta=platform_terbaik, delta_color="off")
            with col2:
                st.metric(label="🌐 Dominasi Platform", value=f"{total_platform} / 4", delta="Platform Aktif", delta_color="off")

            # Detail Kesimpulan Kualitatif
            st.markdown(f"""
            > **Insight Utama:**
            > * Lagu ini paling sukses merajai **{platform_terbaik}** dengan berhasil menduduki peringkat **#{posisi_terbaik}**.
            > * Dari 4 platform utama yang dipantau, lagu ini berhasil menembus tangga lagu di **{total_platform} platform**. Hal ini menandakan distribusi pendengar yang {'sangat luas dan merata' if total_platform >= 3 else 'cukup tersegmentasi di platform tertentu'}.
            """)
            
        else:
            # Jika semua nilai val_* adalah 0
            st.info("ℹ️ **Informasi:** Lagu ini saat ini belum terdaftar atau sudah keluar dari top tangga lagu (posisi 0) di keempat platform utama tersebut.")

    else:
        st.warning("⚠️ Data tidak ditemukan untuk pencarian tersebut. Silakan coba filter lain.")

    # SUNTIKKAN STYLESHEET DARURAT PEMBUNUH MASSAL TEKS UNDEFINED
    st.markdown("""
        <style>
            /* Menyembunyikan paksa tulisan teks telanjang berbau undefined di dalam kontainer grafik */
            .clean-chart-container {
                position: relative;
            }
            .clean-chart-container:contains("undefined"), 
            .clean-chart-container div:empty {
                color: transparent !important;
                font-size: 0px !important;
                height: 0px !important;
            }
            /* Penghancur teks tak dikenal pasca visualisasi rendering */
            [data-testid="stVerticalBlock"] > div:has(iframe) + div:not([data-testid]) {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

# --- MENU 3: COLLABORATION ROI CALCULATOR ---
elif menu_pilihan == "Collaboration ROI Calculator":
    st.title("💰 Collaboration ROI & Personnel Optimization Hub")
    st.markdown("""
    Halaman ini menggabungkan **Analisis Finansial (ROI)** dan **Distribusi Statistik Capaian Pasar** untuk menjawab 
    formasi jumlah penyanyi mana yang paling ideal, konsisten, dan menguntungkan di industri musik digital dunia.
    """)
    
    # =========================================================================
    # REVISI: SEGMEN KONTROL TAHUN DIHAPUS, BERFOKUS PADA FILTER ARTIS & MUSIK
    # =========================================================================
    st.sidebar.subheader("⚙️ Segment Kontrol")
    
    nama_kolom_artis = 'artist(s)_name'
    nama_kolom_lagu = 'track_name'
    
    daftar_artis = sorted(df[nama_kolom_artis].dropna().unique())
    daftar_lagu = sorted(df[nama_kolom_lagu].dropna().unique())
    
    st.sidebar.markdown("🔍 **Filter Spesifik** *(Kosongkan untuk Semua Data)*")
    filter_artis = st.sidebar.multiselect("Pilih Artis:", options=daftar_artis)
    filter_lagu = st.sidebar.multiselect("Pilih Judul Lagu:", options=daftar_lagu)
    # =========================================================================
    
    st.markdown("##### 📱 Select Streaming Ecosystem Network:")
    platform_terpilih = st.segmented_control("Pilih Platform Analisis:", options=["Spotify", "Apple Music", "Deezer"], default="Spotify", label_visibility="collapsed")
    st.markdown(" ") 
    
    # Menggunakan salinan data awal secara utuh (karena filter tahun sudah ditiadakan)
    df_roi = df.copy()
    
    # =========================================================================
    # EKSEKUSI FILTER BERDASARKAN INPUT USER
    # =========================================================================
    if filter_artis:
        df_roi = df_roi[df_roi[nama_kolom_artis].isin(filter_artis)]
        
    if filter_lagu:
        df_roi = df_roi[df_roi[nama_kolom_lagu].isin(filter_lagu)]
    # =========================================================================
    
    def kelompokkan_format(jumlah):
        if jumlah == 1: return "Solo (1 Artis)"
        elif jumlah == 2: return "Duet (2 Artis)"
        else: return "Grup (3+ Artis)"
            
    df_roi['Format Tampil'] = df_roi['artist_count'].apply(kelompokkan_format)
    
    # Validasi jika data kosong setelah difilter
    if df_roi.empty:
        st.warning("⚠️ Data tidak ditemukan untuk kombinasi filter tersebut. Silakan atur ulang filter Anda pada sidebar.")
    else:
        KURS = 15500
        if platform_terpilih == "Spotify":
            tarif_usd = 0.00318  
            pangsa_pasar = 0.55
            warna_grafik = '#1DB954'
            info_tarif = f"🟢 **Spotify Pay-Per-Stream Rate**: ~$0.00318 (Nilai Tengah | Sistem bagi hasil paket gratisan)"
        elif platform_terpilih == "Apple Music":
            tarif_usd = 0.008  
            pangsa_pasar = 0.30
            warna_grafik = '#FA243C'
            info_tarif = f"🔴 **Apple Music Pay-Per-Stream Rate**: ~$0.008 (Nilai Tengah Premium | Berbasis langganan Premium)"
        else:
            tarif_usd = 0.0011 
            pangsa_pasar = 0.15
            warna_grafik = "#9D0CE6"
            info_tarif = f"🟣 **Deezer Pay-Per-Stream Rate**: ~$0.0011 (Rata-rata Laporan Artist-Centric)"

        df_roi['Pendapatan_Platform'] = df_roi['streams'] * pangsa_pasar * tarif_usd * KURS
        df_roi['Rev_Shazam_Bonus'] = df_roi['in_shazam_charts'].fillna(0) * 10000 * 0.0010 * KURS
        df_roi['Total_Pendapatan_Plus_Bonus'] = df_roi['Pendapatan_Platform'] + df_roi['Rev_Shazam_Bonus']
        
        st.info(f"{info_tarif}  \n**Estimasi Konversi Kurs Rupiah:** Rp {tarif_usd * KURS:.2f} per stream kotor (Asumsi $1 = Rp{KURS:,}).")
        
        st.subheader("📊 Visualisasi Komparasi Formasi Artis")
        
        df_plot_platform = df_roi.groupby('Format Tampil')['Pendapatan_Platform'].mean().reset_index()
        fig_single_revenue = px.bar(df_plot_platform, x='Format Tampil', y='Pendapatan_Platform', labels={'Pendapatan_Platform': 'Rata-Rata Pendapatan (Rp)'}, category_orders={"Format Tampil": ["Solo (1 Artis)", "Duet (2 Artis)", "Grup (3+ Artis)"]}, color_discrete_sequence=[warna_grafik], title="Rata-Rata Estimasi Pendapatan Finansial")
        apply_custom_theme(fig_single_revenue)
        st.plotly_chart(fig_single_revenue, use_container_width=True)

        summary_roi = df_roi.groupby('Format Tampil').agg(
            Volume_Streams=('streams', 'sum'),
            Total_Pendapatan=('Total_Pendapatan_Plus_Bonus', 'sum'),
            Rata_Rata_Mean=('Total_Pendapatan_Plus_Bonus', 'mean'),
            Jumlah_Lagu=('streams', 'count')
        ).reset_index()
        
        summary_roi['sort_key'] = summary_roi['Format Tampil'].map({"Solo (1 Artis)": 1, "Duet (2 Artis)": 2, "Grup (3+ Artis)": 3})
        summary_roi = summary_roi.sort_values('sort_key').drop(columns=['sort_key']).reset_index(drop=True)
        
        format_pemenang = summary_roi.loc[summary_roi['Rata_Rata_Mean'].idxmax()]['Format Tampil']
        keuntungan_maks = summary_roi['Rata_Rata_Mean'].max()
        
        summary_roi['Volume_Streams'] = summary_roi['Volume_Streams'].apply(format_miliar_juta)
        for col in ['Total_Pendapatan', 'Rata_Rata_Mean']:
            summary_roi[col] = summary_roi[col].apply(lambda x: f"Rp {format_miliar_juta(x)}")
            
        summary_roi.columns = ['Format Penyanyi', '🎵 Total Volume Putaran', f'💰 Total Pendapatan {platform_terpilih}', '📈 Rata-Rata Finansial (Mean)', '📋 Jumlah Lagu']
        st.markdown("#### 📋 Tabel Perbandingan ROI Finansial & Volume Distribusi Musik")
        st.table(summary_roi)

        st.markdown("### 💡 Strategic Synergy & Personnel Conclusion:")
        st.info(
            f"Berdasarkan pemrosesan data kumulatif dari seluruh linimasa dataset, "
            f"format penampilan yang terbukti mendatangkan performa finansial rata-rata tertinggi di platform **{platform_terpilih}** "
            f"adalah **{format_pemenang}** dengan estimasi rata-rata senilai **Rp {format_miliar_juta(keuntungan_maks)}** per proyek aransemen lagu. \n\n"
            f"Melalui pengelompokkan formasi ini, Anda dapat melihat secara jelas bagaimana kontribusi volume putaran (streams) "
            f"berbanding lurus dengan hasil pendapatan kotor yang diperoleh oleh para kreator musik di industri digital."
        )

        st.markdown("### REFERENSI:")
        st.info(
            f" Referensi pengambilan data harga per stream di setiap platform nya diambil di https://producerhive.com/music-marketing-tips/streaming-royalties-breakdown/#ftoc-heading-16"
        )

# --- MENU 5: ANATOMI SEBUAH LAGU GLOBAL HIT (VERSI FILTER BERTINGKAT) ---
elif menu_pilihan == "Anatomi Sebuah Lagu Global Hit":
    st.title("🧠 Audio Fingerprint Comparison (Perbandingan Akustik Lagu)")
    st.markdown("Pilih seorang musisi untuk langsung membandingkan sidik jari akustik (*acoustic fingerprint*) dari seluruh karya lagu mereka yang masuk ke dalam dataset global hits.")
    
    # --- 1. DATA PREPARATION ---
    audio_features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
    
    # Bersihkan data dari null values pada kolom nama lagu dan artis
    df_clean = df.dropna(subset=['track_name', 'artist(s)_name']).copy()
    
    # Pecah artis jika ada kolaborasi (split by ', ') agar nama artis individu tetap terdata
    list_all_artists = df_clean['artist(s)_name'].str.split(', ').explode().dropna().unique()
    list_all_artists = sorted(list_all_artists)
    
    st.markdown("### 🔍 Filter Target Komparasi")
    
    # 1. Filter Pertama: Pilih Nama Artis (Paling Atas) - Urutan asli tetap terjaga
    artis_terpilih = st.selectbox(
        "1. Pilih Nama Artis / Musisi:",
        options=list_all_artists,
        index=0 if len(list_all_artists) > 0 else None
    )
    
    # Saring data awal berdasarkan nama artis yang dipilih
    df_filtered_artist = df_clean[df_clean['artist(s)_name'].str.contains(artis_terpilih, case=False, na=False)].copy()
    
    # 2. Filter Kedua: Pilih Lagu
    list_lagu_artis = sorted(df_filtered_artist['track_name'].unique())
    
    # PERBAIKAN DI SINI: default diubah menjadi [] agar awal-awal tidak otomatis memilih semua lagu (kosong)
    lagu_terpilih = st.multiselect(
        f"2. Pilih Lagu dari {artis_terpilih}:",
        options=list_lagu_artis,
        default=[], 
        placeholder="Silakan klik atau ketik di sini untuk memilih lagu yang ingin dibandingkan..."
    )
    
    # Filter akhir berdasarkan lagu yang dipilih user di multi-select
    df_filtered_songs = df_filtered_artist[df_filtered_artist['track_name'].isin(lagu_terpilih)].copy()
    
    # LOGIKA PENGKONDISIAN: Jika user belum memilih lagu apa pun
    if df_filtered_songs.empty:
        st.info(f"💡 Kolom pilihan lagu di atas masih kosong. Silakan pilih satu atau beberapa lagu dari **{artis_terpilih}** untuk menampilkan grafik radar perbandingan.")
        
    else:
        # --- 2. TRANSFORMAST DATA (MELTING) UNTUK RADAR CHART ---
        df_melted = df_filtered_songs.melt(
            id_vars=['track_name', 'artist(s)_name'],
            value_vars=audio_features,
            var_name='Karakteristik Audio',
            value_name='Nilai (%)'
        )
        
        # Merapikan nama karakteristik audio agar indah dilihat
        df_melted['Karakteristik Audio'] = df_melted['Karakteristik Audio'].str.replace('_%', '').str.title()
        
        # --- 3. VISUALISASI UTAMA: MULTI-LINE RADAR CHART ---
        total_lagu = len(df_filtered_songs)
        
        fig_radar = px.line_polar(
            df_melted, 
            r='Nilai (%)', 
            theta='Karakteristik Audio', 
            color='track_name', 
            line_close=True, 
            title=f"Sidik Jari Akustik: Perbandingan {total_lagu} Lagu oleh {artis_terpilih}"
        )
        
        # Efek fill transparan jika lagunya tidak terlalu banyak (agar tidak merusak visual)
        if total_lagu <= 3:
            fig_radar.update_traces(fill='toself', opacity=0.3)
            
        fig_radar.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        
        try:
            apply_custom_theme(fig_radar)
        except:
            pass
            
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # --- 4. TABEL RINCIAN FITUR AUDIO (INDEX ANGKA KIRI DIHAPUS) ---
        st.markdown(f"### 📋 Rincian Nilai Akustik")
        
        df_tabel_komparasi = df_filtered_songs[['track_name', 'artist(s)_name'] + audio_features].copy()
        df_tabel_komparasi.columns = ['Judul Lagu', 'Artis/Kolaborator', 'Danceability', 'Valence', 'Energy', 'Acousticness', 'Instrumentalness', 'Liveness', 'Speechiness']
        
        # Tetap menyembunyikan angka index 0, 1, 2 agar rapi
        st.dataframe(df_tabel_komparasi, use_container_width=True, hide_index=True)
        
        # --- 5. PENAMBAHAN: HASIL ANALISIS OTOMATIS ---
        st.markdown("---")
        st.markdown(f"### 💡 Analisis Karakteristik Akustik ({artis_terpilih})")
        
        # Mengambil insight otomatis jika lagu yang dipilih lebih dari atau sama dengan 1
        with st.container():
            # 1. Lagu Paling Energik & Paling Kalem
            lagu_energi_max = df_tabel_komparasi.loc[df_tabel_komparasi['Energy'].idxmax()]['Judul Lagu']
            nilai_energi_max = df_tabel_komparasi['Energy'].max()
            
            # 2. Lagu Paling Ceria (Valence tinggi menunjukkan rasa bahagia/positif)
            lagu_valence_max = df_tabel_komparasi.loc[df_tabel_komparasi['Valence'].idxmax()]['Judul Lagu']
            nilai_valence_max = df_tabel_komparasi['Valence'].max()
            
            # 3. Lagu Paling Enak Dibuat Joget (Danceability)
            lagu_dance_max = df_tabel_komparasi.loc[df_tabel_komparasi['Danceability'].idxmax()]['Judul Lagu']
            nilai_dance_max = df_tabel_komparasi['Danceability'].max()
            
            # 4. Lagu Paling Akustik / Organik
            lagu_acoustic_max = df_tabel_komparasi.loc[df_tabel_komparasi['Acousticness'].idxmax()]['Judul Lagu']
            nilai_acoustic_max = df_tabel_komparasi['Acousticness'].max()

            # Tampilan Output Menggunakan Kolom Berjejer (Metrik Utama)
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🕺 **Paling Danceable:**\n\nLagu **\"{lagu_dance_max}\"** memiliki skor kecocokan berdansa tertinggi sebesar **{nilai_dance_max}%**.")
                st.success(f"🔥 **Energi Tertinggi:**\n\nLagu **\"{lagu_energi_max}\"** adalah lagu paling intens dan bertenaga dengan skor **{nilai_energi_max}%**.")
            
            with col2:
                st.warning(f"☀️ **Paling Ceria/Positif (Valence):**\n\nLagu **\"{lagu_valence_max}\"** membawa nuansa paling bahagia di dataset ini dengan skor **{nilai_valence_max}%**.")
                st.error(f"🎸 **Paling Akustik:**\n\nLagu **\"{lagu_acoustic_max}\"** mendominasi instrumen organik/akustik murni dengan skor **{nilai_acoustic_max}%**.")
            
# --- MENU 6: POLA RILIS MUSIK MUSIMAN ---
elif menu_pilihan == "Pola Rilis Musik Musiman":
    st.title("🍂 Seasonal Release Patterns & Calendar Heatmap")
    st.markdown("Analisis ini mendeteksi strategi penanggalan rilis atau perilaku serentak (*herd behavior*) musisi besar dunia.")
    
    df_season = df.groupby(['released_month', 'released_day']).size().reset_index(name='Jumlah Lagu')
    pivot_season = df_season.pivot(index='released_month', columns='released_day', values='Jumlah Lagu').fillna(0)
    nama_bulan = {1: '1. Januari', 2: '2. Februari', 3: '3. Maret', 4: '4. April', 5: '5. Mei', 6: '6. Juni', 7: '7. Juli', 8: '8. Agustus', 9: '9. September', 10: '10. Oktober', 11: '11. November', 12: '12. Desember'}
    pivot_season.index = pivot_season.index.map(nama_bulan)
    
    fig_heatmap_season = px.imshow(pivot_season, labels=dict(x="Tanggal Rilis", y="Bulan Rilis", color="total Lagu"), x=pivot_season.columns, y=pivot_season.index, color_continuous_scale='YlOrRd', title="Heatmap Kalender: Kepadatan Jadwal Rilis Musisi Hits Dunia")
    apply_custom_theme(fig_heatmap_season)
    st.plotly_chart(fig_heatmap_season, use_container_width=True)
    
    df_bulan_saja = df.groupby('released_month').size().reset_index(name='Total')
    id_bulan_terpadat = df_bulan_saja.loc[df_bulan_saja['Total'].idxmax()]['released_month']
    nama_bulan_terpadat = nama_bulan[id_bulan_terpadat].split('. ')[1]
    
    # 🛠️ PERBAIKAN: Hitung nilai modus dari kolom bpm agar variabel 'bpm_modus' terdefinisi dan tidak error
    if 'bpm' in df.columns and not df['bpm'].dropna().empty:
        bpm_modus = df['bpm'].mode()[0]
    else:
        bpm_modus = 120 # Nilai fallback/cadangan jika kolom bpm tidak ditemukan
    
    st.markdown("### 💡 Kesimpulan Analisis Pola Rilis Musiman:")
    st.info(
        f"Grafik Heat Kalender di atas mendeteksi adanya **anomali kepadatan rilis** pada waktu-waktu spesifik. "
        f"Data membuktikan bahwa bulan **{nama_bulan_terpadat}** merupakan periode paling padat di mana musisi global melepas lagu mereka "
        f"dengan akumulasi mencapai **{df_bulan_saja['Total'].max()} lagu hits**.\n\n"
        f"**Rekomendasi Strategis Distribusi:** Pola penumpukan warna merah di awal tahun (seperti Januari) atau pada tanggal 1 di setiap bulan "
        f"menunjukkan adanya strategi musisi mengejar akumulasi performa chart tahunan. Bagi musisi independen baru, disarankan untuk "
        f"**menghindari** rilis di tanggal-tanggal super padat tersebut agar tidak tenggelam oleh persaingan promosi dari label-label raksasa."
    )

    # Variabel bpm_modus sekarang sudah aman dipanggil di bawah ini tanpa memicu NameError lagi
    st.info(f"**💡 Kesimpulan Analisis Data:** Berdasarkan grafik data Spotify yang kita miliki dan didukung oleh temuan Dyer & McKune (2013), penonton global terbukti lebih memilih musik yang menjaga keseimbangan psikologis mereka. Puncak kurva yang berada di area **{bpm_modus:.0f} BPM** menunjukkan bahwa popularitas sebuah lagu hits sangat dipengaruhi oleh bagaimana ritme (BPM) tersebut beresonansi dengan kenyamanan biologis tubuh manusia.")
# --- MENU 7: DISTRIBUSI KECEPATAN MUSIK (BPM) ---
elif menu_pilihan == "Distribusi Kecepatan Musik (BPM)":
    st.title("🥁 Acoustic Velocity Distribution & Psychophysiological Rhythm")
    st.markdown("Mengukur letak puncak *sweet spot* ritme kecepatan tempo musik hits dunia berdasarkan respons kenyamanan biologis.")
    
    # Memastikan kolom penting dibersihkan dan diubah menjadi tipe numerik
    df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    
    # Membuat kolom nama lagu yang bersih untuk pencarian filter grafik
    nama_kolom_lagu = 'track_name'
    df[nama_kolom_lagu] = df[nama_kolom_lagu].astype(str).str.strip()
    
    df_bpm_hist = df.dropna(subset=['bpm', 'streams']).copy()
    
    # ===== REVISI PERHITUNGAN METRIK: TERTINGGI, TERENDAH, MODUS =====
    bpm_tertinggi = df_bpm_hist['bpm'].max()
    bpm_terendah = df_bpm_hist['bpm'].min()
    bpm_median = df_bpm_hist['bpm'].median()
    bpm_modus = df_bpm_hist['bpm'].mode()[0] if not df_bpm_hist['bpm'].mode().empty else bpm_median
    
    # Menampilkan metrik ke dalam kolom
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Tempo Tertinggi (Max)", f"{bpm_tertinggi:.0f} BPM")
    col_stat2.metric("Tempo Terendah (Min)", f"{bpm_terendah:.0f} BPM")
    col_stat3.metric("Titik Terbanyak (Modus)", f"{bpm_modus:.0f} BPM")
    st.markdown("---")
    
    # =========================================================================
    # KONTROL FILTER: UNTUK MENANDAI LAGU PADA GRAFIK GLOBAL
    # =========================================================================
    st.markdown("🔍 **Sorot Posisi BPM Lagu Spesifik pada Kurva**")
    daftar_lagu_grafik = sorted(df_bpm_hist[nama_kolom_lagu].unique())
    filter_lagu_grafik = st.multiselect(
        "Pilih atau Cari Judul Lagu untuk Ditandai pada Grafik:", 
        options=daftar_lagu_grafik,
        placeholder="Ketik nama lagu di sini... (Bisa pilih lebih dari satu)"
    )
    # =========================================================================
    
    # GRAFIK MUTLAK: Selalu menampilkan seluruh sebaran histogram dari awal sampai akhir
    fig_hist = px.histogram(
        df_bpm_hist, 
        x='bpm', 
        nbins=35, 
        labels={'bpm': 'Tempo Musik (BPM)'}, 
        title="Kurva Distribusi Kepadatan Tempo Musik Populer Global", 
        color_discrete_sequence=['#1DB954']
    )
    
    # Menamai data dasar histogram di legenda agar rapi
    fig_hist.data[0].name = "Distribusi Global"
    fig_hist.data[0].showlegend = True

    # MEMBERIKAN GARIS TEPI (BORDER) PADA SETIAP BATANG HISTOGRAM
    fig_hist.update_traces(
        marker_line_color='#121212', 
        marker_line_width=1.5
    )
    
    # =========================================================================
    # SOLUSI AGAR TIDAK NABRAK: MEMINDAHKAN LABEL KE LEGENDA INTERAKTIF
    # =========================================================================
    if filter_lagu_grafik:
        warna_penanda = ['#FF4B4B', '#00DF89', '#3182CE', '#D69E2E', '#9F7AEA', '#ED64A6']
        
        for idx, lagu in enumerate(filter_lagu_grafik):
            data_lagu = df_bpm_hist[df_bpm_hist[nama_kolom_lagu] == lagu]
            if not data_lagu.empty:
                bpm_lagu = data_lagu['bpm'].values[0]
                warna_aktif = warna_penanda[idx % len(warna_penanda)]
                
                # 1. Menambahkan garis vertikal murni
                fig_hist.add_vline(
                    x=bpm_lagu, 
                    line_dash="dash", 
                    line_color=warna_aktif,
                    line_width=2
                )
                
                # 2. Menambahkan trace dummy khusus untuk legenda
                import plotly.graph_objects as go
                fig_hist.add_trace(
                    go.Scatter(
                        x=[bpm_lagu],
                        y=[0],
                        mode='lines',
                        line=dict(color=warna_aktif, dash='dash', width=2),
                        name=f"📍 {lagu} ({bpm_lagu} BPM)",
                        hoverinfo='none'
                    )
                )
    # =========================================================================
                
    fig_hist.update_layout(
        yaxis_title="Jumlah Judul Lagu Hits", 
        height=450, 
        bargap=0.05,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    try:
        apply_custom_theme(fig_hist)
    except:
        pass

    # MEMAKSA GARIS KISI LAYOUT (GRIDLINES) TETAP MUNCUL JIKA TERTIMPA THEME
    fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255, 255, 255, 0.05)')
    fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255, 255, 255, 0.05)')
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("### 🧠 Analisis Teoretis: Mengapa Kurva Menumpuk di Area Tertentu?")
    col_teori1, col_teori2 = st.columns(2)
    with col_teori1:
        st.info("🟢 **Rentang 110–120 BPM: Zona 'Preferred Motor Tempo'**\n\nRitme di area ini selaras dengan kondisi homeostasis tubuh manusia saat beraktivitas aktif—seperti detak jantung saat berjalan santai atau berdansa ringan. Pendengar mendapatkan stimulasi pas tanpa kelelahan sensorik sehingga tingkat pemutaran ulang (*replayability*) menjadi sangat tinggi.")
    with col_teori2:
        st.warning("🟡 **Rentang di Atas 140 BPM: Zona 'Hyper-Arousal'**\n\nMusik di atas 140 BPM memicu stimulasi berlebih pada otak. Tempo cepat sangat bagus untuk memicu adrenalin instan (musik olahraga), namun jika didengarkan terus-menerus akan memicu stres sensorik dan kelelahan mental, menyebabkan grafiknya melandai turun.")

    # ===== TABEL LAGU BERDASARKAN KATEGORI BPM =====
    st.markdown("---")
    st.subheader("🎵 Telusuri Lagu Berdasarkan Kategori Kecepatan Tempo")

    bpm_kategori = st.segmented_control(
        "Pilih Kategori BPM:",
        options=[
            "BPM ≥ 140 (Hyper Zone)",
            "BPM 110–139 (Sweet Spot)",
            "BPM < 110 (Chill Zone)"
        ],
        default="BPM 110–139 (Sweet Spot)",
        label_visibility="collapsed"
    )

    # Inisialisasi variabel rekomendasi aktivitas
    rekomendasi_aktivitas = ""

    if bpm_kategori == "BPM ≥ 140 (Hyper Zone)":
        df_bpm_tabel = df_bpm_hist[df_bpm_hist['bpm'] >= 140].copy()
        desc_kategori = "**140 BPM ke atas** — Zona Hiperaktif"
        rekomendasi_aktivitas = (
            "🏃‍♂️ **Rekomendasi Aktivitas:** Sangat cocok untuk **Olahraga Kardio Intensitas Tinggi (HIIT), Running/Sprinting, Powerlifting,** atau "
            "saat membutuhkan *instant adrenaline rush*. Tempo tinggi ini memicu dorongan fisik yang kuat, namun kurang ideal untuk fokus belajar."
        )
    elif bpm_kategori == "BPM 110–139 (Sweet Spot)":
        df_bpm_tabel = df_bpm_hist[(df_bpm_hist['bpm'] >= 110) & (df_bpm_hist['bpm'] <= 139)].copy()
        desc_kategori = "**BPM 110–139** — Zona Sweet Spot (Preferred Motor Tempo)"
        rekomendasi_aktivitas = (
            "🚶‍♂️ **Rekomendasi Aktivitas:** Sangat ideal untuk **Berjalan Cepat (Brisk Walking), Bersepeda Santai, Housework (Beres-beres Rumah), "
            "atau Senam Ringan (Aerobik).** Ritme ini selaras dengan gerakan motorik alami tubuh manusia saat aktif bergerak tanpa membuat stres."
        )
    else:
        df_bpm_tabel = df_bpm_hist[df_bpm_hist['bpm'] < 110].copy()
        desc_kategori = "**di bawah 110 BPM** — Zona Chill & Melankolis"
        rekomendasi_aktivitas = (
            "🧠 **Rekomendasi Aktivitas:** Sangat pantes untuk **Fokus Belajar, Coding/Programming, Membaca, Yoga, Kontemplasi,** atau "
            "menjelang **Tidur/Relaksasi**. Tempo lambat membantu menurunkan frekuensi gelombang otak menuju kondisi rileks dan meningkatkan fokus kognitif."
        )

    # Menampilkan rekomendasi aktivitas tepat di bawah pilihan kategori
    st.markdown(f"> {rekomendasi_aktivitas}")
    st.write("") # Memberi sedikit space kosong

    # KONTROL FILTER JUMLAH BARIS TAMPILAN (TOP ROWS)
    col_tabel_header, col_limit = st.columns([2, 1])
    
    with col_tabel_header:
        st.markdown(f"##### 📋 Daftar Lagu ({desc_kategori})")
        
    with col_limit:
        limit_pilihan = st.selectbox(
            "Tampilkan Jumlah Data:",
            options=["Top 10", "Top 50", "Top 100", "All"],
            index=0,
            label_visibility="collapsed"
        )

    if not df_bpm_tabel.empty:
        # REVISI: Hanya mengambil kolom nama lagu, nama artis, dan bpm (menghapus streams)
        tabel_bpm = df_bpm_tabel[['track_name', 'artist(s)_name', 'bpm']].copy()
        
        # REVISI: Mengurutkan dari nilai BPM tertinggi ke terendah (ascending=False)
        tabel_bpm = tabel_bpm.sort_values('bpm', ascending=False).reset_index(drop=True)
        
        if limit_pilihan == "Top 10":
            tabel_bpm = tabel_bpm.head(10)
        elif limit_pilihan == "Top 50":
            tabel_bpm = tabel_bpm.head(50)
        elif limit_pilihan == "Top 100":
            tabel_bpm = tabel_bpm.head(100)
            
        st.caption(f"Menampilkan {len(tabel_bpm)} dari total {len(df_bpm_tabel)} lagu yang terdeteksi.")
            
        tabel_bpm.index += 1
        tabel_bpm.columns = ['Judul Lagu', 'Nama Artis', 'Tempo (BPM)']
        st.table(tabel_bpm)
    else:
        st.warning("⚠️ Tidak ada lagu yang ditemukan pada rentang BPM ini dalam dataset.")