import streamlit as st
import streamlit.components.v1 as components
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
    page_title="Peccioli Eyes on New Orleans",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed"
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
SEC_ALTRO = "#fff7c2"        # giallo chiaro (apre e chiude con lo stesso colore di Temi)

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

# Foto Muro degli Occhi (opera "Sguardi" di Peccioli)
sguardi_path = find_img("sguardi_peccioli.jpg", "sguardi_peccioli.jpeg", "sguardi_peccioli.png", "muro_occhi.jpg", "muro_occhi.jpeg", "muro_occhi.png", " sguardi_peccioli.jpg", "_sguardi_peccioli.jpg")
sguardi_b64, sguardi_mime = img_to_base64(sguardi_path, max_width=1000, quality=80) if sguardi_path else (None, None)

# Foto hero (Bourbon Street, NOLA - temporanea, da sostituire con foto royalty-free)
hero_bg_path = find_img("hero_nola_bourbon.jpg", "hero_nola_bourbon.jpeg", "hero_nola_bourbon.png", "hero_nola.jpg", "hero_bourbon.jpg")
hero_bg_b64, hero_bg_mime = img_to_base64(hero_bg_path, max_width=1600, quality=82) if hero_bg_path else (None, None)
HERO_BG_DATAURL = f"data:{hero_bg_mime};base64,{hero_bg_b64}" if hero_bg_b64 else ""

# Logo Jazz Peccioli (per la card evento nel calendario)
jazz_logo_path = find_img("jazz_peccioli_logo.png", "jazz_peccioli.png", "jazz_peccioli_logo.jpg")
jazz_logo_b64, jazz_logo_mime = img_to_base64(jazz_logo_path, max_width=400, quality=88) if jazz_logo_path else (None, None)

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

html {{
    scroll-behavior: smooth;
    scroll-padding-top: 50px;
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
    padding-top: 56px !important;
    padding-bottom: 2rem;
}}
@media (max-width: 768px) {{
    .block-container {{
        padding-top: 44px !important;
    }}
}}

#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stAppViewBlockContainer"] footer,
.viewerBadge_container__1QSob, .viewerBadge_link__qRIco,
#stDecoration, .streamlit-footer,
[data-testid="stBottom"], section[data-testid="stBottom"],
div[class*="StatusWidget"], div[class*="viewerBadge"],
button[title="View fullscreen"] {{ display: none !important; }}

/* Sidebar Streamlit COMPLETAMENTE rimossa su tutti i device */
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
button[kind="header"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}

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
        padding-top: 44px !important;
    }}
    .main .block-container {{
        padding-bottom: 75px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    .main > div:first-child {{
        padding-top: 0 !important;
    }}
}}

/* TOPBAR */

/* FADE-IN sezioni (applicato dinamicamente da JS - default invisibile) */
.fade-in-ready {{
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.7s ease-out, transform 0.7s ease-out;
}}
.fade-in-ready.fade-in-visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* BACK TO TOP - bottone freccia in basso a destra */
.back-to-top {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 48px;
    height: 48px;
    background: {BRAND_BLUE};
    color: {BRAND_YELLOW};
    border: 2px solid {BRAND_YELLOW};
    border-radius: 50%;
    font-size: 1.3rem;
    font-weight: 800;
    cursor: pointer;
    z-index: 99997;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s, visibility 0.3s, background 0.2s, transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    line-height: 1;
}}
.back-to-top.visible {{
    opacity: 1;
    visibility: visible;
}}
.back-to-top:hover {{
    background: {BRAND_YELLOW};
    color: {BRAND_BLUE};
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.35);
}}
@media (max-width: 768px) {{
    .back-to-top {{
        bottom: 90px;
        right: 18px;
        width: 42px;
        height: 42px;
        font-size: 1.15rem;
    }}
}}
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

/* Top nav orizzontale (desktop) */
.topbar-nav {{
    display: none;
    align-items: center;
    gap: 0.2rem;
}}
.topbar-nav a {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.85rem;
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.18s ease;
    position: relative;
    white-space: nowrap;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}}
.topbar-nav a .nav-icon {{
    font-size: 0.95rem;
    line-height: 1;
}}
.topbar-nav a:hover {{
    color: {BRAND_YELLOW};
    background: rgba(255,222,89,0.08);
}}
.topbar-nav a:hover::after {{
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0.85rem;
    right: 0.85rem;
    height: 2px;
    background: {BRAND_YELLOW};
    border-radius: 2px;
}}

/* Desktop: topbar diventa layout titolo + nav */
@media (min-width: 769px) {{
    .sticky-topbar {{
        height: 56px;
        justify-content: space-between;
        padding: 0 2rem;
    }}
    .sticky-topbar-title {{
        font-size: 0.95rem;
        flex-shrink: 0;
    }}
    .sticky-topbar-title em {{
        font-size: 1rem;
    }}
    .topbar-nav {{
        display: flex;
    }}
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
        display:flex; flex-direction:column; align-items:center; gap:1px;
        text-decoration:none; flex:1; padding:2px 0; cursor:pointer; min-width: 0;
    }}
    .bn-icon {{ font-size:1rem; line-height:1; }}
    .bn-label {{ font-size:0.48rem; text-align:center; line-height:1.1; font-family:sans-serif; color:rgba(255,255,255,0.65); white-space: nowrap; }}
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
    background-color: {BRAND_BLUE};
    background-image: url("{HERO_BG_DATAURL}"), url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%201200%20700%22%20preserveAspectRatio%3D%22xMidYMid%20slice%22%3E%3Cg%20fill%3D%22%23FFDE59%22%20opacity%3D%220.18%22%3E%3Cg%20transform%3D%22translate%2880%2C80%29%22%3E%3Cellipse%20rx%3D%2235%22%20ry%3D%2222%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28220%2C60%29%20rotate%288%29%22%3E%3Cellipse%20rx%3D%2228%22%20ry%3D%2218%22/%3E%3Ccircle%20r%3D%229%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28370%2C100%29%20rotate%28-5%29%22%3E%3Cellipse%20rx%3D%2240%22%20ry%3D%2225%22/%3E%3Ccircle%20r%3D%2213%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%226%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28540%2C70%29%20rotate%283%29%22%3E%3Cellipse%20rx%3D%2230%22%20ry%3D%2219%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28720%2C90%29%20rotate%28-8%29%22%3E%3Cellipse%20rx%3D%2238%22%20ry%3D%2224%22/%3E%3Ccircle%20r%3D%2212%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28880%2C60%29%20rotate%285%29%22%3E%3Cellipse%20rx%3D%2232%22%20ry%3D%2220%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%281060%2C80%29%20rotate%28-3%29%22%3E%3Cellipse%20rx%3D%2236%22%20ry%3D%2223%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%2850%2C240%29%20rotate%28-2%29%22%3E%3Cellipse%20rx%3D%2232%22%20ry%3D%2220%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28180%2C220%29%20rotate%287%29%22%3E%3Cellipse%20rx%3D%2238%22%20ry%3D%2224%22/%3E%3Ccircle%20r%3D%2212%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28340%2C250%29%20rotate%28-4%29%22%3E%3Cellipse%20rx%3D%2230%22%20ry%3D%2219%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28870%2C240%29%20rotate%286%29%22%3E%3Cellipse%20rx%3D%2234%22%20ry%3D%2222%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%281020%2C220%29%20rotate%28-7%29%22%3E%3Cellipse%20rx%3D%2238%22%20ry%3D%2224%22/%3E%3Ccircle%20r%3D%2212%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%281140%2C250%29%20rotate%282%29%22%3E%3Cellipse%20rx%3D%2228%22%20ry%3D%2218%22/%3E%3Ccircle%20r%3D%229%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%2880%2C420%29%20rotate%284%29%22%3E%3Cellipse%20rx%3D%2236%22%20ry%3D%2223%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28240%2C440%29%20rotate%28-6%29%22%3E%3Cellipse%20rx%3D%2230%22%20ry%3D%2219%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28940%2C430%29%20rotate%283%29%22%3E%3Cellipse%20rx%3D%2232%22%20ry%3D%2220%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%281100%2C460%29%20rotate%28-3%29%22%3E%3Cellipse%20rx%3D%2236%22%20ry%3D%2223%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%2860%2C580%29%20rotate%28-5%29%22%3E%3Cellipse%20rx%3D%2240%22%20ry%3D%2225%22/%3E%3Ccircle%20r%3D%2213%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%226%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28220%2C600%29%20rotate%287%29%22%3E%3Cellipse%20rx%3D%2232%22%20ry%3D%2220%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28390%2C580%29%20rotate%28-2%29%22%3E%3Cellipse%20rx%3D%2234%22%20ry%3D%2222%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28580%2C610%29%20rotate%285%29%22%3E%3Cellipse%20rx%3D%2230%22%20ry%3D%2219%22/%3E%3Ccircle%20r%3D%2210%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%224%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28770%2C590%29%20rotate%28-4%29%22%3E%3Cellipse%20rx%3D%2236%22%20ry%3D%2223%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%28950%2C620%29%20rotate%286%29%22%3E%3Cellipse%20rx%3D%2234%22%20ry%3D%2222%22/%3E%3Ccircle%20r%3D%2211%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3Cg%20transform%3D%22translate%281120%2C590%29%20rotate%28-7%29%22%3E%3Cellipse%20rx%3D%2238%22%20ry%3D%2224%22/%3E%3Ccircle%20r%3D%2212%22%20fill%3D%22white%22/%3E%3Ccircle%20r%3D%225%22%20fill%3D%22%23130089%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    background-size: cover, cover;
    background-position: center, center;
    background-repeat: no-repeat, no-repeat;
    margin: -44px -1rem 0 -1rem;
    padding: 3rem 2rem 3rem; text-align: center;
    min-height: 70vh;
    display: flex; align-items: center; justify-content: center;
}}
/* Overlay scuro per leggibilita del testo sopra la foto */
.hero-full::before {{
    content: "";
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(10,0,82,0.55) 0%, rgba(19,0,137,0.65) 50%, rgba(10,0,82,0.85) 100%);
    z-index: 0;
}}
@media (min-width: 769px) {{
    .hero-full {{
        margin: -44px -3rem 0 -3rem;
        padding: 3.5rem 3rem 3.5rem;
        min-height: 70vh;
    }}
}}
@media (max-width: 768px) {{
    .hero-full {{
        margin-top: -120px;
        margin-left: -1rem;
        margin-right: -1rem;
        padding-top: 8rem;
        padding-bottom: 2rem;
        min-height: 65vh;
    }}
}}
/* Freccia animata scroll giu */
.hero-scroll-arrow {{
    position: absolute;
    bottom: 1.5rem; left: 50%;
    transform: translateX(-50%);
    color: {BRAND_YELLOW};
    font-size: 1.8rem;
    opacity: 0.85;
    animation: bounceDown 2s infinite;
    z-index: 2;
    text-decoration: none;
    line-height: 1;
}}
.hero-scroll-arrow:hover {{ opacity: 1; transform: translateX(-50%) scale(1.15); }}
@keyframes bounceDown {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateX(-50%) translateY(0); }}
    40% {{ transform: translateX(-50%) translateY(-12px); }}
    60% {{ transform: translateX(-50%) translateY(-6px); }}
}}
@media (max-width: 768px) {{
    .hero-scroll-arrow {{ display: none; }}
}}
.hero-title-main {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.5rem, 8vw, 5rem); font-weight: 800;
    color: white; line-height: 0.95;
    letter-spacing: 0.02em; text-transform: uppercase;
    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
}}
.hero-title-script {{
    font-family: 'Lobster Two', cursive; font-style: italic; font-weight: 700;
    font-size: clamp(1.6rem, 5vw, 3rem);
    color: {BRAND_YELLOW}; line-height: 1.1; margin-top: 0.3rem;
    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
}}
.hero-year {{
    display:inline-block; margin-top: 1.2rem;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.3em;
    color: {BRAND_BLUE}; background: {BRAND_YELLOW};
    padding: 0.45rem 1.1rem;
    border-radius: 999px;
    box-shadow: 0 4px 16px rgba(255,222,89,0.4);
}}

/* HOME SECTION */
.home-section {{
    background: white;
    margin: 0 -1rem;
    padding: 0.8rem 1rem 2.8rem;
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
# Colori dei temi mappa
COL_IDENTITA = BRAND_BLUE       # blu brand - Identità e storia
COL_MUSICA = "#e6b800"          # oro - Musica
COL_RESILIENZA = "#4a3fb8"      # viola indaco - Resilienza
COL_SOCIETA = "#b8860b"         # bronzo - Società

# Icone SVG per tema (usate nei marker della mappa)
# Ogni icona è un path SVG 20x20, viene colorata via CSS
SVG_IDENTITA = '<svg viewBox="0 0 24 24" width="14" height="14" fill="white"><path d="M12 2L2 7v2h20V7L12 2zm-8 9v8H2v2h20v-2h-2v-8h-2v8h-3v-8h-2v8h-2v-8H9v8H6v-8H4z"/></svg>'  # colonna/tempio (storia)
SVG_MUSICA = '<svg viewBox="0 0 24 24" width="14" height="14" fill="white"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>'  # nota musicale
SVG_RESILIENZA = '<svg viewBox="0 0 24 24" width="14" height="14" fill="white"><path d="M2 12c1.5-1.5 3-1.5 4.5 0S9 13.5 10.5 12 13.5 10.5 15 12s3 1.5 4.5 0S22 10.5 22 12s-1.5 1.5-3 0-3-1.5-4.5 0S12 13.5 10.5 12 7.5 10.5 6 12s-3 1.5-4 0z"/><path d="M2 17c1.5-1.5 3-1.5 4.5 0S9 18.5 10.5 17s3-1.5 4.5 0 3 1.5 4.5 0S22 15.5 22 17s-1.5 1.5-3 0-3-1.5-4.5 0S12 18.5 10.5 17s-3-1.5-4.5 0-3 1.5-4 0z"/></svg>'  # onde (acqua/resilienza)
SVG_SOCIETA = '<svg viewBox="0 0 24 24" width="14" height="14" fill="white"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>'  # 3 persone

# Luoghi con coordinate verificate (Google Places, aprile 2026)
# Foto: thumb Wikimedia Commons 400px (lazy-loaded nel popup, no peso iniziale)
luoghi_dati = [
    # IDENTITÀ E STORIA (blu brand)
    {"nome": "French Quarter", "lat": 29.9584426, "lon": -90.0644107,
     "desc": "Il quartiere più iconico, tra architettura storica, balconi in ferro battuto e stratificazioni culturali.",
     "colore": COL_IDENTITA, "tema": "Identità e storia", "icona": SVG_IDENTITA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/French_Quarter03_New_Orleans.JPG/400px-French_Quarter03_New_Orleans.JPG"},
    {"nome": "Jackson Square", "lat": 29.9574024, "lon": -90.0629495,
     "desc": "Piazza centrale e simbolica: la Cattedrale di San Luigi, artisti di strada e identità storica.",
     "colore": COL_IDENTITA, "tema": "Identità e storia", "icona": SVG_IDENTITA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Jackson_Square%2C_New_Orleans.jpg/400px-Jackson_Square%2C_New_Orleans.jpg"},
    {"nome": "St. Louis Cemetery", "lat": 29.9598326, "lon": -90.0707266,
     "desc": "Il cimitero più antico di New Orleans, con le tombe sopraelevate e la leggenda di Marie Laveau.",
     "colore": COL_IDENTITA, "tema": "Identità e storia", "icona": SVG_IDENTITA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/St_Louis_Cemetery_1_New_Orleans_1_Dec_2017.jpg/400px-St_Louis_Cemetery_1_New_Orleans_1_Dec_2017.jpg"},
    {"nome": "Garden District", "lat": 29.9292146, "lon": -90.0828533,
     "desc": "Quartiere delle grandi ville antebellum, simbolo della storia americana del Sud.",
     "colore": COL_IDENTITA, "tema": "Identità e storia", "icona": SVG_IDENTITA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Buckner_Mansion_New_Orleans.jpg/400px-Buckner_Mansion_New_Orleans.jpg"},
    # MUSICA (oro)
    {"nome": "Frenchmen Street", "lat": 29.9641512, "lon": -90.0578074,
     "desc": "La strada più autentica per il jazz dal vivo, lontana dal turismo di Bourbon Street.",
     "colore": COL_MUSICA, "tema": "Musica", "icona": SVG_MUSICA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Frenchmen_Street_at_Night_New_Orleans.jpg/400px-Frenchmen_Street_at_Night_New_Orleans.jpg"},
    {"nome": "Congo Square", "lat": 29.9612773, "lon": -90.0686699,
     "desc": "Luogo simbolico delle radici africane della musica americana: qui si danzava e suonava già nel '700.",
     "colore": COL_MUSICA, "tema": "Musica", "icona": SVG_MUSICA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/CongoSquareSign.jpg/400px-CongoSquareSign.jpg"},
    {"nome": "Louis Armstrong Park", "lat": 29.9627574, "lon": -90.0677536,
     "desc": "Il parco dedicato al più celebre musicista di New Orleans, nel cuore del quartiere Tremé.",
     "colore": COL_MUSICA, "tema": "Musica", "icona": SVG_MUSICA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Louis_Armstrong_Park_Entrance_Nov_2011.jpg/400px-Louis_Armstrong_Park_Entrance_Nov_2011.jpg"},
    {"nome": "Preservation Hall", "lat": 29.9582893, "lon": -90.0653897,
     "desc": "La sala concerti storica nel French Quarter, tempio vivente del jazz tradizionale di New Orleans.",
     "colore": COL_MUSICA, "tema": "Musica", "icona": SVG_MUSICA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Preservation_Hall_New_Orleans.jpg/400px-Preservation_Hall_New_Orleans.jpg"},
    # RESILIENZA (viola indaco)
    {"nome": "Lower Ninth Ward", "lat": 29.9682712, "lon": -90.0139908,
     "desc": "Il quartiere più colpito da Katrina nel 2005. Simbolo della resilienza e della lentezza della ricostruzione.",
     "colore": COL_RESILIENZA, "tema": "Resilienza", "icona": SVG_RESILIENZA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/FEMA_-_18742_-_Photograph_by_Marvin_Nauman_taken_on_10-28-2005_in_Louisiana.jpg/400px-FEMA_-_18742_-_Photograph_by_Marvin_Nauman_taken_on_10-28-2005_in_Louisiana.jpg"},
    {"nome": "Lake Pontchartrain", "lat": 30.020, "lon": -90.100,
     "desc": "Il lago ai cui argini fallirono le dighe durante Katrina, causando l'inondazione della città.",
     "colore": COL_RESILIENZA, "tema": "Resilienza", "icona": SVG_RESILIENZA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Lake_Pontchartrain_Causeway_Bridge_2006.jpg/400px-Lake_Pontchartrain_Causeway_Bridge_2006.jpg"},
    {"nome": "Make It Right Houses", "lat": 29.9736938, "lon": -90.019238,
     "desc": "Le case colorate costruite da Brad Pitt dopo Katrina per i residenti del Lower Ninth Ward.",
     "colore": COL_RESILIENZA, "tema": "Resilienza", "icona": SVG_RESILIENZA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Make_It_Right_homes_in_Lower_9th_Ward.jpg/400px-Make_It_Right_homes_in_Lower_9th_Ward.jpg"},
    # SOCIETÀ (bronzo)
    {"nome": "Tremé", "lat": 29.9690775, "lon": -90.0732223,
     "desc": "Il quartiere afroamericano più antico degli USA, culla della cultura creola e della comunità nera.",
     "colore": COL_SOCIETA, "tema": "Società", "icona": SVG_SOCIETA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Treme_Brass_Band_at_Jazz_Fest_2010.jpg/400px-Treme_Brass_Band_at_Jazz_Fest_2010.jpg"},
    {"nome": "Warehouse District", "lat": 29.9467923, "lon": -90.0753832,
     "desc": "Zona di musei e gallerie che mostra la trasformazione urbana e le nuove tensioni sociali della città.",
     "colore": COL_SOCIETA, "tema": "Società", "icona": SVG_SOCIETA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Julia_Street_NOLA_CAC.jpg/400px-Julia_Street_NOLA_CAC.jpg"},
    {"nome": "Bywater", "lat": 29.9633867, "lon": -90.0403757,
     "desc": "Quartiere creativo e in gentrificazione: murales, artisti e contraddizioni della New Orleans contemporanea.",
     "colore": COL_SOCIETA, "tema": "Società", "icona": SVG_SOCIETA,
     "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bywater_Dauphine_Shotgun_Houses.jpg/400px-Bywater_Dauphine_Shotgun_Houses.jpg"},
]

# ============================
# ============================
# SIDEBAR (rimossa - sostituita da hamburger menu su tutti i device)
# ============================

# ============================
# HAMBURGER MENU MOBILE (sostituisce la bottom bar)
# ============================
st.markdown(f"""
<style>
/* Bottone hamburger - mobile: solo icona, desktop: pillola con testo */
.hamburger-btn {{
    display: none;
    position: fixed;
    top: 52px;
    right: 12px;
    width: 42px;
    height: 42px;
    background: {BRAND_YELLOW};
    border: 2px solid {BRAND_BLUE};
    border-radius: 12px;
    cursor: pointer;
    z-index: 2147483647;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    padding: 0;
    transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: {BRAND_BLUE};
}}
.hamburger-btn:active {{ transform: scale(0.94); }}

.hamburger-btn .hb-lines {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}}
.hamburger-btn .hb-lines span {{
    display: block;
    width: 18px;
    height: 2.5px;
    background: {BRAND_BLUE};
    border-radius: 2px;
    margin: 2px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.hamburger-btn .hb-text {{
    display: none;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

/* Stato aperto: hamburger diventa X */
.hamburger-btn.open .hb-lines span:nth-child(1) {{
    transform: translateY(6.5px) rotate(45deg);
}}
.hamburger-btn.open .hb-lines span:nth-child(2) {{
    opacity: 0;
}}
.hamburger-btn.open .hb-lines span:nth-child(3) {{
    transform: translateY(-6.5px) rotate(-45deg);
}}

/* Su desktop (>768px): hamburger NASCOSTO (c'è la top nav nella topbar) */
@media (min-width: 769px) {{
    .hamburger-btn {{
        display: none !important;
    }}
    .menu-drawer {{
        display: none !important;
    }}
}}

/* Su mobile: pulsante quadrato con solo icona */
@media (max-width: 768px) {{
    .hamburger-btn {{
        display: flex !important;
    }}
    /* Nascondi bottom bar legacy */
    .bottom-nav {{ display: none !important; }}
}}

/* Overlay tendina */
.menu-drawer {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(165deg, #0a0052 0%, {BRAND_BLUE} 50%, #1a0fb8 100%);
    z-index: 2147483646;
    overflow-y: auto;
    padding: 70px 1.5rem 2rem;
    opacity: 0;
    transform: translateY(-30px);
    transition: opacity 0.3s ease-out, transform 0.3s ease-out;
}}
.menu-drawer.open {{
    display: block;
    opacity: 1;
    transform: translateY(0);
}}

.menu-eyebrow {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: {BRAND_YELLOW};
    opacity: 0.7;
    margin: 0.5rem 0 1.2rem;
    text-align: center;
}}

.menu-list {{
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    max-width: 400px;
    margin: 0 auto;
}}

.menu-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.2rem;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,222,89,0.15);
    border-radius: 14px;
    color: white;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.2s;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}}
.menu-item:active {{
    background: rgba(255,222,89,0.2);
    transform: scale(0.98);
}}
.menu-item .menu-icon {{
    font-size: 1.6rem;
    width: 36px;
    text-align: center;
    flex-shrink: 0;
}}
.menu-item .menu-label {{
    flex: 1;
}}
.menu-item .menu-arrow {{
    color: {BRAND_YELLOW};
    opacity: 0.6;
    font-size: 1.2rem;
}}

.menu-footer {{
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.7rem;
    margin-top: 2rem;
    letter-spacing: 0.05em;
}}

/* Solo mobile */
@media (max-width: 768px) {{
    .hamburger-btn {{ display: block; }}
    /* Nascondi bottom bar */
    .bottom-nav {{ display: none !important; }}
    /* Riduci padding bottom del block-container (era spazio per la bottom bar) */
    .main .block-container {{ padding-bottom: 1rem !important; }}
}}

</style>

<button class="hamburger-btn" id="hamburgerBtn" aria-label="Apri menu">
    <span class="hb-lines"><span></span><span></span><span></span></span>
    <span class="hb-text">Menu</span>
</button>

<div class="menu-drawer" id="menuDrawer">
    <div class="menu-eyebrow">Naviga il portale</div>
    <div class="menu-list">
        <a class="menu-item" data-target="home"><span class="menu-icon">🏠</span><span class="menu-label">Home</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="temi"><span class="menu-icon">👁</span><span class="menu-label">Temi del viaggio</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="briefing"><span class="menu-icon">📅</span><span class="menu-label">Calendario</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="mappe"><span class="menu-icon">🗺</span><span class="menu-label">Mappa</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="programma"><span class="menu-icon">🗓</span><span class="menu-label">Programma</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="documenti"><span class="menu-icon">📂</span><span class="menu-label">Documenti</span><span class="menu-arrow">›</span></a>
        <a class="menu-item" data-target="approfondimenti"><span class="menu-icon">📚</span><span class="menu-label">Approfondimenti</span><span class="menu-arrow">›</span></a>
    </div>
    <div class="menu-footer">Peccioli Eyes · 2026</div>
</div>
""", unsafe_allow_html=True)

# JavaScript del menu (deve essere in components.html per essere eseguito da Streamlit)
components.html("""
<script>
(function() {
    function findInParent(selector) {
        try {
            return window.parent.document.querySelector(selector);
        } catch(e) { return null; }
    }
    function findAllInParent(selector) {
        try {
            return window.parent.document.querySelectorAll(selector);
        } catch(e) { return []; }
    }

    function setupMenu() {
        const btn = findInParent('#hamburgerBtn');
        const drawer = findInParent('#menuDrawer');
        if (!btn || !drawer) {
            setTimeout(setupMenu, 500);
            return;
        }
        if (btn.dataset.menuReady === '1') return;
        btn.dataset.menuReady = '1';

        function closeMenu() {
            drawer.classList.remove('open');
            btn.classList.remove('open');
            window.parent.document.body.style.overflow = '';
        }
        function openMenu() {
            drawer.classList.add('open');
            btn.classList.add('open');
            window.parent.document.body.style.overflow = 'hidden';
        }
        function toggleMenu() {
            if (drawer.classList.contains('open')) closeMenu();
            else openMenu();
        }

        btn.addEventListener('click', toggleMenu);

        const items = findAllInParent('#menuDrawer .menu-item');
        items.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const target = item.getAttribute('data-target');
                closeMenu();
                setTimeout(() => {
                    const el = window.parent.document.getElementById(target);
                    if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    } else {
                        window.parent.location.hash = '#' + target;
                    }
                }, 250);
            });
        });

        window.parent.document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && drawer.classList.contains('open')) {
                closeMenu();
            }
        });
    }

    if (window.parent.document.readyState === 'loading') {
        window.parent.document.addEventListener('DOMContentLoaded', setupMenu);
    } else {
        setupMenu();
    }

    // ============================================
    // FADE-IN sezioni - SAFE MODE
    // Applica opacity:0 SOLO se IntersectionObserver funziona,
    // altrimenti le sezioni restano sempre visibili (no rischio schermo bianco)
    // ============================================
    function setupFadeIn() {
        // Verifica supporto IntersectionObserver
        if (!('IntersectionObserver' in window)) return;

        const targetIds = ['temi', 'briefing', 'mappe', 'programma', 'documenti', 'approfondimenti'];
        const sections = [];

        targetIds.forEach(id => {
            const anchor = window.parent.document.getElementById(id);
            if (!anchor) return;
            // Prendi l'elemento DIV subito dopo lo span anchor
            const wrap = anchor.nextElementSibling;
            if (wrap && !wrap.classList.contains('fade-in-ready')) {
                wrap.classList.add('fade-in-ready');
                sections.push(wrap);
            }
        });

        if (sections.length === 0) return;

        // Safety net: dopo 4 secondi forza visibile tutto (anche se observer non scatta)
        const safetyTimeout = setTimeout(() => {
            sections.forEach(s => s.classList.add('fade-in-visible'));
        }, 4000);

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        sections.forEach(s => observer.observe(s));
    }

    // ============================================
    // BACK TO TOP - SAFE MODE
    // Crea il bottone via JS e lo aggiunge al body parent
    // ============================================
    function setupBackToTop() {
        const parentDoc = window.parent.document;
        const parentWin = window.parent;

        // Se già esiste, esci
        if (parentDoc.getElementById('backToTop')) return;

        // Crea il bottone
        const btn = parentDoc.createElement('button');
        btn.id = 'backToTop';
        btn.className = 'back-to-top';
        btn.setAttribute('aria-label', 'Torna su');
        btn.setAttribute('type', 'button');
        btn.innerHTML = '&uarr;';
        parentDoc.body.appendChild(btn);

        function onScroll() {
            if (parentWin.scrollY > 400) {
                btn.classList.add('visible');
            } else {
                btn.classList.remove('visible');
            }
        }

        parentWin.addEventListener('scroll', onScroll, { passive: true });
        onScroll();

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            parentWin.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Avvia fade-in dopo che il DOM è completamente carico (con piccola attesa per sicurezza)
    if (window.parent.document.readyState === 'complete') {
        setTimeout(setupFadeIn, 600);
        setTimeout(setupBackToTop, 600);
    } else {
        window.parent.addEventListener('load', () => {
            setTimeout(setupFadeIn, 600);
            setTimeout(setupBackToTop, 600);
        });
    }
})();
</script>
""", height=0)

# ============================
# TOPBAR
# ============================
eyes_tag_topbar = f'<img src="data:{eyes_logo_yellow_mime};base64,{eyes_logo_yellow_b64}" style="height:26px;width:auto;object-fit:contain;margin-right:0.5rem;vertical-align:middle;">' if eyes_logo_yellow_b64 else ""
eyes_tag_hero = f'<img src="data:{eyes_logo_white_mime};base64,{eyes_logo_white_b64}" style="height:90px;width:auto;object-fit:contain;margin-bottom:0.8rem;display:block;margin-left:auto;margin-right:auto;">' if eyes_logo_white_b64 else ""

st.markdown(f"""
<div class="sticky-topbar">
    <div class="sticky-topbar-title">{eyes_tag_topbar}PECCIOLI EYES<em>on New Orleans</em></div>
    <nav class="topbar-nav">
        <a href="#home"><span class="nav-icon">🏠</span>Home</a>
        <a href="#temi"><span class="nav-icon">👁</span>Temi</a>
        <a href="#briefing"><span class="nav-icon">📅</span>Calendario</a>
        <a href="#mappe"><span class="nav-icon">🗺</span>Mappa</a>
        <a href="#programma"><span class="nav-icon">🗓</span>Programma</a>
        <a href="#documenti"><span class="nav-icon">📂</span>Documenti</a>
        <a href="#approfondimenti"><span class="nav-icon">📚</span>Altro</a>
    </nav>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# 🏠 HERO + HOME
# ============================================================================
st.markdown(f"""
<span id="home" class="section-anchor"></span>
<div class="hero-full">
    <div style="position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;">
        {eyes_tag_hero}
        <div class="hero-title-main">Peccioli Eyes</div>
        <div class="hero-title-script">on New Orleans</div>
        <div class="hero-year">2026</div>
    </div>
    <a href="#scopri" class="hero-scroll-arrow" aria-label="Scopri di piu">▾</a>
</div>

<span id="scopri" class="section-anchor"></span>
<div class="home-section">
""", unsafe_allow_html=True)

# Countdown
expert_paths = get_expert_paths()

# Foto esperti per timeline briefing (medium size)
morelli_b64_tl, morelli_mime_tl = img_to_base64(expert_paths["morelli"], max_width=500, quality=75) if expert_paths["morelli"] else (None, None)
gardner_b64_tl, gardner_mime_tl = img_to_base64(expert_paths["gardner"], max_width=500, quality=75) if expert_paths["gardner"] else (None, None)
costa_b64_tl, costa_mime_tl = img_to_base64(expert_paths["costa"], max_width=500, quality=75) if expert_paths["costa"] else (None, None)

# === LOGICA AUTOMATICA: PROSSIMO EVENTO ===
# Lista di TUTTI gli eventi del calendario con data effettiva.
# Per aggiungere/modificare eventi, basta editare anche questa lista
# (deve restare allineata con `briefing_full` più in basso).
from datetime import date

eventi_calendario = [
    {"data": date(2026, 5, 7),  "titolo": "Elia Morelli",      "data_str": "7 maggio 2026",   "foto_b64": morelli_b64_tl, "foto_mime": morelli_mime_tl},
    {"data": date(2026, 5, 21), "titolo": "Anthony Gardner",   "data_str": "21 maggio 2026",  "foto_b64": gardner_b64_tl, "foto_mime": gardner_mime_tl},
    {"data": date(2026, 6, 18), "titolo": "Francesco Costa",   "data_str": "18 giugno 2026",  "foto_b64": costa_b64_tl,   "foto_mime": costa_mime_tl},
    {"data": date(2026, 7, 7),  "titolo": "Jazz Peccioli 2026","data_str": "7-11 luglio 2026","foto_b64": jazz_logo_b64,  "foto_mime": jazz_logo_mime},
]

# Trova il primo evento >= oggi
oggi = date.today()
prossimi = [e for e in eventi_calendario if e["data"] >= oggi]

if prossimi:
    prossimo_evento = prossimi[0]
    prossimo_titolo = prossimo_evento["titolo"]
    prossimo_data_str = prossimo_evento["data_str"]
    prossimo_b64 = prossimo_evento["foto_b64"]
    prossimo_mime = prossimo_evento["foto_mime"]
else:
    # Tutti gli eventi sono passati: mostro placeholder generico
    prossimo_titolo = "Partenza per New Orleans"
    prossimo_data_str = "21 settembre 2026"
    prossimo_b64 = None
    prossimo_mime = None

# Costruisco l'HTML della foto del prossimo evento
if prossimo_b64:
    prossimo_foto = f'<img class="cd-meeting-photo" src="data:{prossimo_mime};base64,{prossimo_b64}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid {BRAND_YELLOW};flex-shrink:0;">'
else:
    prossimo_foto = f'<div class="cd-meeting-photo" style="width:44px;height:44px;border-radius:50%;background:{BRAND_YELLOW};flex-shrink:0;"></div>'

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
.cd-num { font-size:1.5rem; font-weight:800; color:white; line-height:1.2; white-space:nowrap; }
.cd-num .cd-sec { 
    display:inline-block;
    transition: color 0.2s;
}
.cd-num .cd-sec.tick { color:""" + BRAND_YELLOW + """; }
.cd-box {
    flex:1; min-width:0; background:white; border-radius:18px;
    padding:0.85rem 1rem; border:1px solid rgba(19,0,137,0.1);
    box-shadow:0 4px 14px rgba(19,0,137,0.06);
    display:flex; flex-direction:column; justify-content:center; flex-shrink:0;
}
@media (max-width:600px) {
    html, body { overflow:hidden; }
    .cd-wrap { flex-direction:column; gap:0.7rem; height:auto; }
    .cd-main { padding:1rem 1.2rem; border-radius:16px; }
    .cd-label { font-size:0.68rem; margin-bottom:0.35rem; }
    .cd-num { font-size:1.4rem !important; }
    .cd-box { padding:0.95rem 1.1rem; border-radius:16px; }
    .cd-meeting-label { font-size:0.7rem !important; margin-bottom:0.55rem !important; }
    .cd-meeting-name { font-size:0.95rem !important; }
    .cd-meeting-date { font-size:0.78rem !important; }
    .cd-meeting-photo { width:48px !important; height:48px !important; }
}
</style>
<div class="cd-wrap">
    <div class="cd-main">
        <div class="cd-label">&#9203; Mancano al viaggio</div>
        <div class="cd-num" id="cd">&#8212;</div>
    </div>
    <div class="cd-box">
        <div class="cd-meeting-label" style="font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:""" + BRAND_BLUE + """;margin-bottom:0.45rem;">&#128197; Prossimo incontro</div>
        <div style="display:flex;align-items:center;gap:0.6rem;">
            """ + prossimo_foto + """
            <div>
                <div class="cd-meeting-name" style="font-size:0.82rem;font-weight:700;color:""" + BRAND_BLUE + """;line-height:1.2;">""" + prossimo_titolo + """</div>
                <div class="cd-meeting-date" style="font-size:0.72rem;color:#5b6472;margin-top:0.15rem;">""" + prossimo_data_str + """</div>
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
    var s = Math.floor((t % 60000) / 1000);
    // Padding 0 sui secondi (sempre 2 cifre per stabilità visiva)
    var sStr = s < 10 ? '0' + s : s;
    // Su mobile usa font piu piccolo via classe
    var isMobile = window.innerWidth <= 600;
    var bigSize = isMobile ? "1.4rem" : "1.5rem";
    var smallSize = isMobile ? "0.72rem" : "0.78rem";
    el.innerHTML =
        "<span style='font-size:" + bigSize + ";font-weight:800;'>" + d + "</span><span style='font-size:" + smallSize + ";opacity:0.6;margin:0 0.3rem 0 0.05rem;'>g</span>" +
        "<span style='font-size:" + bigSize + ";font-weight:800;'>" + h + "</span><span style='font-size:" + smallSize + ";opacity:0.6;margin:0 0.3rem 0 0.05rem;'>h</span>" +
        "<span style='font-size:" + bigSize + ";font-weight:800;'>" + m + "</span><span style='font-size:" + smallSize + ";opacity:0.6;margin:0 0.3rem 0 0.05rem;'>m</span>" +
        "<span class='cd-sec' style='font-size:" + bigSize + ";font-weight:800;'>" + sStr + "</span><span style='font-size:" + smallSize + ";opacity:0.6;margin-left:0.05rem;'>s</span>";
    
    // Effetto "tick" giallo sui secondi
    var secEl = el.querySelector('.cd-sec');
    if (secEl) {
        secEl.classList.add('tick');
        setTimeout(function() { secEl.classList.remove('tick'); }, 150);
    }
}
tick();
setInterval(tick, 1000);

// Resize iframe in base all'altezza reale del contenuto
function resizeIframe() {
    try {
        var wrap = document.querySelector('.cd-wrap');
        if (!wrap) return;
        var h = wrap.offsetHeight + 10; // +10px di margine
        // Trova l'iframe nel parent e ne aggiorna l'altezza
        var iframes = window.parent.document.querySelectorAll('iframe');
        for (var i = 0; i < iframes.length; i++) {
            if (iframes[i].contentWindow === window) {
                iframes[i].style.height = h + 'px';
                iframes[i].height = h;
                break;
            }
        }
    } catch (e) {}
}
window.addEventListener('load', resizeIframe);
window.addEventListener('resize', resizeIframe);
setTimeout(resizeIframe, 100);
setTimeout(resizeIframe, 500);
</script>
""")
components.html(countdown_html, height=220, scrolling=False)

# Dialog "L'opera che ci ispira" (popup quando si clicca sul bottone sotto)
@st.dialog(" ", width="large")
def mostra_opera_ispira():
    if sguardi_b64:
        st.markdown(f"""
        <div style="position:relative;border-radius:18px;overflow:hidden;margin-bottom:1.2rem;box-shadow:0 12px 36px rgba(19,0,137,0.18);">
            <img src="data:{sguardi_mime};base64,{sguardi_b64}" alt="Sguardi - Muro degli Occhi a Peccioli"
                 style="width:100%;height:auto;display:block;aspect-ratio:3/2;object-fit:cover;">
            <div style="position:absolute;bottom:14px;left:14px;background:{BRAND_BLUE};color:white;padding:0.5rem 1rem;border-radius:999px;font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;box-shadow:0 4px 14px rgba(0,0,0,0.25);">
                "Sguardi" · <span style="color:{BRAND_YELLOW};">Peccioli</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;aspect-ratio:3/2;background:linear-gradient(135deg,{BRAND_BLUE},#1a2f6c);color:{BRAND_YELLOW};font-family:'Playfair Display',Georgia,serif;font-style:italic;font-size:1rem;text-align:center;padding:2rem;border-radius:18px;margin-bottom:1.2rem;">
            📷 Foto del Muro degli Occhi<br><span style="font-size:0.75rem;opacity:0.75;font-style:normal;">(da caricare nel repo come sguardi_peccioli.jpg)</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:0.5rem;">
        <span style="display:inline-block;font-size:0.7rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:{BRAND_BLUE};background:{BRAND_YELLOW};padding:0.4rem 0.9rem;border-radius:999px;margin-bottom:1rem;">L'opera che ci ispira</span>
        <h2 style="font-family:'Playfair Display',Georgia,serif;font-weight:800;font-size:1.8rem;line-height:1.1;margin-bottom:0.3rem;color:{BRAND_BLUE};">Lo sguardo di Peccioli</h2>
        <div style="font-family:'Lobster Two',cursive;font-style:italic;font-size:1.2rem;color:{BRAND_BLUE};margin-bottom:1.3rem;opacity:0.7;">Vittorio Corsini, 2017</div>
        <p style="font-size:0.98rem;line-height:1.7;color:#2a3140;margin-bottom:0.9rem;">
            In Via Borgherucci, su una terrazza che guarda la vallata, una parete
            è punteggiata da decine di fotografie: gli <strong style="color:{BRAND_BLUE};">occhi degli abitanti di Peccioli</strong>.
            Azzurri, grigi, giovani o saggi, allegri o malinconici, fissano l'orizzonte
            aperto davanti a loro. Una moltitudine di sguardi rivolti idealmente al futuro,
            consapevoli di essere parte di una comunità che cresce trasformandosi —
            accogliendo il nuovo e mantenendo la forza delle proprie radici.
        </p>
        <p style="font-size:0.98rem;line-height:1.7;color:#2a3140;margin-bottom:0.6rem;">
            L'opera di Vittorio Corsini è stata esposta anche a <strong style="color:{BRAND_BLUE};">New York</strong>,
            portando lo sguardo di Peccioli oltre i confini italiani.
            Ed è proprio da quest'opera che nasce il nostro progetto:
            <strong style="color:{BRAND_BLUE};">tanti ragazzi che, partendo dagli occhi di Peccioli,
            si aprono al mondo e arrivano fino a New Orleans</strong> —
            con sguardi attenti, curiosi, pronti a tornare cambiati.
        </p>
    </div>
    """, unsafe_allow_html=True)

if "show_opera" not in st.session_state:
    st.session_state.show_opera = False
if st.session_state.show_opera:
    mostra_opera_ispira()
    st.session_state.show_opera = False

st.markdown(f"""
<div style="background:{BRAND_BLUE_LIGHT};border-radius:18px;padding:1.1rem 1.3rem;margin:1rem 0 0.6rem;border-left:4px solid {BRAND_YELLOW};">
    <p style="font-size:0.98rem;color:{BRAND_BLUE};line-height:1.65;margin:0;font-style:italic;">
        <strong style="font-style:normal;">Peccioli Eyes</strong> è uno sguardo che parte dal nostro piccolo territorio e si apre al mondo, mettendo al centro i giovani, la cultura e l'esperienza.
    </p>
</div>
""", unsafe_allow_html=True)

# Bottone trigger del popup opera (discreto, vicino alla descrizione)
col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
with col_btn_center:
    if st.button("👁  Da dove viene il nome \"Peccioli Eyes\"?", key="btn_opera_ispira", use_container_width=True):
        st.session_state.show_opera = True
        st.rerun()

st.markdown(f"""
<div style="display:flex;align-items:center;gap:1rem;margin:1.5rem 0 0.8rem;">
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

# ============================================================================
# 📊 STATISTICHE DEL VIAGGIO (collassabili)
# ============================================================================
st.markdown(f"""
<style>
.stats-section {{
    margin: 1.5rem 0 1.5rem;
}}
.stats-toggle {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.7rem;
    width: 100%;
    max-width: 360px;
    margin: 0 auto;
    padding: 0.7rem 1.2rem;
    background: white;
    border: 1px solid rgba(19,0,137,0.12);
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
    color: {BRAND_BLUE};
    box-shadow: 0 2px 8px rgba(19,0,137,0.05);
    -webkit-tap-highlight-color: transparent;
}}
.stats-toggle:hover {{
    background: {BRAND_YELLOW_LIGHT};
    border-color: {BRAND_YELLOW};
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(19,0,137,0.1);
}}
.stats-toggle-icon {{
    font-size: 1rem;
}}
.stats-toggle-text {{
    font-family: 'Lobster Two', cursive;
    font-style: italic;
    font-size: 1.1rem;
    font-weight: 700;
    color: {BRAND_BLUE};
    flex: 1;
    text-align: left;
}}
.stats-toggle-eyebrow {{
    display: block;
    font-family: 'Inter', sans-serif;
    font-style: normal;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {BRAND_BLUE};
    opacity: 0.55;
    margin-bottom: 0.1rem;
    line-height: 1;
}}
.stats-toggle-arrow {{
    font-size: 1rem;
    color: {BRAND_BLUE};
    transition: transform 0.3s ease;
    flex-shrink: 0;
}}
.stats-toggle.open .stats-toggle-arrow {{
    transform: rotate(180deg);
}}

.stats-content {{
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.45s ease-out, margin-top 0.3s ease-out;
    margin-top: 0;
}}
.stats-content.open {{
    max-height: 1200px;
    margin-top: 1rem;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}}
.stat-card {{
    background: white;
    border-radius: 18px;
    padding: 1.1rem 1rem 1rem;
    text-align: center;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 4px 14px rgba(19,0,137,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}}
.stat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(19,0,137,0.12);
}}
.stat-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: {BRAND_YELLOW};
}}
.stat-icon {{
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
    display: block;
}}
.stat-value {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: {BRAND_BLUE};
    line-height: 1;
    margin-bottom: 0.2rem;
}}
.stat-value-suffix {{
    font-size: 0.78rem;
    color: #5b6472;
    font-weight: 600;
    margin-left: 0.15rem;
}}
.stat-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #667;
    margin-top: 0.25rem;
}}
.stat-sub {{
    font-size: 0.7rem;
    color: #8b8b9a;
    margin-top: 0.2rem;
    line-height: 1.3;
}}
@media (max-width: 700px) {{
    .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 0.6rem;
    }}
    .stat-card {{ padding: 0.9rem 0.7rem 0.8rem; }}
    .stat-value {{ font-size: 1.35rem; }}
    .stat-icon {{ font-size: 1.3rem; }}
    .stats-toggle-text {{ font-size: 1rem; }}
}}
</style>

<div class="stats-section">
    <button class="stats-toggle" id="statsToggle" type="button" aria-expanded="false">
        <span class="stats-toggle-icon">📊</span>
        <span class="stats-toggle-text">
            <span class="stats-toggle-eyebrow">Il viaggio in numeri</span>
            Scopri di più
        </span>
        <span class="stats-toggle-arrow">▾</span>
    </button>
    <div class="stats-content" id="statsContent">
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon">✈️</span>
                <div class="stat-value">8.234<span class="stat-value-suffix">km</span></div>
                <div class="stat-label">Distanza</div>
                <div class="stat-sub">Da Peccioli a New Orleans</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🕐</span>
                <div class="stat-value">−7<span class="stat-value-suffix">h</span></div>
                <div class="stat-label">Fuso orario</div>
                <div class="stat-sub">Quando da noi è mezzogiorno, lì sono le 5 del mattino</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🛫</span>
                <div class="stat-value">~12<span class="stat-value-suffix">h</span></div>
                <div class="stat-label">Volo</div>
                <div class="stat-sub">Milano → Chicago → New Orleans</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">👥</span>
                <div class="stat-value">376<span class="stat-value-suffix">mila</span></div>
                <div class="stat-label">Abitanti NOLA</div>
                <div class="stat-sub">Peccioli ne ha ~4.500</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🌡️</span>
                <div class="stat-value">28°<span class="stat-value-suffix">C</span></div>
                <div class="stat-label">Temperatura</div>
                <div class="stat-sub">Media a settembre, umidità alta</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">⚜️</span>
                <div class="stat-value">1718</div>
                <div class="stat-label">Fondazione NOLA</div>
                <div class="stat-sub">Più antica degli Stati Uniti, fondata dai francesi</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript per il toggle delle statistiche
components.html("""
<script>
(function() {
    function setupStatsToggle() {
        const doc = window.parent.document;
        const btn = doc.getElementById('statsToggle');
        const content = doc.getElementById('statsContent');
        if (!btn || !content || btn.dataset.ready === '1') return;
        btn.dataset.ready = '1';

        btn.addEventListener('click', () => {
            const isOpen = btn.classList.contains('open');
            if (isOpen) {
                btn.classList.remove('open');
                content.classList.remove('open');
                btn.setAttribute('aria-expanded', 'false');
            } else {
                btn.classList.add('open');
                content.classList.add('open');
                btn.setAttribute('aria-expanded', 'true');
            }
        });
    }

    if (window.parent.document.readyState === 'complete') {
        setTimeout(setupStatsToggle, 400);
    } else {
        window.parent.addEventListener('load', () => setTimeout(setupStatsToggle, 400));
    }
})();
</script>
""", height=0)

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
# 👁 TEMI — GIALLO CHIARO — 8 SGUARDI
# ============================================================================
st.markdown(f"""
<span id="temi" class="section-anchor"></span>
<div class="section-wrap sec-temi">
    <span class="section-eyebrow">01 · Come guardare la città</span>
    <div class="section-title">Otto sguardi su New Orleans</div>
    <div class="section-subtitle">Le chiavi di lettura del viaggio</div>
    <p class="section-desc">
        Non quattro categorie separate, ma otto prospettive da tenere sempre attive durante il viaggio.
        Ogni sguardo è un modo diverso di osservare la stessa città — la sua storia, le sue voci, il suo ritmo, le sue contraddizioni.
        Insieme compongono un ritratto plurale di New Orleans, fedele alla complessità del luogo.
    </p>
</div>
<div class="section-body sec-temi">
""", unsafe_allow_html=True)

# CSS specifico per le card "Sguardi" — versione snella ed elegante
st.markdown("""
<style>
.sguardo-card {
    position: relative;
    background: white;
    border-radius: 20px;
    padding: 1.8rem 1.6rem 1.6rem;
    border: 1px solid rgba(19,0,137,0.08);
    box-shadow: 0 6px 20px rgba(19,0,137,0.05);
    overflow: hidden;
    height: 100%;
    transition: transform 0.25s, box-shadow 0.25s;
    margin-bottom: 1rem;
}
.sguardo-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(19,0,137,0.12);
}
.sguardo-card.dark {
    background: linear-gradient(160deg, #130089 0%, #1a0fb8 100%);
    color: white;
    border: 1px solid rgba(255,222,89,0.25);
}
/* Numero gigante decorativo sullo sfondo */
.sguardo-numero {
    position: absolute;
    top: -28px;
    right: 8px;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 10rem;
    font-weight: 800;
    color: #130089;
    opacity: 0.05;
    line-height: 1;
    pointer-events: none;
    user-select: none;
    letter-spacing: -0.04em;
}
.sguardo-card.dark .sguardo-numero {
    color: #FFDE59;
    opacity: 0.11;
}
/* Header: icona + label inline */
.sguardo-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.1rem;
    position: relative;
    z-index: 1;
}
.sguardo-icona {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 52px; height: 52px;
    border-radius: 14px;
    background: #FFDE59;
    font-size: 1.7rem;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(255,222,89,0.45);
}
.sguardo-eyebrow {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #130089;
    opacity: 0.5;
    line-height: 1;
}
.sguardo-card.dark .sguardo-eyebrow {
    color: #FFDE59;
    opacity: 0.85;
}
.sguardo-titolo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.65rem;
    font-weight: 800;
    color: #130089;
    line-height: 1.05;
    margin-bottom: 0.3rem;
    position: relative;
    z-index: 1;
    letter-spacing: -0.01em;
}
.sguardo-card.dark .sguardo-titolo {
    color: white;
}
.sguardo-sub {
    font-family: 'Lobster Two', cursive;
    font-style: italic;
    font-size: 1.05rem;
    color: #130089;
    opacity: 0.65;
    margin-bottom: 1.3rem;
    line-height: 1.3;
    position: relative;
    z-index: 1;
}
.sguardo-card.dark .sguardo-sub {
    color: #FFDE59;
    opacity: 0.92;
}
/* Linea divisoria gialla */
.sguardo-divider {
    width: 36px;
    height: 2px;
    background: #FFDE59;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
    border-radius: 2px;
}
/* Blocchi di testo: label piccola + paragrafo */
.sguardo-block {
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}
.sguardo-block:last-child {
    margin-bottom: 0;
}
.sguardo-label {
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #130089;
    opacity: 0.55;
    margin-bottom: 0.3rem;
}
.sguardo-card.dark .sguardo-label {
    color: #FFDE59;
    opacity: 0.85;
}
.sguardo-text {
    font-size: 0.92rem;
    line-height: 1.55;
    color: #3a4a5c;
}
.sguardo-card.dark .sguardo-text {
    color: rgba(255,255,255,0.92);
}
@media (max-width: 720px) {
    .sguardo-numero { font-size: 7rem; top: -18px; }
    .sguardo-titolo { font-size: 1.4rem; }
    .sguardo-card { padding: 1.5rem 1.3rem 1.3rem; }
    .sguardo-icona { width: 46px; height: 46px; font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# Definizione degli 8 sguardi — versione snella
sguardi = [
    {
        "n": "01", "icona": "🏛️", "titolo": "Sguardo Storico", "sub": "Le radici",
        "focus": "La stratificazione coloniale, il quartiere francese, l'eredità spagnola e africana.",
        "missione": "Trovare le tracce del passato che sopravvivono nel presente.",
        "dark": False,
    },
    {
        "n": "02", "icona": "🌊", "titolo": "Sguardo Politico", "sub": "Il potere e il fiume",
        "focus": "Il porto di New Orleans, il ruolo del Mississippi nell'economia globale, le relazioni internazionali.",
        "missione": "Raccontare come una città del Sud parli al mondo intero.",
        "dark": True,
    },
    {
        "n": "03", "icona": "🤝", "titolo": "Sguardo Sociale", "sub": "Contrasti americani",
        "focus": "Le contraddizioni della società americana: ricchezza e povertà, gentrificazione, questioni razziali.",
        "missione": "Osservare le due Americhe che convivono nello stesso isolato.",
        "dark": False,
    },
    {
        "n": "04", "icona": "🎷", "titolo": "Sguardo Sonoro", "sub": "Il ritmo del Delta",
        "focus": "Jazz, blues, second lines, musicisti di strada di Frenchmen Street.",
        "missione": "Catturare il rumore della città. Non solo musica, ma chi la vive come lavoro.",
        "dark": True,
    },
    {
        "n": "05", "icona": "🏚️", "titolo": "Sguardo Resiliente", "sub": "L'acqua e la ricostruzione",
        "focus": "L'eredità di Katrina, il cambiamento climatico, l'architettura della sopravvivenza.",
        "missione": "Raccontare come una comunità si rialza dopo il disastro.",
        "dark": False,
    },
    {
        "n": "06", "icona": "🍲", "titolo": "Sguardo Gastronomico", "sub": "Il melting pot nel piatto",
        "focus": "Cucina Creole e Cajun, il rito del gumbo e dei beignets, i mercati locali.",
        "missione": "Spiegare la cultura attraverso il cibo, come fusione di popoli.",
        "dark": True,
    },
    {
        "n": "07", "icona": "🔮", "titolo": "Sguardo Mistico", "sub": "Spiritualità e tradizioni",
        "focus": "Il voodoo, i cimiteri monumentali, il Mardi Gras, il folklore.",
        "missione": "Indagare la parte invisibile di New Orleans — magia e riti comunitari.",
        "dark": False,
    },
    {
        "n": "08", "icona": "👁️", "titolo": "Sguardo Umano", "sub": "Humans of NOLA",
        "focus": "I volti delle persone, l'accoglienza del Sud, le storie individuali.",
        "missione": "La squadra più vicina all'installazione di Peccioli: incrociare lo sguardo dei locali.",
        "dark": True,
    },
]

# Render: 2 colonne, alterna chiare/scure
col_s1, col_s2 = st.columns(2, gap="small")

for i, s in enumerate(sguardi):
    target_col = col_s1 if i % 2 == 0 else col_s2
    card_class = "sguardo-card dark" if s.get("dark") else "sguardo-card"
    
    card_html = (
        f'<div class="{card_class}">'
        f'<div class="sguardo-numero">{s["n"]}</div>'
        f'<div class="sguardo-header">'
        f'<div class="sguardo-icona">{s["icona"]}</div>'
        f'<div class="sguardo-eyebrow">Sguardo {s["n"]}</div>'
        f'</div>'
        f'<div class="sguardo-titolo">{s["titolo"]}</div>'
        f'<div class="sguardo-sub">«{s["sub"]}»</div>'
        f'<div class="sguardo-divider"></div>'
        f'<div class="sguardo-block">'
        f'<div class="sguardo-label">Focus</div>'
        f'<div class="sguardo-text">{s["focus"]}</div>'
        f'</div>'
        f'<div class="sguardo-block">'
        f'<div class="sguardo-label">Missione</div>'
        f'<div class="sguardo-text">{s["missione"]}</div>'
        f'</div>'
        f'</div>'
    )
    
    with target_col:
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 📅 BRIEFING — BLU NAVY
# ============================================================================
st.markdown(f"""
<span id="briefing" class="section-anchor"></span>
<div class="section-wrap sec-briefing">
    <span class="section-eyebrow">02 · Prima del viaggio</span>
    <div class="section-title">Calendario</div>
    <div class="section-subtitle">Incontri, eventi e appuntamenti</div>
    <p class="section-desc">
        Tutte le date che ci accompagnano fino alla partenza: tre serate con esperti per arrivare a New Orleans con strumenti culturali già solidi, ed eventi sul territorio che aprono un ponte vivo tra Peccioli e la Louisiana.
    </p>
</div>
<div class="section-body sec-briefing brief-section">
""", unsafe_allow_html=True)

briefing_full = [
    {
        "data": "7 maggio", "ora": "ore 21", "giorno": "Giovedì",
        "day_num": "7", "month": "Maggio",
        "titolo": "Elia Morelli",
        "ruolo": "Ricercatore in storia moderna · Università di Pisa",
        "bio": "Ricercatore in storia moderna all'Università di Pisa. Come analista geopolitico, scrive per Domino, rivista edita da Enrico Mentana. Membro della Società Italiana per la Storia dell'Età Moderna, della Società Italiana per lo Studio della Storia Contemporanea e della Renaissance Society of America.",
        "tema": "Storia culturale, politico-economica e geopolitica di New Orleans e della Louisiana.",
        "foto": expert_paths["morelli"],
        "foto_b64": morelli_b64_tl, "foto_mime": morelli_mime_tl,
        "emoji": "🏛", "colore": BRAND_YELLOW,
    },
    {
        "data": "21 maggio", "ora": "ore 21", "giorno": "Giovedì",
        "day_num": "21", "month": "Maggio",
        "titolo": "Anthony Gardner",
        "ruolo": "Ex ambasciatore USA all'UE · Consiglio di sicurezza nazionale",
        "bio": "Ex ambasciatore degli Stati Uniti presso l'Unione Europea dal 2014 al 2017 su nomina del presidente Obama. Ha lavorato per oltre vent'anni sulle relazioni tra USA ed Europa, su temi come i negoziati commerciali transatlantici, la privacy dei dati, l'economia digitale e la sicurezza energetica.",
        "tema": "Sguardo istituzionale e geopolitico: il ruolo di New Orleans e il rapporto tra USA ed Europa.",
        "foto": expert_paths["gardner"],
        "foto_b64": gardner_b64_tl, "foto_mime": gardner_mime_tl,
        "emoji": "🌐", "colore": BRAND_YELLOW,
    },
    {
        "data": "18 giugno", "ora": "ore 21", "giorno": "Giovedì",
        "day_num": "18", "month": "Giugno",
        "titolo": "Francesco Costa",
        "ruolo": "Giornalista · Direttore de Il Post",
        "bio": "Direttore responsabile de Il Post. Tra i principali divulgatori italiani sulla società e politica americana, autore di libri e progetti dedicati agli Stati Uniti. Dal 2021 al 2025 ha condotto per il Post il podcast giornaliero Morning, una rassegna stampa commentata che è stata definita \"il primo vero podcast daily italiano\".",
        "tema": "Punto di vista sociale, narrativo e attuale sugli Stati Uniti: leggere l'America oltre gli stereotipi.",
        "foto": expert_paths["costa"],
        "foto_b64": costa_b64_tl, "foto_mime": costa_mime_tl,
        "emoji": "📰", "colore": BRAND_YELLOW,
    },
    {
        "tipo": "evento",
        "data": "7-11 luglio", "ora": "5 giorni", "giorno": "Mar-Sab",
        "day_num": "7-11", "month": "Luglio",
        "titolo": "Jazz Peccioli 2026",
        "ruolo": "Festival jazz · Peccioli ↔ New Orleans",
        "bio": "Dal 7 all'11 luglio Peccioli si riempirà di musica e suoni aprendo un ponte simbolico e culturale con New Orleans. Il festival, nato dal gemellaggio ufficiale tra il Comune di Peccioli e New Orleans, vedrà protagonista la New Orleans Jazz Orchestra, affiancata da artisti di rilievo internazionale. Le parate quotidiane della LSU Brass Band animeranno il centro con l'energia inconfondibile della tradizione second line.",
        "tema": "Concerti, parate, workshop. Un'anteprima dal vivo di NOLA, qui a Peccioli.",
        "foto": jazz_logo_path,
        "foto_b64": jazz_logo_b64, "foto_mime": jazz_logo_mime,
        "emoji": "🎺", "colore": BRAND_YELLOW,
        "link_sito": "https://www.jazzpeccioli.com",
        "link_instagram": "https://www.instagram.com/jazzpeccioli/",
    },
    # =====================================================================
    # PER AGGIUNGERE NUOVE DATE / INCONTRI / SCADENZE:
    # Copia uno dei blocchi sopra e modifica i valori. Esempio sotto.
    # Per nascondere temporaneamente un evento, commenta tutto il blocco
    # mettendo # davanti a ogni riga (oppure cancellalo).
    # =====================================================================
    # ESEMPIO SCADENZA (decommentare per attivare):
    # {
    #     "tipo": "scadenza",
    #     "data": "15 luglio", "ora": "entro le 23:59", "giorno": "Martedì",
    #     "day_num": "15", "month": "Luglio",
    #     "titolo": "Scadenza documenti",
    #     "ruolo": "Consegna documenti firmati al Comune",
    #     "bio": "Tutti i documenti firmati dai genitori devono essere consegnati all'ufficio del Comune di Peccioli entro questa data.",
    #     "tema": "Modulo adesione, copia documento d'identità, modulo sanitario.",
    #     "foto": None,
    #     "foto_b64": None, "foto_mime": None,
    #     "emoji": "📋", "colore": BRAND_YELLOW,
    # },
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

# === TIMELINE HTML ===
# CSS della timeline (definito una volta)
timeline_css = f"""
<style>
.brief-timeline {{
    position: relative;
    max-width: 860px;
    margin: 0 auto;
    padding-left: 0;
}}
.brief-timeline::before {{
    content: "";
    position: absolute;
    left: 48px;
    top: 40px;
    bottom: 40px;
    width: 3px;
    background: linear-gradient(to bottom,
        {BRAND_YELLOW} 0%,
        {BRAND_YELLOW} 40%,
        rgba(255,222,89,0.5) 75%,
        rgba(255,222,89,0.2) 100%);
    border-radius: 2px;
    z-index: 0;
}}
.brief-step {{
    position: relative;
    padding-left: 120px;
    margin-bottom: 2.2rem;
}}
.brief-step:last-child {{
    margin-bottom: 0;
}}
.brief-marker {{
    position: absolute;
    left: 10px;
    top: 10px;
    width: 78px;
    height: 78px;
    border-radius: 50%;
    background: {BRAND_YELLOW};
    color: {BRAND_BLUE};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 0 4px {SEC_BRIEFING}, 0 4px 14px rgba(0,0,0,0.25);
    z-index: 2;
    line-height: 1;
    padding-top: 3px;
}}
.brief-marker .marker-day {{
    font-family: 'Playfair Display', Georgia, serif;
    font-weight: 800;
    font-size: 2rem;
    line-height: 1;
}}
/* Range di date (es. "7-11") con font ridotto */
.brief-marker .marker-day.range {{
    font-size: 1.25rem;
    letter-spacing: -0.02em;
}}
.brief-marker .marker-month {{
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}}
.brief-card {{
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    color: {BRAND_BLUE};
    display: grid;
    grid-template-columns: 200px 1fr;
    min-height: 220px;
}}
.brief-photo {{
    position: relative;
    background: linear-gradient(135deg, {BRAND_BLUE}, {SEC_BRIEFING});
    overflow: hidden;
}}
.brief-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}
.brief-photo-emoji {{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;
    color: {BRAND_YELLOW};
}}

/* === STILE CARD TIPO "EVENTO" (differenziato dagli esperti) === */
.brief-card.evento {{
    background: linear-gradient(135deg, {BRAND_BLUE} 0%, #1a0fb8 100%);
    color: white;
    border: 2px solid {BRAND_YELLOW};
}}
.brief-card.evento .brief-photo {{
    background: linear-gradient(135deg, {BRAND_BLUE_DARK} 0%, {BRAND_BLUE} 100%);
    position: relative;
}}
.brief-card.evento .brief-photo-emoji {{
    color: {BRAND_YELLOW};
    font-size: 4.5rem;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
}}
/* Logo evento (es. Jazz Peccioli) - mantenuto intero, sfondo bianco */
.evento-logo-wrap {{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    padding: 1.2rem;
}}
.evento-logo {{
    max-width: 80%;
    max-height: 80%;
    object-fit: contain;
    filter: drop-shadow(0 4px 14px rgba(0,0,0,0.15));
}}
.brief-card.evento .brief-time {{
    color: {BRAND_YELLOW};
    opacity: 0.95;
}}
.brief-card.evento .brief-name {{
    color: white;
}}
.brief-card.evento .brief-role {{
    color: rgba(255,255,255,0.8);
}}
.brief-card.evento .brief-tema {{
    background: rgba(255,222,89,0.15);
    color: white;
    border-left-color: {BRAND_YELLOW};
}}
.evento-badge {{
    position: absolute;
    top: 0.7rem;
    left: 0.7rem;
    background: {BRAND_YELLOW};
    color: {BRAND_BLUE};
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    z-index: 2;
}}
.evento-links {{
    display: flex;
    gap: 0.5rem;
    margin-top: 0.9rem;
    flex-wrap: wrap;
}}
.evento-link {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,222,89,0.4);
    color: white !important;
    text-decoration: none !important;
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    transition: all 0.2s;
}}
.evento-link:hover {{
    background: {BRAND_YELLOW};
    color: {BRAND_BLUE} !important;
    border-color: {BRAND_YELLOW};
    transform: translateY(-2px);
}}
.brief-content {{
    padding: 1.3rem 1.5rem 1.3rem;
    display: flex;
    flex-direction: column;
}}
.brief-time {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #667;
    margin-bottom: 0.25rem;
}}
.brief-name {{
    font-family: 'Playfair Display', Georgia, serif;
    font-weight: 800;
    font-size: 1.4rem;
    line-height: 1.15;
    margin-bottom: 0.3rem;
    color: {BRAND_BLUE};
}}
.brief-role {{
    font-size: 0.8rem;
    color: #5b6472;
    margin-bottom: 0.85rem;
    line-height: 1.4;
}}
.brief-tema {{
    font-size: 0.84rem;
    color: #3a4a5c;
    line-height: 1.55;
    padding: 0.7rem 0.95rem;
    background: {BRAND_BLUE_LIGHT};
    border-left: 3px solid {BRAND_YELLOW};
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.3rem;
    flex: 1;
}}
@media (max-width: 720px) {{
    .brief-timeline::before {{ left: 30px; top: 30px; bottom: 30px; }}
    .brief-step {{ padding-left: 75px; margin-bottom: 1.6rem; }}
    .brief-marker {{
        left: 0;
        top: 6px;
        width: 60px;
        height: 60px;
        box-shadow: 0 0 0 3px {SEC_BRIEFING}, 0 3px 10px rgba(0,0,0,0.2);
    }}
    .brief-marker .marker-day {{ font-size: 1.5rem; }}
    .brief-marker .marker-month {{ font-size: 0.52rem; margin-top: 2px; }}
    .brief-card {{
        grid-template-columns: 1fr;
        min-height: auto;
        border-radius: 16px;
    }}
    .brief-photo {{
        height: 180px;
    }}
    .brief-content {{ padding: 1rem 1.1rem 1.1rem; }}
    .brief-name {{ font-size: 1.2rem; }}
    .brief-role {{ font-size: 0.78rem; }}
    .brief-tema {{ font-size: 0.82rem; padding: 0.6rem 0.8rem; }}
}}
</style>
"""

st.markdown(timeline_css, unsafe_allow_html=True)

# Rendering timeline: parte HTML + pulsanti Streamlit sottostanti
st.markdown('<div class="brief-timeline">', unsafe_allow_html=True)

# Abbreviazioni mesi per il pallino (maiuscolo)
month_abbr = {"Maggio": "MAG", "Giugno": "GIU", "Luglio": "LUG", "Aprile": "APR", "Settembre": "SET", "Ottobre": "OTT", "Novembre": "NOV", "Dicembre": "DIC", "Gennaio": "GEN", "Febbraio": "FEB", "Marzo": "MAR", "Agosto": "AGO"}

for i, b in enumerate(briefing_full):
    tipo_card = b.get("tipo", "esperto")
    
    # Foto: logica diversa per evento (logo contained) vs esperto (foto cover)
    if b["foto_b64"]:
        if tipo_card == "evento":
            # Logo: sfondo bianco, contenuto centrato, non tagliato
            photo_block = f'<div class="evento-logo-wrap"><img src="data:{b["foto_mime"]};base64,{b["foto_b64"]}" alt="{b["titolo"]}" class="evento-logo"></div>'
        else:
            # Foto persona: cover, riempie tutto
            photo_block = f'<img src="data:{b["foto_mime"]};base64,{b["foto_b64"]}" alt="{b["titolo"]}">'
    else:
        photo_block = f'<div class="brief-photo-emoji">{b["emoji"]}</div>'

    month_short = month_abbr.get(b["month"], b["month"][:3].upper())
    
    # Classe per giorno (range tipo "7-11" usa font ridotto)
    day_class = "marker-day range" if "-" in str(b["day_num"]) else "marker-day"
    
    # Card class + badge + links per tipo evento
    card_class = "brief-card"
    badge_html = ""
    links_html = ""
    
    if tipo_card == "evento":
        card_class = "brief-card evento"
        badge_html = '<div class="evento-badge">🎺 Festival</div>'
        # Link Instagram + sito se presenti
        link_parts = []
        if b.get("link_sito"):
            link_parts.append(f'<a class="evento-link" href="{b["link_sito"]}" target="_blank" rel="noopener">🌐 Sito ufficiale</a>')
        if b.get("link_instagram"):
            link_parts.append(f'<a class="evento-link" href="{b["link_instagram"]}" target="_blank" rel="noopener">📷 Instagram</a>')
        if link_parts:
            links_html = '<div class="evento-links">' + "".join(link_parts) + '</div>'

    st.markdown(f"""<div class="brief-step">
<div class="brief-marker">
<span class="{day_class}">{b["day_num"]}</span>
<span class="marker-month">{month_short}</span>
</div>
<div class="{card_class}">
<div class="brief-photo">
{badge_html}
{photo_block}
</div>
<div class="brief-content">
<div class="brief-time">{b["giorno"]} · {b["ora"]}</div>
<div class="brief-name">{b["titolo"]}</div>
<div class="brief-role">{b["ruolo"]}</div>
<div class="brief-tema">{b["tema"]}</div>
{links_html}
</div>
</div>
</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Pulsanti "Scopri di più" sotto (stile coerente con la timeline)
# Solo per ESPERTI (escludo eventi e scadenze)
eventi_con_bio = [b for b in briefing_full if b.get("bio") and b.get("foto") is not None and b.get("tipo", "esperto") == "esperto"]
if eventi_con_bio:
    n_eventi = len(eventi_con_bio)
    grid_cols = min(n_eventi, 4)  # max 4 per riga su desktop
    st.markdown(f'<div style="max-width:860px;margin:1.5rem auto 0;display:grid;grid-template-columns:repeat({grid_cols},1fr);gap:0.7rem;">', unsafe_allow_html=True)
    btn_cols = st.columns(grid_cols)
    for i, b in enumerate(eventi_con_bio):
        with btn_cols[i % grid_cols]:
            # Ricavo l'indice originale per riferirsi al dialog corretto
            idx_originale = briefing_full.index(b)
            if st.button(f"▸ Scopri {b['titolo'].split()[0]}", key=f"dialog_{idx_originale}", use_container_width=True):
                st.session_state.dialog_idx = idx_originale
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
        14 luoghi simbolici organizzati per tema. Esplora la mappa interattiva qui sotto
        o scorri le schede per conoscerli uno a uno.
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

@st.fragment
def mostra_mappa():
    # Vista centrale tra tutti i punti - zoom ampio per vedere anche Lake Pontchartrain
    m = folium.Map(
        location=[29.975, -90.065],
        zoom_start=12,
        tiles="CartoDB positron",
        control_scale=True,
    )

    # Aree semi-trasparenti per tema (cluster visivi)
    # Disegnate PRIMA dei marker così stanno sotto
    # Identità: raggruppa French Quarter, Jackson Square, St. Louis Cemetery
    folium.Circle(
        location=[29.958, -90.067], radius=650,
        color=COL_IDENTITA, fill=True, fill_color=COL_IDENTITA,
        fill_opacity=0.08, opacity=0.25, weight=1,
    ).add_to(m)
    # Musica: raggruppa Frenchmen Street + Congo Square + Armstrong Park + Preservation Hall
    folium.Circle(
        location=[29.961, -90.063], radius=700,
        color=COL_MUSICA, fill=True, fill_color=COL_MUSICA,
        fill_opacity=0.08, opacity=0.25, weight=1,
    ).add_to(m)
    # Resilienza: Lower Ninth + Make It Right
    folium.Circle(
        location=[29.971, -90.017], radius=550,
        color=COL_RESILIENZA, fill=True, fill_color=COL_RESILIENZA,
        fill_opacity=0.08, opacity=0.25, weight=1,
    ).add_to(m)

    # Marker custom con icone tematiche SVG
    for i, luogo in enumerate(luoghi_dati, start=1):
        icon_html = f'''
        <div style="
            position: relative;
            width: 34px; height: 34px;
            background: {luogo["colore"]};
            border: 2.5px solid white;
            border-radius: 50%;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            transform: translate(-17px, -17px);
        ">
            <div style="display:flex;align-items:center;justify-content:center;">
                {luogo["icona"]}
            </div>
            <div style="
                position: absolute;
                top: -7px; right: -7px;
                width: 18px; height: 18px;
                background: white;
                color: {luogo["colore"]};
                border-radius: 50%;
                font-size: 11px;
                font-weight: 800;
                font-family: 'Playfair Display', Georgia, serif;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            ">{i}</div>
        </div>
        '''

        popup_html = f'''
        <div style="font-family: 'Inter', sans-serif; min-width: 220px; max-width: 260px;">
            <img src="{luogo["foto"]}" loading="lazy"
                 style="width:100%; height:130px; object-fit:cover; border-radius:6px 6px 0 0; margin:-10px -10px 0 -10px; width:calc(100% + 20px); display:block;"
                 onerror="this.style.display='none';" alt="{luogo['nome']}">
            <div style="
                background: {luogo["colore"]};
                color: white;
                padding: 0.5rem 0.8rem;
                margin: 0 -10px 0.6rem -10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.5rem;
            ">
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;opacity:0.9;">
                    {luogo["tema"]}
                </div>
                <div style="
                    width: 22px; height: 22px;
                    background: white;
                    color: {luogo["colore"]};
                    border-radius: 50%;
                    font-size: 12px;
                    font-weight: 800;
                    font-family: 'Playfair Display', Georgia, serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">{i}</div>
            </div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.05rem;font-weight:800;color:{BRAND_BLUE};margin-bottom:0.4rem;line-height:1.2;padding:0 0.2rem;">
                {luogo["nome"]}
            </div>
            <div style="font-size:0.82rem;color:#3a4a5c;line-height:1.55;padding:0 0.2rem 0.2rem;">
                {luogo["desc"]}
            </div>
        </div>
        '''

        folium.Marker(
            location=[luogo["lat"], luogo["lon"]],
            icon=folium.DivIcon(
                html=icon_html,
                icon_size=(0, 0),
                icon_anchor=(0, 0),
            ),
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=folium.Tooltip(f"<b>{i}.</b> {luogo['nome']}", sticky=True),
        ).add_to(m)

    st_folium(m, width=None, height=520, use_container_width=True, returned_objects=[])

mostra_mappa()

st.markdown(f"""
<div style="margin-top:0.5rem;margin-bottom:1.2rem;font-size:0.82rem;color:rgba(255,255,255,0.8);font-style:italic;">
    Clicca sui marker per scoprire ciascun luogo. I numeri corrispondono alle schede qui sotto.
</div>
""", unsafe_allow_html=True)

# Cards dei luoghi con numerazione corrispondente
col_m1, col_m2 = st.columns(2)
for i, luogo in enumerate(luoghi_dati, start=1):
    with (col_m1 if (i - 1) % 2 == 0 else col_m2):
        st.markdown(f"""
        <div class="legend-card" style="border-left:4px solid {luogo['colore']};margin-bottom:0.6rem;position:relative;">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;">
                <div style="
                    flex-shrink:0;
                    width:28px;height:28px;
                    background:{luogo['colore']};
                    color:white;
                    border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Playfair Display',Georgia,serif;font-weight:800;font-size:0.85rem;
                ">{i}</div>
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:0.98rem;font-weight:800;color:{BRAND_BLUE};line-height:1.2;">{luogo['nome']}</div>
            </div>
            <div style="font-size:0.72rem;font-weight:700;color:{luogo['colore']};margin-bottom:0.35rem;letter-spacing:0.05em;text-transform:uppercase;">{luogo['tema']}</div>
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
    <div class="section-title">Risorse utili</div>
</div>
<div class="section-body sec-documenti">
    <div style="background:white;border-left:4px solid {BRAND_YELLOW};border-radius:0 12px 12px 0;
         padding:0.8rem 1.2rem;margin-bottom:1.4rem;font-size:0.88rem;color:{BRAND_BLUE};font-weight:500;box-shadow:0 2px 8px rgba(19,0,137,0.05);">
        📋 I documenti saranno caricati progressivamente nelle settimane prima della partenza.
    </div>
""", unsafe_allow_html=True)

import base64 as _base64

def file_to_b64(filename):
    """Carica un file dalla cartella del repo e lo restituisce come base64 per il download."""
    p = BASE_DIR / filename
    if p.exists():
        with open(p, "rb") as f:
            return _base64.b64encode(f.read()).decode("ascii")
    return None

# Lista documenti. Ogni voce ha:
#   - icona, titolo, descrizione
#   - filename: nome del file da caricare nel repo (None se non ancora disponibile)
#   - mime: tipo MIME del file (necessario per il download)
# Quando filename esiste nel repo, la card mostra un bottone "Scarica" cliccabile.
# Quando filename è None o il file non esiste, mostra "In arrivo".
documenti = [
    {"icona": "📊", "titolo": "Presentazione dell'incontro introduttivo", 
     "desc": "Slide del primo incontro di presentazione del progetto.",
     "filename": "doc_presentazione_introduttivo.pdf", "mime": "application/pdf"},
    {"icona": "📊", "titolo": "Presentazione di Elia Morelli", 
     "desc": "Slide dell'incontro con Elia Morelli sulla storia di New Orleans.",
     "filename": "doc_slide_morelli.pdf", "mime": "application/pdf"},
    {"icona": "🎧", "titolo": "Registrazione incontro Morelli",
     "desc": "Audio integrale dell'incontro con Elia Morelli (7 maggio 2026).",
     "filename": "audio_morelli.mp3", "mime": "audio/mpeg"},
    {"icona": "🎧", "titolo": "Registrazione incontro Gardner",
     "desc": "Audio integrale dell'incontro con Anthony Gardner (21 maggio 2026).",
     "filename": "audio_gardner.mp3", "mime": "audio/mpeg"},
    {"icona": "✈️", "titolo": "Prime informazioni sul viaggio",
     "desc": "Dettagli su volo, scalo e sistemazione a New Orleans.",
     "filename": "doc_info_viaggio.pdf", "mime": "application/pdf"},
    {"icona": "📱", "titolo": "Contatti e riferimenti",
     "desc": "Numeri di emergenza, referenti locali, chat di gruppo.",
     "filename": None, "mime": None},
]

for doc in documenti:
    icona = doc["icona"]
    titolo = doc["titolo"]
    desc = doc["desc"]
    
    # Controllo se il file esiste e genero blocco di download
    file_b64 = file_to_b64(doc["filename"]) if doc["filename"] else None
    
    if file_b64:
        # File presente: mostro bottone "Scarica" cliccabile
        # Estrae estensione per il nome del file scaricato
        download_filename = doc["filename"]
        stato_html = f'<a href="data:{doc["mime"]};base64,{file_b64}" download="{download_filename}" style="display:inline-block;background:{BRAND_BLUE};color:white;text-decoration:none;padding:0.45rem 0.95rem;border-radius:999px;font-size:0.72rem;font-weight:700;letter-spacing:0.04em;">⬇ Scarica</a>'
    else:
        # File non ancora caricato
        stato_html = f'<div style="font-size:0.72rem;font-weight:700;color:#9aa3b0;">⏳ In arrivo</div>'
    
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
            {stato_html}
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Libri", "🎬 Film e TV", "🎞 Documentari", "▶️ YouTube", "🌐 Risorse"])

with tab1:
    col_l1, col_l2 = st.columns(2)
    libri = [
        {"titolo": "Una banda di idioti", "autore": "John Kennedy Toole", "anno": "1980 · Pulitzer",
         "desc": "Capolavoro ambientato nella New Orleans degli anni '60. Satira geniale e irresistibile — il modo più divertente per entrare nell'anima della città.",
         "link": "https://it.wikipedia.org/wiki/Una_banda_di_idioti", "colore": BRAND_YELLOW},
        {"titolo": "Intervista col vampiro", "autore": "Anne Rice", "anno": "1976 · Gothic horror",
         "desc": "Il romanzo d'esordio di Anne Rice, nata a New Orleans. Louis, vampiro bicentenario, racconta la sua vita tra piantagioni della Louisiana e il French Quarter. 8+ milioni di copie vendute, ha inaugurato le Vampire Chronicles.",
         "link": "https://it.wikipedia.org/wiki/Intervista_col_vampiro_(romanzo)", "colore": "#4a3fb8"},
        {"titolo": "Blues Highway", "autore": "Rob Siebert", "anno": "Reportage narrativo",
         "desc": "Viaggio da Chicago a New Orleans sulle tracce delle origini della musica americana: blues, jazz, gospel. Per capire il legame tra musica e territorio.",
         "link": "https://marcosymarcos.com/libri/gli-alianti/blues-highway/", "colore": BRAND_BLUE},
        {"titolo": "The Moviegoer", "autore": "Walker Percy", "anno": "1961 · National Book Award",
         "desc": "Romanzo ambientato a New Orleans, vincitore del National Book Award. Racconta l'alienazione e la ricerca di senso di un giovane creolo nella città del Mardi Gras.",
         "link": "https://it.wikipedia.org/wiki/Walker_Percy", "colore": BRAND_BLUE},
        {"titolo": "L'ora delle streghe", "autore": "Anne Rice", "anno": "1990 · Gothic supernatural",
         "desc": "Saga della famiglia Mayfair, streghe del Garden District di New Orleans. Ambientato nella villa vittoriana dove Anne Rice visse davvero per 15 anni. Bestseller da milioni di copie, serie TV AMC dal 2023.",
         "link": "https://it.wikipedia.org/wiki/L%27ora_delle_streghe_(romanzo)", "colore": "#e6b800"},
        {"titolo": "Zeitoun", "autore": "Dave Eggers", "anno": "2009 · Non fiction",
         "desc": "La storia vera di un siriano-americano rimasto a New Orleans durante Katrina. Un racconto potente su resilienza, razzismo e fallimento istituzionale dopo la catastrofe.",
         "link": "https://it.wikipedia.org/wiki/Zeitoun_(libro)", "colore": BRAND_YELLOW},
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
         "desc": "Con Marlon Brando e Vivien Leigh. Classico assoluto girato nella New Orleans reale. 4 Oscar vinti.",
         "link": "https://www.imdb.com/title/tt0044081/", "colore": BRAND_YELLOW},
        {"titolo": "12 anni schiavo", "anno": "2013 · Steve McQueen",
         "desc": "Oscar come miglior film. Girato in Louisiana, racconta la schiavitù nelle piantagioni vicino a New Orleans. Duro ma essenziale per capire le radici del Sud americano.",
         "link": "https://www.imdb.com/title/tt2024544/", "colore": BRAND_BLUE},
        {"titolo": "Intervista col vampiro", "anno": "1994 · Neil Jordan",
         "desc": "Tom Cruise, Brad Pitt, Kirsten Dunst. Cattura l'atmosfera gotica e decadente della Louisiana.",
         "link": "https://www.imdb.com/title/tt0110632/", "colore": "#4a3fb8"},
        {"titolo": "Il curioso caso di Benjamin Button", "anno": "2008 · David Fincher",
         "desc": "New Orleans dal dopoguerra a Katrina come sfondo per una storia sull'identità e la memoria. 3 Oscar vinti.",
         "link": "https://www.imdb.com/title/tt0421715/", "colore": "#e6b800"},
        {"titolo": "Re della terra selvaggia", "anno": "2012 · Benh Zeitlin",
         "desc": "Nei bayou della Louisiana post-Katrina, la piccola Hushpuppy affronta l'apocalisse. 4 nomination Oscar. Favola poetica sulla resilienza della Louisiana.",
         "link": "https://www.imdb.com/title/tt2125435/", "colore": BRAND_YELLOW},
        {"titolo": "La principessa e il ranocchio", "anno": "2009 · Disney",
         "desc": "Ultima grande Disney disegnata a mano. Ambientata totalmente a New Orleans anni '20, con il jazz di Randy Newman. La prima principessa afroamericana Disney.",
         "link": "https://www.imdb.com/title/tt0780521/", "colore": BRAND_BLUE},
        {"titolo": "Treme", "anno": "2010–2013 · HBO",
         "desc": "La serie più importante su New Orleans dopo Katrina. Emmy Award. Da vedere assolutamente.",
         "link": "https://www.imdb.com/title/tt1279972/", "colore": "#4a3fb8"},
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
    st.markdown(f"""
    <div style="background:white;border-left:4px solid {BRAND_YELLOW};border-radius:0 12px 12px 0;
         padding:0.8rem 1.2rem;margin-bottom:1.4rem;font-size:0.88rem;color:{BRAND_BLUE};font-weight:500;box-shadow:0 2px 8px rgba(19,0,137,0.05);">
        ▶️ Sei video per entrare nell'atmosfera della città — geografia, cibo, musica, vita locale e camminate immersive.
    </div>
    """, unsafe_allow_html=True)

    youtube_videos = [
        {"titolo": "New Orleans Map, Explained",
         "canale": "Geography Now style · in inglese",
         "desc": "Guida visuale alla geografia di New Orleans: quartieri, fiume, lago, argini. Per orientarsi prima di partire.",
         "link": "https://www.youtube.com/watch?v=dC3CD7Ht0ek",
         "thumb": "https://img.youtube.com/vi/dC3CD7Ht0ek/hqdefault.jpg",
         "colore": BRAND_BLUE},
        {"titolo": "Following Bienville: The Founding of New Orleans",
         "canale": "Storia · documentario",
         "desc": "Sulle tracce di Jean-Baptiste Le Moyne de Bienville, fondatore di New Orleans: come nacque la città francese sul Mississippi.",
         "link": "https://www.youtube.com/watch?v=no2mKeSJbzk",
         "thumb": "https://img.youtube.com/vi/no2mKeSJbzk/hqdefault.jpg",
         "colore": "#e6b800"},
        {"titolo": "Peaceful French Quarter Walking Tour",
         "canale": "Walking tour · no music",
         "desc": "Camminata immersiva nel French Quarter di prima mattina, senza musica. Solo i suoni della città che si sveglia.",
         "link": "https://www.youtube.com/watch?v=grN4Oacu1fM",
         "thumb": "https://img.youtube.com/vi/grN4Oacu1fM/hqdefault.jpg",
         "colore": "#4a3fb8"},
        {"titolo": "La schiavitù senza filtri: 12 Anni Schiavo",
         "canale": "Analisi · cinema e storia",
         "desc": "Analisi del film di Steve McQueen sulla tratta degli schiavi: l'eredità più dolorosa della Louisiana raccontata attraverso il cinema.",
         "link": "https://www.youtube.com/watch?v=Y1HJvVVAZpg&t=206s",
         "thumb": "https://img.youtube.com/vi/Y1HJvVVAZpg/hqdefault.jpg",
         "colore": BRAND_YELLOW},
        {"titolo": "Billie Holiday & Louis Armstrong — New Orleans",
         "canale": "Musica · 1947",
         "desc": "Scena musicale dal film 'New Orleans' (1947): due leggende del jazz insieme. L'anima musicale della città in meno di 5 minuti.",
         "link": "https://www.youtube.com/watch?v=m4jU8IQK5b0",
         "thumb": "https://img.youtube.com/vi/m4jU8IQK5b0/hqdefault.jpg",
         "colore": "#4a3fb8"},
        {"titolo": "How to Experience New Orleans Like a Local",
         "canale": "Condé Nast Traveler · in inglese",
         "desc": "Internet vs Expert: due viaggiatori a confronto su come vivere davvero New Orleans, lontano dai cliché turistici.",
         "link": "https://www.youtube.com/watch?v=CiXF3IMwac4",
         "thumb": "https://img.youtube.com/vi/CiXF3IMwac4/hqdefault.jpg",
         "colore": BRAND_YELLOW},
    ]

    col_y1, col_y2 = st.columns(2)
    for i, v in enumerate(youtube_videos):
        with (col_y1 if i % 2 == 0 else col_y2):
            st.markdown(f"""
            <a href="{v['link']}" target="_blank" rel="noopener" style="text-decoration:none;">
                <div style="background:white;border-radius:18px;overflow:hidden;margin-bottom:1rem;
                     box-shadow:0 4px 16px rgba(19,0,137,0.08);
                     border-top:4px solid {v['colore']};">
                    <div style="position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;background:#000;">
                        <img src="{v['thumb']}" alt="{v['titolo']}"
                             style="width:100%;height:100%;object-fit:cover;display:block;">
                        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                             width:56px;height:56px;border-radius:50%;
                             background:rgba(255,0,0,0.9);
                             display:flex;align-items:center;justify-content:center;
                             box-shadow:0 3px 12px rgba(0,0,0,0.4);">
                            <div style="width:0;height:0;
                                 border-left:18px solid white;
                                 border-top:11px solid transparent;
                                 border-bottom:11px solid transparent;
                                 margin-left:4px;"></div>
                        </div>
                    </div>
                    <div style="padding:1rem 1.2rem 1.1rem;">
                        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                             color:{v['colore']};margin-bottom:0.3rem;">{v['canale']}</div>
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1rem;font-weight:800;
                             color:{BRAND_BLUE};line-height:1.25;margin-bottom:0.45rem;">{v['titolo']}</div>
                        <div style="font-size:0.83rem;color:#3a4a5c;line-height:1.55;">{v['desc']}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

with tab5:
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
        {"titolo": "🎙️ Podcast su New Orleans — Spotify",
         "desc": "Episodio podcast da ascoltare per entrare nell'atmosfera della città prima del viaggio.",
         "link": "https://open.spotify.com/episode/0bUQRduCBPvvkbqwue4pQ3", "colore": "#1DB954"},
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

# ============================================================================
# 📞 CONTATTI UTILI
# ============================================================================
# CSS della sezione contatti (separato per evitare problemi di rendering)
contatti_css = """
<style>
.contatti-section {
    margin: 3rem 0 2rem;
    padding: 2.2rem 2rem;
    background: linear-gradient(165deg, #f8f7ff 0%, #fff 100%);
    border-radius: 20px;
    border: 1px solid rgba(19,0,137,0.08);
}
.contatti-eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #130089;
    opacity: 0.6;
    margin-bottom: 0.4rem;
    text-align: center;
}
.contatti-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-weight: 800;
    font-size: 1.8rem;
    color: #130089;
    margin-bottom: 0.3rem;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}
.contatti-sub {
    font-family: 'Lobster Two', cursive;
    font-style: italic;
    font-size: 1.1rem;
    color: #130089;
    opacity: 0.7;
    margin-bottom: 2rem;
    text-align: center;
}
.contatti-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
}
.contatto-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.3rem;
    border: 1px solid rgba(19,0,137,0.1);
    box-shadow: 0 2px 10px rgba(19,0,137,0.05);
    transition: all 0.2s;
}
.contatto-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(19,0,137,0.1);
}
.contatto-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
    display: block;
}
.contatto-org {
    font-weight: 800;
    color: #130089;
    font-size: 1.05rem;
    margin-bottom: 0.15rem;
    line-height: 1.2;
}
.contatto-name {
    font-size: 0.88rem;
    color: #5b6472;
    margin-bottom: 0.85rem;
    font-style: italic;
}
.contatto-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
    font-size: 0.86rem;
    color: #2a3140;
}
.contatto-row-icon {
    color: #130089;
    opacity: 0.7;
    flex-shrink: 0;
    width: 16px;
    text-align: center;
}
.contatto-row a {
    color: #130089;
    text-decoration: none;
    font-weight: 500;
}
.contatto-row a:hover {
    text-decoration: underline;
}
@media (max-width: 700px) {
    .contatti-grid { grid-template-columns: 1fr; gap: 1rem; }
    .contatti-section { padding: 1.8rem 1.1rem; }
    .contatti-title { font-size: 1.45rem; }
    .contatti-sub { font-size: 0.98rem; }
}
</style>
"""
st.markdown(contatti_css, unsafe_allow_html=True)

# HTML della sezione contatti (separato dal CSS)
contatti_html = """
<div class="contatti-section">
    <div class="contatti-eyebrow">Per qualsiasi domanda</div>
    <div class="contatti-title">Contatti utili</div>
    <div class="contatti-sub">Siamo qui per te</div>
    <div class="contatti-grid">
        <div class="contatto-card">
            <span class="contatto-icon">🏛</span>
            <div class="contatto-org">Comune di Peccioli</div>
            <div class="contatto-name">Ufficio Staff</div>
            <div class="contatto-row">
                <span class="contatto-row-icon">✉</span>
                <a href="mailto:info@comune.peccioli.pi.it">info@comune.peccioli.pi.it</a>
            </div>
            <div class="contatto-row">
                <span class="contatto-row-icon">☎</span>
                <a href="tel:+390587672602">0587 672602</a>
            </div>
            <div class="contatto-row">
                <span class="contatto-row-icon">💬</span>
                <a href="https://wa.me/393355710746" target="_blank" rel="noopener">WhatsApp 335 5710746</a>
            </div>
        </div>
        <div class="contatto-card">
            <span class="contatto-icon">✈</span>
            <div class="contatto-org">Equipe Viaggi</div>
            <div class="contatto-name">Simone Turini</div>
            <div class="contatto-row">
                <span class="contatto-row-icon">✉</span>
                <a href="mailto:s.turini@equipeviaggi.it">s.turini@equipeviaggi.it</a>
            </div>
            <div class="contatto-row">
                <span class="contatto-row-icon">☎</span>
                <a href="tel:+390571387070">0571 387070</a>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(contatti_html, unsafe_allow_html=True)

st.markdown(f"<div class='footer-box'>Peccioli Eyes on New Orleans · 2026</div>", unsafe_allow_html=True)
