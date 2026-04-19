import streamlit as st
import folium
from streamlit_folium import st_folium
from pathlib import Path
import base64
import io
try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

st.set_page_config(
    page_title="Peccioli x New Orleans 2026",
    page_icon="🎷",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

def find_image(possible_names):
    for name in possible_names:
        p = BASE_DIR / name
        if p.exists():
            return str(p)
    return None

@st.cache_data(show_spinner=False)
def img_to_base64(path):
    if path and Path(path).exists():
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            return base64.b64encode(f.read()).decode(), mime
    return None, None

@st.cache_data(show_spinner=False)
def img_to_base64_small(path, max_width=600):
    """Compressed version for mobile scroll — much smaller file size."""
    if not path or not Path(path).exists():
        return None, None
    if HAS_PIL:
        try:
            img = PILImage.open(path)
            img = img.convert("RGB")
            ratio = min(max_width / img.width, 1.0)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, PILImage.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=72, optimize=True)
            return base64.b64encode(buf.getvalue()).decode(), "image/jpeg"
        except Exception:
            pass
    return img_to_base64(path)

# ----------------------------
# Immagini — lazy loading per sezione
# ----------------------------
# Solo logo e header caricate sempre
logo_path      = find_image(["logo_comune.png", "logo_comune.jpg"])
nola_logo_path = find_image(["New_Orleans_Logo.png", "New_Orleans_Logo.jpg"])
ponte_path     = find_image(["piazza_nola_ponte.png", "piazza_nola_ponte.jpg", "Schermata_2026-04-18_alle_11_58_52.png"])

logo_b64, logo_mime           = img_to_base64(logo_path)
nola_logo_b64, nola_logo_mime = img_to_base64(nola_logo_path)
ponte_b64, ponte_mime         = img_to_base64(ponte_path)

# Galleria (solo percorsi, caricamento b64 avviene nella Home)
gallery_items = [
    {"key": "artistica", "title": "Street art",          "desc": "Murale che racconta la voce artistica e comunitaria di New Orleans.",                                                                    "path": find_image(["home_artistica.jpg"])},
    {"key": "urbana",    "title": "Atmosfera urbana",    "desc": "Una composizione visiva che restituisce l'energia e i contrasti della città.",                                                           "path": find_image(["home_urbana.jpeg", "home_urbana.jpg", "home_urbana.png"])},
    {"key": "simbolica", "title": "La città e il fiume", "desc": "Veduta aerea di New Orleans affacciata sul Mississippi, con il ponte Crescent City Connection.",                                        "path": find_image(["home_simbolica.jpg", "home_simbolica.jpeg"])},
    {"key": "sociale",   "title": "Mardi Gras",          "desc": "Un carro del Mardi Gras sfila tra la folla lungo le strade del French Quarter. Il carnevale di New Orleans è uno dei più spettacolari al mondo.", "path": find_image(["Home_carnevale.jpg", "home_carnevale.jpg", "home_sociale.jpg"])},
    {"key": "umana",     "title": "Volti della città",   "desc": "Un ritratto che racconta il lato umano e quotidiano di New Orleans, attraverso le persone che la vivono.",                               "path": find_image(["home_umana.jpg"])},
    {"key": "musicale",  "title": "Jazz dal vivo",       "desc": "Gruppo di artisti jazz in una serata nel French Quarter: la musica come anima pulsante della città.",                                   "path": find_image(["home_musicale.jpg"])},
]

# Immagini per sezione — caricate solo quando servono
@st.cache_data(show_spinner=False)
def load_briefing_imgs():
    return (
        find_image(["morelli.jpg", "morelli.png"]),
        find_image(["gardner.jpg", "gardner.png"]),
        find_image(["costa.jpg", "costa.png"]),
    )

def inline_img(path, style=""):
    b64, mime = img_to_base64(path)
    if b64:
        return f'<img src="data:{mime};base64,{b64}" style="{style}">'
    return '<div style="background:#dde3ec;width:100%;height:100%;border-radius:50%;"></div>'

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.block-container { max-width: 1200px; padding-top: 0.5rem; padding-bottom: 2rem; }
@media (max-width: 768px) {
    .block-container { padding-top: 0.2rem !important; }
}

/* Nascondi elementi Streamlit */
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stAppViewBlockContainer"] footer { display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }
.viewerBadge_link__qRIco { display: none !important; }
#stDecoration { display: none !important; }
.streamlit-footer { display: none !important; }
[data-testid="stBottom"] { display: none !important; }
section[data-testid="stBottom"] { display: none !important; }
div[class*="StatusWidget"] { display: none !important; }
div[class*="viewerBadge"] { display: none !important; }
button[title="View fullscreen"] { display: none !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #17305a 100%);
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: white !important; }

/* ── HERO PULITA ── */
.hero-clean {
    background: linear-gradient(135deg, #0d1f3c 0%, #17305a 60%, #1a3a6b 100%);
    border-radius: 28px;
    padding: 0;
    margin-bottom: 1.6rem;
    display: flex;
    align-items: stretch;
    overflow: hidden;
    min-height: 230px;
    box-shadow: 0 16px 48px rgba(13,31,60,0.18);
}
.hero-left {
    flex: 1;
    padding: 2.2rem 2rem 2rem 2.4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.5rem;
}
.hero-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #d08c38;
}
.hero-title {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: white;
    line-height: 1.08;
}
.hero-title span { color: #d08c38; }
.hero-nola-logo {
    margin-top: 0.6rem;
    opacity: 0.55;
    filter: brightness(0) invert(1);
    width: 54px;
}
.hero-right {
    flex: 1.1;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    overflow: hidden;
    background: white;
}
.hero-right img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center bottom;
    display: block;
}

/* ── INTRO BOX ── */
.intro-box {
    background: #f0f4fb;
    border-radius: 20px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1.5rem;
    border-left: 5px solid #d08c38;
}
.intro-box p {
    margin: 0;
    font-size: 1rem;
    color: #1e3050;
    line-height: 1.7;
}
.intro-box strong { color: #d08c38; }

/* ── STAT BAR ── */
.stat-bar { display: flex; gap: 1rem; margin-bottom: 1.6rem; }
.stat-item {
    flex: 1; background: white; border-radius: 18px;
    padding: 1.1rem 1rem; text-align: center;
    border: 1px solid rgba(20,33,61,0.08);
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}
.stat-num {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 2.4rem; font-weight: 800; color: #d08c38; line-height: 1;
}
.stat-label { font-size: 0.82rem; color: #5b6472; margin-top: 0.2rem; font-weight: 500; }

/* ── GALLERY ── */
.gallery-caption {
    text-align: center; color: #16324f; font-size: 1rem;
    margin: 0.5rem 0 1.2rem; font-weight: 500;
}
.thumb-title {
    font-size: 0.8rem; font-weight: 700; color: #16324f;
    margin-top: 0.3rem; text-align: center;
}

/* ── CARDS HOME ── */
.home-card {
    background: white; border-radius: 20px; padding: 1.3rem 1.2rem;
    border: 1px solid rgba(20,33,61,0.07);
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    height: 100%;
}
.home-card-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.home-card-title {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.05rem; font-weight: 700; color: #14213d; margin-bottom: 0.35rem;
}
.home-card-text { font-size: 0.93rem; color: #5b6472; line-height: 1.6; }

/* ── TIMELINE ── */
.timeline { position: relative; padding: 0.5rem 0; margin: 1.5rem 0; }
.timeline::before {
    content: ""; position: absolute; left: 36px; top: 0; bottom: 0;
    width: 3px; background: linear-gradient(180deg, #d08c38, #17305a);
    border-radius: 3px;
}
.tl-item { display: flex; gap: 1.2rem; margin-bottom: 1.6rem; align-items: flex-start; }
.tl-dot {
    flex-shrink: 0; width: 74px; height: 74px; border-radius: 50%;
    overflow: hidden; border: 3px solid #d08c38; background: #dde3ec; z-index: 1;
}
.tl-dot img { width: 100%; height: 100%; object-fit: cover; }
.tl-dot-placeholder {
    flex-shrink: 0; width: 74px; height: 74px; border-radius: 50%;
    background: #17305a; border: 3px solid #d08c38;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; z-index: 1;
}
.tl-content {
    background: white; border-radius: 18px; padding: 1rem 1.1rem;
    border: 1px solid rgba(20,33,61,0.08);
    box-shadow: 0 6px 20px rgba(0,0,0,0.06); flex: 1;
}
.tl-date { font-size: 0.78rem; font-weight: 700; color: #d08c38; text-transform: uppercase; letter-spacing: 0.07em; }
.tl-name { font-family: "Playfair Display", Georgia, serif; font-size: 1.15rem; font-weight: 700; color: #14213d; margin: 0.1rem 0; }
.tl-role { font-size: 0.87rem; color: #5b6472; margin-bottom: 0.4rem; }
.tl-desc { font-size: 0.95rem; color: #2c3e50; line-height: 1.65; }

/* ── GENERIC CARD ── */
.card {
    background: white; border-radius: 22px; padding: 1.1rem 1rem;
    border: 1px solid rgba(20,33,61,0.08);
    box-shadow: 0 8px 24px rgba(0,0,0,0.06); height: 100%;
}
.card-title {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.05rem; font-weight: 700; color: #14213d; margin-bottom: 0.35rem;
}
.note { color: #5b6472; font-size: 0.93rem; line-height: 1.6; }

/* ── QUOTE ── */
.quote-box {
    background: #f5f8fc; border-left: 5px solid #d08c38;
    border-radius: 16px; padding: 1rem 1.2rem;
    margin-bottom: 1rem; color: #16324f; font-style: italic;
}

/* ── PAGE TITLE ── */
.page-title {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.9rem; font-weight: 800; color: #14213d; margin-bottom: 0.2rem;
}
.gold-line { width: 48px; height: 4px; background: #d08c38; border-radius: 4px; margin-bottom: 1.2rem; }

/* ── LEGEND ── */
.legend-card {
    background: white; border-radius: 18px; padding: 0.95rem;
    border: 1px solid rgba(20,33,61,0.08);
    box-shadow: 0 6px 16px rgba(0,0,0,0.05); margin-bottom: 0.75rem;
}

/* ── PILLS SIDEBAR ── */
.small-pill {
    display: inline-block; background: rgba(255,255,255,0.13); color: white;
    padding: 0.28rem 0.6rem; border-radius: 999px; font-size: 0.8rem;
    margin-right: 0.3rem; margin-bottom: 0.3rem; border: 1px solid rgba(255,255,255,0.22);
}

/* ── MATERIALI ── */
.mat-card {
    background: white; border-radius: 18px; padding: 1rem 1.2rem;
    border-left: 4px solid #d08c38;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05); margin-bottom: 0.7rem;
    font-size: 0.97rem; color: #2c3e50;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .hero-title { font-size: 1.8rem !important; }
    .stat-bar { flex-wrap: wrap; }
    .stat-bar > div { min-width: 45%; }
    .tl-item { flex-direction: column; }
    .timeline::before { display: none; }
}

/* ── FOOTER ── */
.footer-box {
    text-align: center; color: #9aa3b0; font-size: 0.88rem;
    margin-top: 1.5rem; padding-top: 1rem;
    border-top: 1px solid rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Dati
# ----------------------------
briefing_data = [
    {
        "data": "7 maggio", "titolo": "Elia Morelli",
        "ruolo": "Assegnista di ricerca in Storia Moderna · Università di Pisa",
        "descrizione": "Un briefing dedicato alla storia culturale, politico-economica e geopolitica di New Orleans e della Louisiana. Il punto di vista storico che aiuterà i ragazzi a leggere le radici della città.",
        "foto": None, "emoji": "🏛"
    },
    {
        "data": "21 maggio", "titolo": "Anthony Gardner",
        "ruolo": "Ex ambasciatore USA all'Unione Europea · Consiglio di sicurezza nazionale",
        "descrizione": "Uno sguardo istituzionale e geopolitico, utile a capire il ruolo di New Orleans e il rapporto tra Stati Uniti, Europa e relazioni internazionali.",
        "foto": None, "emoji": "🌐"
    },
    {
        "data": "15 giugno", "titolo": "Francesco Costa",
        "ruolo": "Giornalista · Direttore de Il Post",
        "descrizione": "Il punto di vista sociale, narrativo e attuale sugli Stati Uniti, per aiutare i ragazzi a leggere la realtà americana oltre gli stereotipi.",
        "foto": None, "emoji": "📰"
    },
]

materiali_data = [
    ("📖", "Schede introduttive sui temi del viaggio"),
    ("🎙", "Materiali di approfondimento collegati ai briefing dei tre esperti"),
    ("🗞", "Contenuti su storia, cultura, società e attualità di New Orleans e degli Stati Uniti"),
    ("🗺", "Mappe e riferimenti essenziali per orientarsi nella città e nei suoi quartieri simbolici"),
]

squadre = [
    {"titolo": "🏛 Sguardo Storico",      "focus": "La stratificazione coloniale, il quartiere francese, l'eredità spagnola e africana.",       "missione": "Trovare le tracce del passato che sopravvivono nel presente.",                  "esperto": "Rif. Elia Morelli"},
    {"titolo": "🌐 Sguardo Politico",     "focus": "Il porto, il Mississippi nell'economia globale, le relazioni internazionali.",                "missione": "Raccontare come una città del Sud parli al mondo intero.",                      "esperto": "Rif. Anthony Gardner"},
    {"titolo": "⚖️ Sguardo Sociale",      "focus": "Le contraddizioni: ricchezza e povertà, gentrificazione, questioni razziali.",               "missione": "Osservare le due Americhe che convivono nello stesso isolato.",                  "esperto": "Rif. Francesco Costa"},
    {"titolo": "🎷 Sguardo Sonoro",       "focus": "Jazz, Blues, Second Lines, musicisti di strada di Frenchmen Street.",                        "missione": "Catturare il rumore della città come linguaggio vivo.",                         "esperto": "Dimensione musicale e culturale"},
    {"titolo": "🌊 Sguardo Resiliente",   "focus": "L'eredità di Katrina, il cambiamento climatico, l'architettura della sopravvivenza.",        "missione": "Raccontare come una comunità si rialza dopo il disastro.",                      "esperto": "Resilienza urbana e sociale"},
    {"titolo": "🍲 Sguardo Gastronomico", "focus": "Cucina Creole e Cajun, Gumbo, Beignets, i mercati locali.",                                 "missione": "Spiegare la cultura attraverso il cibo come fusione di popoli.",                 "esperto": "Multiculturalità quotidiana"},
    {"titolo": "🕯 Sguardo Mistico",      "focus": "Il Voodoo, i cimiteri monumentali, il Mardi Gras, il folklore.",                            "missione": "Indagare la parte invisibile di New Orleans, tra simboli e immaginario.",        "esperto": "Tradizioni culturali e popolari"},
    {"titolo": "👁 Sguardo Umano",        "focus": "I volti delle persone, l'accoglienza del Sud, le storie individuali.",                       "missione": "Incrociare lo sguardo dei locali e raccontare la città attraverso chi la vive.", "esperto": "Ponte tra comunità"},
]

luoghi_dati = [
    # IDENTITÀ E STORIA — rosso #c0392b
    {"nome": "French Quarter",       "lat": 29.9584, "lon": -90.0645, "desc": "Il quartiere più iconico, tra architettura storica, balconi in ferro battuto e stratificazioni culturali.",  "colore": "#c0392b", "tema": "Identità e storia"},
    {"nome": "Jackson Square",       "lat": 29.9623, "lon": -90.0637, "desc": "Piazza centrale e simbolica: la Cattedrale di San Luigi, artisti di strada e identità storica.",             "colore": "#c0392b", "tema": "Identità e storia"},
    {"nome": "St. Louis Cemetery",   "lat": 29.9647, "lon": -90.0706, "desc": "Il cimitero più antico di New Orleans, con le tombe sopraelevate e la leggenda di Marie Laveau.",           "colore": "#c0392b", "tema": "Identità e storia"},
    {"nome": "Garden District",      "lat": 29.9277, "lon": -90.0972, "desc": "Quartiere delle grandi ville antebellum, simbolo della storia americana del Sud.",                           "colore": "#c0392b", "tema": "Identità e storia"},

    # MUSICA — giallo/oro #d4a017
    {"nome": "Frenchmen Street",     "lat": 29.9608, "lon": -90.0519, "desc": "La strada più autentica per il jazz dal vivo, lontana dal turismo di Bourbon Street.",                      "colore": "#d4a017", "tema": "Musica"},
    {"nome": "Congo Square",         "lat": 29.9596, "lon": -90.0773, "desc": "Luogo simbolico delle radici africane della musica americana: qui si danzava e suonava già nel '700.",      "colore": "#d4a017", "tema": "Musica"},
    {"nome": "Louis Armstrong Park", "lat": 29.9608, "lon": -90.0736, "desc": "Il parco dedicato al più celebre musicista di New Orleans, nel cuore del quartiere Tremé.",                 "colore": "#d4a017", "tema": "Musica"},
    {"nome": "Preservation Hall",    "lat": 29.9576, "lon": -90.0659, "desc": "La sala concerti storica nel French Quarter, tempio vivente del jazz tradizionale di New Orleans.",         "colore": "#d4a017", "tema": "Musica"},

    # RESILIENZA — blu #17305a
    {"nome": "Lower Ninth Ward",     "lat": 29.9214, "lon": -90.0310, "desc": "Il quartiere più colpito da Katrina nel 2005. Simbolo della resilienza e della lentezza della ricostruzione.", "colore": "#17305a", "tema": "Resilienza"},
    {"nome": "Lake Pontchartrain",   "lat": 30.0500, "lon": -90.1000, "desc": "Il lago ai cui argini fallirono le dighe durante Katrina, causando l'inondazione della città.",              "colore": "#17305a", "tema": "Resilienza"},
    {"nome": "Make It Right Houses", "lat": 29.9230, "lon": -90.0320, "desc": "Le case colorate costruite da Brad Pitt dopo Katrina per i residenti del Lower Ninth Ward.",                 "colore": "#17305a", "tema": "Resilienza"},

    # SOCIETÀ — verde #2e7d5e
    {"nome": "Tremé",                "lat": 29.9636, "lon": -90.0760, "desc": "Il quartiere afroamericano più antico degli USA, culla della cultura creola e della comunità nera.",        "colore": "#2e7d5e", "tema": "Società"},
    {"nome": "Warehouse District",   "lat": 29.9449, "lon": -90.0715, "desc": "Zona di musei e gallerie che mostra la trasformazione urbana e le nuove tensioni sociali della città.",    "colore": "#2e7d5e", "tema": "Società"},
    {"nome": "Bywater",              "lat": 29.9527, "lon": -90.0394, "desc": "Quartiere creativo e in gentrificazione: murales, artisti e contraddizioni della New Orleans contemporanea.", "colore": "#2e7d5e", "tema": "Società"},
]

def section_header(numero, sopratitolo, titolo, desc, colore="#d08c38"):
    ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.07;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""
    st.markdown(f"""
    <style>
    .sec-header-full {{
        position:relative; overflow:hidden;
        background:linear-gradient(135deg,#0d1f3c 0%,#17305a 100%);
        margin:-5rem -1rem 1.6rem -1rem;
        padding:5.5rem 2rem 1.8rem;
    }}
    @media (min-width:769px) {{
        .sec-header-full {{ margin:-5rem -3rem 1.6rem -3rem; padding:5.5rem 3rem 2rem; }}
    }}
    </style>
    <div class="sec-header-full">
        {ponte_bg}
        <div style="position:relative;z-index:1;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                        color:{colore};margin-bottom:0.35rem;">{sopratitolo}</div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.8rem;font-weight:800;
                        color:white;line-height:1.1;margin-bottom:0.5rem;">{titolo}</div>
            <div style="font-size:0.9rem;color:rgba(255,255,255,0.6);line-height:1.65;max-width:520px;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
# ----------------------------
# SIDEBAR
# ----------------------------

# Leggi navigazione da query params (bottom bar mobile)
qp = st.query_params
_pagine_valide = ["Home", "Temi del viaggio", "Briefing", "Approfondimenti", "Mappe", "Programma", "Documenti"]
if "page" in qp and qp["page"] in _pagine_valide:
    st.session_state.nav_target = qp["page"]
    st.query_params.clear()
    st.rerun()

with st.sidebar:
    if logo_path:
        st.image(logo_path, width=100)

    st.markdown("""
    <div style="margin-top:0.2rem;margin-bottom:1.4rem;">
        <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-bottom:0.2rem;">Comune di Peccioli</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.15rem;font-weight:700;color:white;line-height:1.2;">Peccioli × New Orleans<br><span style="color:#d08c38;">2026</span></div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.1);margin-bottom:1.2rem;"></div>
    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-bottom:0.6rem;">Naviga</div>
    """, unsafe_allow_html=True)

    options = ["Home", "Temi del viaggio", "Briefing", "Approfondimenti", "Mappe", "Programma", "Documenti"]

    if "nav_target" not in st.session_state:
        st.session_state.nav_target = "Home"

    cur_index = options.index(st.session_state.nav_target) if st.session_state.nav_target in options else 0

    pagina_radio = st.radio(
        label="",
        options=options,
        label_visibility="collapsed",
        index=cur_index,
    )

    st.session_state.nav_target = pagina_radio
    pagina = pagina_radio

    st.markdown("""
    <div style="height:1px;background:rgba(255,255,255,0.1);margin:1.2rem 0;"></div>
    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-bottom:0.8rem;">Il viaggio</div>

    <div style="display:flex;flex-direction:column;gap:0.55rem;">
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">📅</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">Date</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">21–28 settembre 2026</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">📍</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">Destinazione</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">New Orleans, Louisiana</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">👥</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">Partecipanti</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">80 giovani</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">🎙</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">Incontri preparatori</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">3 briefing con esperti</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# NAVIGAZIONE MOBILE — TOPBAR CON MENU A TENDINA
# ----------------------------
active_page = st.session_state.get("nav_target", "Home")

def build_mobile_topbar(current_page):
    pages = [
        ("Home", "Home"),
        ("Temi", "Temi del viaggio"),
        ("Briefing", "Briefing"),
        ("Extra", "Approfondimenti"),
        ("Mappe", "Mappe"),
        ("Programma", "Programma"),
        ("Documenti", "Documenti"),
    ]

    options_html = ""
    for label, value in pages:
        selected = "selected" if value == current_page else ""
        options_html += f'<option value="{value}" {selected}>{label}</option>'

    return f"""
    <style>
    @media (max-width: 768px) {{
        [data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="collapsedControl"] {{ display: none !important; }}
        [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
        button[kind="header"] {{ display: none !important; }}

        .main .block-container {{
            padding-top: 58px !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        .mobile-topbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 52px;
            background: #0d1f3c;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            padding: 0 0.9rem;
            z-index: 999999;
        }}

        .mobile-topbar-title {{
            font-size: 0.78rem;
            font-weight: 700;
            color: rgba(255,255,255,0.82);
            line-height: 1.1;
            white-space: nowrap;
        }}

        .mobile-topbar-title span {{
            color: #d08c38;
        }}

        .mobile-nav-select {{
            background: #17305a;
            color: white;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 0.45rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 600;
            max-width: 170px;
            outline: none;
        }}

        .sticky-topbar {{
            display: none !important;
        }}
    }}

    @media (min-width: 769px) {{
        .mobile-topbar {{
            display: none !important;
        }}
    }}
    </style>

    <div class="mobile-topbar">
        <div class="mobile-topbar-title">Peccioli × <span>NOLA</span> 2026</div>
        <form method="get" style="margin:0;">
            <select class="mobile-nav-select" name="page" onchange="this.form.submit()">
                {options_html}
            </select>
        </form>
    </div>
    """

st.markdown(build_mobile_topbar(active_page), unsafe_allow_html=True)
# ----------------------------
# HEADER
# ----------------------------
if nola_logo_b64:
    nola_logo_tag = f'<img src="data:{nola_logo_mime};base64,{nola_logo_b64}" class="nola-logo-inline" style="height:44px;opacity:0.65;filter:brightness(0) saturate(100%) invert(16%) sepia(60%) saturate(500%) hue-rotate(190deg);margin-left:0.8rem;vertical-align:middle;position:relative;top:-4px;">'
else:
    nola_logo_tag = ""

logo_tag = f'<img src="data:{logo_mime};base64,{logo_b64}" style="height:62px;object-fit:contain;flex-shrink:0;">' if logo_b64 else ""
logo_tag_small = f'<img src="data:{logo_mime};base64,{logo_b64}" style="height:32px;object-fit:contain;flex-shrink:0;">' if logo_b64 else ""

if pagina == "Home":
    ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.12;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""

    header_html = f"""
    <style>
    /* Hero a tutta larghezza — compensa i margini di Streamlit */
    .hero-full {{
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0d1f3c 0%, #17305a 100%);
        margin: -1rem -1rem 1.4rem -1rem;
        padding: 3rem 2rem 2.8rem;
        text-align: center;
    }}
    @media (min-width: 769px) {{
        .hero-full {{
            margin: -1.2rem -3rem 1.6rem -3rem;
            padding: 3.5rem 3rem 3rem;
        }}
    }}
    .hero-eyebrow {{
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.4);
        margin-bottom: 0.6rem;
    }}
    .hero-title {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2rem, 6vw, 3.2rem);
        font-weight: 800;
        color: white;
        line-height: 1.05;
        letter-spacing: -0.02em;
    }}
    .hero-title span {{ color: #d08c38; }}
    .hero-divider {{
        width: 36px; height: 2px;
        background: #d08c38;
        border-radius: 2px;
        margin: 1rem auto 0;
        opacity: 0.7;
    }}

    /* Topbar fissa in cima — visibile sempre */
    .sticky-topbar {{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 44px;
        background: #0d1f3c;
        display: flex;
        align-items: center;
        padding: 0 1.2rem;
        z-index: 999998;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .sticky-topbar-title {{
        font-size: 0.82rem;
        font-weight: 700;
        color: rgba(255,255,255,0.7);
        letter-spacing: 0.05em;
    }}
    .sticky-topbar-title span {{ color: #d08c38; }}

    /* Compensazione padding per la topbar fissa */
    .main .block-container {{ padding-top: 44px !important; }}
    </style>

    <!-- Topbar fissa -->
    <div class="sticky-topbar">
        <div class="sticky-topbar-title">Peccioli × <span>New Orleans</span> 2026</div>
    </div>

    <!-- Hero a tutta larghezza -->
    <div class="hero-full">
        {ponte_bg}
        <div style="position:relative;z-index:1;">
            <div class="hero-eyebrow">Comune di Peccioli · Progetto di viaggio</div>
            <div class="hero-title">Peccioli &times; <span>New Orleans</span> 2026</div>
            <div class="hero-divider"></div>
        </div>
    </div>
    """
else:
    header_html = f"""
    <style>
    .sticky-topbar {{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 44px;
        background: #0d1f3c;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.2rem;
        z-index: 999998;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .sticky-topbar-title {{
        font-size: 0.82rem;
        font-weight: 700;
        color: rgba(255,255,255,0.7);
        letter-spacing: 0.05em;
    }}
    .sticky-topbar-title span {{ color: #d08c38; }}
    .main .block-container {{ padding-top: 44px !important; }}
    </style>
    <div class="sticky-topbar">
        <div class="sticky-topbar-title">Peccioli × <span>New Orleans</span> 2026</div>
        <a href="?page=Home" style="font-size:0.75rem;font-weight:600;color:#d08c38;text-decoration:none;">← Home</a>
    </div>
    <div style="height:0.8rem;"></div>
    """
st.markdown(header_html, unsafe_allow_html=True)

# ----------------------------
# HOME
# ----------------------------
if pagina == "Home":

    # Countdown funzionante via st.components — mobile responsive
    import streamlit.components.v1 as components

    # Carica solo la foto di Morelli per il countdown (lazy)
    _morelli_path = find_image(["morelli.jpg", "morelli.png"])
    morelli_b64, morelli_mime = img_to_base64(_morelli_path)
    prossimo_foto = f'<img src="data:{morelli_mime};base64,{morelli_b64}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #d08c38;flex-shrink:0;">' if morelli_b64 else '<div style="width:44px;height:44px;border-radius:50%;background:#dde3ec;flex-shrink:0;"></div>'

    countdown_html = ("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { overflow:hidden; background:transparent; }
    .cd-wrap { display:flex; gap:0.75rem; font-family:'Inter',sans-serif; height:110px; align-items:stretch; }
    .cd-main { flex:1.6; min-width:0; background:linear-gradient(135deg,#0d1f3c,#17305a); border-radius:18px; padding:1rem 1.4rem; color:white; display:flex; flex-direction:column; justify-content:center; flex-shrink:0; }
    .cd-label { font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#d08c38; margin-bottom:0.3rem; }
    .cd-num { font-size:1.65rem; font-weight:800; color:white; line-height:1.2; }
    .cd-box { flex:1; min-width:0; background:white; border-radius:18px; padding:0.85rem 1rem; border:1px solid rgba(20,33,61,0.08); box-shadow:0 4px 14px rgba(0,0,0,0.05); display:flex; flex-direction:column; justify-content:center; flex-shrink:0; }
    @media (max-width:600px) {
        html, body { overflow-x:auto; }
        .cd-wrap { overflow-x:auto; scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch; gap:0.6rem; height:100px; }
        .cd-wrap::-webkit-scrollbar { display:none; }
        .cd-main { min-width:190px; scroll-snap-align:start; padding:0.85rem 1rem; }
        .cd-box { min-width:180px; scroll-snap-align:start; }
        .cd-num { font-size:1.4rem; }
    }
    </style>
    <div class="cd-wrap">
        <div class="cd-main">
            <div class="cd-label">&#9203; Mancano al viaggio</div>
            <div class="cd-num" id="cd">&#8212;</div>
        </div>
        <div class="cd-box">
            <div style="font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#d08c38;margin-bottom:0.45rem;">&#128197; Prossimo incontro</div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
    """ + prossimo_foto + """
                <div>
                    <div style="font-size:0.82rem;font-weight:700;color:#14213d;line-height:1.2;">Elia Morelli</div>
                    <div style="font-size:0.72rem;color:#5b6472;margin-top:0.1rem;">7 maggio 2026</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function tick() {
            var t = new Date("2026-09-21T00:00:00").getTime() - Date.now();
            var el = document.getElementById("cd");
            if (!el) return;
            if (t <= 0) { el.innerHTML = "&#127926; Ci siamo!"; return; }
            var d = Math.floor(t / 86400000);
            var h = Math.floor((t % 86400000) / 3600000);
            var m = Math.floor((t % 3600000) / 60000);
            el.innerHTML = "<span style='font-size:1.65rem;font-weight:800;'>" + d + "</span><span style='font-size:0.82rem;opacity:0.6;margin:0 0.3rem 0 0.15rem;'>g</span>" +
                           "<span style='font-size:1.65rem;font-weight:800;'>" + h + "</span><span style='font-size:0.82rem;opacity:0.6;margin:0 0.3rem 0 0.15rem;'>h</span>" +
                           "<span style='font-size:1.65rem;font-weight:800;'>" + m + "</span><span style='font-size:0.82rem;opacity:0.6;margin-left:0.15rem;'>min</span>";
        }
        tick();
        setInterval(tick, 30000);
    </script>
    """)
    components.html(countdown_html, height=120, scrolling=False)

    # 4 bottoni grandi touch-friendly
    st.markdown("""
    <style>
    .quick-grid { display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin:0.8rem 0; }
    .quick-btn {
        display:block; text-align:left; text-decoration:none;
        background:white; color:#14213d; border-radius:14px;
        padding:0.85rem 1rem; font-weight:700; font-size:0.88rem;
        line-height:1.3; border:1px solid rgba(20,33,61,0.09);
        box-shadow:0 2px 8px rgba(0,0,0,0.04);
        border-left: 3px solid #d08c38;
    }
    .quick-btn-label { font-size:0.68rem; color:#d08c38; font-weight:700;
                       text-transform:uppercase; letter-spacing:0.08em;
                       display:block; margin-bottom:0.15rem; }
    </style>
    <div class="quick-grid">
        <a href="?page=Programma" class="quick-btn"><span class="quick-btn-label">🗓 Programma</span>Tappe e attività</a>
        <a href="?page=Briefing" class="quick-btn"><span class="quick-btn-label">📅 Briefing</span>Gli esperti</a>
        <a href="?page=Mappe" class="quick-btn"><span class="quick-btn-label">🗺 Mappe</span>I luoghi</a>
        <a href="?page=Documenti" class="quick-btn"><span class="quick-btn-label">📂 Documenti</span>Moduli e scadenze</a>
    </div>
    """, unsafe_allow_html=True)

    # Descrizione
    st.markdown("""
    <p style="font-size:1rem;color:#3a4a5c;line-height:1.7;margin-bottom:0.4rem;">
    Il portale ufficiale del progetto <strong>Peccioli × New Orleans 2026</strong> — 80 ragazzi, settembre 2026.
    </p>
    """, unsafe_allow_html=True)
    with st.expander("Scopri a cosa serve →"):
        st.markdown("""
        <p style="font-size:0.95rem;color:#3a4a5c;line-height:1.75;">
        Questo spazio è pensato per accompagnare i ragazzi <strong>prima, durante e dopo il viaggio</strong>.
        Qui troverete in tempo reale il <strong>programma aggiornato</strong> del viaggio con tutte le tappe e le attività,
        i <strong>documenti da compilare</strong> con le relative scadenze,
        i <strong>briefing con gli esperti</strong> per prepararsi culturalmente,
        e gli <strong>approfondimenti</strong> — libri, film, documentari — per arrivare a New Orleans
        con uno sguardo già orientato sui quattro temi del viaggio: musica, resilienza, società, identità.
        </p>
        """, unsafe_allow_html=True)

    # Webcam + News + Spotify
    st.markdown("## ")
    st.markdown("""
    <style>
    .home-bottom-grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
    @media (max-width:640px) { .home-bottom-grid { grid-template-columns:1fr; } }
    .hb-card { background:white;border-radius:20px;padding:1.1rem 1.3rem;
               border:1px solid rgba(20,33,61,0.08);box-shadow:0 4px 16px rgba(0,0,0,0.04); }
    .hb-title { font-family:'Playfair Display',Georgia,serif;font-size:1rem;font-weight:700;
                color:#14213d;margin-bottom:0.25rem; }
    .hb-sub { font-size:0.78rem;color:#9aa3b0;margin-bottom:0.7rem; }
    .news-link { display:flex;align-items:center;padding:0.35rem 0;
                 text-decoration:none;border-bottom:1px solid rgba(20,33,61,0.05); }
    .news-link:last-child { border-bottom:none; }
    .news-link-dot { width:6px;height:6px;border-radius:50%;flex-shrink:0;margin-right:0.5rem; }
    .news-link-text { font-size:0.8rem;font-weight:600;color:#14213d; }
    </style>

    <!-- Webcam + News affiancati -->
    <div class="home-bottom-grid" style="margin-bottom:1rem;">
        <div class="hb-card">
            <div class="hb-title">📹 Live da New Orleans</div>
            <div class="hb-sub">French Quarter · Bourbon Street · 24/7</div>
            <a href="https://www.earthcam.com/usa/louisiana/neworleans/bourbonstreet/" target="_blank"
               style="display:inline-block;background:#0d1f3c;color:white;padding:0.4rem 0.9rem;
                      border-radius:999px;font-size:0.78rem;font-weight:600;text-decoration:none;">
                🎥 Guarda →
            </a>
        </div>
        <div class="hb-card">
            <div class="hb-title">🗞 Notizie</div>
            <div class="hb-sub">Fonti locali di New Orleans</div>
            <a href="https://www.nola.com" target="_blank" class="news-link">
                <div class="news-link-dot" style="background:#d08c38;"></div>
                <span class="news-link-text">The Times-Picayune</span>
            </a>
            <a href="https://www.wwno.org" target="_blank" class="news-link">
                <div class="news-link-dot" style="background:#17305a;"></div>
                <span class="news-link-text">WWNO Public Radio</span>
            </a>
            <a href="https://thelensnola.org" target="_blank" class="news-link">
                <div class="news-link-dot" style="background:#2e7d5e;"></div>
                <span class="news-link-text">The Lens NOLA</span>
            </a>
        </div>
    </div>

    <!-- Spotify a tutta larghezza sotto -->
    <div style="border-radius:20px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.08);">
        <iframe style="border-radius:20px;display:block;"
            src="https://open.spotify.com/embed/playlist/0iMiZcvIy26MqHQln5kkrI?utm_source=generator&theme=0"
            width="100%" height="152" frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy">
        </iframe>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# BRIEFING
# ----------------------------
elif pagina == "Briefing":

    section_header("02", "Prima del viaggio", "Incontri propedeutici al viaggio",
        "Tre serate con tre esperti per arrivare a New Orleans con strumenti culturali già solidi. Non lezioni — conversazioni aperte su storia, geopolitica e società americana. Clicca su un relatore per scoprire chi è.")

    # Dati completi con biografia — immagini caricate qui (lazy)
    morelli_img, gardner_img, costa_img = load_briefing_imgs()

    briefing_full = [
        {
            "data": "7 maggio", "ora": "ore 21",
            "titolo": "Elia Morelli",
            "ruolo": "Ricercatore in storia moderna · Università di Pisa",
            "bio": "Ricercatore in storia moderna all'Università di Pisa. Come analista geopolitico, scrive per Domino, rivista edita da Enrico Mentana. Membro della Società Italiana per la Storia dell'Età Moderna, della Società Italiana per lo Studio della Storia Contemporanea e della Renaissance Society of America.",
            "tema": "Storia culturale, politico-economica e geopolitica di New Orleans e della Louisiana.",
            "foto": morelli_img, "emoji": "🏛", "colore": "#d08c38",
        },
        {
            "data": "21 maggio", "ora": "ore 21",
            "titolo": "Anthony Gardner",
            "ruolo": "Ex ambasciatore USA all'UE · Consiglio di sicurezza nazionale",
            "bio": "Ex ambasciatore degli Stati Uniti presso l'Unione Europea dal 2014 al 2017 su nomina del presidente Obama. Ha lavorato per oltre vent'anni sulle relazioni tra USA ed Europa, su temi come i negoziati commerciali transatlantici, la privacy dei dati, l'economia digitale e la sicurezza energetica.",
            "tema": "Sguardo istituzionale e geopolitico: il ruolo di New Orleans e il rapporto tra USA ed Europa.",
            "foto": gardner_img, "emoji": "🌐", "colore": "#17305a",
        },
        {
            "data": "18 giugno", "ora": "ore 21",
            "titolo": "Francesco Costa",
            "ruolo": "Giornalista · Direttore de Il Post",
            "bio": "Direttore responsabile de Il Post. Tra i principali divulgatori italiani sulla società e politica americana, autore di libri e progetti dedicati agli Stati Uniti. Dal 2021 al 2025 ha condotto per il Post il podcast giornaliero Morning, una rassegna stampa commentata che è stata definita \"il primo vero podcast daily italiano\".",
            "tema": "Punto di vista sociale, narrativo e attuale sugli Stati Uniti: leggere l'America oltre gli stereotipi.",
            "foto": costa_img, "emoji": "📰", "colore": "#2e7d5e",
        },
    ]

    # Dialog popup per ogni relatore
    @st.dialog(" ")
    def mostra_relatore(idx):
        b = briefing_full[idx]
        b64, mime = img_to_base64(b["foto"])
        if b64:
            col_foto, col_info = st.columns([1, 2])
            with col_foto:
                st.markdown(f'<img src="data:{mime};base64,{b64}" style="width:100%;border-radius:16px;object-fit:cover;">', unsafe_allow_html=True)
            with col_info:
                st.markdown(f"""
                <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:{b['colore']};">{b['data']} · {b['ora']}</div>
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.4rem;font-weight:800;color:#14213d;margin:0.2rem 0 0.3rem;">{b['titolo']}</div>
                <div style="font-size:0.85rem;color:#5b6472;margin-bottom:0.8rem;">{b['ruolo']}</div>
                """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#f5f8fc;border-radius:14px;padding:1rem 1.1rem;margin:0.5rem 0;">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{b['colore']};margin-bottom:0.4rem;">Chi è</div>
            <div style="font-size:0.92rem;color:#3a4a5c;line-height:1.65;">{b['bio']}</div>
        </div>
        <div style="background:#fff8ee;border-radius:14px;padding:1rem 1.1rem;margin-top:0.6rem;border-left:3px solid {b['colore']};">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{b['colore']};margin-bottom:0.4rem;">Di cosa parlerà</div>
            <div style="font-size:0.92rem;color:#3a4a5c;line-height:1.65;">{b['tema']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Inizializza stato dialog
    if "dialog_idx" not in st.session_state:
        st.session_state.dialog_idx = None
    if st.session_state.dialog_idx is not None:
        mostra_relatore(st.session_state.dialog_idx)
        st.session_state.dialog_idx = None

    # Card tre relatori affiancate
    c1, c2, c3 = st.columns(3)
    for i, (col, b) in enumerate(zip([c1, c2, c3], briefing_full)):
        b64, mime = img_to_base64(b["foto"])
        foto_tag = f'<img src="data:{mime};base64,{b64}" style="width:90px;height:90px;border-radius:50%;object-fit:cover;border:3px solid {b["colore"]};margin:0 auto 0.8rem;display:block;">' if b64 else f'<div style="width:90px;height:90px;border-radius:50%;background:#dde3ec;margin:0 auto 0.8rem;display:flex;align-items:center;justify-content:center;font-size:2rem;">{b["emoji"]}</div>'
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:22px;padding:1.4rem 1rem 1.2rem;
                        border:1px solid rgba(20,33,61,0.08);box-shadow:0 6px 22px rgba(0,0,0,0.06);
                        text-align:center;margin-bottom:0.5rem;">
                {foto_tag}
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{b['colore']};margin-bottom:0.2rem;">{b['data']} · {b['ora']}</div>
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:800;color:#14213d;line-height:1.2;margin-bottom:0.3rem;">{b['titolo']}</div>
                <div style="font-size:0.78rem;color:#5b6472;line-height:1.4;">{b['ruolo']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Scopri {b['titolo'].split()[0]}", key=f"dialog_{i}", use_container_width=True):
                st.session_state.dialog_idx = i
                st.rerun()

# ----------------------------
# APPROFONDIMENTI
# ----------------------------
elif pagina == "Approfondimenti":
    section_header("03", "Per prepararsi", "Approfondimenti",
        "Libri, film, documentari e risorse online per arrivare a New Orleans con uno sguardo già allenato.")

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Libri", "🎬 Film e TV", "🎞 Documentari", "🌐 Risorse"])

    with tab1:
        st.markdown("## ")
        col1, col2 = st.columns(2)
        libri = [
            {
                "titolo": "Una banda di idioti",
                "autore": "John Kennedy Toole",
                "anno": "1980 · Pulitzer",
                "desc": "Capolavoro ambientato nella New Orleans degli anni '60. Satira geniale e irresistibile — il modo più divertente per entrare nell'anima della città.",
                "link": "https://it.wikipedia.org/wiki/Una_banda_di_idioti",
                "colore": "#d08c38",
            },
            {
                "titolo": "Blues Highway",
                "autore": "Rob Siebert",
                "anno": "Reportage narrativo",
                "desc": "Viaggio da Chicago a New Orleans sulle tracce delle origini della musica americana: blues, jazz, gospel. Per capire il legame tra musica e territorio.",
                "link": "https://marcosymarcos.com/libri/gli-alianti/blues-highway/",
                "colore": "#17305a",
            },
            {
                "titolo": "The Moviegoer",
                "autore": "Walker Percy",
                "anno": "1961 · National Book Award",
                "desc": "Romanzo ambientato a New Orleans, vincitore del National Book Award. Racconta l'alienazione e la ricerca di senso di un giovane creolo nella città del Mardi Gras.",
                "link": "https://it.wikipedia.org/wiki/Walker_Percy",
                "colore": "#2e7d5e",
            },
            {
                "titolo": "Zeitoun",
                "autore": "Dave Eggers",
                "anno": "2009 · Non fiction",
                "desc": "La storia vera di un siriano-americano rimasto a New Orleans durante Katrina. Un racconto potente su resilienza, razzismo e fallimento istituzionale dopo la catastrofe.",
                "link": "https://it.wikipedia.org/wiki/Zeitoun_(libro)",
                "colore": "#7b3f00",
            },
        ]
        for i, libro in enumerate(libri):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div style="background:white;border-radius:20px;padding:1.2rem 1.3rem;
                            border-top:4px solid {libro['colore']};
                            box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:1rem;">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                                color:{libro['colore']};margin-bottom:0.3rem;">{libro['anno']}</div>
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.05rem;font-weight:800;
                                color:#14213d;line-height:1.2;margin-bottom:0.15rem;">{libro['titolo']}</div>
                    <div style="font-size:0.8rem;color:#9aa3b0;margin-bottom:0.6rem;">{libro['autore']}</div>
                    <div style="font-size:0.88rem;color:#3a4a5c;line-height:1.6;margin-bottom:0.8rem;">{libro['desc']}</div>
                    <a href="{libro['link']}" target="_blank"
                       style="font-size:0.78rem;font-weight:600;color:{libro['colore']};text-decoration:none;">
                        Approfondisci →
                    </a>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("## ")
        film = [
            {"titolo": "Un tram che si chiama Desiderio", "anno": "1951 · Elia Kazan", "desc": "Con Marlon Brando e Vivien Leigh. Classico assoluto girato nella New Orleans reale.", "link": "https://www.imdb.com/title/tt0044081/", "colore": "#d08c38"},
            {"titolo": "Intervista col vampiro", "anno": "1994 · Neil Jordan", "desc": "Tom Cruise, Brad Pitt, Kirsten Dunst. Cattura l'atmosfera gotica e decadente della Louisiana.", "link": "https://www.imdb.com/title/tt0110632/", "colore": "#17305a"},
            {"titolo": "Il curioso caso di Benjamin Button", "anno": "2008 · David Fincher", "desc": "New Orleans dal dopoguerra a Katrina come sfondo per una storia sull'identità e la memoria.", "link": "https://www.imdb.com/title/tt0421715/", "colore": "#2e7d5e"},
            {"titolo": "Treme", "anno": "2010–2013 · HBO", "desc": "La serie più importante su New Orleans dopo Katrina. Emmy Award. Da vedere assolutamente.", "link": "https://www.imdb.com/title/tt1279972/", "colore": "#d4a017"},
            {"titolo": "Easy Rider", "anno": "1969 · Dennis Hopper", "desc": "Icona della controcultura. Il Mardi Gras di New Orleans in una delle scene più celebri del cinema.", "link": "https://www.imdb.com/title/tt0064276/", "colore": "#7b3f00"},
        ]
        for f in film:
            st.markdown(f"""
            <div style="background:white;border-radius:18px;padding:1rem 1.2rem;margin-bottom:0.7rem;
                        display:flex;align-items:center;gap:1rem;
                        border-left:4px solid {f['colore']};
                        box-shadow:0 3px 12px rgba(0,0,0,0.05);">
                <div style="flex:1;">
                    <div style="font-size:0.7rem;color:{f['colore']};font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">{f['anno']}</div>
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:1rem;font-weight:700;color:#14213d;">{f['titolo']}</div>
                    <div style="font-size:0.85rem;color:#5b6472;margin-top:0.2rem;">{f['desc']}</div>
                </div>
                <a href="{f['link']}" target="_blank"
                   style="flex-shrink:0;background:#0d1f3c;color:white;padding:0.35rem 0.8rem;
                          border-radius:999px;font-size:0.75rem;font-weight:600;text-decoration:none;white-space:nowrap;">
                    IMDb →
                </a>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("## ")
        docs = [
            {"titolo": "Katrina: Come Hell and High Water", "anno": "Netflix · 2025 · Spike Lee", "desc": "Tre episodi, vent'anni dopo: i sopravvissuti raccontano la catastrofe e i fallimenti istituzionali.", "link": "https://www.netflix.com/title/81676595", "label": "Netflix →", "colore": "#c0392b"},
            {"titolo": "Hurricane Katrina: Race Against Time", "anno": "National Geographic · 2025", "desc": "Cinque episodi. Critics Choice Award 2025. Ricostruzione minuto per minuto con footage inedito.", "link": "https://www.imdb.com/title/tt37458027/", "label": "IMDb →", "colore": "#17305a"},
            {"titolo": "When the Levees Broke", "anno": "HBO · 2006 · Spike Lee", "desc": "Quattro atti, il documentario che ha raccontato al mondo la devastazione di Katrina. Pietra miliare.", "link": "https://www.imdb.com/title/tt0783105/", "label": "IMDb →", "colore": "#2e7d5e"},
        ]
        for d in docs:
            st.markdown(f"""
            <div style="background:white;border-radius:20px;padding:1.3rem 1.4rem;margin-bottom:0.8rem;
                        border-top:4px solid {d['colore']};box-shadow:0 4px 16px rgba(0,0,0,0.06);">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;">
                    <div>
                        <div style="font-size:0.7rem;color:{d['colore']};font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;">{d['anno']}</div>
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:800;color:#14213d;margin-bottom:0.4rem;">{d['titolo']}</div>
                        <div style="font-size:0.88rem;color:#5b6472;line-height:1.6;">{d['desc']}</div>
                    </div>
                    <a href="{d['link']}" target="_blank"
                       style="flex-shrink:0;background:{d['colore']};color:white;padding:0.4rem 0.9rem;
                              border-radius:999px;font-size:0.78rem;font-weight:600;text-decoration:none;white-space:nowrap;align-self:center;">
                        {d['label']}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("## ")
        risorse = [
            {"titolo": "New Orleans — Wikipedia italiana", "desc": "Panoramica su storia, cultura, musica e geografia. Ottimo punto di partenza.", "link": "https://it.wikipedia.org/wiki/New_Orleans", "colore": "#17305a"},
            {"titolo": "The Times-Picayune · NOLA.com", "desc": "Il principale quotidiano di New Orleans per seguire l'attualità della città.", "link": "https://www.nola.com", "colore": "#d08c38"},
            {"titolo": "Da Costa a Costa — Francesco Costa", "desc": "Newsletter e YouTube dell'esperto di America che incontreremo al briefing.", "link": "https://www.ilpost.it/costa/", "colore": "#2e7d5e"},
        ]
        for r in risorse:
            st.markdown(f"""
            <a href="{r['link']}" target="_blank" style="text-decoration:none;">
            <div style="background:white;border-radius:18px;padding:1.1rem 1.3rem;margin-bottom:0.7rem;
                        display:flex;align-items:center;gap:1rem;
                        border:1px solid rgba(20,33,61,0.08);
                        box-shadow:0 3px 12px rgba(0,0,0,0.05);">
                <div style="width:6px;height:40px;border-radius:3px;background:{r['colore']};flex-shrink:0;"></div>
                <div>
                    <div style="font-size:0.95rem;font-weight:700;color:#14213d;">{r['titolo']}</div>
                    <div style="font-size:0.82rem;color:#5b6472;margin-top:0.15rem;">{r['desc']}</div>
                </div>
                <div style="margin-left:auto;color:{r['colore']};font-size:1.1rem;flex-shrink:0;">→</div>
            </div>
            </a>
            """, unsafe_allow_html=True)

# ----------------------------
# TEMI DEL VIAGGIO
# ----------------------------
elif pagina == "Temi del viaggio":
    section_header("01", "Come guardare la città", "Temi del viaggio",
        "Quattro chiavi di lettura per osservare New Orleans durante il viaggio. Non categorie separate, ma prospettive da tenere sempre attive.", colore="#d4a017")
    st.markdown('<p style="font-size:1rem;color:#3a4a5c;line-height:1.7;margin-bottom:1.6rem;"></p>', unsafe_allow_html=True)

    # SVG decorativi per ogni tema
    svg_musica = """
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.12;position:absolute;bottom:0;right:0;">
      <circle cx="160" cy="60" r="50" fill="#d08c38"/>
      <circle cx="120" cy="90" r="30" fill="#d08c38"/>
      <!-- onde sonore -->
      <path d="M20 60 Q50 30 80 60 Q110 90 140 60" stroke="#d08c38" stroke-width="4" fill="none"/>
      <path d="M10 75 Q45 40 80 75 Q115 110 150 75" stroke="#d08c38" stroke-width="3" fill="none"/>
      <path d="M30 45 Q60 20 90 45 Q120 70 150 45" stroke="#d08c38" stroke-width="2" fill="none"/>
      <!-- nota musicale -->
      <circle cx="170" cy="35" r="8" fill="#d08c38"/>
      <line x1="178" y1="35" x2="178" y2="5" stroke="#d08c38" stroke-width="3"/>
      <line x1="178" y1="5" x2="195" y2="10" stroke="#d08c38" stroke-width="3"/>
    </svg>"""

    svg_resilienza = """
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.12;position:absolute;bottom:0;right:0;">
      <!-- onde acqua -->
      <path d="M0 90 Q25 70 50 90 Q75 110 100 90 Q125 70 150 90 Q175 110 200 90 L200 120 L0 120 Z" fill="#17305a"/>
      <path d="M0 75 Q25 55 50 75 Q75 95 100 75 Q125 55 150 75 Q175 95 200 75 L200 120 L0 120 Z" fill="#17305a" opacity="0.6"/>
      <!-- forma che emerge -->
      <polygon points="100,15 115,55 85,55" fill="#d08c38"/>
      <rect x="92" y="55" width="16" height="30" fill="#d08c38"/>
    </svg>"""

    svg_societa = """
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.12;position:absolute;bottom:0;right:0;">
      <!-- figure umane stilizzate -->
      <circle cx="50" cy="40" r="14" fill="#2e7d5e"/>
      <rect x="38" y="54" width="24" height="35" rx="4" fill="#2e7d5e"/>
      <circle cx="100" cy="35" r="16" fill="#d08c38"/>
      <rect x="86" y="51" width="28" height="40" rx="4" fill="#d08c38"/>
      <circle cx="150" cy="40" r="14" fill="#17305a"/>
      <rect x="138" y="54" width="24" height="35" rx="4" fill="#17305a"/>
      <!-- linee connessione -->
      <line x1="64" y1="60" x2="86" y2="58" stroke="#2e7d5e" stroke-width="2" stroke-dasharray="4"/>
      <line x1="114" y1="60" x2="138" y2="60" stroke="#d08c38" stroke-width="2" stroke-dasharray="4"/>
    </svg>"""

    svg_storia = """
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.12;position:absolute;bottom:0;right:0;">
      <!-- arco stile French Quarter -->
      <path d="M60 110 L60 50 Q60 20 90 20 Q120 20 120 50 L120 110" stroke="#7b3f00" stroke-width="5" fill="none"/>
      <!-- balcone -->
      <line x1="45" y1="65" x2="135" y2="65" stroke="#7b3f00" stroke-width="4"/>
      <line x1="48" y1="65" x2="48" y2="80" stroke="#7b3f00" stroke-width="3"/>
      <line x1="70" y1="65" x2="70" y2="80" stroke="#7b3f00" stroke-width="3"/>
      <line x1="90" y1="65" x2="90" y2="80" stroke="#7b3f00" stroke-width="3"/>
      <line x1="110" y1="65" x2="110" y2="80" stroke="#7b3f00" stroke-width="3"/>
      <line x1="132" y1="65" x2="132" y2="80" stroke="#7b3f00" stroke-width="3"/>
      <line x1="43" y1="80" x2="137" y2="80" stroke="#7b3f00" stroke-width="4"/>
      <!-- stelle/decorazioni -->
      <circle cx="155" cy="30" r="5" fill="#d08c38"/>
      <circle cx="170" cy="50" r="4" fill="#d08c38"/>
      <circle cx="160" cy="70" r="6" fill="#d08c38"/>
      <circle cx="180" cy="25" r="3" fill="#d08c38"/>
    </svg>"""

    temi = [
        {
            "titolo": "Musica",
            "label": "JAZZ",
            "colore": "#d08c38",
            "bg": "#fff8ee",
            "sottotitolo": "Jazz, blues e il ritmo della città",
            "domanda": "Perché il jazz è nato proprio qui, e non altrove?",
            "desc": "New Orleans è la culla del jazz e del blues. La musica non è intrattenimento: è linguaggio sociale, memoria collettiva, forma di resistenza. Dalle second line nei funerali di strada a Frenchmen Street la sera, la città vive attraverso il suono.",
            "luoghi": "Frenchmen Street · Congo Square · Louis Armstrong Park",
            "svg": svg_musica,
        },
        {
            "titolo": "Resilienza",
            "label": "KATRINA",
            "colore": "#17305a",
            "bg": "#f0f4fb",
            "sottotitolo": "Katrina, ricostruzione e cambiamento climatico",
            "domanda": "Come si ricostruisce una città dopo che l'acqua se la porta via?",
            "desc": "Il 2005 ha messo a nudo le fragilità strutturali della città: infrastrutture, disuguaglianze razziali, risposta istituzionale. Vent'anni dopo, la città è ancora in cammino. Il Lower Ninth Ward è il luogo dove questo tema si tocca con mano.",
            "luoghi": "Lower Ninth Ward · Argini del Mississippi · Lakeview",
            "svg": svg_resilienza,
        },
        {
            "titolo": "Società",
            "label": "PEOPLE",
            "colore": "#2e7d5e",
            "bg": "#f0faf5",
            "sottotitolo": "Diversità culturale, questioni razziali, umanità",
            "domanda": "Cosa succede quando culture lontanissime vivono nello stesso isolato da tre secoli?",
            "desc": "New Orleans è una delle città più multiculturali e diseguali degli Stati Uniti. L'eredità della schiavitù, la comunità creola, le contraddizioni tra turismo e vita reale: osservare la città attraverso le persone che la abitano è il modo più onesto di capirla.",
            "luoghi": "Congo Square · Tremé · Garden District",
            "svg": svg_societa,
        },
        {
            "titolo": "Identità e storia",
            "label": "NOLA",
            "colore": "#7b3f00",
            "bg": "#fdf6f0",
            "sottotitolo": "Radici coloniali, voodoo, Mardi Gras, French Quarter",
            "domanda": "Perché New Orleans non somiglia a nessun'altra città americana?",
            "desc": "Fondata dai francesi, ceduta agli spagnoli, acquistata dagli Stati Uniti. Questa stratificazione di culture — europea, africana, caraibica — ha prodotto un'identità unica: il French Quarter, il voodoo, il Mardi Gras, la cucina creola.",
            "luoghi": "French Quarter · St. Louis Cemetery · Jackson Square",
            "svg": svg_storia,
        },
    ]

    col1, col2 = st.columns(2)
    for i, tema in enumerate(temi):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(f"{tema['titolo']}  ·  {tema['sottotitolo']}", expanded=True):
                st.markdown(f"""
                <div style="position:relative;background:{tema['bg']};border-radius:16px;
                            padding:1.2rem 1rem 1rem;
                            border:1px solid {tema['colore']}22;
                            overflow:hidden;">
                    {tema['svg']}
                    <div style="position:absolute;top:-10px;right:12px;
                                font-family:'Playfair Display',Georgia,serif;
                                font-size:4.5rem;font-weight:800;
                                color:{tema['colore']};opacity:0.07;
                                line-height:1;user-select:none;pointer-events:none;">
                        {tema['label']}
                    </div>
                    <div style="position:relative;z-index:1;">
                        <div style="font-size:0.92rem;font-style:italic;color:{tema['colore']};
                                    font-weight:600;margin-bottom:0.7rem;line-height:1.5;">
                            &ldquo;{tema['domanda']}&rdquo;
                        </div>
                        <div style="font-size:0.87rem;color:#3a4a5c;line-height:1.65;margin-bottom:0.8rem;">
                            {tema['desc']}
                        </div>
                        <div style="font-size:0.75rem;font-weight:600;color:{tema['colore']};
                                    border-top:1px solid {tema['colore']}30;padding-top:0.6rem;">
                            &#128205; {tema['luoghi']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Galleria fotografica in fondo ai temi
    st.markdown("""
    <div style="display:flex;align-items:center;gap:1rem;margin:2rem 0 0.8rem;">
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(20,33,61,0.15));"></div>
        <div style="text-align:center;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#d08c38;margin-bottom:0.2rem;">New Orleans vista da vicino</div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.35rem;font-weight:800;color:#0d1f3c;line-height:1.1;">Sguardi sulla città</div>
        </div>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(20,33,61,0.15),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    valid_items = [item for item in gallery_items if item["path"]]

    @st.fragment
    def galleria():
        if "selected_home_image" not in st.session_state:
            st.session_state.selected_home_image = 0
        idx = min(st.session_state.selected_home_image, len(valid_items) - 1)
        selected = valid_items[idx]
        col_prev, col_img, col_next = st.columns([1, 14, 1])
        with col_prev:
            if st.button("←", key="prev_img"):
                st.session_state.selected_home_image = (idx - 1) % len(valid_items)
                st.rerun(scope="fragment")
        with col_img:
            st.image(selected["path"], use_container_width=True)
        with col_next:
            if st.button("→", key="next_img"):
                st.session_state.selected_home_image = (idx + 1) % len(valid_items)
                st.rerun(scope="fragment")
        st.markdown(f'<div class="gallery-caption"><strong>{selected["title"]}</strong> — {selected["desc"]}</div>', unsafe_allow_html=True)
        dots_html = '<div style="display:flex;justify-content:center;gap:6px;margin-bottom:0.8rem;">'
        for i in range(len(valid_items)):
            color = "#d08c38" if i == idx else "rgba(20,33,61,0.15)"
            dots_html += f'<div style="width:7px;height:7px;border-radius:50%;background:{color};"></div>'
        dots_html += '</div>'
        st.markdown(dots_html, unsafe_allow_html=True)
    galleria()

# ----------------------------
# MAPPE
# ----------------------------
elif pagina == "Mappe":
    section_header("04", "Orientarsi nella città", "Mappa di New Orleans",
        "I luoghi simbolici del viaggio, organizzati per tema. Clicca sui marker per leggere la descrizione di ogni posto.", colore="#2e7d5e")

    @st.fragment
    def mostra_mappa():
        m = folium.Map(location=[29.950, -90.065], zoom_start=13, tiles="CartoDB positron")
        for luogo in luoghi_dati:
            folium.CircleMarker(
                location=[luogo["lat"], luogo["lon"]],
                radius=11, color=luogo["colore"], fill=True,
                fill_color=luogo["colore"], fill_opacity=0.88,
                popup=folium.Popup(
                    f"<b style='font-size:14px'>{luogo['nome']}</b><br>"
                    f"<span style='font-size:12px;color:#444'>{luogo['desc']}</span>",
                    max_width=250
                ),
                tooltip=folium.Tooltip(luogo["nome"], sticky=True)
            ).add_to(m)
        st_folium(m, width=None, height=480, use_container_width=True)
    mostra_mappa()

    # Legenda temi
    st.markdown("## ")
    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1.2rem;">
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(0,0,0,0.08);font-size:0.82rem;font-weight:600;">
            <div style="width:12px;height:12px;border-radius:50%;background:#c0392b;flex-shrink:0;"></div> Identità e storia
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(0,0,0,0.08);font-size:0.82rem;font-weight:600;">
            <div style="width:12px;height:12px;border-radius:50%;background:#d4a017;flex-shrink:0;"></div> Musica
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(0,0,0,0.08);font-size:0.82rem;font-weight:600;">
            <div style="width:12px;height:12px;border-radius:50%;background:#17305a;flex-shrink:0;"></div> Resilienza
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(0,0,0,0.08);font-size:0.82rem;font-weight:600;">
            <div style="width:12px;height:12px;border-radius:50%;background:#2e7d5e;flex-shrink:0;"></div> Società
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, luogo in enumerate(luoghi_dati):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="legend-card" style="border-left:4px solid {luogo['colore']};margin-bottom:0.6rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:0.95rem;font-weight:700;color:#14213d;">{luogo['nome']}</div>
                </div>
                <div style="font-size:0.72rem;font-weight:600;color:{luogo['colore']};margin-bottom:0.2rem;">{luogo['tema']}</div>
                <div class="note">{luogo['desc']}</div>
            </div>""", unsafe_allow_html=True)

# ----------------------------
# PROGRAMMA
# ----------------------------
elif pagina == "Programma":
    section_header("05", "Il viaggio", "Programma",
        "Il programma dettagliato è ancora in costruzione. Questa sezione verrà aggiornata con tutte le tappe non appena il percorso sarà definito.", colore="#d08c38")

    st.markdown("""
    <div style="background:#fff8ee;border:2px dashed #d08c38;border-radius:24px;padding:2.5rem 2rem;text-align:center;max-width:580px;margin:2rem auto;">
        <div style="font-size:2.5rem;margin-bottom:0.6rem;">🗓</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.4rem;font-weight:700;color:#14213d;margin-bottom:0.6rem;">Programma in definizione</div>
        <div style="font-size:0.97rem;color:#5b6472;line-height:1.75;">
            Il programma dettagliato del viaggio è ancora in fase di costruzione.<br>
            Questa sezione verrà aggiornata con tutte le tappe, gli appuntamenti
            e le attività non appena il percorso sarà definito.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# DOCUMENTI
# ----------------------------
elif pagina == "Documenti":
    section_header("06", "Prima della partenza", "Materiali e documenti",
        "Documenti da consultare, compilare e consegnare in vista del viaggio.", colore="#17305a")

    st.markdown("""
    <div style="background:#f0f4fb;border-left:4px solid #17305a;border-radius:0 12px 12px 0;
                padding:0.8rem 1.2rem;margin-bottom:1.4rem;font-size:0.88rem;color:#17305a;">
        📋 I documenti saranno caricati progressivamente nelle settimane prima della partenza.
    </div>
    """, unsafe_allow_html=True)

    documenti = [
        ("📋", "Modulo di adesione", "Da compilare e riconsegnare firmato dai genitori.", False),
        ("🛂", "Copia documento d'identità", "Carta d'identità o passaporto in corso di validità.", False),
        ("🏥", "Modulo sanitario", "Informazioni mediche e allergie da comunicare all'organizzazione.", False),
        ("✈️", "Informazioni sul volo", "Orari, scalo, indicazioni per l'aeroporto di partenza.", False),
        ("🏨", "Sistemazione", "Dettagli sull'alloggio a New Orleans.", False),
        ("📱", "Contatti e riferimenti", "Numeri di emergenza, referenti locali, chat di gruppo.", False),
    ]

    for icona, titolo, desc, completato in documenti:
        colore_stato = "#2e7d5e" if completato else "#9aa3b0"
        stato_testo = "✅ Disponibile" if completato else "⏳ In arrivo"
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:0.9rem 1.1rem;margin-bottom:0.6rem;
                    display:flex;align-items:center;gap:1rem;
                    border:1px solid rgba(20,33,61,0.07);box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:1.5rem;flex-shrink:0;">{icona}</div>
            <div style="flex:1;">
                <div style="font-weight:700;color:#14213d;font-size:0.92rem;margin-bottom:0.1rem;">{titolo}</div>
                <div style="font-size:0.8rem;color:#5b6472;">{desc}</div>
            </div>
            <div style="flex-shrink:0;">
                <div style="font-size:0.72rem;font-weight:600;color:{colore_stato};">{stato_testo}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='footer-box'>Demo grafica v12 · Portale ragazzi Peccioli × New Orleans 2026</div>", unsafe_allow_html=True)
