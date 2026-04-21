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
BRAND_BLUE = "#130089"
BRAND_YELLOW = "#FFDE59"
BRAND_WHITE = "#FFFFFF"
BRAND_BLUE_DARK = "#0a0052"
BRAND_BLUE_LIGHT = "#f0eeff"
BRAND_YELLOW_LIGHT = "#fffbe5"

# ============================
# UTILITY — caching aggressivo
# ============================
@st.cache_data(show_spinner=False)
def find_image(possible_names_tuple):
    """Tuple per essere hashable e cacheable."""
    for name in possible_names_tuple:
        p = BASE_DIR / name
        if p.exists():
            return str(p)
    return None

def find_img(*names):
    """Wrapper comodo."""
    return find_image(tuple(names))

@st.cache_data(show_spinner=False)
def img_to_base64_raw(path):
    """Legge il file originale — USARE SOLO per PNG con trasparenza (logo)."""
    if path and Path(path).exists():
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            return base64.b64encode(f.read()).decode(), mime
    return None, None

@st.cache_data(show_spinner=False)
def img_to_base64(path, max_width=800, quality=75):
    """
    Versione COMPRESSA — default per tutte le foto JPG.
    Redimensiona a max_width e comprime come JPEG quality=75.
    """
    if not path or not Path(path).exists():
        return None, None
    if not HAS_PIL:
        return img_to_base64_raw(path)
    try:
        img = PILImage.open(path)
        # Se ha trasparenza, passa al raw
        if img.mode in ("RGBA", "LA", "P"):
            return img_to_base64_raw(path)
        img = img.convert("RGB")
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, PILImage.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return base64.b64encode(buf.getvalue()).decode(), "image/jpeg"
    except Exception:
        return img_to_base64_raw(path)

# ============================
# CARICAMENTO IMMAGINI — solo l'essenziale upfront
# ============================
# Logo comune (piccolo, serve in sidebar)
logo_path = find_img("logo_comune.png", "logo_comune.jpg")

# Ponte sfondo — compresso aggressivo perché appare solo come texture a bassa opacità
ponte_path = find_img("piazza_nola_ponte.png", "piazza_nola_ponte.jpg", "Schermata_2026-04-18_alle_11_58_52.png")
ponte_b64, ponte_mime = img_to_base64(ponte_path, max_width=800, quality=60) if ponte_path else (None, None)

# Logo Peccioli Eyes — 3 versioni (PNG con trasparenza, usa raw)
eyes_logo_yellow_path = find_img("peccioli_eyes_logo_yellow.png")
eyes_logo_blue_path = find_img("peccioli_eyes_logo_blue.png")
eyes_logo_white_path = find_img("peccioli_eyes_logo_white.png")

eyes_logo_yellow_b64, eyes_logo_yellow_mime = img_to_base64_raw(eyes_logo_yellow_path)
eyes_logo_blue_b64, eyes_logo_blue_mime = img_to_base64_raw(eyes_logo_blue_path)
eyes_logo_white_b64, eyes_logo_white_mime = img_to_base64_raw(eyes_logo_white_path)

# Path gallery (non carichiamo base64 — useremo st.image)
gallery_items = [
    {"key": "artistica", "title": "Street art",
     "desc": "Murale che racconta la voce artistica e comunitaria di New Orleans.",
     "path": find_img("home_artistica.jpg")},
    {"key": "urbana", "title": "Atmosfera urbana",
     "desc": "Una composizione visiva che restituisce l'energia e i contrasti della città.",
     "path": find_img("home_urbana.jpeg", "home_urbana.jpg", "home_urbana.png")},
    {"key": "simbolica", "title": "La città e il fiume",
     "desc": "Veduta aerea di New Orleans affacciata sul Mississippi, con il ponte Crescent City Connection.",
     "path": find_img("home_simbolica.jpg", "home_simbolica.jpeg")},
    {"key": "sociale", "title": "Mardi Gras",
     "desc": "Un carro del Mardi Gras sfila tra la folla lungo le strade del French Quarter. Il carnevale di New Orleans è uno dei più spettacolari al mondo.",
     "path": find_img("Home_carnevale.jpg", "home_carnevale.jpg", "home_sociale.jpg")},
    {"key": "umana", "title": "Volti della città",
     "desc": "Un ritratto che racconta il lato umano e quotidiano di New Orleans, attraverso le persone che la vivono.",
     "path": find_img("home_umana.jpg")},
    {"key": "musicale", "title": "Jazz dal vivo",
     "desc": "Gruppo di artisti jazz in una serata nel French Quarter: la musica come anima pulsante della città.",
     "path": find_img("home_musicale.jpg")},
]

# Path esperti (base64 solo per contesti dove serve HTML inline)
@st.cache_data(show_spinner=False)
def get_expert_paths():
    return {
        "morelli": find_img("morelli.jpg", "morelli.png"),
        "gardner": find_img("gardner.jpg", "gardner.png"),
        "costa":   find_img("costa.jpg", "costa.png"),
    }

# ============================
# CSS UNICO — un solo blocco all'inizio
# ============================
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Lobster+Two:ital,wght@1,700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">

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
    padding-top: 44px !important;
    padding-bottom: 2rem;
}}

/* Nascondi elementi Streamlit */
#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stAppViewBlockContainer"] footer,
.viewerBadge_container__1QSob, .viewerBadge_link__qRIco,
#stDecoration, .streamlit-footer,
[data-testid="stBottom"], section[data-testid="stBottom"],
div[class*="StatusWidget"], div[class*="viewerBadge"],
button[title="View fullscreen"] {{ display: none !important; }}

[data-testid="stSidebar"] {{
    background: {BRAND_BLUE};
    border-right: 1px solid rgba(255,255,255,0.1);
}}
[data-testid="stSidebar"] * {{ color: white !important; }}

/* ── CARDS ── */
.card {{
    background: white; border-radius: 22px; padding: 1.1rem 1rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 8px 24px rgba(19,0,137,0.06); height: 100%;
}}
.card-title {{
    font-family: "Playfair Display", Georgia, serif;
    font-size: 1.05rem; font-weight: 800;
    color: var(--brand-blue); margin-bottom: 0.35rem;
}}
.note {{ color: #5b6472; font-size: 0.93rem; line-height: 1.6; }}

.legend-card {{
    background: white; border-radius: 18px; padding: 0.95rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 6px 16px rgba(19,0,137,0.05);
    margin-bottom: 0.75rem;
}}

.gallery-caption {{
    text-align: center; color: var(--brand-blue);
    font-size: 1rem; margin: 0.5rem 0 1.2rem; font-weight: 500;
}}

.footer-box {{
    text-align: center; color: #9aa3b0; font-size: 0.88rem;
    margin-top: 1.5rem; padding-top: 1rem;
    border-top: 1px solid rgba(19,0,137,0.08);
}}

/* Streamlit buttons */
.stButton>button {{
    background: {BRAND_BLUE} !important; color: white !important;
    border: none !important; font-weight: 600 !important;
    border-radius: 10px !important;
}}
.stButton>button:hover {{
    background: {BRAND_BLUE_DARK} !important; color: {BRAND_YELLOW} !important;
}}

/* ── MOBILE ── */
@media (max-width: 768px) {{
    .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
    button[kind="header"] {{ display: none !important; }}
    .main .block-container {{
        padding-bottom: 75px !important;
        padding-left: 1rem !important; padding-right: 1rem !important;
    }}
}}

/* ── TOPBAR ── */
.sticky-topbar {{
    position: fixed; top: 0; left: 0; right: 0;
    height: 44px; background: {BRAND_BLUE};
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 1.2rem; z-index: 999998;
    border-bottom: 2px solid {BRAND_YELLOW};
}}
.sticky-topbar-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.85rem; font-weight: 800; color: white;
    letter-spacing: 0.08em; text-transform: uppercase;
}}
.sticky-topbar-title em {{
    font-family: 'Lobster Two', cursive; font-style: italic;
    font-weight: 600; color: {BRAND_YELLOW};
    text-transform: none; letter-spacing: 0; margin-left: 0.3rem;
}}

/* ── BOTTOM NAV MOBILE ── */
.bottom-nav {{ display: none; }}
@media (max-width: 768px) {{
    .bottom-nav {{
        display: flex; position: fixed;
        bottom: 0; left: 0; right: 0; background: {BRAND_BLUE};
        border-top: 2px solid {BRAND_YELLOW};
        padding: 6px 2px calc(10px + env(safe-area-inset-bottom));
        z-index: 2147483647;
        justify-content: space-around; align-items: flex-end;
    }}
    .bn-item {{
        display:flex; flex-direction:column; align-items:center; gap:2px;
        text-decoration:none; flex:1; padding:2px 1px; cursor:pointer;
    }}
    .bn-icon {{ font-size:1.1rem; line-height:1; }}
    .bn-label {{ font-size:0.5rem; text-align:center; line-height:1.2; font-family:sans-serif; }}
}}

/* ── QUICK BUTTONS HOME ── */
.quick-grid {{
    display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin:0.8rem 0;
}}
.quick-btn {{
    display:block; text-align:left; text-decoration:none;
    background:white; color:{BRAND_BLUE}; border-radius:14px;
    padding:0.85rem 1rem; font-weight:700; font-size:0.88rem; line-height:1.3;
    border:1px solid rgba(19,0,137,0.12);
    box-shadow:0 2px 8px rgba(19,0,137,0.05);
    border-left: 3px solid {BRAND_YELLOW}; cursor:pointer;
}}
.quick-btn:hover {{ background:{BRAND_BLUE_LIGHT}; }}
.quick-btn-label {{
    font-size:0.68rem; color:{BRAND_BLUE}; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em;
    display:block; margin-bottom:0.15rem; opacity:0.7;
}}

/* ── HERO HOME ── */
.hero-full {{
    position: relative; overflow: hidden;
    background: {BRAND_BLUE};
    margin: -44px -1rem 1.4rem -1rem;
    padding: 4rem 2rem 3rem; text-align: center;
}}
@media (min-width: 769px) {{
    .hero-full {{
        margin: -44px -3rem 1.6rem -3rem;
        padding: 4.5rem 3rem 3.5rem;
    }}
}}
}}
.hero-eyebrow {{
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.22em;
    text-transform: uppercase; color: rgba(255,255,255,0.55);
    margin-bottom: 0.7rem;
}}
.hero-title-main {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.3rem, 7vw, 4rem); font-weight: 800;
    color: white; line-height: 0.95;
    letter-spacing: 0.02em; text-transform: uppercase;
}}
.hero-title-script {{
    font-family: 'Lobster Two', cursive; font-style: italic; font-weight: 700;
    font-size: clamp(1.5rem, 4.5vw, 2.6rem);
    color: {BRAND_YELLOW}; line-height: 1.1; margin-top: 0.2rem;
}}
.hero-year {{
    display:inline-block; margin-top: 1rem;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.3em;
    color: rgba(255,255,255,0.6); padding: 0.35rem 0.9rem;
    border: 1px solid rgba(255,222,89,0.5); border-radius: 999px;
}}

/* ── SECTION HEADER ── */
.sec-header-full {{
    position:relative; overflow:hidden;
    background:{BRAND_BLUE};
    margin:-3rem -1rem 1.6rem -1rem;
    padding:3.5rem 2rem 1.8rem;
}}
@media (min-width:769px) {{
    .sec-header-full {{
        margin:-3rem -3rem 1.6rem -3rem;
        padding:3.5rem 3rem 2rem;
    }}
}}

/* ── HOME BOTTOM GRID ── */
.home-bottom-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }}
@media (max-width:640px) {{ .home-bottom-grid {{ grid-template-columns:1fr; }} }}
.hb-card {{
    background:white; border-radius:20px; padding:1.1rem 1.3rem;
    border:1px solid rgba(19,0,137,0.1);
    box-shadow:0 4px 16px rgba(19,0,137,0.05);
}}
.hb-title {{
    font-family:'Playfair Display',Georgia,serif; font-size:1rem; font-weight:800;
    color:{BRAND_BLUE}; margin-bottom:0.25rem;
}}
.hb-sub {{ font-size:0.78rem; color:#9aa3b0; margin-bottom:0.7rem; }}
.news-link {{
    display:flex; align-items:center; padding:0.35rem 0;
    text-decoration:none; border-bottom:1px solid rgba(19,0,137,0.07);
}}
.news-link:last-child {{ border-bottom:none; }}
.news-link-dot {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; margin-right:0.5rem; }}
.news-link-text {{ font-size:0.8rem; font-weight:600; color:{BRAND_BLUE}; }}
</style>
""", unsafe_allow_html=True)

# ============================
# Dati
# ============================
luoghi_dati = [
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
    {"nome": "Lower Ninth Ward", "lat": 29.9214, "lon": -90.0310,
     "desc": "Il quartiere più colpito da Katrina nel 2005. Simbolo della resilienza e della lentezza della ricostruzione.",
     "colore": "#4a3fb8", "tema": "Resilienza"},
    {"nome": "Lake Pontchartrain", "lat": 30.0500, "lon": -90.1000,
     "desc": "Il lago ai cui argini fallirono le dighe durante Katrina, causando l'inondazione della città.",
     "colore": "#4a3fb8", "tema": "Resilienza"},
    {"nome": "Make It Right Houses", "lat": 29.9230, "lon": -90.0320,
     "desc": "Le case colorate costruite da Brad Pitt dopo Katrina per i residenti del Lower Ninth Ward.",
     "colore": "#4a3fb8", "tema": "Resilienza"},
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

# ============================
# NAVIGAZIONE — senza doppio rerun
# ============================
_pagine_valide = ["Home", "Temi del viaggio", "Briefing", "Approfondimenti", "Mappe", "Programma", "Documenti"]

# Se arriva un query param valido e diverso dal target corrente → aggiorna e via
_qp_page = st.query_params.get("page")
if _qp_page in _pagine_valide:
    if st.session_state.get("nav_target") != _qp_page:
        st.session_state.nav_target = _qp_page
    # Pulisce query param senza rerun esplicito — al prossimo giro sarà già pulito
    try:
        del st.query_params["page"]
    except KeyError:
        pass

if "nav_target" not in st.session_state:
    st.session_state.nav_target = "Home"

# ============================
# SIDEBAR
# ============================
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

    cur_index = _pagine_valide.index(st.session_state.nav_target) if st.session_state.nav_target in _pagine_valide else 0
    pagina_radio = st.radio(label="", options=_pagine_valide, label_visibility="collapsed", index=cur_index)
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

# ============================
# BOTTOM BAR MOBILE
# ============================
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
    "Home": "Home", "Briefing": "Briefing", "Temi": "Temi del viaggio",
    "Mappe": "Mappe", "Programma": "Programma",
    "Documenti": "Documenti", "Altro": "Approfondimenti",
}
active = st.session_state.get("nav_target", "Home")

bottom_items = ""
for icon, short in voci_nav:
    label = voci_map[short]
    is_active = (label == active)
    color = BRAND_YELLOW if is_active else "rgba(255,255,255,0.6)"
    weight = "700" if is_active else "400"
    page_param = label.replace(" ", "+")
    bottom_items += f'<a href="?page={page_param}" target="_top" class="bn-item"><span class="bn-icon">{icon}</span><span class="bn-label" style="color:{color};font-weight:{weight};">{short}</span></a>'

st.markdown(f'<div class="bottom-nav">{bottom_items}</div>', unsafe_allow_html=True)

# ============================
# HEADER (topbar + hero)
# ============================
eyes_tag_hero = f'<img src="data:{eyes_logo_white_mime};base64,{eyes_logo_white_b64}" style="height:90px;width:auto;object-fit:contain;margin-bottom:0.8rem;display:block;margin-left:auto;margin-right:auto;">' if eyes_logo_white_b64 else ""
eyes_tag_topbar = f'<img src="data:{eyes_logo_yellow_mime};base64,{eyes_logo_yellow_b64}" style="height:26px;width:auto;object-fit:contain;margin-right:0.5rem;vertical-align:middle;">' if eyes_logo_yellow_b64 else ""

if pagina == "Home":
    ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.08;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""
    st.markdown(f"""
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
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="sticky-topbar">
        <div class="sticky-topbar-title">{eyes_tag_topbar}PECCIOLI EYES<em>to New Orleans</em></div>
        <a href="?page=Home" target="_top" style="font-size:0.75rem;font-weight:700;color:{BRAND_YELLOW};text-decoration:none;">← Home</a>
    </div>
    <div style="height:0.8rem;"></div>
    """, unsafe_allow_html=True)

# ============================
# HOME
# ============================
if pagina == "Home":
    import streamlit.components.v1 as components

    expert_paths = get_expert_paths()
    _morelli_path = expert_paths["morelli"]
    # Comprimo AGGRESSIVAMENTE per il countdown: è solo una miniatura 44x44
    morelli_b64, morelli_mime = img_to_base64(_morelli_path, max_width=100, quality=75) if _morelli_path else (None, None)
    prossimo_foto = f'<img src="data:{morelli_mime};base64,{morelli_b64}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid {BRAND_YELLOW};flex-shrink:0;">' if morelli_b64 else f'<div style="width:44px;height:44px;border-radius:50%;background:{BRAND_YELLOW};flex-shrink:0;"></div>'

    countdown_html = ("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { overflow:hidden; background:transparent; }
    .cd-wrap { display:flex; gap:0.75rem; font-family:'Inter',sans-serif; height:110px; align-items:stretch; }
    .cd-main {
        flex:1.6; min-width:0; background:""" + BRAND_BLUE + """;
        border-radius:18px; padding:1rem 1.4rem; color:white;
        display:flex; flex-direction:column; justify-content:center; flex-shrink:0;
    }
    .cd-label { font-size:0.65rem; font-weight:700; letter-spacing:0.12em;
        text-transform:uppercase; color:""" + BRAND_YELLOW + """; margin-bottom:0.3rem; }
    .cd-num { font-size:1.65rem; font-weight:800; color:white; line-height:1.2; }
    .cd-box {
        flex:1; min-width:0; background:white; border-radius:18px;
        padding:0.85rem 1rem; border:1px solid rgba(19,0,137,0.1);
        box-shadow:0 4px 14px rgba(19,0,137,0.06);
        display:flex; flex-direction:column; justify-content:center; flex-shrink:0;
    }
    @media (max-width:600px) {
        html, body { overflow-x:auto; }
        .cd-wrap { overflow-x:auto; scroll-snap-type:x mandatory;
            -webkit-overflow-scrolling:touch; gap:0.6rem; height:100px; }
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
            <div style="font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:""" + BRAND_BLUE + """;margin-bottom:0.45rem;">&#128197; Prossimo incontro</div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                """ + prossimo_foto + """
                <div>
                    <div style="font-size:0.82rem;font-weight:700;color:""" + BRAND_BLUE + """;line-height:1.2;">Elia Morelli</div>
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
        el.innerHTML =
            "<span style='font-size:1.65rem;font-weight:800;'>" + d + "</span><span style='font-size:0.82rem;opacity:0.6;margin:0 0.3rem 0 0.15rem;'>g</span>" +
            "<span style='font-size:1.65rem;font-weight:800;'>" + h + "</span><span style='font-size:0.82rem;opacity:0.6;margin:0 0.3rem 0 0.15rem;'>h</span>" +
            "<span style='font-size:1.65rem;font-weight:800;'>" + m + "</span><span style='font-size:0.82rem;opacity:0.6;margin-left:0.15rem;'>min</span>";
    }
    tick();
    setInterval(tick, 30000);
    </script>
    """)
    components.html(countdown_html, height=120, scrolling=False)

    st.markdown(f"""
    <div class="quick-grid">
        <a href="?page=Programma" target="_top" class="quick-btn"><span class="quick-btn-label">🗓 Programma</span>Tappe e attività</a>
        <a href="?page=Briefing" target="_top" class="quick-btn"><span class="quick-btn-label">📅 Briefing</span>Gli esperti</a>
        <a href="?page=Mappe" target="_top" class="quick-btn"><span class="quick-btn-label">🗺 Mappe</span>I luoghi</a>
        <a href="?page=Documenti" target="_top" class="quick-btn"><span class="quick-btn-label">📂 Documenti</span>Moduli e scadenze</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:{BRAND_BLUE_LIGHT};border-radius:18px;padding:1.1rem 1.3rem;margin:0.8rem 0;border-left:4px solid {BRAND_YELLOW};">
        <p style="font-size:0.98rem;color:{BRAND_BLUE};line-height:1.65;margin:0;font-style:italic;">
            <strong style="font-style:normal;">Peccioli Eyes</strong> è uno sguardo che parte dal nostro piccolo territorio e si apre al mondo, mettendo al centro i giovani, la cultura e l'esperienza.
        </p>
    </div>
    <p style="font-size:1rem;color:#3a4a5c;line-height:1.7;margin-bottom:0.4rem;">
        Il portale ufficiale del progetto — 80 ragazzi, settembre 2026.
    </p>
    """, unsafe_allow_html=True)

    with st.expander("Scopri a cosa serve →"):
        st.markdown(f"""
        <p style="font-size:0.95rem;color:#3a4a5c;line-height:1.75;">
            Questo spazio è pensato per accompagnare i ragazzi <strong>prima, durante e dopo il viaggio</strong>.
            Qui troverete in tempo reale il <strong>programma aggiornato</strong> del viaggio con tutte le tappe e le attività,
            i <strong>documenti da compilare</strong> con le relative scadenze,
            i <strong>briefing con gli esperti</strong> per prepararsi culturalmente,
            e gli <strong>approfondimenti</strong> — libri, film, documentari — per arrivare a New Orleans
            con uno sguardo già orientato sui quattro temi del viaggio: musica, resilienza, società, identità.
        </p>
        """, unsafe_allow_html=True)

    st.markdown("## ")
    st.markdown(f"""
    <div class="home-bottom-grid" style="margin-bottom:1rem;">
        <div class="hb-card">
            <div class="hb-title">📹 Live da New Orleans</div>
            <div class="hb-sub">French Quarter · Bourbon Street · 24/7</div>
            <a href="https://www.earthcam.com/usa/louisiana/neworleans/bourbonstreet/"
               target="_blank" rel="noopener"
               style="display:inline-block;background:{BRAND_BLUE};color:white;padding:0.4rem 0.9rem;
                      border-radius:999px;font-size:0.78rem;font-weight:600;text-decoration:none;">
                🎥 Guarda →
            </a>
        </div>
        <div class="hb-card">
            <div class="hb-title">🗞 Notizie</div>
            <div class="hb-sub">Fonti locali di New Orleans</div>
            <a href="https://www.nola.com" target="_blank" rel="noopener" class="news-link">
                <div class="news-link-dot" style="background:{BRAND_YELLOW};"></div>
                <span class="news-link-text">The Times-Picayune</span>
            </a>
            <a href="https://www.wwno.org" target="_blank" rel="noopener" class="news-link">
                <div class="news-link-dot" style="background:{BRAND_BLUE};"></div>
                <span class="news-link-text">WWNO Public Radio</span>
            </a>
            <a href="https://thelensnola.org" target="_blank" rel="noopener" class="news-link">
                <div class="news-link-dot" style="background:#4a3fb8;"></div>
                <span class="news-link-text">The Lens NOLA</span>
            </a>
        </div>
    </div>

    <div style="border-radius:20px;overflow:hidden;box-shadow:0 4px 16px rgba(19,0,137,0.1);">
        <iframe style="border-radius:20px;display:block;"
            src="https://open.spotify.com/embed/playlist/0iMiZcvIy26MqHQln5kkrI?utm_source=generator&theme=0"
            width="100%" height="152" frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy">
        </iframe>
    </div>
    """, unsafe_allow_html=True)

# ============================
# BRIEFING — foto esperti via st.image nelle card
# ============================
elif pagina == "Briefing":
    section_header("02", "Prima del viaggio", "Incontri propedeutici al viaggio",
                   "Tre serate con tre esperti per arrivare a New Orleans con strumenti culturali già solidi. Non lezioni — conversazioni aperte su storia, geopolitica e società americana. Clicca su un relatore per scoprire chi è.")

    expert_paths = get_expert_paths()

    briefing_full = [
        {
            "data": "7 maggio", "ora": "ore 21",
            "titolo": "Elia Morelli",
            "ruolo": "Ricercatore in storia moderna · Università di Pisa",
            "bio": "Ricercatore in storia moderna all'Università di Pisa. Come analista geopolitico, scrive per Domino, rivista edita da Enrico Mentana. Membro della Società Italiana per la Storia dell'Età Moderna, della Società Italiana per lo Studio della Storia Contemporanea e della Renaissance Society of America.",
            "tema": "Storia culturale, politico-economica e geopolitica di New Orleans e della Louisiana.",
            "foto": expert_paths["morelli"], "emoji": "🏛", "colore": BRAND_YELLOW,
        },
        {
            "data": "21 maggio", "ora": "ore 21",
            "titolo": "Anthony Gardner",
            "ruolo": "Ex ambasciatore USA all'UE · Consiglio di sicurezza nazionale",
            "bio": "Ex ambasciatore degli Stati Uniti presso l'Unione Europea dal 2014 al 2017 su nomina del presidente Obama. Ha lavorato per oltre vent'anni sulle relazioni tra USA ed Europa, su temi come i negoziati commerciali transatlantici, la privacy dei dati, l'economia digitale e la sicurezza energetica.",
            "tema": "Sguardo istituzionale e geopolitico: il ruolo di New Orleans e il rapporto tra USA ed Europa.",
            "foto": expert_paths["gardner"], "emoji": "🌐", "colore": BRAND_BLUE,
        },
        {
            "data": "18 giugno", "ora": "ore 21",
            "titolo": "Francesco Costa",
            "ruolo": "Giornalista · Direttore de Il Post",
            "bio": "Direttore responsabile de Il Post. Tra i principali divulgatori italiani sulla società e politica americana, autore di libri e progetti dedicati agli Stati Uniti. Dal 2021 al 2025 ha condotto per il Post il podcast giornaliero Morning, una rassegna stampa commentata che è stata definita \"il primo vero podcast daily italiano\".",
            "tema": "Punto di vista sociale, narrativo e attuale sugli Stati Uniti: leggere l'America oltre gli stereotipi.",
            "foto": expert_paths["costa"], "emoji": "📰", "colore": "#e6b800",
        },
    ]

   # CSS custom per foto rotonda centrata nelle card briefing
    st.markdown(f"""
    <style>
    /* Foto esperti: cerchio perfetto + centratura */
    div[data-testid="stImage"] {{
        display: flex !important;
        justify-content: center !important;
    }}
    div[data-testid="stImage"] img {{
        border-radius: 50%;
        width: 90px !important;
        height: 90px !important;
        object-fit: cover;
        border: 3px solid {BRAND_BLUE};
        display: block;
    }}
    /* Nel dialog popup la foto è più grande e rettangolare (non cerchio) */
    div[data-testid="stDialog"] div[data-testid="stImage"] img {{
        border-radius: 16px;
        width: 100% !important;
        height: auto !important;
        max-height: 260px;
        object-fit: cover;
        border: none;
    }}
    </style>
    """, unsafe_allow_html=True)

    @st.dialog(" ")
    def mostra_relatore(idx):
        b = briefing_full[idx]
        if b["foto"]:
            col_foto, col_info = st.columns([1, 2])
            with col_foto:
                st.image(b["foto"], use_container_width=True)
            with col_info:
                st.markdown(f"""
                <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:{b['colore']};">{b['data']} · {b['ora']}</div>
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.4rem;font-weight:800;color:{BRAND_BLUE};margin:0.2rem 0 0.3rem;">{b['titolo']}</div>
                <div style="font-size:0.85rem;color:#5b6472;margin-bottom:0.8rem;">{b['ruolo']}</div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:{BRAND_BLUE_LIGHT};border-radius:14px;padding:1rem 1.1rem;margin:0.5rem 0;">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{BRAND_BLUE};margin-bottom:0.4rem;">Chi è</div>
            <div style="font-size:0.92rem;color:#3a4a5c;line-height:1.65;">{b['bio']}</div>
        </div>
        <div style="background:{BRAND_YELLOW_LIGHT};border-radius:14px;padding:1rem 1.1rem;margin-top:0.6rem;border-left:3px solid {BRAND_YELLOW};">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{BRAND_BLUE};margin-bottom:0.4rem;">Di cosa parlerà</div>
            <div style="font-size:0.92rem;color:#3a4a5c;line-height:1.65;">{b['tema']}</div>
        </div>
        """, unsafe_allow_html=True)

    if "dialog_idx" not in st.session_state:
        st.session_state.dialog_idx = None
    if st.session_state.dialog_idx is not None:
        mostra_relatore(st.session_state.dialog_idx)
        st.session_state.dialog_idx = None

    c1, c2, c3 = st.columns(3)
    for i, (col, b) in enumerate(zip([c1, c2, c3], briefing_full)):
        with col:
            # Wrapper centrato per la foto
            if b["foto"]:
                # Tre sub-colonne per centrare st.image (trucco affidabile)
                sp1, sp_img, sp2 = st.columns([1, 2, 1])
                with sp_img:
                    st.image(b["foto"], use_container_width=True)
            else:
                st.markdown(f'<div style="width:90px;height:90px;border-radius:50%;background:{b["colore"]};margin:0 auto 0.8rem;display:flex;align-items:center;justify-content:center;font-size:2rem;color:white;">{b["emoji"]}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="text-align:center;margin-top:0.2rem;">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{BRAND_BLUE};margin-bottom:0.2rem;opacity:0.7;">{b['data']} · {b['ora']}</div>
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:800;color:{BRAND_BLUE};line-height:1.2;margin-bottom:0.3rem;">{b['titolo']}</div>
                <div style="font-size:0.78rem;color:#5b6472;line-height:1.4;margin-bottom:0.6rem;">{b['ruolo']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Scopri {b['titolo'].split()[0]}", key=f"dialog_{i}", use_container_width=True):
                st.session_state.dialog_idx = i
                st.rerun()

# ============================
# APPROFONDIMENTI
# ============================
elif pagina == "Approfondimenti":
    section_header("03", "Per prepararsi", "Approfondimenti",
                   "Libri, film, documentari e risorse online per arrivare a New Orleans con uno sguardo già allenato.")

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Libri", "🎬 Film e TV", "🎞 Documentari", "🌐 Risorse"])

    with tab1:
        st.markdown("## ")
        col1, col2 = st.columns(2)
        libri = [
            {"titolo": "Una banda di idioti", "autore": "John Kennedy Toole", "anno": "1980 · Pulitzer",
             "desc": "Capolavoro ambientato nella New Orleans degli anni '60. Satira geniale e irresistibile — il modo più divertente per entrare nell'anima della città.",
             "link": "https://it.wikipedia.org/wiki/Una_banda_di_idioti", "colore": BRAND_YELLOW},
            {"titolo": "Blues Highway", "autore": "Rob Siebert", "anno": "Reportage narrativo",
             "desc": "Viaggio da Chicago a New Orleans sulle tracce delle origini della musica americana: blues, jazz, gospel. Per capire il legame tra musica e territorio.",
             "link": "https://marcosymarcos.com/libri/gli-alianti/blues-highway/", "colore": BRAND_BLUE},
            {"titolo": "The Moviegoer", "autore": "Walker Percy", "anno": "1961 · National Book Award",
             "desc": "Romanzo ambientato a New Orleans, vincitore del National Book Award. Racconta l'alienazione e la ricerca di senso di un giovane creolo nella città del Mardi Gras.",
             "link": "https://it.wikipedia.org/wiki/Walker_Percy", "colore": "#e6b800"},
            {"titolo": "Zeitoun", "autore": "Dave Eggers", "anno": "2009 · Non fiction",
             "desc": "La storia vera di un siriano-americano rimasto a New Orleans durante Katrina. Un racconto potente su resilienza, razzismo e fallimento istituzionale dopo la catastrofe.",
             "link": "https://it.wikipedia.org/wiki/Zeitoun_(libro)", "colore": "#4a3fb8"},
        ]
        for i, libro in enumerate(libri):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div style="background:white;border-radius:20px;padding:1.2rem 1.3rem;
                     border-top:4px solid {libro['colore']};
                     box-shadow:0 4px 16px rgba(19,0,137,0.06);margin-bottom:1rem;">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                         color:{BRAND_BLUE};margin-bottom:0.3rem;opacity:0.7;">{libro['anno']}</div>
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.05rem;font-weight:800;
                         color:{BRAND_BLUE};line-height:1.2;margin-bottom:0.15rem;">{libro['titolo']}</div>
                    <div style="font-size:0.8rem;color:#9aa3b0;margin-bottom:0.6rem;">{libro['autore']}</div>
                    <div style="font-size:0.88rem;color:#3a4a5c;line-height:1.6;margin-bottom:0.8rem;">{libro['desc']}</div>
                    <a href="{libro['link']}" target="_blank" rel="noopener"
                       style="font-size:0.78rem;font-weight:700;color:{BRAND_BLUE};text-decoration:none;">
                        Approfondisci →
                    </a>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("## ")
        film = [
            {"titolo": "Un tram che si chiama Desiderio", "anno": "1951 · Elia Kazan",
             "desc": "Con Marlon Brando e Vivien Leigh. Classico assoluto girato nella New Orleans reale.",
             "link": "https://www.imdb.com/title/tt0044081/", "colore": BRAND_YELLOW},
            {"titolo": "Intervista col vampiro", "anno": "1994 · Neil Jordan",
             "desc": "Tom Cruise, Brad Pitt, Kirsten Dunst. Cattura l'atmosfera gotica e decadente della Louisiana.",
             "link": "https://www.imdb.com/title/tt0110632/", "colore": BRAND_BLUE},
            {"titolo": "Il curioso caso di Benjamin Button", "anno": "2008 · David Fincher",
             "desc": "New Orleans dal dopoguerra a Katrina come sfondo per una storia sull'identità e la memoria.",
             "link": "https://www.imdb.com/title/tt0421715/", "colore": "#e6b800"},
            {"titolo": "Treme", "anno": "2010–2013 · HBO",
             "desc": "La serie più importante su New Orleans dopo Katrina. Emmy Award. Da vedere assolutamente.",
             "link": "https://www.imdb.com/title/tt1279972/", "colore": "#4a3fb8"},
            {"titolo": "Easy Rider", "anno": "1969 · Dennis Hopper",
             "desc": "Icona della controcultura. Il Mardi Gras di New Orleans in una delle scene più celebri del cinema.",
             "link": "https://www.imdb.com/title/tt0064276/", "colore": BRAND_YELLOW},
        ]
        for f in film:
            st.markdown(f"""
            <div style="background:white;border-radius:18px;padding:1rem 1.2rem;margin-bottom:0.7rem;
                 display:flex;align-items:center;gap:1rem;
                 border-left:4px solid {f['colore']};
                 box-shadow:0 3px 12px rgba(19,0,137,0.05);">
                <div style="flex:1;">
                    <div style="font-size:0.7rem;color:{BRAND_BLUE};font-weight:700;text-transform:uppercase;letter-spacing:0.08em;opacity:0.7;">{f['anno']}</div>
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:1rem;font-weight:800;color:{BRAND_BLUE};">{f['titolo']}</div>
                    <div style="font-size:0.85rem;color:#5b6472;margin-top:0.2rem;">{f['desc']}</div>
                </div>
                <a href="{f['link']}" target="_blank" rel="noopener"
                   style="flex-shrink:0;background:{BRAND_BLUE};color:white;padding:0.35rem 0.8rem;
                          border-radius:999px;font-size:0.75rem;font-weight:600;text-decoration:none;white-space:nowrap;">
                    IMDb →
                </a>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("## ")
        docs = [
            {"titolo": "Katrina: Come Hell and High Water", "anno": "Netflix · 2025 · Spike Lee",
             "desc": "Tre episodi, vent'anni dopo: i sopravvissuti raccontano la catastrofe e i fallimenti istituzionali.",
             "link": "https://www.netflix.com/title/81676595", "label": "Netflix →", "colore": BRAND_BLUE},
            {"titolo": "Hurricane Katrina: Race Against Time", "anno": "National Geographic · 2025",
             "desc": "Cinque episodi. Critics Choice Award 2025. Ricostruzione minuto per minuto con footage inedito.",
             "link": "https://www.imdb.com/title/tt37458027/", "label": "IMDb →", "colore": "#4a3fb8"},
            {"titolo": "When the Levees Broke", "anno": "HBO · 2006 · Spike Lee",
             "desc": "Quattro atti, il documentario che ha raccontato al mondo la devastazione di Katrina. Pietra miliare.",
             "link": "https://www.imdb.com/title/tt0783105/", "label": "IMDb →", "colore": "#e6b800"},
        ]
        for d in docs:
            st.markdown(f"""
            <div style="background:white;border-radius:20px;padding:1.3rem 1.4rem;margin-bottom:0.8rem;
                 border-top:4px solid {d['colore']};box-shadow:0 4px 16px rgba(19,0,137,0.06);">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;">
                    <div>
                        <div style="font-size:0.7rem;color:{BRAND_BLUE};font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;opacity:0.7;">{d['anno']}</div>
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:800;color:{BRAND_BLUE};margin-bottom:0.4rem;">{d['titolo']}</div>
                        <div style="font-size:0.88rem;color:#5b6472;line-height:1.6;">{d['desc']}</div>
                    </div>
                    <a href="{d['link']}" target="_blank" rel="noopener"
                       style="flex-shrink:0;background:{d['colore']};color:{BRAND_BLUE};padding:0.4rem 0.9rem;
                              border-radius:999px;font-size:0.78rem;font-weight:700;text-decoration:none;white-space:nowrap;align-self:center;">
                        {d['label']}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("## ")
        risorse = [
            {"titolo": "New Orleans — Wikipedia italiana",
             "desc": "Panoramica su storia, cultura, musica e geografia. Ottimo punto di partenza.",
             "link": "https://it.wikipedia.org/wiki/New_Orleans", "colore": BRAND_BLUE},
            {"titolo": "The Times-Picayune · NOLA.com",
             "desc": "Il principale quotidiano di New Orleans per seguire l'attualità della città.",
             "link": "https://www.nola.com", "colore": BRAND_YELLOW},
            {"titolo": "Da Costa a Costa — Francesco Costa",
             "desc": "Newsletter e YouTube dell'esperto di America che incontreremo al briefing.",
             "link": "https://www.ilpost.it/costa/", "colore": "#4a3fb8"},
        ]
        for r in risorse:
            st.markdown(f"""
            <a href="{r['link']}" target="_blank" rel="noopener" style="text-decoration:none;">
                <div style="background:white;border-radius:18px;padding:1.1rem 1.3rem;margin-bottom:0.7rem;
                     display:flex;align-items:center;gap:1rem;
                     border:1px solid rgba(19,0,137,0.1);
                     box-shadow:0 3px 12px rgba(19,0,137,0.05);">
                    <div style="width:6px;height:40px;border-radius:3px;background:{r['colore']};flex-shrink:0;"></div>
                    <div>
                        <div style="font-size:0.95rem;font-weight:800;color:{BRAND_BLUE};">{r['titolo']}</div>
                        <div style="font-size:0.82rem;color:#5b6472;margin-top:0.15rem;">{r['desc']}</div>
                    </div>
                    <div style="margin-left:auto;color:{BRAND_BLUE};font-size:1.1rem;flex-shrink:0;">→</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

# ============================
# TEMI DEL VIAGGIO — gallery con st.image
# ============================
elif pagina == "Temi del viaggio":
    section_header("01", "Come guardare la città", "Temi del viaggio",
                   "Quattro chiavi di lettura per osservare New Orleans durante il viaggio. Non categorie separate, ma prospettive da tenere sempre attive.")

    st.markdown('<p style="font-size:1rem;color:#3a4a5c;line-height:1.7;margin-bottom:1.6rem;"></p>', unsafe_allow_html=True)

    svg_musica = f"""
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.14;position:absolute;bottom:0;right:0;">
        <circle cx="160" cy="60" r="50" fill="{BRAND_BLUE}"/>
        <circle cx="120" cy="90" r="30" fill="{BRAND_BLUE}"/>
        <path d="M20 60 Q50 30 80 60 Q110 90 140 60" stroke="{BRAND_BLUE}" stroke-width="4" fill="none"/>
        <path d="M10 75 Q45 40 80 75 Q115 110 150 75" stroke="{BRAND_BLUE}" stroke-width="3" fill="none"/>
        <path d="M30 45 Q60 20 90 45 Q120 70 150 45" stroke="{BRAND_BLUE}" stroke-width="2" fill="none"/>
        <circle cx="170" cy="35" r="8" fill="{BRAND_BLUE}"/>
        <line x1="178" y1="35" x2="178" y2="5" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="178" y1="5" x2="195" y2="10" stroke="{BRAND_BLUE}" stroke-width="3"/>
    </svg>"""
    svg_resilienza = f"""
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.14;position:absolute;bottom:0;right:0;">
        <path d="M0 90 Q25 70 50 90 Q75 110 100 90 Q125 70 150 90 Q175 110 200 90 L200 120 L0 120 Z" fill="{BRAND_BLUE}"/>
        <path d="M0 75 Q25 55 50 75 Q75 95 100 75 Q125 55 150 75 Q175 95 200 75 L200 120 L0 120 Z" fill="{BRAND_BLUE}" opacity="0.6"/>
        <polygon points="100,15 115,55 85,55" fill="{BRAND_YELLOW}"/>
        <rect x="92" y="55" width="16" height="30" fill="{BRAND_YELLOW}"/>
    </svg>"""
    svg_societa = f"""
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.14;position:absolute;bottom:0;right:0;">
        <circle cx="50" cy="40" r="14" fill="{BRAND_BLUE}"/>
        <rect x="38" y="54" width="24" height="35" rx="4" fill="{BRAND_BLUE}"/>
        <circle cx="100" cy="35" r="16" fill="{BRAND_YELLOW}"/>
        <rect x="86" y="51" width="28" height="40" rx="4" fill="{BRAND_YELLOW}"/>
        <circle cx="150" cy="40" r="14" fill="{BRAND_BLUE}"/>
        <rect x="138" y="54" width="24" height="35" rx="4" fill="{BRAND_BLUE}"/>
        <line x1="64" y1="60" x2="86" y2="58" stroke="{BRAND_BLUE}" stroke-width="2" stroke-dasharray="4"/>
        <line x1="114" y1="60" x2="138" y2="60" stroke="{BRAND_BLUE}" stroke-width="2" stroke-dasharray="4"/>
    </svg>"""
    svg_storia = f"""
    <svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;opacity:0.14;position:absolute;bottom:0;right:0;">
        <path d="M60 110 L60 50 Q60 20 90 20 Q120 20 120 50 L120 110" stroke="{BRAND_BLUE}" stroke-width="5" fill="none"/>
        <line x1="45" y1="65" x2="135" y2="65" stroke="{BRAND_BLUE}" stroke-width="4"/>
        <line x1="48" y1="65" x2="48" y2="80" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="70" y1="65" x2="70" y2="80" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="90" y1="65" x2="90" y2="80" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="110" y1="65" x2="110" y2="80" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="132" y1="65" x2="132" y2="80" stroke="{BRAND_BLUE}" stroke-width="3"/>
        <line x1="43" y1="80" x2="137" y2="80" stroke="{BRAND_BLUE}" stroke-width="4"/>
        <circle cx="155" cy="30" r="5" fill="{BRAND_YELLOW}"/>
        <circle cx="170" cy="50" r="4" fill="{BRAND_YELLOW}"/>
        <circle cx="160" cy="70" r="6" fill="{BRAND_YELLOW}"/>
        <circle cx="180" cy="25" r="3" fill="{BRAND_YELLOW}"/>
    </svg>"""

    temi = [
        {"titolo": "Musica", "label": "JAZZ", "colore": BRAND_BLUE, "bg": BRAND_YELLOW_LIGHT,
         "sottotitolo": "Jazz, blues e il ritmo della città",
         "domanda": "Perché il jazz è nato proprio qui, e non altrove?",
         "desc": "New Orleans è la culla del jazz e del blues. La musica non è intrattenimento: è linguaggio sociale, memoria collettiva, forma di resistenza. Dalle second line nei funerali di strada a Frenchmen Street la sera, la città vive attraverso il suono.",
         "luoghi": "Frenchmen Street · Congo Square · Louis Armstrong Park", "svg": svg_musica},
        {"titolo": "Resilienza", "label": "KATRINA", "colore": BRAND_BLUE, "bg": BRAND_BLUE_LIGHT,
         "sottotitolo": "Katrina, ricostruzione e cambiamento climatico",
         "domanda": "Come si ricostruisce una città dopo che l'acqua se la porta via?",
         "desc": "Il 2005 ha messo a nudo le fragilità strutturali della città: infrastrutture, disuguaglianze razziali, risposta istituzionale. Vent'anni dopo, la città è ancora in cammino. Il Lower Ninth Ward è il luogo dove questo tema si tocca con mano.",
         "luoghi": "Lower Ninth Ward · Argini del Mississippi · Lakeview", "svg": svg_resilienza},
        {"titolo": "Società", "label": "PEOPLE", "colore": BRAND_BLUE, "bg": BRAND_YELLOW_LIGHT,
         "sottotitolo": "Diversità culturale, questioni razziali, umanità",
         "domanda": "Cosa succede quando culture lontanissime vivono nello stesso isolato da tre secoli?",
         "desc": "New Orleans è una delle città più multiculturali e diseguali degli Stati Uniti. L'eredità della schiavitù, la comunità creola, le contraddizioni tra turismo e vita reale: osservare la città attraverso le persone che la abitano è il modo più onesto di capirla.",
         "luoghi": "Congo Square · Tremé · Garden District", "svg": svg_societa},
        {"titolo": "Identità e storia", "label": "NOLA", "colore": BRAND_BLUE, "bg": BRAND_BLUE_LIGHT,
         "sottotitolo": "Radici coloniali, voodoo, Mardi Gras, French Quarter",
         "domanda": "Perché New Orleans non somiglia a nessun'altra città americana?",
         "desc": "Fondata dai francesi, ceduta agli spagnoli, acquistata dagli Stati Uniti. Questa stratificazione di culture — europea, africana, caraibica — ha prodotto un'identità unica: il French Quarter, il voodoo, il Mardi Gras, la cucina creola.",
         "luoghi": "French Quarter · St. Louis Cemetery · Jackson Square", "svg": svg_storia},
    ]

    col1, col2 = st.columns(2)
    for i, tema in enumerate(temi):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(f"{tema['titolo']} · {tema['sottotitolo']}", expanded=True):
                st.markdown(f"""
                <div style="position:relative;background:{tema['bg']};border-radius:16px;
                     padding:1.2rem 1rem 1rem;
                     border:1px solid {tema['colore']}22;
                     overflow:hidden;">
                    {tema['svg']}
                    <div style="position:absolute;top:-10px;right:12px;
                         font-family:'Playfair Display',Georgia,serif;
                         font-size:4.5rem;font-weight:800;
                         color:{tema['colore']};opacity:0.08;
                         line-height:1;user-select:none;pointer-events:none;">
                        {tema['label']}
                    </div>
                    <div style="position:relative;z-index:1;">
                        <div style="font-family:'Lobster Two',cursive;font-style:italic;
                             font-size:1rem;color:{tema['colore']};
                             font-weight:700;margin-bottom:0.7rem;line-height:1.4;">
                            &ldquo;{tema['domanda']}&rdquo;
                        </div>
                        <div style="font-size:0.87rem;color:#3a4a5c;line-height:1.65;margin-bottom:0.8rem;">
                            {tema['desc']}
                        </div>
                        <div style="font-size:0.75rem;font-weight:700;color:{tema['colore']};
                             border-top:1px solid {tema['colore']}30;padding-top:0.6rem;">
                            &#128205; {tema['luoghi']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Gallery con st.image (il browser cacha le immagini per URL)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1rem;margin:2rem 0 0.8rem;">
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(19,0,137,0.2));"></div>
        <div style="text-align:center;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:{BRAND_BLUE};margin-bottom:0.2rem;opacity:0.7;">New Orleans vista da vicino</div>
            <div style="font-family:'Lobster Two',cursive;font-style:italic;font-size:1.4rem;font-weight:700;color:{BRAND_BLUE};line-height:1;">Sguardi sulla città</div>
        </div>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(19,0,137,0.2),transparent);"></div>
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
            color = BRAND_YELLOW if i == idx else "rgba(19,0,137,0.2)"
            dots_html += f'<div style="width:7px;height:7px;border-radius:50%;background:{color};"></div>'
        dots_html += '</div>'
        st.markdown(dots_html, unsafe_allow_html=True)

    galleria()

# ============================
# MAPPE
# ============================
elif pagina == "Mappe":
    section_header("04", "Orientarsi nella città", "Mappa di New Orleans",
                   "I luoghi simbolici del viaggio, organizzati per tema. Clicca sui marker per leggere la descrizione di ogni posto.")

    @st.fragment
    def mostra_mappa():
        m = folium.Map(location=[29.950, -90.065], zoom_start=13, tiles="CartoDB positron")
        for luogo in luoghi_dati:
            folium.CircleMarker(
                location=[luogo["lat"], luogo["lon"]], radius=11,
                color=luogo["colore"], fill=True, fill_color=luogo["colore"], fill_opacity=0.88,
                popup=folium.Popup(
                    f"<b style='font-size:14px;color:{BRAND_BLUE}'>{luogo['nome']}</b><br>"
                    f"<span style='font-size:12px;color:#444'>{luogo['desc']}</span>",
                    max_width=250
                ),
                tooltip=folium.Tooltip(luogo["nome"], sticky=True)
            ).add_to(m)
        st_folium(m, width=None, height=480, use_container_width=True)

    mostra_mappa()

    st.markdown("## ")
    st.markdown(f"""
    <div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1.2rem;">
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(19,0,137,0.12);font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
            <div style="width:12px;height:12px;border-radius:50%;background:{BRAND_BLUE};flex-shrink:0;"></div> Identità e storia
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(19,0,137,0.12);font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
            <div style="width:12px;height:12px;border-radius:50%;background:#e6b800;flex-shrink:0;"></div> Musica
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(19,0,137,0.12);font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
            <div style="width:12px;height:12px;border-radius:50%;background:#4a3fb8;flex-shrink:0;"></div> Resilienza
        </div>
        <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;border:1px solid rgba(19,0,137,0.12);font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
            <div style="width:12px;height:12px;border-radius:50%;background:#b8860b;flex-shrink:0;"></div> Società
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, luogo in enumerate(luoghi_dati):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="legend-card" style="border-left:4px solid {luogo['colore']};margin-bottom:0.6rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:0.95rem;font-weight:800;color:{BRAND_BLUE};">{luogo['nome']}</div>
                </div>
                <div style="font-size:0.72rem;font-weight:700;color:{luogo['colore']};margin-bottom:0.2rem;">{luogo['tema']}</div>
                <div class="note">{luogo['desc']}</div>
            </div>""", unsafe_allow_html=True)

# ============================
# PROGRAMMA
# ============================
elif pagina == "Programma":
    section_header("05", "Il viaggio", "Programma",
                   "Il programma dettagliato è ancora in costruzione. Questa sezione verrà aggiornata con tutte le tappe non appena il percorso sarà definito.")

    st.markdown(f"""
    <div style="background:{BRAND_YELLOW_LIGHT};border:2px dashed {BRAND_YELLOW};border-radius:24px;padding:2.5rem 2rem;text-align:center;max-width:580px;margin:2rem auto;">
        <div style="font-size:2.5rem;margin-bottom:0.6rem;">🗓</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.5rem;font-weight:800;color:{BRAND_BLUE};margin-bottom:0.6rem;">Programma in definizione</div>
        <div style="font-size:0.97rem;color:#5b6472;line-height:1.75;">
            Il programma dettagliato del viaggio è ancora in fase di costruzione.<br>
            Questa sezione verrà aggiornata con tutte le tappe, gli appuntamenti e le attività non appena il percorso sarà definito.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================
# DOCUMENTI
# ============================
elif pagina == "Documenti":
    section_header("06", "Prima della partenza", "Materiali e documenti",
                   "Documenti da consultare, compilare e consegnare in vista del viaggio.")

    st.markdown(f"""
    <div style="background:{BRAND_BLUE_LIGHT};border-left:4px solid {BRAND_YELLOW};border-radius:0 12px 12px 0;
         padding:0.8rem 1.2rem;margin-bottom:1.4rem;font-size:0.88rem;color:{BRAND_BLUE};font-weight:500;">
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
        colore_stato = BRAND_BLUE if completato else "#9aa3b0"
        stato_testo = "✅ Disponibile" if completato else "⏳ In arrivo"
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:0.9rem 1.1rem;margin-bottom:0.6rem;
             display:flex;align-items:center;gap:1rem;
             border:1px solid rgba(19,0,137,0.1);box-shadow:0 2px 8px rgba(19,0,137,0.04);">
            <div style="font-size:1.5rem;flex-shrink:0;">{icona}</div>
            <div style="flex:1;">
                <div style="font-weight:800;color:{BRAND_BLUE};font-size:0.92rem;margin-bottom:0.1rem;">{titolo}</div>
                <div style="font-size:0.8rem;color:#5b6472;">{desc}</div>
            </div>
            <div style="flex-shrink:0;">
                <div style="font-size:0.72rem;font-weight:700;color:{colore_stato};">{stato_testo}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div class='footer-box'>Peccioli Eyes to New Orleans · 2026 · Portale ragazzi</div>", unsafe_allow_html=True)
