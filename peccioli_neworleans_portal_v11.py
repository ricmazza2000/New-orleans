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

def img_to_base64(path):
    if path and Path(path).exists():
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            return base64.b64encode(f.read()).decode(), mime
    return None, None

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
# Immagini
# ----------------------------
logo_path       = find_image(["logo_comune.png", "logo_comune.jpg"])
morelli_img     = find_image(["morelli.jpg", "morelli.png"])
gardner_img     = find_image(["gardner.jpg", "gardner.png"])
costa_img       = find_image(["costa.jpg", "costa.png"])
briefing_img    = find_image(["briefing.jpg", "briefing.png"])
materiali_img   = find_image(["materiali.jpg", "materiali.png"])
gruppi_img      = find_image(["gruppi.jpg", "gruppi.png"])
skyline_path    = find_image(["neworleans_stilizzata.png", "neworleans_stilizzata.jpeg", "neworleans_stilizzata.jpg"])
nola_logo_path  = find_image(["New_Orleans_Logo.png", "New_Orleans_Logo.jpg"])

gallery_items = [
    {"key": "artistica", "title": "Street art",         "desc": "Murale che racconta la voce artistica e comunitaria di New Orleans.",         "path": find_image(["home_artistica.jpg"])},
    {"key": "musicale",  "title": "Jazz dal vivo",      "desc": "Gruppo di artisti jazz in una serata nel French Quarter.",                    "path": find_image(["home_musicale.jpg"])},
    {"key": "simbolica", "title": "La città e il fiume","desc": "Veduta simbolica di New Orleans affacciata sul Mississippi.",                 "path": find_image(["home_simbolica.jpg", "home_simbolica.jpeg"])},
    {"key": "sociale",   "title": "Mardi Gras",          "desc": "Un carro del Mardi Gras sfila tra la folla lungo le strade del French Quarter. Il carnevale di New Orleans è uno dei più spettacolari al mondo.",       "path": find_image(["Home_carnevale.jpg", "home_carnevale.jpg", "home_sociale.jpg"])},
    {"key": "umana",     "title": "Volti della città",  "desc": "Un ritratto che richiama il lato umano e quotidiano di New Orleans.",         "path": find_image(["home_umana.jpg"])},
    {"key": "urbana",    "title": "Atmosfera urbana",   "desc": "Una composizione visiva che restituisce l'energia e i contrasti della città.", "path": find_image(["home_urbana.jpeg", "home_urbana.jpg", "home_urbana.png"])},
]

skyline_b64, skyline_mime = img_to_base64(skyline_path)
nola_logo_b64, nola_logo_mime = img_to_base64(nola_logo_path)
logo_b64, logo_mime = img_to_base64(logo_path)

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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: "Inter", "Segoe UI", sans-serif; }
.block-container { max-width: 1200px; padding-top: 1.2rem; padding-bottom: 2rem; }

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
        "foto": morelli_img, "emoji": "🏛"
    },
    {
        "data": "21 maggio", "titolo": "Anthony Gardner",
        "ruolo": "Ex ambasciatore USA all'Unione Europea · Consiglio di sicurezza nazionale",
        "descrizione": "Uno sguardo istituzionale e geopolitico, utile a capire il ruolo di New Orleans e il rapporto tra Stati Uniti, Europa e relazioni internazionali.",
        "foto": gardner_img, "emoji": "🌐"
    },
    {
        "data": "15 giugno", "titolo": "Francesco Costa",
        "ruolo": "Giornalista · Direttore de Il Post",
        "descrizione": "Il punto di vista sociale, narrativo e attuale sugli Stati Uniti, per aiutare i ragazzi a leggere la realtà americana oltre gli stereotipi.",
        "foto": costa_img, "emoji": "📰"
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
    {"nome": "French Quarter",    "lat": 29.9584, "lon": -90.0645, "desc": "Il quartiere più iconico, tra architettura storica e balconi in ferro battuto.",        "colore": "#d08c38"},
    {"nome": "Congo Square",      "lat": 29.9596, "lon": -90.0773, "desc": "Luogo simbolico per la storia afroamericana e le radici musicali di New Orleans.",      "colore": "#17305a"},
    {"nome": "Warehouse District","lat": 29.9489, "lon": -90.0715, "desc": "Il volto contemporaneo della città: musei, cultura e trasformazioni urbane.",            "colore": "#17305a"},
    {"nome": "Lower Ninth Ward",  "lat": 29.9214, "lon": -90.0790, "desc": "Il luogo più legato alla memoria dell'uragano Katrina e alla ricostruzione.",           "colore": "#c0392b"},
    {"nome": "Jackson Square",    "lat": 29.9623, "lon": -90.0637, "desc": "Piazza centrale e simbolica: arte, turismo e identità storica.",                        "colore": "#17305a"},
    {"nome": "Frenchmen Street",  "lat": 29.9691, "lon": -90.0519, "desc": "La strada più rappresentativa per il jazz dal vivo e l'atmosfera più autentica.",       "colore": "#d08c38"},
]

# ----------------------------
# SIDEBAR
# ----------------------------
# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    # Logo comune
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

    options = ["Home", "Briefing", "Approfondimenti", "Temi del viaggio", "Mappe", "Programma", "Documenti"]

    if "nav_target" not in st.session_state:
        st.session_state.nav_target = "Home"

    cur_index = options.index(st.session_state.nav_target) if st.session_state.nav_target in options else 0

    pagina_radio = st.radio(
        label="",
        options=options,
        label_visibility="collapsed",
        index=cur_index,
    )

    # Se l'utente clicca manualmente la sidebar, aggiorna nav_target
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
# HEADER — semplice: logo + titolo + skyline
# ----------------------------
if nola_logo_b64:
    nola_logo_tag = f'<img src="data:{nola_logo_mime};base64,{nola_logo_b64}" style="height:48px;opacity:0.65;filter:brightness(0) saturate(100%) invert(16%) sepia(60%) saturate(500%) hue-rotate(190deg);margin-left:1rem;vertical-align:middle;position:relative;top:-4px;">'
else:
    nola_logo_tag = ""

logo_tag = f'<img src="data:{logo_mime};base64,{logo_b64}" style="height:62px;object-fit:contain;flex-shrink:0;">' if logo_b64 else ""

header_html = f"""
<div style="display:flex;align-items:center;gap:1.2rem;padding:1.2rem 0 0.6rem 0;">
    {logo_tag}
    <div>
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#d08c38;margin-bottom:0.25rem;">🎷 Comune di Peccioli · Progetto di viaggio</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:2.6rem;font-weight:800;color:#0d1f3c;line-height:1.05;letter-spacing:-0.01em;">
            Peccioli &times; <span style="color:#d08c38;">New Orleans</span> 2026{nola_logo_tag}
        </div>
    </div>
</div>
<div style="height:2px;background:linear-gradient(90deg,#d08c38 0%,#17305a 40%,transparent 100%);margin:0.5rem 0 1.6rem 0;border-radius:2px;opacity:0.35;"></div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ----------------------------
# HOME
# ----------------------------
if pagina == "Home":

    # Countdown funzionante via st.components — mobile responsive
    import streamlit.components.v1 as components

    morelli_b64, morelli_mime = img_to_base64(morelli_img)
    prossimo_foto = f'<img src="data:{morelli_mime};base64,{morelli_b64}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #d08c38;flex-shrink:0;">' if morelli_b64 else '<div style="width:44px;height:44px;border-radius:50%;background:#dde3ec;flex-shrink:0;"></div>'

    countdown_html = ("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { overflow:hidden; background:transparent; }
    .cd-wrap {
        display:flex;
        gap:0.75rem;
        font-family:'Inter',sans-serif;
        height:110px;
        align-items:stretch;
    }
    .cd-main {
        flex:1.4;
        min-width:0;
        background:linear-gradient(135deg,#0d1f3c,#17305a);
        border-radius:18px;
        padding:1rem 1.4rem;
        color:white;
        display:flex;
        flex-direction:column;
        justify-content:center;
        flex-shrink:0;
    }
    .cd-label { font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#d08c38; margin-bottom:0.3rem; }
    .cd-num { font-size:2rem; font-weight:800; color:white; line-height:1.1; }
    .cd-box {
        flex:1;
        min-width:0;
        background:white;
        border-radius:18px;
        padding:0.8rem;
        text-align:center;
        border:1px solid rgba(20,33,61,0.08);
        box-shadow:0 4px 14px rgba(0,0,0,0.05);
        display:flex;
        flex-direction:column;
        justify-content:center;
        flex-shrink:0;
    }
    .cd-box-num { font-size:1.8rem; font-weight:800; color:#d08c38; line-height:1; font-family:Georgia,serif; }
    .cd-box-label { font-size:0.72rem; color:#5b6472; margin-top:0.2rem; font-weight:500; }

    @media (max-width:600px) {
        html, body { overflow:hidden; }
        .cd-wrap {
            overflow-x:auto;
            overflow-y:hidden;
            -webkit-overflow-scrolling:touch;
            scroll-snap-type:x mandatory;
            gap:0.6rem;
            height:100px;
            padding-bottom:2px;
        }
        .cd-wrap::-webkit-scrollbar { display:none; }
        .cd-main {
            min-width:200px;
            max-width:200px;
            scroll-snap-align:start;
            padding:0.85rem 1rem;
        }
        .cd-box {
            min-width:150px;
            max-width:150px;
            scroll-snap-align:start;
        }
        .cd-box-last {
            min-width:180px;
            max-width:180px;
            scroll-snap-align:start;
            text-align:left;
            padding:0.8rem 1rem;
        }
        .cd-num { font-size:1.75rem; }
        .cd-box-num { font-size:1.5rem; }
    }
    </style>
    <div class="cd-wrap">
        <div class="cd-main">
            <div class="cd-label">&#9203; Mancano al viaggio</div>
            <div class="cd-num" id="cd">&#8212;</div>
        </div>
        <div class="cd-box">
            <div class="cd-box-num">21&#8211;28</div>
            <div class="cd-box-label">Settembre 2026</div>
        </div>
        <div class="cd-box cd-box-last" style="text-align:left;padding:0.8rem 1rem;">
            <div style="font-size:0.62rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#d08c38;margin-bottom:0.4rem;">&#128197; Prossimo incontro</div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
    """ + prossimo_foto + """
                <div>
                    <div style="font-size:0.8rem;font-weight:700;color:#14213d;line-height:1.2;">Elia Morelli</div>
                    <div style="font-size:0.72rem;color:#5b6472;margin-top:0.1rem;">7 maggio 2026</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        var t = new Date("2026-09-21T00:00:00").getTime() - Date.now();
        var el = document.getElementById("cd");
        if (el) {
            if (t <= 0) { el.textContent = "Ci siamo!"; }
            else {
                var d = Math.floor(t / 86400000);
                el.innerHTML = d + "<span style='font-size:0.95rem;font-weight:400;opacity:0.65;margin-left:0.3rem;'>giorni</span>";
            }
        }
    </script>
    """)
    components.html(countdown_html, height=120, scrolling=False)

    # Descrizione
    st.markdown("""
    <p style="font-size:1rem;color:#3a4a5c;line-height:1.7;margin-bottom:1.2rem;">
    Questo spazio accompagna i ragazzi nel percorso di preparazione al viaggio:
    tre incontri formativi con esperti, materiali di approfondimento, una mappa interattiva
    e otto gruppi tematici per osservare New Orleans con sguardi diversi.
    </p>
    """, unsafe_allow_html=True)

    # Galleria — frecce su desktop e mobile
    st.markdown("### 📸 Sguardi su New Orleans")
    valid_items = [item for item in gallery_items if item["path"]]

    if "selected_home_image" not in st.session_state:
        st.session_state.selected_home_image = 0
    idx = min(st.session_state.selected_home_image, len(valid_items) - 1)
    selected = valid_items[idx]

    col_prev, col_img, col_next = st.columns([1, 14, 1])
    with col_prev:
        if st.button("←", key="prev_img"):
            st.session_state.selected_home_image = (idx - 1) % len(valid_items)
            st.rerun()
    with col_img:
        st.image(selected["path"], use_container_width=True)
    with col_next:
        if st.button("→", key="next_img"):
            st.session_state.selected_home_image = (idx + 1) % len(valid_items)
            st.rerun()

    st.markdown(f'<div class="gallery-caption"><strong>{selected["title"]}</strong> — {selected["desc"]}</div>', unsafe_allow_html=True)

    # Pallini indicatori
    dots_html = '<div style="display:flex;justify-content:center;gap:6px;margin-bottom:0.8rem;">'
    for i in range(len(valid_items)):
        color = "#d08c38" if i == idx else "rgba(20,33,61,0.15)"
        dots_html += f'<div style="width:7px;height:7px;border-radius:50%;background:{color};"></div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

    # Webcam + News affiancati
    st.markdown("## ")
    cam_col, news_col = st.columns(2)

    with cam_col:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:1.2rem 1.4rem;border:1px solid rgba(20,33,61,0.08);box-shadow:0 6px 20px rgba(0,0,0,0.05);height:100%;">
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:700;color:#14213d;margin-bottom:0.3rem;">
                📹 Live da New Orleans
            </div>
            <div style="font-size:0.85rem;color:#5b6472;margin-bottom:1rem;line-height:1.5;">
                Webcam in diretta dal French Quarter · Bourbon Street, angolo St. Peter
            </div>
            <a href="https://www.earthcam.com/usa/louisiana/neworleans/bourbonstreet/" target="_blank"
               style="display:inline-block;background:#0d1f3c;color:white;padding:0.55rem 1.2rem;
                      border-radius:999px;font-size:0.88rem;font-weight:600;text-decoration:none;">
                🎥 Guarda la webcam live →
            </a>
            <div style="font-size:0.75rem;color:#9aa3b0;margin-top:0.8rem;">
                Fonte: EarthCam · Cats Meow Karaoke Bar · 24/7
            </div>
        </div>
        """, unsafe_allow_html=True)

    with news_col:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:1.2rem 1.4rem;border:1px solid rgba(20,33,61,0.08);box-shadow:0 6px 20px rgba(0,0,0,0.05);height:100%;">
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;font-weight:700;color:#14213d;margin-bottom:0.3rem;">
                🗞 Notizie da New Orleans
            </div>
            <div style="font-size:0.85rem;color:#5b6472;margin-bottom:1rem;line-height:1.5;">
                Le fonti locali per seguire la città prima del viaggio
            </div>
            <div style="display:flex;flex-direction:column;gap:0.5rem;">
                <a href="https://www.nola.com" target="_blank"
                   style="display:flex;align-items:center;gap:0.6rem;padding:0.55rem 0.8rem;
                          background:#f5f8fc;border-radius:12px;text-decoration:none;
                          border-left:3px solid #d08c38;">
                    <span style="font-size:1rem;">📰</span>
                    <div>
                        <div style="font-size:0.85rem;font-weight:600;color:#14213d;">The Times-Picayune</div>
                        <div style="font-size:0.72rem;color:#9aa3b0;">Il principale quotidiano di New Orleans</div>
                    </div>
                </a>
                <a href="https://www.wwno.org" target="_blank"
                   style="display:flex;align-items:center;gap:0.6rem;padding:0.55rem 0.8rem;
                          background:#f5f8fc;border-radius:12px;text-decoration:none;
                          border-left:3px solid #17305a;">
                    <span style="font-size:1rem;">📻</span>
                    <div>
                        <div style="font-size:0.85rem;font-weight:600;color:#14213d;">WWNO Public Radio</div>
                        <div style="font-size:0.72rem;color:#9aa3b0;">Radio pubblica NPR di New Orleans</div>
                    </div>
                </a>
                <a href="https://thelensnola.org" target="_blank"
                   style="display:flex;align-items:center;gap:0.6rem;padding:0.55rem 0.8rem;
                          background:#f5f8fc;border-radius:12px;text-decoration:none;
                          border-left:3px solid #2e7d5e;">
                    <span style="font-size:1rem;">🔍</span>
                    <div>
                        <div style="font-size:0.85rem;font-weight:600;color:#14213d;">The Lens NOLA</div>
                        <div style="font-size:0.72rem;color:#9aa3b0;">Giornalismo investigativo locale</div>
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card sezioni cliccabili
    st.markdown("## ")
    sezioni_home = [
        ("📅", "Briefing",          "Tre incontri con esperti di storia, geopolitica e giornalismo.",       "Briefing"),
        ("📚", "Approfondimenti",   "Libri, film, documentari e risorse su New Orleans.",                   "Approfondimenti"),
        ("🎷", "Temi del viaggio",  "Quattro chiavi di lettura per osservare la città.",                    "Temi del viaggio"),
        ("🗺", "Mappe",             "Mappa interattiva con i luoghi simbolici del viaggio.",                "Mappe"),
        ("🗓", "Programma",         "Il programma del viaggio — in costruzione.",                           "Programma"),
        ("📂", "Documenti",         "Documenti e scadenze per la preparazione al viaggio.",                 "Documenti"),
    ]
    c1, c2, c3 = st.columns(3)
    cols_cycle = [c1, c2, c3, c1, c2, c3]
    for i, (icon, title, desc, dest) in enumerate(sezioni_home):
        with cols_cycle[i]:
            st.markdown(f"""
            <div class="home-card" style="margin-bottom:0.8rem;">
                <div class="home-card-icon">{icon}</div>
                <div class="home-card-title">{title}</div>
                <div class="home-card-text">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Vai a {title}", key=f"nav_{dest}", use_container_width=True):
                st.session_state.nav_target = dest
                st.rerun()

# ----------------------------
# BRIEFING
# ----------------------------
elif pagina == "Briefing":
    st.markdown('<div class="page-title">Briefing</div><div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="quote-box">I briefing costruiranno un primo sguardo sulla città, mettendo insieme storia, geopolitica e attualità.</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])
    with left:
        st.write("In preparazione al viaggio, i ragazzi seguiranno tre incontri con tre esperti che racconteranno storia, cultura, società e attualità su New Orleans. L'idea è di chiamarli briefing, più che lezioni.")
    with right:
        if briefing_img:
            st.image(briefing_img, use_container_width=True)

    st.markdown("## ")
    timeline_html = '<div class="timeline">'
    for b in briefing_data:
        b64, mime = img_to_base64(b["foto"])
        dot = f'<div class="tl-dot"><img src="data:{mime};base64,{b64}"></div>' if b64 else f'<div class="tl-dot-placeholder">{b["emoji"]}</div>'
        timeline_html += f"""
        <div class="tl-item">
            {dot}
            <div class="tl-content">
                <div class="tl-date">{b["data"]}</div>
                <div class="tl-name">{b["titolo"]}</div>
                <div class="tl-role">{b["ruolo"]}</div>
                <div class="tl-desc">{b["descrizione"]}</div>
            </div>
        </div>"""
    timeline_html += '</div>'
    st.markdown(timeline_html, unsafe_allow_html=True)

# ----------------------------
# APPROFONDIMENTI
# ----------------------------
elif pagina == "Approfondimenti":
    st.markdown('<div class="page-title">Approfondimenti</div><div class="gold-line"></div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with left:
        st.write("Libri, film, documentari e risorse online per arrivare a New Orleans con uno sguardo già allenato.")
    with right:
        if materiali_img:
            st.image(materiali_img, use_container_width=True)

    st.markdown("## ")

    sezioni = [
        {
            "titolo": "📚 Libri su New Orleans",
            "items": [
                {
                    "titolo": "Una banda di idioti — John Kennedy Toole",
                    "desc": "Capolavoro della letteratura americana ambientato nella New Orleans degli anni '60. Satira sociale geniale, vincitore postumo del Pulitzer. Il modo più divertente per entrare nell'anima della città.",
                    "link": "https://it.wikipedia.org/wiki/Una_banda_di_idioti",
                    "label": "Leggi su Wikipedia"
                },
                {
                    "titolo": "Intervista col vampiro — Anne Rice",
                    "desc": "Il romanzo che ha reso New Orleans capitale mondiale del gotico americano. Ambientato tra il French Quarter e le piantagioni della Louisiana, mescola storia, atmosfera e questioni razziali in modo unico.",
                    "link": "https://it.wikipedia.org/wiki/Intervista_col_vampiro_(romanzo)",
                    "label": "Leggi su Wikipedia"
                },
                {
                    "titolo": "Blues Highway — Rob Siebert",
                    "desc": "Viaggio narrativo da Chicago a New Orleans sulle tracce delle origini della musica americana: blues, jazz, gospel. Perfetto per capire il legame tra musica, storia e territorio.",
                    "link": "https://marcosymarcos.com/libri/gli-alianti/blues-highway/",
                    "label": "Scheda editoriale"
                },
                {
                    "titolo": "Un tram che si chiama Desiderio — Tennessee Williams",
                    "desc": "Il capolavoro teatrale ambientato a New Orleans, scritto da Williams proprio nel French Quarter. Punto di riferimento assoluto per capire il Sud americano, la tensione sociale e l'immaginario della città.",
                    "link": "https://it.wikipedia.org/wiki/Un_tram_che_si_chiama_Desiderio",
                    "label": "Leggi su Wikipedia"
                },
            ]
        },
        {
            "titolo": "🎬 Film e serie TV",
            "items": [
                {
                    "titolo": "Un tram che si chiama Desiderio (1951) — Elia Kazan",
                    "desc": "Il film tratto dalla pièce di Tennessee Williams con Marlon Brando e Vivien Leigh. Classico assoluto, girato nella New Orleans reale. La tensione tra i personaggi rispecchia le contraddizioni della città.",
                    "link": "https://www.imdb.com/title/tt0044081/",
                    "label": "Scheda IMDb"
                },
                {
                    "titolo": "Intervista col vampiro (1994) — Neil Jordan",
                    "desc": "Con Tom Cruise, Brad Pitt e una giovanissima Kirsten Dunst. Girato tra New Orleans e la Oak Alley Plantation, cattura perfettamente l'atmosfera gotica e decadente della Louisiana.",
                    "link": "https://www.imdb.com/title/tt0110632/",
                    "label": "Scheda IMDb"
                },
                {
                    "titolo": "Il curioso caso di Benjamin Button (2008) — David Fincher",
                    "desc": "Con Brad Pitt e Cate Blanchett. Ambientato a New Orleans dal dopoguerra a Katrina, usa la città come sfondo per una storia sull'identità, il tempo e la memoria collettiva.",
                    "link": "https://www.imdb.com/title/tt0421715/",
                    "label": "Scheda IMDb"
                },
                {
                    "titolo": "Treme — serie HBO (2010-2013)",
                    "desc": "La serie più importante mai realizzata su New Orleans dopo Katrina. Segue i residenti del quartiere Tremé mentre cercano di ricostruire la loro vita e la loro musica. Vince un Emmy Award.",
                    "link": "https://www.imdb.com/title/tt1279972/",
                    "label": "Scheda IMDb"
                },
                {
                    "titolo": "Easy Rider (1969) — Dennis Hopper",
                    "desc": "Icona della controcultura americana. I protagonisti raggiungono New Orleans per il Mardi Gras in una delle scene più celebri della storia del cinema indipendente americano.",
                    "link": "https://www.imdb.com/title/tt0064276/",
                    "label": "Scheda IMDb"
                },
            ]
        },
        {
            "titolo": "🎬 Documentari su Katrina",
            "items": [
                {
                    "titolo": "Katrina: Come Hell and High Water (Netflix, 2025)",
                    "desc": "Serie in 3 episodi prodotta da Spike Lee: venti anni dopo, i sopravvissuti raccontano in prima persona la catastrofe e i fallimenti istituzionali. Da vedere prima del viaggio.",
                    "link": "https://www.netflix.com/title/81676595",
                    "label": "Guarda su Netflix"
                },
                {
                    "titolo": "Hurricane Katrina: Race Against Time (Nat. Geographic, 2025)",
                    "desc": "Docuserie in 5 episodi, vincitrice del Critics Choice Award 2025. Ricostruisce minuto per minuto la catastrofe con footage inedito e testimonianze dirette dei sopravvissuti.",
                    "link": "https://www.imdb.com/title/tt37458027/",
                    "label": "Scheda IMDb"
                },
                {
                    "titolo": "When the Levees Broke — Spike Lee (2006)",
                    "desc": "Il documentario classico in 4 atti che ha raccontato al mondo la devastazione di Katrina. Pietra miliare sul tema, ancora oggi imprescindibile per capire cosa è successo davvero.",
                    "link": "https://www.imdb.com/title/tt0783105/",
                    "label": "Scheda IMDb"
                },
            ]
        },
        {
            "titolo": "🌐 Risorse online",
            "items": [
                {
                    "titolo": "New Orleans — Wikipedia italiana",
                    "desc": "Panoramica completa su storia, cultura, musica e geografia della città. Ottimo punto di partenza per orientarsi prima di approfondire.",
                    "link": "https://it.wikipedia.org/wiki/New_Orleans",
                    "label": "Leggi"
                },
                {
                    "titolo": "The Times-Picayune | The New Orleans Advocate",
                    "desc": "Il principale quotidiano di New Orleans. Utile per seguire l'attualità della città nelle settimane prima della partenza.",
                    "link": "https://www.nola.com",
                    "label": "Visita il sito"
                },
                {
                    "titolo": "Da Costa a Costa — Francesco Costa (Il Post)",
                    "desc": "Newsletter e canale YouTube dell'esperto di America che incontreremo al briefing. Il modo migliore per seguire l'attualità americana con occhi italiani.",
                    "link": "https://www.ilpost.it/costa/",
                    "label": "Segui"
                },
            ]
        },
    ]

    for sez in sezioni:
        st.markdown(f'<div style="font-family:\'Playfair Display\',Georgia,serif;font-size:1.2rem;font-weight:700;color:#14213d;margin:1.4rem 0 0.7rem 0;">{sez["titolo"]}</div>', unsafe_allow_html=True)
        for item in sez["items"]:
            st.markdown(f"""
            <div class="mat-card" style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
                <div style="flex:1;">
                    <div style="font-weight:700;color:#14213d;margin-bottom:0.25rem;">{item['titolo']}</div>
                    <div style="font-size:0.9rem;color:#5b6472;line-height:1.55;">{item['desc']}</div>
                </div>
                <a href="{item['link']}" target="_blank" style="flex-shrink:0;background:#0d1f3c;color:white;padding:0.4rem 0.9rem;border-radius:999px;font-size:0.8rem;font-weight:600;text-decoration:none;white-space:nowrap;align-self:center;">{item['label']} &#8594;</a>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------
# TEMI DEL VIAGGIO
# ----------------------------
elif pagina == "Temi del viaggio":
    st.markdown('<div class="page-title">Temi del viaggio</div><div class="gold-line"></div>', unsafe_allow_html=True)
    st.write("Quattro chiavi di lettura per osservare New Orleans durante il viaggio. Non sono gruppi separati, ma prospettive da tenere sempre attive.")

    st.markdown("## ")

    temi = [
        {
            "emoji": "🎷",
            "titolo": "Musica",
            "colore": "#d08c38",
            "sottotitolo": "Jazz, blues e il ritmo della città",
            "desc": "New Orleans è la culla del jazz e del blues americano. La musica qui non è solo intrattenimento: è linguaggio sociale, memoria collettiva, forma di resistenza. Dalle second line nei funerali di strada a Frenchmen Street la sera, la città vive e comunica attraverso il suono.",
            "parole": ["Jazz", "Blues", "Second line", "Frenchmen Street", "Louis Armstrong", "Brass band"],
        },
        {
            "emoji": "🌊",
            "titolo": "Resilienza",
            "colore": "#17305a",
            "sottotitolo": "Katrina, ricostruzione e cambiamento climatico",
            "desc": "L'uragano Katrina del 2005 ha devastato New Orleans e messo a nudo le fragilità strutturali della città: infrastrutture, disuguaglianze razziali, risposta istituzionale. Vent'anni dopo, la città è ancora in cammino. Il Lower Ninth Ward è il luogo dove questo tema si tocca con mano.",
            "parole": ["Katrina 2005", "Lower Ninth Ward", "Argini e dighe", "Rigenerazione urbana", "Cambiamento climatico"],
        },
        {
            "emoji": "⚖️",
            "titolo": "Società",
            "colore": "#2e7d5e",
            "sottotitolo": "Diversità culturale, questioni razziali, parte umana",
            "desc": "New Orleans è una delle città più multiculturali e diseguali degli Stati Uniti. L'eredità della schiavitù, la comunità creola, le contraddizioni tra turismo e vita reale, la povertà accanto all'opulenza: osservare la città attraverso le persone che la abitano è il modo più onesto di capirla.",
            "parole": ["Comunità creola", "Storia afroamericana", "Congo Square", "Gentrificazione", "Diversità"],
        },
        {
            "emoji": "🏛",
            "titolo": "Identità e storia",
            "colore": "#7b3f00",
            "sottotitolo": "Radici coloniali, voodoo, Mardi Gras e French Quarter",
            "desc": "New Orleans è l'unica città americana fondata dai francesi, ceduta agli spagnoli e poi agli Stati Uniti. Questa stratificazione di culture — europea, africana, caraibica — ha prodotto un'identità unica: l'architettura del French Quarter, il voodoo, il Mardi Gras, la cucina creola. Una città che non somiglia a nessun'altra.",
            "parole": ["French Quarter", "Voodoo", "Mardi Gras", "Architettura coloniale", "Cucina creola", "Marie Laveau"],
        },
    ]

    for tema in temi:
        pills = "".join([f'<span style="display:inline-block;background:{tema["colore"]}20;color:{tema["colore"]};border:1px solid {tema["colore"]}40;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.75rem;font-weight:600;margin-right:0.35rem;margin-bottom:0.35rem;">{p}</span>' for p in tema["parole"]])
        st.markdown(f"""
        <div style="background:white;border-radius:22px;padding:1.4rem 1.5rem;border:1px solid rgba(20,33,61,0.07);
                    box-shadow:0 6px 22px rgba(0,0,0,0.05);margin-bottom:1rem;
                    border-left:5px solid {tema['colore']};">
            <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.5rem;">
                <span style="font-size:1.8rem;">{tema['emoji']}</span>
                <div>
                    <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.25rem;font-weight:800;color:#14213d;">{tema['titolo']}</div>
                    <div style="font-size:0.85rem;color:{tema['colore']};font-weight:600;">{tema['sottotitolo']}</div>
                </div>
            </div>
            <div style="font-size:0.95rem;color:#3a4a5c;line-height:1.7;margin-bottom:0.8rem;">{tema['desc']}</div>
            <div>{pills}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# MAPPE
# ----------------------------
elif pagina == "Mappe":
    st.markdown('<div class="page-title">Mappa di New Orleans</div><div class="gold-line"></div>', unsafe_allow_html=True)
    st.write("Mappa interattiva con i luoghi simbolici del viaggio. Clicca sui marker per leggere la descrizione.")

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

    st.markdown("## ")
    col1, col2 = st.columns(2)
    for i, luogo in enumerate(luoghi_dati):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="legend-card">
                <div class="card-title" style="color:{luogo['colore']}">{luogo['nome']}</div>
                <div class="note">{luogo['desc']}</div>
            </div>""", unsafe_allow_html=True)

# ----------------------------
# PROGRAMMA
# ----------------------------
elif pagina == "Programma":
    st.markdown('<div class="page-title">Programma del viaggio</div><div class="gold-line"></div>', unsafe_allow_html=True)

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
    st.markdown('<div class="page-title">Materiali e documenti</div><div class="gold-line"></div>', unsafe_allow_html=True)
    st.write("Qui troverete i documenti da consultare, compilare e consegnare in vista del viaggio, con relative scadenze.")

    st.markdown("""
    <div style="background:#f0f4fb;border:2px dashed rgba(20,33,61,0.2);border-radius:24px;padding:2.5rem 2rem;text-align:center;max-width:580px;margin:2rem auto;">
        <div style="font-size:2.5rem;margin-bottom:0.6rem;">📂</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.4rem;font-weight:700;color:#14213d;margin-bottom:0.6rem;">Documenti in arrivo</div>
        <div style="font-size:0.97rem;color:#5b6472;line-height:1.75;">
            I documenti, le schede e le scadenze non sono ancora stati definiti.<br>
            Questa sezione verrà aggiornata non appena i materiali saranno pronti<br>
            e le date di consegna stabilite.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer-box'>Demo grafica v12 · Portale ragazzi Peccioli × New Orleans 2026</div>", unsafe_allow_html=True)
