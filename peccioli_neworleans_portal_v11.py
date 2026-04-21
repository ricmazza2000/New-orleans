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

# Palette sezioni — tutto nel range blu/giallo brand
SEC_TEMI = "#fff7c2"         # giallo chiaro
SEC_BRIEFING = "#1a2f6c"     # blu navy profondo
SEC_MAPPA = "#0a5a7a"        # blu petrolio
SEC_PROGRAMMA = "#2a3f7a"    # blu medio (tenue ma scuro)
SEC_DOCUMENTI = "#f0eeff"    # lavanda chiara (blu chiarissimo)
SEC_ALTRO = "#fff3d1"        # giallo crema (leggermente più caldo di Temi)

# ============================
# UTILITY
# ============================
@st.cache_data(show_spinner=False)
def find_image(possible_names_tuple):
    for name in possible_names_tuple:
        p = BASE_DIR / name
        if p.exists():
            return str(p)
    return None

def find_img(*names):
    return find_image(tuple(names))

@st.cache_data(show_spinner=False)
def img_to_base64_raw(path):
    if path and Path(path).exists():
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            return base64.b64encode(f.read()).decode(), mime
    return None, None

@st.cache_data(show_spinner=False)
def img_to_base64(path, max_width=800, quality=75):
    if not path or not Path(path).exists():
        return None, None
    if not HAS_PIL:
        return img_to_base64_raw(path)
    try:
        img = PILImage.open(path)
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
# CARICAMENTO IMMAGINI
# ============================
logo_path = find_img("logo_comune.png", "logo_comune.jpg")
ponte_path = find_img("piazza_nola_ponte.png", "piazza_nola_ponte.jpg", "Schermata_2026-04-18_alle_11_58_52.png")
ponte_b64, ponte_mime = img_to_base64(ponte_path, max_width=800, quality=60) if ponte_path else (None, None)

eyes_logo_yellow_path = find_img("peccioli_eyes_logo_yellow.png")
eyes_logo_white_path = find_img("peccioli_eyes_logo_white.png")

eyes_logo_yellow_b64, eyes_logo_yellow_mime = img_to_base64_raw(eyes_logo_yellow_path)
eyes_logo_white_b64, eyes_logo_white_mime = img_to_base64_raw(eyes_logo_white_path)

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

@st.cache_data(show_spinner=False)
def get_expert_paths():
    return {
        "morelli": find_img("morelli.jpg", "morelli.png"),
        "gardner": find_img("gardner.jpg", "gardner.png"),
        "costa":   find_img("costa.jpg", "costa.png"),
    }

# ============================
# CSS
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

html, body {{
    scroll-behavior: smooth;
    scroll-padding-top: 50px;
    margin: 0 !important;
    padding: 0 !important;
    background: {BRAND_BLUE} !important;
}}
.stApp {{
    background: {BRAND_BLUE} !important;
}}

html, body, [class*="css"] {{
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

/* FIX gap mobile: impedisce che il margine negativo dell'hero "trapeli" fuori dal container */
.block-container, .main {{
    overflow-x: clip;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 44px !important;
    padding-bottom: 2rem;
}}

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

.stButton>button {{
    background: {BRAND_BLUE} !important; color: white !important;
    border: none !important; font-weight: 600 !important;
    border-radius: 10px !important;
}}
.stButton>button:hover {{
    background: {BRAND_BLUE_DARK} !important; color: {BRAND_YELLOW} !important;
}}

@media (max-width: 768px) {{
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 0 !important;
    }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
    button[kind="header"] {{ display: none !important; }}
    .main .block-container {{
        padding-bottom: 75px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 0 !important;
    }}
    .main > div:first-child {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    /* L'hero su mobile parte da sotto la topbar e non ha margin negativo */
  /* Hero su mobile: zero spazio tra topbar e hero */
    .hero-full {{
        margin-top: 44px !important;
        margin-left: -1rem !important;
        margin-right: -1rem !important;
        padding-top: 2rem !important;
    }}
    /* Qualsiasi wrapper sopra l'hero deve avere zero spazio visibile */
    .main .block-container > div:first-child,
    [data-testid="stVerticalBlock"] > div:first-child,
    [data-testid="stVerticalBlockBorderWrapper"]:first-child,
    [data-testid="element-container"]:first-child {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    /* La topbar ha già il suo colore blu di fondo; estendiamolo leggermente anche sotto per coprire il seam */
    .sticky-topbar {{
        box-shadow: 0 0 0 2px {BRAND_BLUE};
    }}
}}
/* TOPBAR */
.sticky-topbar {{
    position: fixed; top: 0; left: 0; right: 0;
    height: 44px; background: {BRAND_BLUE};
    display: flex; align-items: center; justify-content: center;
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

/* BOTTOM NAV MOBILE */
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
   .bn-label {{ font-size:0.48rem; text-align:center; line-height:1.2; font-family:sans-serif; color:rgba(255,255,255,0.6); letter-spacing:-0.01em; }}
}}

/* Anchor per scroll */
.section-anchor {{
    display: block;
    position: relative;
    top: -50px;
    visibility: hidden;
    height: 0;
}}

/* ── SEZIONI long-page ── */
.section-wrap {{
    position: relative;
    margin-left: -1rem;
    margin-right: -1rem;
    padding: 3rem 1rem 2.5rem;
}}
@media (min-width: 769px) {{
    .section-wrap {{
        margin-left: -3rem;
        margin-right: -3rem;
        padding: 3.5rem 3rem 2.8rem;
    }}
}}

.section-body {{
    margin-left: -1rem;
    margin-right: -1rem;
    padding: 0 1rem 2.5rem;
}}
@media (min-width: 769px) {{
    .section-body {{
        margin-left: -3rem;
        margin-right: -3rem;
        padding: 0 3rem 3rem;
    }}
}}

/* ── Palette per sezione ── */
/* Temi — giallo chiaro con testo blu */
.sec-temi {{ background: {SEC_TEMI}; color: #3a4a5c; }}
.sec-temi .section-eyebrow {{ color: #6b5600; }}
.sec-temi .section-title {{ color: {BRAND_BLUE}; }}
.sec-temi .section-subtitle {{ color: #b38600; }}
.sec-temi .section-desc {{ color: #3a4a5c; }}

/* Briefing — blu navy */
.sec-briefing {{ background: {SEC_BRIEFING}; color: white; }}
.sec-briefing .section-eyebrow {{ color: {BRAND_YELLOW}; }}
.sec-briefing .section-title {{ color: white; }}
.sec-briefing .section-subtitle {{ color: {BRAND_YELLOW}; }}
.sec-briefing .section-desc {{ color: rgba(255,255,255,0.8); }}

/* Mappa — blu petrolio */
.sec-mappa {{ background: {SEC_MAPPA}; color: white; }}
.sec-mappa .section-eyebrow {{ color: {BRAND_YELLOW}; }}
.sec-mappa .section-title {{ color: white; }}
.sec-mappa .section-subtitle {{ color: {BRAND_YELLOW}; }}
.sec-mappa .section-desc {{ color: rgba(255,255,255,0.82); }}

/* Programma — blu medio */
.sec-programma {{ background: {SEC_PROGRAMMA}; color: white; }}
.sec-programma .section-eyebrow {{ color: {BRAND_YELLOW}; }}
.sec-programma .section-title {{ color: white; }}
.sec-programma .section-subtitle {{ color: {BRAND_YELLOW}; }}
.sec-programma .section-desc {{ color: rgba(255,255,255,0.85); }}

/* Documenti — lavanda chiara, testo blu brand */
.sec-documenti {{ background: {SEC_DOCUMENTI}; color: #3a4a5c; }}
.sec-documenti .section-eyebrow {{ color: {BRAND_BLUE}; opacity: 0.75; }}
.sec-documenti .section-title {{ color: {BRAND_BLUE}; }}
.sec-documenti .section-subtitle {{ color: #4a3fb8; }}
.sec-documenti .section-desc {{ color: #3a4a5c; }}

/* Altro — giallo chiaro (come Temi) */
.sec-altro {{ background: {SEC_ALTRO}; color: #3a4a5c; }}
.sec-altro .section-eyebrow {{ color: #6b5600; }}
.sec-altro .section-title {{ color: {BRAND_BLUE}; }}
.sec-altro .section-subtitle {{ color: #b38600; }}
.sec-altro .section-desc {{ color: #3a4a5c; }}

.section-eyebrow {{
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    display: block;
}}
.section-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(1.7rem, 4.5vw, 2.3rem);
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 0.7rem;
    letter-spacing: -0.01em;
}}
.section-subtitle {{
    font-family: 'Lobster Two', cursive; font-style: italic;
    font-size: 1.15rem; font-weight: 700;
    margin-bottom: 1rem;
}}
.section-desc {{
    font-size: 0.95rem; line-height: 1.7;
    max-width: 640px;
}}

/* HERO HOME */
.hero-full {{
    position: relative; overflow: hidden;
    background: {BRAND_BLUE};
    margin: -44px -1rem 0 -1rem;
    padding: 4rem 2rem 3.5rem; text-align: center;
}}
@media (min-width: 769px) {{
    .hero-full {{ margin: -44px -3rem 0 -3rem; padding: 4.5rem 3rem 4rem; }}
}}
@media (max-width: 768px) {{
    .hero-full {{
        margin-top: -44px;
        margin-left: -1rem;
        margin-right: -1rem;
    }}
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

/* HOME SECTION */
.home-section {{
    background: white;
    margin: 0 -1rem;
    padding: 1.8rem 1rem 2.8rem;
}}
@media (min-width: 769px) {{
    .home-section {{ margin: 0 -3rem; padding: 2rem 3rem 3rem; }}
}}

.legend-card {{
    background: white; border-radius: 18px; padding: 0.95rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 6px 16px rgba(19,0,137,0.05);
    margin-bottom: 0.75rem;
}}
.note {{ color: #5b6472; font-size: 0.93rem; line-height: 1.6; }}

.gallery-caption {{
    text-align: center; color: {BRAND_BLUE};
    font-size: 1rem; margin: 0.5rem 0 1.2rem; font-weight: 500;
}}

/* HOME STRIP */
.home-strip {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.6rem;
    margin: 0.6rem 0 0;
}}
@media (max-width: 640px) {{
    .home-strip {{ grid-template-columns: 1fr; gap: 0.5rem; }}
}}
.strip-card {{
    background: white;
    border-radius: 14px;
    padding: 0.7rem 0.85rem;
    border: 1px solid rgba(19,0,137,0.1);
    box-shadow: 0 2px 8px rgba(19,0,137,0.04);
    border-left: 3px solid {BRAND_YELLOW};
    text-decoration: none;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    cursor: pointer;
}}
.strip-card:hover {{ background: {BRAND_BLUE_LIGHT}; }}
.strip-label {{
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: {BRAND_BLUE}; opacity: 0.65;
}}
.strip-title {{
    font-size: 0.85rem; font-weight: 700; color: {BRAND_BLUE}; line-height: 1.2;
}}
.strip-sub {{
    font-size: 0.7rem; color: #5b6472; line-height: 1.3;
}}
.home-news-links {{
    margin-top: 0.3rem;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}
.home-news-links a {{
    font-size: 0.72rem; color: {BRAND_BLUE}; text-decoration: none;
    font-weight: 600; padding: 0.12rem 0;
    border-bottom: 1px dotted rgba(19,0,137,0.15);
}}
.home-news-links a:last-child {{ border-bottom: none; }}

/* FOTO ESPERTI centrate */
div[data-testid="stImage"] {{
    display: flex !important;
    justify-content: center !important;
}}
.brief-section div[data-testid="stImage"] img {{
    border-radius: 50% !important;
    width: 90px !important;
    height: 90px !important;
    object-fit: cover !important;
    border: 3px solid {SEC_BRIEFING};
}}
div[data-testid="stDialog"] div[data-testid="stImage"] img {{
    border-radius: 16px !important;
    width: 100% !important;
    height: auto !important;
    max-height: 260px;
    object-fit: cover !important;
    border: none !important;
}}

.footer-box {{
    text-align: center; color: #9aa3b0; font-size: 0.88rem;
    margin-top: 2rem; padding: 2rem 0 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ============================
# DATI
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
    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:0.8rem;">Naviga</div>

    <style>
    .sidebar-nav a {{
        display:block;
        padding: 0.55rem 0.8rem;
        color: rgba(255,255,255,0.85) !important;
        text-decoration: none;
        border-radius: 8px;
        font-size: 0.92rem;
        font-weight: 500;
        margin-bottom: 0.15rem;
        border-left: 2px solid transparent;
        transition: all 0.15s;
    }}
    .sidebar-nav a:hover {{
        background: rgba(255,222,89,0.12);
        color: {BRAND_YELLOW} !important;
        border-left-color: {BRAND_YELLOW};
    }}
    </style>
    <div class="sidebar-nav">
        <a href="#home">🏠 &nbsp; Home</a>
        <a href="#temi">👁 &nbsp; Temi del viaggio</a>
        <a href="#briefing">📅 &nbsp; Briefing</a>
        <a href="#mappe">🗺 &nbsp; Mappa</a>
        <a href="#programma">🗓 &nbsp; Programma</a>
        <a href="#documenti">📂 &nbsp; Documenti</a>
        <a href="#approfondimenti">📚 &nbsp; Altro</a>
    </div>

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
    </div>
    """, unsafe_allow_html=True)

# ============================
# BOTTOM BAR MOBILE
# ============================
st.markdown(f"""
<div class="bottom-nav">
    <a href="#home" class="bn-item"><span class="bn-icon">🏠</span><span class="bn-label">Home</span></a>
    <a href="#temi" class="bn-item"><span class="bn-icon">👁</span><span class="bn-label">Temi</span></a>
    <a href="#briefing" class="bn-item"><span class="bn-icon">📅</span><span class="bn-label">Briefing</span></a>
    <a href="#mappe" class="bn-item"><span class="bn-icon">🗺</span><span class="bn-label">Mappa</span></a>
    <a href="#programma" class="bn-item"><span class="bn-icon">🗓</span><span class="bn-label">Progr.</span></a>
    <a href="#documenti" class="bn-item"><span class="bn-icon">📂</span><span class="bn-label">Doc.</span></a>
    <a href="#approfondimenti" class="bn-item"><span class="bn-icon">📚</span><span class="bn-label">Altro</span></a>
</div>
""", unsafe_allow_html=True)
# ============================
# TOPBAR
# ============================
eyes_tag_topbar = f'<img src="data:{eyes_logo_yellow_mime};base64,{eyes_logo_yellow_b64}" style="height:26px;width:auto;object-fit:contain;margin-right:0.5rem;vertical-align:middle;">' if eyes_logo_yellow_b64 else ""
eyes_tag_hero = f'<img src="data:{eyes_logo_white_mime};base64,{eyes_logo_white_b64}" style="height:90px;width:auto;object-fit:contain;margin-bottom:0.8rem;display:block;margin-left:auto;margin-right:auto;">' if eyes_logo_white_b64 else ""

st.markdown(f"""
<div class="sticky-topbar">
    <div class="sticky-topbar-title">{eyes_tag_topbar}PECCIOLI EYES<em>to New Orleans</em></div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# 🏠 HERO + HOME
# ============================================================================
ponte_bg = f'<img src="data:{ponte_mime};base64,{ponte_b64}" style="position:absolute;bottom:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0.08;pointer-events:none;filter:invert(1);">' if ponte_b64 else ""

st.markdown(f"""
<span id="home" class="section-anchor"></span>
<div class="hero-full">
    {ponte_bg}
    <div style="position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;">
        {eyes_tag_hero}
        <div class="hero-title-main">Peccioli Eyes</div>
        <div class="hero-title-script">to New Orleans</div>
        <div class="hero-year">2026</div>
    </div>
</div>

<div class="home-section">
""", unsafe_allow_html=True)

# Countdown
import streamlit.components.v1 as components
expert_paths = get_expert_paths()
_morelli_path = expert_paths["morelli"]
morelli_b64_cd, morelli_mime_cd = img_to_base64(_morelli_path, max_width=100, quality=75) if _morelli_path else (None, None)
prossimo_foto = f'<img src="data:{morelli_mime_cd};base64,{morelli_b64_cd}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid {BRAND_YELLOW};flex-shrink:0;">' if morelli_b64_cd else f'<div style="width:44px;height:44px;border-radius:50%;background:{BRAND_YELLOW};flex-shrink:0;"></div>'

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
<div style="background:{BRAND_BLUE_LIGHT};border-radius:18px;padding:1.1rem 1.3rem;margin:1rem 0 1.2rem;border-left:4px solid {BRAND_YELLOW};">
    <p style="font-size:0.98rem;color:{BRAND_BLUE};line-height:1.65;margin:0;font-style:italic;">
        <strong style="font-style:normal;">Peccioli Eyes</strong> è uno sguardo che parte dal nostro piccolo territorio e si apre al mondo, mettendo al centro i giovani, la cultura e l'esperienza.
    </p>
</div>

<div style="display:flex;align-items:center;gap:1rem;margin:0.8rem 0 0.8rem;">
    <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(19,0,137,0.2));"></div>
    <div style="text-align:center;">
        <div style="font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:{BRAND_BLUE};margin-bottom:0.15rem;opacity:0.7;">New Orleans vista da vicino</div>
        <div style="font-family:'Lobster Two',cursive;font-style:italic;font-size:1.3rem;font-weight:700;color:{BRAND_BLUE};line-height:1;">Sguardi sulla città</div>
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
    dots_html = '<div style="display:flex;justify-content:center;gap:6px;margin-bottom:0.4rem;">'
    for i in range(len(valid_items)):
        color = BRAND_YELLOW if i == idx else "rgba(19,0,137,0.2)"
        dots_html += f'<div style="width:7px;height:7px;border-radius:50%;background:{color};"></div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

if valid_items:
    galleria()

st.markdown(f"""
<div class="home-strip">
    <a href="https://www.earthcam.com/usa/louisiana/neworleans/bourbonstreet/" target="_blank" rel="noopener" class="strip-card">
        <div class="strip-label">📹 Live</div>
        <div class="strip-title">Bourbon Street</div>
        <div class="strip-sub">French Quarter · 24/7</div>
    </a>
    <div class="strip-card" style="cursor:default;border-left-color:{BRAND_BLUE};">
        <div class="strip-label">🗞 Notizie</div>
        <div class="strip-title">Da New Orleans</div>
        <div class="home-news-links">
            <a href="https://www.nola.com" target="_blank" rel="noopener">Times-Picayune →</a>
            <a href="https://www.wwno.org" target="_blank" rel="noopener">WWNO Radio →</a>
            <a href="https://thelensnola.org" target="_blank" rel="noopener">The Lens NOLA</a>
        </div>
    </div>
    <a href="https://open.spotify.com/playlist/0iMiZcvIy26MqHQln5kkrI" target="_blank" rel="noopener" class="strip-card" style="border-left-color:#1DB954;">
        <div class="strip-label">🎧 Playlist</div>
        <div class="strip-title">NOLA Sound</div>
        <div class="strip-sub">Jazz, blues, bounce</div>
    </a>
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# 👁 TEMI — GIALLO CHIARO
# ============================================================================
st.markdown(f"""
<span id="temi" class="section-anchor"></span>
<div class="section-wrap sec-temi">
    <span class="section-eyebrow">01 · Come guardare la città</span>
    <div class="section-title">Temi del viaggio</div>
    <p class="section-desc">
        Quattro chiavi di lettura per osservare New Orleans durante il viaggio.
        Non categorie separate, ma prospettive da tenere sempre attive.
    </p>
</div>
<div class="section-body sec-temi">
""", unsafe_allow_html=True)

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
    {"titolo": "Musica", "label": "JAZZ", "colore": BRAND_BLUE, "bg": "white",
     "sottotitolo": "Jazz, blues e il ritmo della città",
     "domanda": "Perché il jazz è nato proprio qui, e non altrove?",
     "desc": "New Orleans è la culla del jazz e del blues. La musica non è intrattenimento: è linguaggio sociale, memoria collettiva, forma di resistenza. Dalle second line nei funerali di strada a Frenchmen Street la sera, la città vive attraverso il suono.",
     "luoghi": "Frenchmen Street · Congo Square · Louis Armstrong Park", "svg": svg_musica},
    {"titolo": "Resilienza", "label": "KATRINA", "colore": BRAND_BLUE, "bg": BRAND_BLUE_LIGHT,
     "sottotitolo": "Katrina, ricostruzione e cambiamento climatico",
     "domanda": "Come si ricostruisce una città dopo che l'acqua se la porta via?",
     "desc": "Il 2005 ha messo a nudo le fragilità strutturali della città: infrastrutture, disuguaglianze razziali, risposta istituzionale. Vent'anni dopo, la città è ancora in cammino. Il Lower Ninth Ward è il luogo dove questo tema si tocca con mano.",
     "luoghi": "Lower Ninth Ward · Argini del Mississippi · Lakeview", "svg": svg_resilienza},
    {"titolo": "Società", "label": "PEOPLE", "colore": BRAND_BLUE, "bg": "white",
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

col_t1, col_t2 = st.columns(2)
for i, tema in enumerate(temi):
    with (col_t1 if i % 2 == 0 else col_t2):
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

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 📅 BRIEFING — BLU NAVY
# ============================================================================
st.markdown(f"""
<span id="briefing" class="section-anchor"></span>
<div class="section-wrap sec-briefing">
    <span class="section-eyebrow">02 · Prima del viaggio</span>
    <div class="section-title">Incontri propedeutici</div>
    <div class="section-subtitle">Tre esperti, tre sguardi</div>
    <p class="section-desc">
        Tre serate per arrivare a New Orleans con strumenti culturali già solidi.
        Non lezioni — conversazioni aperte su storia, geopolitica e società americana.
    </p>
</div>
<div class="section-body sec-briefing brief-section">
""", unsafe_allow_html=True)

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
        "foto": expert_paths["gardner"], "emoji": "🌐", "colore": BRAND_YELLOW,
    },
    {
        "data": "18 giugno", "ora": "ore 21",
        "titolo": "Francesco Costa",
        "ruolo": "Giornalista · Direttore de Il Post",
        "bio": "Direttore responsabile de Il Post. Tra i principali divulgatori italiani sulla società e politica americana, autore di libri e progetti dedicati agli Stati Uniti. Dal 2021 al 2025 ha condotto per il Post il podcast giornaliero Morning, una rassegna stampa commentata che è stata definita \"il primo vero podcast daily italiano\".",
        "tema": "Punto di vista sociale, narrativo e attuale sugli Stati Uniti: leggere l'America oltre gli stereotipi.",
        "foto": expert_paths["costa"], "emoji": "📰", "colore": BRAND_YELLOW,
    },
]

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
        st.markdown(f"""
        <div style="background:white;border-radius:22px;padding:1.4rem 1rem 0.3rem;
             box-shadow:0 6px 22px rgba(0,0,0,0.18);
             text-align:center;margin-bottom:0.3rem;">
        """, unsafe_allow_html=True)
        if b["foto"]:
            sp1, sp_img, sp2 = st.columns([1, 2, 1])
            with sp_img:
                st.image(b["foto"], use_container_width=True)
        else:
            st.markdown(f'<div style="width:90px;height:90px;border-radius:50%;background:{SEC_BRIEFING};margin:0 auto 0.8rem;display:flex;align-items:center;justify-content:center;font-size:2rem;color:white;">{b["emoji"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-top:0.3rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{SEC_BRIEFING};margin-bottom:0.2rem;opacity:0.85;">{b['data']} · {b['ora']}</div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:800;color:{SEC_BRIEFING};line-height:1.2;margin-bottom:0.3rem;">{b['titolo']}</div>
            <div style="font-size:0.78rem;color:#5b6472;line-height:1.4;margin-bottom:0.6rem;">{b['ruolo']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Scopri {b['titolo'].split()[0]}", key=f"dialog_{i}", use_container_width=True):
            st.session_state.dialog_idx = i
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 🗺 MAPPA — BLU PETROLIO
# ============================================================================
st.markdown(f"""
<span id="mappe" class="section-anchor"></span>
<div class="section-wrap sec-mappa">
    <span class="section-eyebrow">03 · Orientarsi nella città</span>
    <div class="section-title">Mappa di New Orleans</div>
    <p class="section-desc">
        I luoghi simbolici del viaggio, organizzati per tema.
        Apri la mappa interattiva qui sotto per esplorare.
    </p>
</div>
<div class="section-body sec-mappa">
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1.2rem;">
    <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
        <div style="width:12px;height:12px;border-radius:50%;background:{BRAND_BLUE};flex-shrink:0;"></div> Identità e storia
    </div>
    <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
        <div style="width:12px;height:12px;border-radius:50%;background:#e6b800;flex-shrink:0;"></div> Musica
    </div>
    <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
        <div style="width:12px;height:12px;border-radius:50%;background:#4a3fb8;flex-shrink:0;"></div> Resilienza
    </div>
    <div style="display:flex;align-items:center;gap:0.4rem;background:white;padding:0.35rem 0.8rem;border-radius:999px;font-size:0.82rem;font-weight:600;color:{BRAND_BLUE};">
        <div style="width:12px;height:12px;border-radius:50%;background:#b8860b;flex-shrink:0;"></div> Società
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("🗺 Apri la mappa interattiva", expanded=False):
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

col_m1, col_m2 = st.columns(2)
for i, luogo in enumerate(luoghi_dati):
    with (col_m1 if i % 2 == 0 else col_m2):
        st.markdown(f"""
        <div class="legend-card" style="border-left:4px solid {luogo['colore']};margin-bottom:0.6rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:0.95rem;font-weight:800;color:{BRAND_BLUE};">{luogo['nome']}</div>
            </div>
            <div style="font-size:0.72rem;font-weight:700;color:{luogo['colore']};margin-bottom:0.2rem;">{luogo['tema']}</div>
            <div class="note">{luogo['desc']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 🗓 PROGRAMMA — BLU MEDIO
# ============================================================================
st.markdown(f"""
<span id="programma" class="section-anchor"></span>
<div class="section-wrap sec-programma">
    <span class="section-eyebrow">04 · Il viaggio</span>
    <div class="section-title">Programma</div>
    <p class="section-desc">
        Il programma dettagliato è in costruzione. Sarà aggiornato con tutte le tappe non appena il percorso sarà definito.
    </p>
</div>
<div class="section-body sec-programma">
    <div style="background:rgba(255,255,255,0.95);border:2px dashed {BRAND_YELLOW};border-radius:24px;padding:2.5rem 2rem;text-align:center;max-width:580px;margin:0 auto 1rem;">
        <div style="font-size:2.5rem;margin-bottom:0.6rem;">🗓</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.5rem;font-weight:800;color:{SEC_PROGRAMMA};margin-bottom:0.6rem;">Programma in definizione</div>
        <div style="font-size:0.97rem;color:#5b6472;line-height:1.75;">
            Questa sezione verrà aggiornata con tutte le tappe, gli appuntamenti e le attività non appena il percorso sarà definito.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# 📂 DOCUMENTI — LAVANDA CHIARA
# ============================================================================
st.markdown(f"""
<span id="documenti" class="section-anchor"></span>
<div class="section-wrap sec-documenti">
    <span class="section-eyebrow">05 · Prima della partenza</span>
    <div class="section-title">Materiali e documenti</div>
    <p class="section-desc">
        Documenti da consultare, compilare e consegnare in vista del viaggio.
    </p>
</div>
<div class="section-body sec-documenti">
    <div style="background:white;border-left:4px solid {BRAND_YELLOW};border-radius:0 12px 12px 0;
         padding:0.8rem 1.2rem;margin-bottom:1.4rem;font-size:0.88rem;color:{BRAND_BLUE};font-weight:500;box-shadow:0 2px 8px rgba(19,0,137,0.05);">
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
         border:1px solid rgba(19,0,137,0.08);box-shadow:0 2px 8px rgba(19,0,137,0.05);">
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

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 📚 ALTRO — GIALLO CHIARO
# ============================================================================
st.markdown(f"""
<span id="approfondimenti" class="section-anchor"></span>
<div class="section-wrap sec-altro">
    <span class="section-eyebrow">06 · Per prepararsi</span>
    <div class="section-title">Altro da esplorare</div>
    <p class="section-desc">
        Libri, film, documentari e risorse online per arrivare a New Orleans con uno sguardo già allenato.
    </p>
</div>
<div class="section-body sec-altro">
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📚 Libri", "🎬 Film e TV", "🎞 Documentari", "🌐 Risorse"])

with tab1:
    col_l1, col_l2 = st.columns(2)
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
        with (col_l1 if i % 2 == 0 else col_l2):
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

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<div class='footer-box'>Peccioli Eyes to New Orleans · 2026 · Portale ragazzi</div>", unsafe_allow_html=True)
