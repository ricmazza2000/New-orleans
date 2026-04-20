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
    page_title="Peccioli Eyes to New Orleans",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

# ============================
# BRAND IDENTITY
# ============================
BRAND_BLUE = "#130089"       # primario
BRAND_YELLOW = "#FFDE59"     # accento
BRAND_WHITE = "#FFFFFF"
BRAND_BLUE_DARK = "#0a0052"  # per gradienti/hover
BRAND_BLUE_LIGHT = "#f0eeff" # background tenui
BRAND_YELLOW_LIGHT = "#fffbe5"

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
# Immagini
# ----------------------------
logo_path = find_image(["logo_comune.png", "logo_comune.jpg"])
nola_logo_path = find_image(["New_Orleans_Logo.png", "New_Orleans_Logo.jpg"])
ponte_path = find_image(["piazza_nola_ponte.png", "piazza_nola_ponte.jpg", "Schermata_2026-04-18_alle_11_58_52.png"])
# NUOVO: logo Peccioli Eyes (occhio con tromba)
eyes_logo_path = find_image(["peccioli_eyes_logo.png", "peccioli_eyes_logo.jpg", "eyes_logo.png"])

logo_b64, logo_mime = img_to_base64(logo_path)
nola_logo_b64, nola_logo_mime = img_to_base64(nola_logo_path)
ponte_b64, ponte_mime = img_to_base64(ponte_path)
eyes_logo_b64, eyes_logo_mime = img_to_base64(eyes_logo_path)

gallery_items = [
    {"key": "artistica", "title": "Street art",
     "desc": "Murale che racconta la voce artistica e comunitaria di New Orleans.",
     "path": find_image(["home_artistica.jpg"])},
    {"key": "urbana", "title": "Atmosfera urbana",
     "desc": "Una composizione visiva che restituisce l'energia e i contrasti della città.",
     "path": find_image(["home_urbana.jpeg", "home_urbana.jpg", "home_urbana.png"])},
    {"key": "simbolica", "title": "La città e il fiume",
     "desc": "Veduta aerea di New Orleans affacciata sul Mississippi, con il ponte Crescent City Connection.",
     "path": find_image(["home_simbolica.jpg", "home_simbolica.jpeg"])},
    {"key": "sociale", "title": "Mardi Gras",
     "desc": "Un carro del Mardi Gras sfila tra la folla lungo le strade del French Quarter. Il carnevale di New Orleans è uno dei più spettacolari al mondo.",
     "path": find_image(["Home_carnevale.jpg", "home_carnevale.jpg", "home_sociale.jpg"])},
    {"key": "umana", "title": "Volti della città",
     "desc": "Un ritratto che racconta il lato umano e quotidiano di New Orleans, attraverso le persone che la vivono.",
     "path": find_image(["home_umana.jpg"])},
    {"key": "musicale", "title": "Jazz dal vivo",
     "desc": "Gruppo di artisti jazz in una serata nel French Quarter: la musica come anima pulsante della città.",
     "path": find_image(["home_musicale.jpg"])},
]

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
# CSS — NUOVA BRAND IDENTITY
# ----------------------------
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,800;0,900;1,700&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root {{
    --brand-blue: {BRAND_BLUE};
    --brand-blue-dark: {BRAND_BLUE_DARK};
    --brand-blue-light: {BRAND_BLUE_LIGHT};
    --brand-yellow: {BRAND_YELLOW};
    --brand-yellow-light: {BRAND_YELLOW_LIGHT};
    --brand-white: {BRAND_WHITE};
}}

html, body, [class*="css"] {{
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.block-container {{
    max-width: 1200px;
    padding-top: 0.5rem;
    padding-bottom: 2rem;
}}
@media (max-width: 768px) {{
    .block-container {{ padding-top: 0.2rem !important; }}
}}

/* Font classes */
.font-serif {{ font-family: "Playfair Display", Georgia, serif; }}
.font-script {{ font-family: "Lobster Two", cursive; font-style: italic; }}

/* Nascondi elementi Streamlit */
#MainMenu {{ display: none !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}
footer {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}
[data-testid="stAppViewBlockContainer"] footer {{ display: none !important; }}
.viewerBadge_container__1QSob {{ display: none !important; }}
.viewerBadge_link__qRIco {{ display: none !important; }}
#stDecoration {{ display: none !important; }}
.streamlit-footer {{ display: none !important; }}
[data-testid="stBottom"] {{ display: none !important; }}
section[data-testid="stBottom"] {{ display: none !important; }}
div[class*="StatusWidget"] {{ display: none !important; }}
div[class*="viewerBadge"] {{ display: none !important; }}
button[title="View fullscreen"] {{ display: none !important; }}

[data-testid="stSidebar"] {{
    background: {BRAND_BLUE};
    border-right: 1px solid rgba(255,255,255,0.1);
}}
[data-testid="stSidebar"] * {{ color: white !important; }}

/* ── INTRO BOX ── */
.intro-box {{
    background: var(--brand-blue-light);
    border-radius: 20px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1.5rem;
    border-left: 5px solid var(--brand-yellow);
}}
.intro-box p {{
    margin: 0;
    font-size: 1rem;
    color: var(--brand-blue);
    line-height: 1.7;
}}
.intro-box strong {{ color: var(--brand-blue); }}

/* ── GALLERY ── */
.gallery-caption {{
    text-align: center;
    color: var(--brand-blue);
    font-size: 1rem;
    margin: 0.5rem 0 1.2rem;
    font-weight: 500;
}}
.thumb-title {{
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--brand-blue);
    margin-top: 0.3rem;
    text-align: center;
}}

/* ── CARDS HOME ── */
.home-card {{
    background: white;
    border-radius: 20px;
    padding: 1.3rem 1.2rem;
    border: 1px solid rgba(19,0,137,0.1);
    box-shadow: 0 6px 20px rgba(19,0,137,0.06);
    height: 100%;
}}
.home-card-icon {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
.home-card-title {{
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--brand-blue);
    margin-bottom: 0.35rem;
}}
.home-card-text {{
    font-size: 0.93rem;
    color: #5b6472;
    line-height: 1.6;
}}

/* ── GENERIC CARD ── */
.card {{
    background: white;
    border-radius: 22px;
    padding: 1.1rem 1rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 8px 24px rgba(19,0,137,0.06);
    height: 100%;
}}
.card-title {{
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--brand-blue);
    margin-bottom: 0.35rem;
}}
.note {{
    color: #5b6472;
    font-size: 0.93rem;
    line-height: 1.6;
}}

/* ── QUOTE ── */
.quote-box {{
    background: var(--brand-yellow-light);
    border-left: 5px solid var(--brand-yellow);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    color: var(--brand-blue);
    font-style: italic;
}}

/* ── LEGEND ── */
.legend-card {{
    background: white;
    border-radius: 18px;
    padding: 0.95rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 6px 16px rgba(19,0,137,0.05);
    margin-bottom: 0.75rem;
}}

/* ── PILLS SIDEBAR ── */
.small-pill {{
    display: inline-block;
    background: rgba(255,222,89,0.2);
    color: var(--brand-yellow);
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
    font-size: 0.8rem;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    border: 1px solid rgba(255,222,89,0.4);
}}

/* ── MATERIALI ── */
.mat-card {{
    background: white;
    border-radius: 18px;
    padding: 1rem 1.2rem;
    border-left: 4px solid var(--brand-yellow);
    box-shadow: 0 4px 14px rgba(19,0,137,0.05);
    margin-bottom: 0.7rem;
    font-size: 0.97rem;
    color: var(--brand-blue);
}}

/* ── MOBILE ── */
@media (max-width: 768px) {{
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    .hero-title {{ font-size: 1.8rem !important; }}
}}

/* ── FOOTER ── */
.footer-box {{
    text-align: center;
    color: #9aa3b0;
    font-size: 0.88rem;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(19,0,137,0.08);
}}

/* Override Streamlit button style per allinearlo al brand */
.stButton>button {{
    background: {BRAND_BLUE} !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}}
.stButton>button:hover {{
    background: {BRAND_BLUE_DARK} !important;
    color: {BRAND_YELLOW} !important;
}}

/* Radio sidebar */
[data-testid="stSidebar"] .stRadio label {{
    padding: 0.3rem 0;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    color: {BRAND_YELLOW} !important;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Dati
# ----------------------------
briefing_data = [
    {
        "data": "7 maggio",
        "titolo": "Elia Morelli",
        "ruolo": "Assegnista di ricerca in Storia Moderna · Università di Pisa",
        "descrizione": "Un briefing dedicato alla storia culturale, politico-economica e geopolitica di New Orleans e della Louisiana. Il punto di vista storico che aiuterà i ragazzi a leggere le radici della città.",
        "foto": None,
        "emoji": "🏛"
    },
    {
        "data": "21 maggio",
        "titolo": "Anthony Gardner",
        "ruolo": "Ex ambasciatore USA all'Unione Europea · Consiglio di sicurezza nazionale",
        "descrizione": "Uno sguardo istituzionale e geopolitico, utile a capire il ruolo di New Orleans e il rapporto tra Stati Uniti, Europa e relazioni internazionali.",
        "foto": None,
        "emoji": "🌐"
    },
    {
        "data": "15 giugno",
        "titolo": "Francesco Costa",
        "ruolo": "Giornalista · Direttore de Il Post",
        "descrizione": "Il punto di vista sociale, narrativo e attuale sugli Stati Uniti, per aiutare i ragazzi a leggere la realtà americana oltre gli stereotipi.",
        "foto": None,
        "emoji": "📰"
    },
]

materiali_data = [
    ("📖", "Schede introduttive sui temi del viaggio"),
    ("🎙", "Materiali di approfondimento collegati ai briefing dei tre esperti"),
    ("🗞", "Contenuti su storia, cultura, società e attualità di New Orleans e degli Stati Uniti"),
    ("🗺", "Mappe e riferimenti essenziali per orientarsi nella città e nei suoi quartieri simbolici"),
]

# Temi → ora usano palette brand (blu, giallo, blu scuro, giallo scuro)
luoghi_dati = [
    # IDENTITÀ E STORIA — blu scuro
    {"nome": "French Quarter", "lat": 29.9584, "lon": -90.0645,
     "desc": "Il quartiere più iconico, tra architettura storica, balconi in ferro battuto e stratificazioni culturali.",
     "colore": BRAND_BLUE, "tema": "Identità e storia"},
    {"nome": "Jackson Square", "lat": 29.9623, "lon": -90.0637,
     "desc": "Piazza centrale e simbolica: la Cattedrale di San Luigi, artisti di strada e identità storica.",
     "colore": BRAND_BLUE, "tema": "Identità e storia"},
    {"nome": "St. Louis Cemetery", "lat": 29.9647, "lon": -90.0706,
     "desc": "Il cimitero più antico di New Orleans, con le tombe sopraelevate e la leggenda di Marie Laveau.",
     "colore": BRAND_BLUE, "tema": "Identità e storia"},
    {"nome": "Garden District", "lat": 29.9277, "lon": -90.0972,
     "desc": "Quartiere delle grandi ville antebellum, simbolo della storia americana del Sud.",
     "colore": BRAND_BLUE, "tema": "Identità e storia"},

    # MUSICA — giallo
    {"nome": "Frenchmen Street", "lat": 29.9608, "lon": -90.0519,
     "desc": "La strada più autentica per il jazz dal vivo, lontana dal turismo di Bourbon Street.",
     "colore": "#e6b800", "tema": "Musica"},
    {"nome": "Congo Square", "lat": 29.9596, "lon": -90.0773,
     "desc": "Luogo simbolico delle radici africane della musica americana: qui si danzava e suonava già nel '700.",
     "colore": "#e6b800", "tema": "Musica"},
    {"nome": "Louis Armstrong Park", "lat": 29.9608, "lon": -90.0736,
     "desc": "Il parco dedicato al più celebre musicista di New Orleans, nel cuore del quartiere Tremé.",
     "colore": "#e6b800", "tema": "Musica"},
    {"nome": "Preservation Hall", "lat": 29.9576, "lon": -90.0659,
     "desc": "La sala concerti storica nel French Quarter, tempio vivente del jazz tradizionale di New Orleans.",
     "colore": "#e6b800", "tema": "Musica"},

    # RESILIENZA — blu medio
    {"nome": "Lower Ninth Ward", "lat": 29.9214, "lon": -90.0310,
     "desc": "Il quartiere più colpito da Katrina nel 2005. Simbolo della resilienza e della lentezza della ricostruzione.",
     "colore": "#4a3fb8", "tema": "Resilienza"},
    {"nome": "Lake Pontchartrain", "lat": 30.0500, "lon": -90.1000,
     "desc": "Il lago ai cui argini fallirono le dighe durante Katrina, causando l'inondazione della città.",
     "colore": "#4a3fb8", "tema": "Resilienza"},
    {"nome": "Make It Right Houses", "lat": 29.9230, "lon": -90.0320,
     "desc": "Le case colorate costruite da Brad Pitt dopo Katrina per i residenti del Lower Ninth Ward.",
     "colore": "#4a3fb8", "tema": "Resilienza"},

    # SOCIETÀ — giallo scuro/ocra
    {"nome": "Tremé", "lat": 29.9636, "lon": -90.0760,
     "desc": "Il quartiere afroamericano più antico degli USA, culla della cultura creola e della comunità nera.",
     "colore": "#b8860b", "tema": "Società"},
    {"nome": "Warehouse District", "lat": 29.9449, "lon": -90.0715,
     "desc": "Zona di musei e gallerie che mostra la trasformazione urbana e le nuove tensioni sociali della città.",
     "colore": "#b8860b", "tema": "Società"},
    {"nome": "Bywater", "lat": 29.9527, "lon": -90.0394,
     "desc": "Quartiere creativo e in gentrificazione: murales, artisti e contraddizioni della New Orleans contemporanea.",
     "colore": "#b8860b", "tema": "Società"},
]

def section_header(numero, sopratitolo, titolo, desc, colore=None):
    if colore is None:
        colore = BRAND_YELLOW
    ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.07;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""
    st.markdown(f"""
    <style>
    .sec-header-full {{
        position:relative; overflow:hidden;
        background:{BRAND_BLUE};
        margin:-5rem -1rem 1.6rem -1rem;
        padding:5.5rem 2rem 1.8rem;
    }}
    @media (min-width:769px) {{
        .sec-header-full {{
            margin:-5rem -3rem 1.6rem -3rem;
            padding:5.5rem 3rem 2rem;
        }}
    }}
    </style>
    <div class="sec-header-full">
        {ponte_bg}
        <div style="position:relative;z-index:1;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                 color:{colore};margin-bottom:0.35rem;">{sopratitolo}</div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:2rem;font-weight:800;
                 color:white;line-height:1.05;margin-bottom:0.5rem;letter-spacing:-0.01em;">{titolo}</div>
            <div style="font-size:0.9rem;color:rgba(255,255,255,0.75);line-height:1.65;max-width:520px;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# SIDEBAR — query params navigation
# ----------------------------
qp = st.query_params
_pagine_valide = ["Home", "Temi del viaggio", "Briefing", "Approfondimenti", "Mappe", "Programma", "Documenti"]
if "page" in qp and qp["page"] in _pagine_valide:
    st.session_state.nav_target = qp["page"]
    st.query_params.clear()
    st.rerun()

with st.sidebar:
    if logo_path:
        st.image(logo_path, width=100)
    st.markdown(f"""
    <div style="margin-top:0.2rem;margin-bottom:1.4rem;">
        <div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:0.25rem;">Comune di Peccioli</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.4rem;font-weight:800;color:white;line-height:1;letter-spacing:-0.01em;">PECCIOLI EYES</div>
        <div style="font-family:'Lobster Two',cursive;font-style:italic;font-size:1.05rem;color:{BRAND_YELLOW};line-height:1.1;margin-top:0.15rem;">to New Orleans</div>
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.4);margin-top:0.3rem;letter-spacing:0.1em;">2026</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.1);margin-bottom:1.2rem;"></div>
    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:0.6rem;">Naviga</div>
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

    st.markdown(f"""
    <div style="height:1px;background:rgba(255,255,255,0.1);margin:1.2rem 0;"></div>
    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:0.8rem;">Il viaggio</div>
    <div style="display:flex;flex-direction:column;gap:0.55rem;">
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">📅</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.55);">Date</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">21–28 settembre 2026</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">📍</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.55);">Destinazione</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">New Orleans, Louisiana</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">👥</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.55);">Partecipanti</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">80 giovani</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1rem;">🎙</span>
            <div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.55);">Incontri preparatori</div>
                <div style="font-size:0.88rem;font-weight:600;color:white;">3 briefing con esperti</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Bottom bar mobile
voci_nav = [
    ("🏠", "Home"),
    ("📅", "Briefing"),
    ("👁", "Temi"),
    ("🗺", "Mappe"),
    ("🗓", "Programma"),
    ("📂", "Documenti"),
    ("📚", "Altro"),
]
voci_map = {
    "Home": "Home",
    "Briefing": "Briefing",
    "Temi": "Temi del viaggio",
    "Mappe": "Mappe",
    "Programma": "Programma",
    "Documenti": "Documenti",
    "Altro": "Approfondimenti",
}
active = st.session_state.get("nav_target", "Home")

st.markdown(f"""
<style>
@media (max-width: 768px) {{
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
    button[kind="header"] {{ display: none !important; }}
    .main .block-container {{
        padding-bottom: 75px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
}}
.bottom-nav {{ display: none; }}
@media (max-width: 768px) {{
    .bottom-nav {{
        display: flex;
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background: {BRAND_BLUE};
        border-top: 2px solid {BRAND_YELLOW};
        padding: 6px 2px calc(10px + env(safe-area-inset-bottom));
        z-index: 2147483647;
        justify-content: space-around;
        align-items: flex-end;
    }}
    .bn-item {{
        display:flex; flex-direction:column; align-items:center; gap:2px;
        text-decoration:none; flex:1; padding:2px 1px;
    }}
    .bn-icon {{ font-size:1.1rem; line-height:1; }}
    .bn-label {{ font-size:0.5rem; text-align:center; line-height:1.2; font-family:sans-serif; }}
}}
</style>
""", unsafe_allow_html=True)

bottom_items = ""
for icon, short in voci_nav:
    label = voci_map[short]
    is_active = (label == active)
    color = BRAND_YELLOW if is_active else "rgba(255,255,255,0.6)"
    weight = "700" if is_active else "400"
    page_param = label.replace(" ", "+")
    bottom_items += f'<a href="?page={page_param}" class="bn-item"><span class="bn-icon">{icon}</span><span class="bn-label" style="color:{color};font-weight:{weight};">{short}</span></a>'

st.markdown(f'<div class="bottom-nav">{bottom_items}</div>', unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
# Logo Peccioli Eyes (occhio con tromba) — piccolo tag inline riutilizzabile
if eyes_logo_b64:
    eyes_tag_hero = f'<img src="data:{eyes_logo_mime};base64,{eyes_logo_b64}" style="height:68px;width:auto;object-fit:contain;margin-bottom:0.6rem;filter:brightness(0) invert(1);opacity:0.95;">'
    eyes_tag_topbar = f'<img src="data:{eyes_logo_mime};base64,{eyes_logo_b64}" style="height:22px;width:auto;object-fit:contain;filter:brightness(0) saturate(100%) invert(89%) sepia(45%) saturate(550%) hue-rotate(344deg);margin-right:0.5rem;vertical-align:middle;">'
else:
    eyes_tag_hero = ""
    eyes_tag_topbar = ""

if pagina == "Home":
    ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.08;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""
    header_html = f"""
    <style>
    .hero-full {{
        position: relative;
        overflow: hidden;
        background: {BRAND_BLUE};
        margin: -1rem -1rem 1.4rem -1rem;
        padding: 3rem 2rem 3rem;
        text-align: center;
    }}
    @media (min-width: 769px) {{
        .hero-full {{
            margin: -1.2rem -3rem 1.6rem -3rem;
            padding: 3.5rem 3rem 3.5rem;
        }}
    }}
    .hero-eyebrow {{
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.55);
        margin-bottom: 0.7rem;
    }}
    .hero-title-main {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2.3rem, 7vw, 4rem);
        font-weight: 800;
        color: white;
        line-height: 0.95;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }}
    .hero-title-script {{
        font-family: 'Lobster Two', cursive;
        font-style: italic;
        font-weight: 700;
        font-size: clamp(1.5rem, 4.5vw, 2.6rem);
        color: {BRAND_YELLOW};
        line-height: 1.1;
        margin-top: 0.2rem;
    }}
    .hero-year {{
        display:inline-block;
        margin-top: 1rem;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.3em;
        color: rgba(255,255,255,0.6);
        padding: 0.35rem 0.9rem;
        border: 1px solid rgba(255,222,89,0.5);
        border-radius: 999px;
    }}

    .sticky-topbar {{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 44px;
        background: {BRAND_BLUE};
        display: flex;
        align-items: center;
        padding: 0 1.2rem;
        z-index: 999998;
        border-bottom: 2px solid {BRAND_YELLOW};
    }}
    .sticky-topbar-title {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.85rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}
    .sticky-topbar-title em {{
        font-family: 'Lobster Two', cursive;
        font-style: italic;
        font-weight: 600;
        color: {BRAND_YELLOW};
        text-transform: none;
        letter-spacing: 0;
        margin-left: 0.3rem;
    }}

    .main .block-container {{
        padding-top: 44px !important;
    }}
    </style>

    <div class="sticky-topbar">
        <div class="sticky-topbar-title">{eyes_tag_topbar}PECCIOLI EYES<em>to New Orleans</em></div>
    </div>

    <div class="hero-full">
        {ponte_bg}
        <div style="position:relative;z-index:1;">
            <div class="hero-eyebrow">Comune di Peccioli · Progetto di viaggio</div>
            {eyes_tag_hero}
            <div class="hero-title-main">Peccioli Eyes</div>
            <div class="hero-title-script">to New Orleans</div>
            <div class="hero-year">2026</div>
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
        background: {BRAND_BLUE};
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.2rem;
        z-index: 999998;
        border-bottom: 2px solid {BRAND_YELLOW};
    }}
    .sticky-topbar-title {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.85rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}
    .sticky-topbar-title em {{
        font-family: 'Lobster Two', cursive;
        font-style: italic;
        font-weight: 600;
        color: {BRAND_YELLOW};
        text-transform: none;
        letter-spacing: 0;
        margin-left: 0.3rem;
    }}
    .main .block-container {{
        padding-top: 44px !important;
    }}
    </style>
    <div class="sticky-topbar">
        <div class="sticky-topbar-title">{eyes_tag_topbar}PECCIOLI EYES<em>to New Orleans</em></div>
        <a href="?page=Home" style="font-size:0.75rem;font-weight:700;color:{BRAND_YELLOW};text-decoration:none;">← Home</a>
    </div>
    <div style="height:0.8rem;"></div>
    """

st.markdown(header_html, unsafe_allow_html=True)

# ----------------------------
# HOME
# ----------------------------
if pagina == "Home":
    import streamlit.components.v1 as components

    _morelli_path = find_image(["morelli.jpg", "morelli.png"])
    morelli_b64, morelli_mime = img_to_base64(_morelli_path)
    prossimo_foto = f'<img src="data:{morelli_mime};base64,{morelli_b64}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid {BRAND_YELLOW};flex-shrink:0;">' if morelli_b64 else f'<div style="width:44px;height:44px;border-radius:50%;background:{BRAND_YELLOW};flex-shrink:0;"></div>'

    countdown_html = ("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { overflow:hidden; background:transparent; }
    .cd-wrap {
        display:flex; gap:0.75rem; font-family:'Inter',sans-serif;
        height:110px; align-items:stretch;
    }
    .cd-main {
        flex:1.6; min-width:0;
        background:""" + BRAND_BLUE + """;
        border-radius:18px; padding:1rem 1.4rem; color:white;
        display:flex; flex-direction:column; justify-content:center;
        flex-shrink:0;
    }
    .cd-label {
        font-size:0.65rem; font-weight:700; letter-spacing:0.12em;
        text-transform:uppercase; color:""" + BRAND_YELLOW + """; margin-bottom:0.3rem;
    }
    .cd-num {
        font-size:1.65rem; font-weight:800; color:white; line-height:1.2;
    }
    .cd-box {
        flex:1; min-width:0;
        background:white; border-radius:18px; padding:0.85rem 1rem;
        border:1px solid rgba(19,0,137,0.1);
        box-shadow:0 4px 14px rgba(19,0,137,0.06);
        display:flex; flex-direction:column; justify-content:center;
        flex-shrink:0;
    }
    @media (max-width:600px) {
        html, body { overflow-x:auto; }
        .cd-wrap {
            overflow-x:auto; scroll-snap-type:x mandatory;
            -webkit-overflow-scrolling:touch; gap:0.6rem
