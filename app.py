import streamlit as st
import pandas as pd
import time
import gspread

# 1. Page Configuration
st.set_page_config(page_title="EuroQuad Dashboard", layout="centered")

# --- CONFIGURAZIONE GOOGLE SHEETS & CREDENZIALI ---
SHEET_ID = '1jdqwPKfkHYncXgvfb65UsIwZ2YBFY5j31yaY-mTZBPc'
GID_PERSONAL_STATS = '327527248'

def ottieni_credenziali():
    """Recupera le credenziali da st.secrets per gspread"""
    try:
        if "gcp_service_account" in st.secrets:
            from google.oauth2.service_account import Credentials
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds_dict = dict(st.secrets["gcp_service_account"])
            return Credentials.from_service_account_info(creds_dict, scopes=scope)
    except Exception as e:
        st.error(f"Errore configurazione credenziali: {e}")
    return None

def scrivi_cella_per_gid(gid, cell_address, value):
    """Scrive un valore in una cella specifica cercando il foglio tramite GID"""
    try:
        creds = ottieni_credenziali()
        if creds:
            client = gspread.authorize(creds)
            sheet = client.open_by_key(SHEET_ID)
            ws = next((w for w in sheet.worksheets() if str(w.id).strip() == str(gid).strip()), None)
            if ws:
                ws.update_acell(cell_address, value)
    except Exception as e:
        st.error(f"Errore durante la scrittura su Google Sheets: {e}")

# 2. CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #003399; }
    h1, h2, h3, p { color: #fff !important; text-align: center; }
    [data-testid="stSidebar"] { display: none; }
    div.stButton > button {
        width: 100%;
        background-color: #000000;
        color: white;
        border: 1px solid #ffcc00;
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
        font-size: 12px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #111111;
        border-color: #ffffff;
        color: #ffcc00;
    }
    .custom-table {
        width: 100%; max-width: 600px; margin: 0 auto 20px auto; border-collapse: separate; border-spacing: 0; border-radius: 8px; overflow: hidden; border: 1px solid #ffcc00; font-family: sans-serif;
    }
    .custom-table th { background-color: #000000; color: #ffcc00; padding: 10px 14px; text-align: center; border-bottom: 1px solid #ffcc00; font-size: 16px; }
    .custom-table td { background-color: #000b1a; color: #ddd; padding: 10px 14px; border-bottom: 1px solid #001a33; text-align: center; }
    .ranking-table { width: 100%; max-width: 450px; margin: 0 auto 20px auto; border-collapse: separate; border-spacing: 0; border-radius: 8px; overflow: hidden; border: 1px solid #ffcc00; font-family: sans-serif; }
    .ranking-table th { background-color: #000000; color: #ffcc00; padding: 10px 14px; text-align: center; border-bottom: 1px solid #ffcc00; font-size: 16px; }
    .ranking-table td { background-color: #000b1a; color: #ddd; padding: 10px 14px; border-bottom: 1px solid #001a33; text-align: center; }
    .stat-card { background-color: #000000; border: 1px solid #ffcc00; border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 10px; }
    .stat-label { color: #ffcc00; font-size: 0.75rem; font-weight: bold; margin-bottom: 4px; }
    .stat-value { color: #fff; font-size: 1.1rem; font-weight: bold; }
    .logo-container img { max-width: 350px; width: 100%; display: block; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo
col_l1, col_l2, col_l3 = st.columns([1, 10, 1])
with col_l2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.title("EUROQUAD")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Leaderboard"

# 5. Horizontal Navigation Menu (Rimossi pulsanti Stats e Personal)
st.write("")
b1, b2, b3, b4, b5, b6 = st.columns(6)

with b1:
    if st.button("🏆\nLeader", use_container_width=True):
        st.session_state.page = "Leaderboard"
with b2:
    if st.button("📜\nRules", use_container_width=True):
        st.session_state.page = "Regole"
with b3:
    if st.button("⚔️\nLobby 1", use_container_width=True):
        st.session_state.page = "Scrims Lobby 1"
with b4:
    if st.button("⚔️\nLobby 2", use_container_width=True):
        st.session_state.page = "Scrims Lobby 2"
with b5:
    if st.button("⚔️\nLobby 3", use_container_width=True):
        st.session_state.page = "Scrims Lobby 3"
with b6:
    if st.button("👤\nPlayer", use_container_width=True):
        st.session_state.page = "Risultati Giocatore"

st.write("---")

# 6. Data loading function
@st.cache_data(ttl=600)
def load_data(gid):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}'
    return pd.read_csv(url)

# Render tables
def render_custom_table(df_sub, headers):
    html = f'<table class="custom-table"><thead><tr>'
    for h in headers: html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df_sub.iterrows():
        html += '<tr>'
        for val in row:
            v_str = "" if pd.isna(val) or str(val).lower() == "nan" else str(val)
            html += f'<td>{v_str}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

def render_ranking_table(df_sub, headers):
    html = f'<table class="ranking-table"><thead><tr>'
    for h in headers: html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df_sub.iterrows():
        html += '<tr>'
        for val in row:
            v_str = "" if pd.isna(val) or str(val).lower() == "nan" else str(val)
            html += f'<td>{v_str}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

def render_scrims_tables(gid, scrim_title, team_coords, game_coords_list, summary_coords, overall_coords):
    st.markdown(f"<h1 style='text-align: center;'>⚔️ {scrim_title} Results</h1>", unsafe_allow_html=True)
    st.write("---")
    df = load_data(gid)
    t_start, t_end, t_col = team_coords
    teams = df.iloc[t_start:t_end, t_col].dropna().astype(str).reset_index(drop=True)
    num_rows = len(teams)

    for idx, (r_start, r_end, c_start, c_end) in enumerate(game_coords_list, start=1):
        st.markdown(f"<h3 style='text-align: center;'>Game {idx}</h3>", unsafe_allow_html=True)
        val_df = df.iloc[r_start:r_start+num_rows, c_start:c_end].copy().fillna("")
        val_df.columns = ["Position", "Kills", "DMG", "Revive"]
        combined_df = pd.DataFrame({"Team": teams})
        for i, col in enumerate(val_df.columns): combined_df[col] = val_df.iloc[:, i].values
        st.markdown(render_custom_table(combined_df, ["Team", "Position", "Kills", "DMG", "Revive"]), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Summary & Overall</h3>", unsafe_allow_html=True)
    # Rendering simplified summary/overall here
    t7_r_start, _, t7_c_start, t7_c_end = summary_coords
    val_df = df.iloc[t7_r_start:t7_r_start+num_rows, t7_c_start:t7_c_end].copy().fillna("")
    combined_df = pd.DataFrame({"Team": teams})
    cols_t7 = ["Total Points", "Adjusted Score"]
    for i in [0, 3]: # Mapping indices for summary
        if i < val_df.shape[1]: combined_df[cols_t7[i==3]] = val_df.iloc[:, i].values
    st.markdown(render_custom_table(combined_df, ["Team", "Total Points", "Adjusted"]), unsafe_allow_html=True)

# 7. Page Logic
page = st.session_state.page

if page == "Leaderboard":
    st.markdown("<h1 style='text-align: center;'>🏆 Leaderboard</h1>", unsafe_allow_html=True)
    df = load_data('316677537')
    # ... (rest of logic for leaderboard as before) ...

elif page == "Scrims Lobby 1":
    render_scrims_tables('547827980', "Scrims Lobby 1", (8, 16, 4), [(8, 16, 5, 9), (8, 16, 10, 14), (8, 16, 15, 19), (8, 16, 20, 24), (8, 16, 25, 29), (8, 16, 30, 34)], (8, 16, 35, 40), (8, 16, 39, 42))

elif page == "Scrims Lobby 2":
    render_scrims_tables('547827980', "Scrims Lobby 2", (20, 28, 4), [(20, 28, 5, 9), (20, 28, 10, 14), (20, 28, 15, 19), (20, 28, 20, 24), (20, 28, 25, 29), (20, 28, 30, 34)], (20, 28, 35, 40), (20, 28, 39, 42))

elif page == "Scrims Lobby 3":
    render_scrims_tables('547827980', "Scrims Lobby 3", (32, 40, 4), [(32, 40, 5, 9), (32, 40, 10, 14), (32, 40, 15, 19), (32, 40, 20, 24), (32, 40, 25, 29), (32, 40, 30, 34)], (32, 40, 35, 40), (32, 40, 39, 42))

elif page == "Risultati Giocatore":
    st.markdown("<h1 style='text-align: center;'>👤 Player Results</h1>", unsafe_allow_html=True)
    # ... (rest of logic for player results) ...
