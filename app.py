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

# 2. CSS Styling (Sfondo blu ufficiale bandiera UE #003399 e dettagli neri/oro)
st.markdown("""
    <style>
    .stApp { background-color: #003399; }
    h1, h2, h3, p { color: #fff !important; text-align: center; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none; }
    
    /* Navigation buttons style */
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

    /* Standard Table Style */
    .custom-table {
        width: 100%;
        max-width: 600px;
        margin: 0 auto 20px auto;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #ffcc00;
        font-family: sans-serif;
    }
    .custom-table th {
        background-color: #000000;
        color: #ffcc00;
        padding: 10px 14px;
        text-align: center;
        border-bottom: 1px solid #ffcc00;
        font-size: 16px;
    }
    .custom-table td {
        background-color: #000b1a;
        color: #ddd;
        padding: 10px 14px;
        border-bottom: 1px solid #001a33;
        text-align: center;
    }
    .custom-table td:first-child {
        text-align: left; 
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }

    /* Leaderboard Table Style */
    .ranking-table {
        width: 100%;
        max-width: 450px;
        margin: 0 auto 20px auto;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #ffcc00;
        font-family: sans-serif;
    }
    .ranking-table th {
        background-color: #000000;
        color: #ffcc00;
        padding: 10px 14px;
        text-align: center;
        border-bottom: 1px solid #ffcc00;
        font-size: 16px;
    }
    .ranking-table td {
        background-color: #000b1a;
        color: #ddd;
        padding: 10px 14px;
        border-bottom: 1px solid #001a33;
        text-align: center;
    }
    .ranking-table td:first-child {
        text-align: left; 
    }
    .ranking-table tr:last-child td {
        border-bottom: none;
    }
    .ranking-table tbody tr:first-child td {
        color: #ffcc00 !important;
        font-weight: bold !important;
    }

    /* Stat Cards */
    .stat-card {
        background-color: #000000;
        border: 1px solid #ffcc00;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stat-label {
        color: #ffcc00;
        font-size: 0.75rem;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .stat-value {
        color: #fff;
        font-size: 1.1rem;
        font-weight: bold;
    }

    /* Larger Logo Style */
    .logo-container img {
        max-width: 350px;
        width: 100%;
        display: block;
        margin: 0 auto;
    }
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

# 4. Initialize session state for pages
if "page" not in st.session_state:
    st.session_state.page = "Leaderboard"

# 5. Horizontal Navigation Menu (7 pulsanti)
st.write("")
b1, b2, b3, b4, b5, b6, b7 = st.columns(7)

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
with b7:
    if st.button("Personal", use_container_width=True):
        st.session_state.page = "PERSONAL STATS"

st.write("---")

# 6. Data loading function
@st.cache_data(ttl=600)
def load_data(gid):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}'
    return pd.read_csv(url)

# Standard table renderer
def render_custom_table(df_sub, headers):
    html = f'<table class="custom-table"><thead><tr>'
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df_sub.iterrows():
        html += '<tr>'
        for val in row:
            v_str = "" if pd.isna(val) or str(val).lower() == "nan" else str(val)
            html += f'<td>{v_str}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

# Leaderboard table renderer
def render_ranking_table(df_sub, headers):
    html = f'<table class="ranking-table"><thead><tr>'
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df_sub.iterrows():
        html += '<tr>'
        for val in row:
            v_str = "" if pd.isna(val) or str(val).lower() == "nan" else str(val)
            html += f'<td>{v_str}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

# General function to render Scrims tables
def render_scrims_tables(gid, scrim_title, team_coords, game_coords_list):
    st.markdown(f"<h1 style='text-align: center;'>⚔️ {scrim_title} Results</h1>", unsafe_allow_html=True)
    st.write("---")
    
    df = load_data(gid)
    
    try:
        t_start, t_end, t_col = team_coords
        teams = df.iloc[t_start:t_end, t_col].dropna().astype(str).reset_index(drop=True)
        teams = teams[teams.str.strip() != ""]
    except Exception:
        teams = pd.Series(["Team"] * 8)

    num_rows = len(teams)

    for idx, (r_start, r_end, c_start, c_end) in enumerate(game_coords_list, start=1):
        st.markdown(f"<h3 style='text-align: center;'>Game {idx}</h3>", unsafe_allow_html=True)
        try:
            val_df = df.iloc[r_start:r_start+num_rows, c_start:c_end].copy().fillna("")
            val_df.columns = ["Position", "Kills", "DMG", "Revive", "Assist"]
            
            combined_df = pd.DataFrame({"Team": teams})
            for i, col in enumerate(val_df.columns):
                combined_df[col] = val_df.iloc[:, i].values

            st.markdown(render_custom_table(combined_df, ["Team", "Position", "Kills", "DMG", "Revive", "Assist"]), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading Game {idx} data: {e}")

# 7. Page Logic
page = st.session_state.page

if page == "Leaderboard":
    st.markdown("<h1 style='text-align: center;'>🏆 Leaderboard</h1>", unsafe_allow_html=True)
    st.write("---")
    
    df = load_data('316677537')
    
    if not df.empty:
        st.markdown("<h3 style='text-align: center;'>Lobby 1</h3>", unsafe_allow_html=True)
        try:
            lobby1 = df.iloc[12:20, [3, 4]].copy()
            lobby1.columns = ["Team", "Points"]
            lobby1["Points"] = pd.to_numeric(lobby1["Points"].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            st.markdown(render_ranking_table(lobby1, ["Team", "Points"]), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error Lobby 1 Data: {e}")
            
        st.markdown("<h3 style='text-align: center;'>Lobby 2</h3>", unsafe_allow_html=True)
        try:
            lobby2 = df.iloc[12:20, [6, 7]].copy()
            lobby2.columns = ["Team", "Points"]
            lobby2["Points"] = pd.to_numeric(lobby2["Points"].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            st.markdown(render_ranking_table(lobby2, ["Team", "Points"]), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error Lobby 2 Data: {e}")

        st.markdown("<h3 style='text-align: center;'>Lobby 3</h3>", unsafe_allow_html=True)
        try:
            lobby3 = df.iloc[12:21, [9, 10]].copy()
            lobby3.columns = ["Team", "Points"]
            lobby3["Points"] = pd.to_numeric(lobby3["Points"].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            st.markdown(render_ranking_table(lobby3, ["Team", "Points"]), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error Lobby 3 Data: {e}")
    else:
        st.warning("Nessun dato trovato nella Leaderboard.")
elif page == "Regole":
    st.markdown("<h1 style='text-align: center;'>📜 Rules & Info</h1>", unsafe_allow_html=True)
    st.write("---")
    
    scoring_html = """
    <table class="custom-table">
        <thead><tr><th colspan="2">SCORING SYSTEM</th></tr></thead>
        <tbody>
            <tr><td><b>Placement</b></td><td><b>Points</b></td></tr>
            <tr><td>1st</td><td>10 points</td></tr>
            <tr><td>2nd</td><td>8 points</td></tr>
            <tr><td>3rd</td><td>6 points</td></tr>
            <tr><td>4th</td><td>4 points</td></tr>
            <tr><td>5th</td><td>2 points</td></tr>
            <tr><td>6th (& +)</td><td>0 points</td></tr>
            <tr><td>1 Kill</td><td>1 point</td></tr>
            <tr><td>200 damages</td><td>1 point</td></tr>
            <tr><td>Revive factor</td><td>* 0,5 points</td></tr>
        </tbody>
    </table>
    """
    st.markdown(scoring_html, unsafe_allow_html=True)

    info_html = """
    <table class="custom-table">
        <thead><tr><th colspan="2">INFO</th></tr></thead>
        <tbody>
            <tr><td>Map</td><td>EUROQUAD MAPS</td></tr>
            <tr><td>Ping</td><td>EU</td></tr>
            <tr><td>Pod Pul</td><td>Allowed</td></tr>
            <tr><td>Items +/</td><td>Harmonica + /SPR -</td></tr>
            <tr><td>Games</td><td>6</td></tr>
            <tr><td colspan="2" style="font-weight: bold; color: #ffcc00;">“The worst game will NOT be counted” ✅</td></tr>
        </tbody>
    </table>
    """
    st.markdown(info_html, unsafe_allow_html=True)

    zone_html = """
    <table class="custom-table">
        <thead><tr><th colspan="2">ZONE SETTINGS</th></tr></thead>
        <tbody>
            <tr><td>Speed</td><td>130%</td></tr>
            <tr><td>Hold Time</td><td>60%</td></tr>
            <tr><td>Zone Damag</td><td>130%</td></tr>
        </tbody>
    </table>
    """
    st.markdown(zone_html, unsafe_allow_html=True)

elif page == "Scrims Lobby 1":
    s1_teams = (8, 16, 4) 
    s1_games = [
        (8, 16, 5, 10),    
        (8, 16, 11, 16),    
        (8, 16, 17, 22),    
        (8, 16, 23, 28),    
        (8, 16, 29, 34)     # Game 5 (Game 6 rimosso)
    ]
    render_scrims_tables('547827980', "Scrims Lobby 1", s1_teams, s1_games)

elif page == "Scrims Lobby 2":
    s2_teams = (20, 28, 4) 
    s2_games = [
        (20, 28, 5, 10),    
        (20, 28, 11, 16),    
        (20, 28, 17, 22),    
        (20, 28, 23, 28),    
        (20, 28, 29, 34)     # Game 5 (Game 6 rimosso)
    ]
    render_scrims_tables('547827980', "Scrims Lobby 2", s2_teams, s2_games)

elif page == "Scrims Lobby 3":
    s3_teams = (31, 40, 4) 
    s3_games = [
        (31, 40, 5, 10),    
        (31, 40, 11, 16),    
        (31, 40, 17, 22),    
        (31, 40, 23, 28),    
        (31, 40, 29, 34)     # Game 5 (Game 6 rimosso)
    ]
    render_scrims_tables('547827980', "Scrims Lobby 3", s3_teams, s3_games)

elif page == "Risultati Giocatore":
    st.markdown("<h1 style='text-align: center;'>👤 Player Results</h1>", unsafe_allow_html=True)
    st.write("---")
    
    df_player = load_data('717130980')
    headers_player = ["Player", "Kill", "DMG", "MVP", "DHAT", "ACC%"]
    cols = [2, 3, 6, 9, 12, 15]
    
    # --- Lobby 1 ---
    st.markdown("<h3 style='text-align: center;'>Lobby 1</h3>", unsafe_allow_html=True)
    try:
        lobby1_df = df_player.iloc[11:35, cols].copy()
        lobby1_df.columns = headers_player
        st.markdown(render_custom_table(lobby1_df, headers_player), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading Lobby 1 Player Data: {e}")
        
    # --- Lobby 2 ---
    st.markdown("<h3 style='text-align: center;'>Lobby 2</h3>", unsafe_allow_html=True)
    try:
        lobby2_df = df_player.iloc[43:69, cols].copy()
        lobby2_df.columns = headers_player
        st.markdown(render_custom_table(lobby2_df, headers_player), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading Lobby 2 Player Data: {e}")

    # --- Lobby 3 ---
    st.markdown("<h3 style='text-align: center;'>Lobby 3</h3>", unsafe_allow_html=True)
    try:
        lobby3_df = df_player.iloc[71:94, cols].copy() 
        lobby3_df.columns = headers_player
        st.markdown(render_custom_table(lobby3_df, headers_player), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading Lobby 3 Player Data: {e}")
    
# ==========================================
# --- SEZIONE: PERSONAL STATS ---
# ==========================================
elif page == "PERSONAL STATS":
    st.markdown("<div style='background-color: #0e1117; border: 2px solid #262730; border-radius: 12px; padding: 20px;'>", unsafe_allow_html=True)
    st.markdown("### 👤 Personal Stats Dashboard")

    # Inizializzazione sicura delle variabili
    target_ws = None
    current_d13_val = ""
    extracted_players = []

    try:
        creds = ottieni_credenziali()
        if creds:
            client = gspread.authorize(creds)
            sheet = client.open_by_key(SHEET_ID)
            target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_PERSONAL_STATS).strip()), None)
            
            if target_ws:
                # Legge il valore corrente dalla cella D13
                d13_raw = target_ws.acell("D13").value
                if d13_raw is not None and str(d13_raw).strip() != "":
                    current_d13_val = str(d13_raw).strip()
                
                # Estrae la lista dei player dalla colonna C (C12:C60)
                col_c_values = target_ws.get("C12:C60")
                for row in col_c_values:
                    if row and len(row) > 0:
                        p = str(row[0]).strip()
                        if p and p.lower() not in ["nan", "none", ""]:
                            extracted_players.append(p)
                extracted_players = list(dict.fromkeys(extracted_players))
    except Exception as e:
        st.warning(f"Error reading initial Personal Stats sheet: {e}")

    if not extracted_players:
        extracted_players = ["No players available"]

    # Selectbox unico per il Player configurato in D13
    player_index = 0
    if current_d13_val in extracted_players:
        player_index = extracted_players.index(current_d13_val)

    selected_d13_val = st.selectbox("Select Player", extracted_players, index=player_index, key="sb_player_d13")
    
    # Se il player selezionato cambia, aggiorna la cella D13 su Google Sheets e ricarica
    if str(selected_d13_val).strip().lower() != str(current_d13_val).strip().lower():
        scrivi_cella_per_gid(GID_PERSONAL_STATS, "D13", selected_d13_val)
        st.rerun()

    with st.spinner("Updating data..."):
        time.sleep(0.2)

    st.markdown("---")

    def format_val(val, is_percentage=False, decimals=2):
        try:
            if val is None or str(val).strip() == "" or str(val).strip().lower() in ["nan", "none", "#n/a", "#valore!"]:
                return "0.00%" if is_percentage else "0"
            clean_val = str(val).replace("%", "").strip().replace(",", ".")
            num = float(clean_val)
            factor = 10 ** decimals
            truncated = int(num * factor) / factor
            if is_percentage:
                return f"{truncated:.{decimals}f}%"
            elif truncated.is_integer():
                return str(int(truncated))
            else:
                return f"{truncated:.{decimals}f}"
        except Exception:
            return str(val) if val is not None and str(val).strip() != "" else ("0.00%" if is_percentage else "0")

    # Inizializzazione variabili Match Summary (14 campi totali)
    summary_fired, summary_hit, summary_acc, summary_kill, summary_dmg, summary_mvp, summary_death = "0", "0", "0.00%", "0", "0", "0", "0"
    summary_revive, summary_oh_shots, summary_oh_hit, summary_oh_acc = "0", "0", "0", "0.00%"
    summary_th_shots, summary_th_hit, summary_th_acc = "0", "0", "0", "0.00%"
    
    faster_banana_val = "-"
    total_assist_val = "0"
    
    deadliest_weapons = []
    weapon_rows_data = []

    try:
        if target_ws:
            # 1. Match Summary (Riga 16, da F16 a S16)
            f16_s16 = target_ws.get("F16:S16")
            if f16_s16 and len(f16_s16) > 0:
                rv = f16_s16[0]
                summary_fired   = format_val(rv[0] if len(rv) > 0 else 0)
                summary_hit     = format_val(rv[1] if len(rv) > 1 else 0)
                summary_acc     = format_val(rv[2] if len(rv) > 2 else 0, is_percentage=True)
                summary_kill    = format_val(rv[3] if len(rv) > 3 else 0)
                summary_dmg     = format_val(rv[4] if len(rv) > 4 else 0)
                summary_mvp     = format_val(rv[5] if len(rv) > 5 else 0)
                summary_death   = format_val(rv[6] if len(rv) > 6 else 0)
                summary_revive  = format_val(rv[7] if len(rv) > 7 else 0)
                summary_oh_shots= format_val(rv[8] if len(rv) > 8 else 0)
                summary_oh_hit  = format_val(rv[9] if len(rv) > 9 else 0)
                summary_oh_acc  = format_val(rv[10] if len(rv) > 10 else 0, is_percentage=True)
                summary_th_shots= format_val(rv[11] if len(rv) > 11 else 0)
                summary_th_hit  = format_val(rv[12] if len(rv) > 12 else 0)
                summary_th_acc  = format_val(rv[13] if len(rv) > 13 else 0, is_percentage=True)

            # 2. Faster Banana (Riga 18)
            j18_l18 = target_ws.get("J18:L18")
            if j18_l18 and len(j18_l18) > 0 and len(j18_l18[0]) > 0:
                faster_banana_val = format_val(j18_l18[0][0])

            # 2.1 Total Assist (Q18:S18)
            q18_s18 = target_ws.get("Q18:S18")
            if q18_s18 and len(q18_s18) > 0:
                row_qa = q18_s18[0]
                for cell_val in row_qa:
                    v_str = str(cell_val).strip()
                    if v_str and v_str.lower() not in ["nan", "none", ""]:
                        total_assist_val = format_val(v_str)
                        break

            # 3. Deadliest Weapons (Configurazioni mirate per Nome Arma e Dati)
            dw_configs = [
                {"name_range": "H20:I20", "data_range": "H21:S21"},
                {"name_range": "H23:I23", "data_range": "H24:S24"},
                {"name_range": "H26:I26", "data_range": "H27:S27"}
            ]

            for cfg in dw_configs:
                # Legge il nome dell'arma
                n_data = target_ws.get(cfg["name_range"])
                w_name = "-"
                if n_data and len(n_data) > 0:
                    row_n = n_data[0]
                    for cell in row_n:
                        val_str = str(cell).strip()
                        if val_str and val_str.lower() not in ["nan", "none", ""]:
                            w_name = val_str
                            break

                # Legge i dati dell'arma
                r_data = target_ws.get(cfg["data_range"])
                if r_data and len(r_data) > 0:
                    r_w = r_data[0]
                    # H=col 0, I=1, J=2, K=3 (DMG), L=4 (ACC%), M=5, N=6 (Onehand), O=7 (Shit Onehand), P=8 (Acc One), Q=9 (Tohand), R=10 (Shit Tohand), S=11 (Acc Two)
                    deadliest_weapons.append({
                        "name": w_name,
                        "dmg": format_val(r_w[3] if len(r_w) > 3 else 0),          # K
                        "acc": format_val(r_w[4] if len(r_w) > 4 else 0, is_percentage=True), # L
                        "onehand": format_val(r_w[6] if len(r_w) > 6 else 0),      # N
                        "shit_onehand": format_val(r_w[7] if len(r_w) > 7 else 0),# O
                        "acc_onehand": format_val(r_w[8] if len(r_w) > 8 else 0, is_percentage=True), # P
                        "twohand": format_val(r_w[9] if len(r_w) > 9 else 0),    # Q
                        "shit_twohand": format_val(r_w[10] if len(r_w) > 10 else 0),# R
                        "acc_twohand": format_val(r_w[11] if len(r_w) > 11 else 0, is_percentage=True)  # S
                    })
                else:
                    deadliest_weapons.append({
                        "name": w_name, "dmg": "0", "acc": "0.00%", 
                        "onehand": "0", "shit_onehand": "0", "acc_onehand": "0.00%", 
                        "twohand": "0", "shit_twohand": "0", "acc_twohand": "0.00%"
                    })

            # 4. Tabella Armi aggiornata all'intervallo F33:S74
            weapons_raw = target_ws.get("F33:S74")
            if weapons_raw:
                for r_data in weapons_raw:
                    if r_data and len(r_data) > 0:
                        w_name = str(r_data[0]).strip()
                        if w_name and w_name.upper() not in ["NAN", "NONE", ""]:
                            weapon_rows_data.append({
                                "WEAPON": w_name,
                                "TOT SHOTS": format_val(r_data[1] if len(r_data) > 1 else 0),
                                "SHOT HIT": format_val(r_data[2] if len(r_data) > 2 else 0),
                                "ACC%": format_val(r_data[3] if len(r_data) > 3 else 0, is_percentage=True),
                                "DMG": format_val(r_data[4] if len(r_data) > 4 else 0),
                                "HEADSHOT": format_val(r_data[5] if len(r_data) > 5 else 0),
                                "MAX DISTANCE": format_val(r_data[6] if len(r_data) > 6 else 0),
                                "SHOT ONE": format_val(r_data[8] if len(r_data) > 8 else 0),
                                "SHOT HIT ONE": format_val(r_data[9] if len(r_data) > 9 else 0),
                                "ACC% ONE": format_val(r_data[10] if len(r_data) > 10 else 0, is_percentage=True),
                                "SHOT TWO": format_val(r_data[11] if len(r_data) > 11 else 0),
                                "SHOT HIT TWO": format_val(r_data[12] if len(r_data) > 12 else 0),
                                "ACC% TWO": format_val(r_data[13] if len(r_data) > 13 else 0, is_percentage=True)
                            })
    except Exception as e:
        st.warning(f"Error reading dashboard data: {e}")

    # --- RENDER UI: MATCH SUMMARY ---
    st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>MATCH SUMMARY</h4>", unsafe_allow_html=True)
    c_grid1, c_grid2, c_grid3 = st.columns(3)
    
    with c_grid1:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>DMG</div><div class='stat-value'>{summary_dmg}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>SHOTS FIRED</div><div class='stat-value'>{summary_fired}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>DEATH</div><div class='stat-value'>{summary_death}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND SHOTS</div><div class='stat-value'>{summary_oh_shots}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND SHOTS</div><div class='stat-value'>{summary_th_shots}</div></div>", unsafe_allow_html=True)

    with c_grid2:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>KILL</div><div class='stat-value'>{summary_kill}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>SHOTS HIT</div><div class='stat-value'>{summary_hit}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>REVIVE</div><div class='stat-value'>{summary_revive}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND HIT</div><div class='stat-value'>{summary_oh_hit}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND HIT</div><div class='stat-value'>{summary_th_hit}</div></div>", unsafe_allow_html=True)

    with c_grid3:
        st.markdown(f"<div class='stat-card'><div class='stat-label'>MVP</div><div class='stat-value'>{summary_mvp}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>ACCURACY</div><div class='stat-value'>{summary_acc}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>FASTER BANANA</div><div class='stat-value'>{faster_banana_val}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND ACC%</div><div class='stat-value'>{summary_oh_acc}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND ACC%</div><div class='stat-value'>{summary_th_acc}</div></div>", unsafe_allow_html=True)

    # --- RENDER UI: TOTAL ASSIST (Full-width card inserita prima di Deadliest) ---
    st.markdown(f"""
    <div class='stat-card' style='width: 100%; height: 85px; margin-top: 10px;'>
        <div class='stat-label'>TOTAL ASSIST</div>
        <div class='stat-value'>{total_assist_val}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- RENDER UI: DEADLIEST WEAPONS (1, 2, 3) IN BOXES ---
    st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>DEADLIEST WEAPONS</h4>", unsafe_allow_html=True)
    
    for i, dw in enumerate(deadliest_weapons):
        st.markdown(f"""
        <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
            <p style='color: #93c5fd; font-weight: bold; font-size: 1.1rem; margin-top: 0; margin-bottom: 12px; text-align: center;'>
                Deadliest Weapon {i+1}: {dw['name']}
            </p>
        """, unsafe_allow_html=True)
        
        # 1ª Riga: DMG e ACC%
        dw_r1_c1, dw_r1_c2 = st.columns(2)
        with dw_r1_c1:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>DMG</div><div class='stat-value'>{dw['dmg']}</div></div>", unsafe_allow_html=True)
        with dw_r1_c2:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC%</div><div class='stat-value'>{dw['acc']}</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # 2ª Riga: ONEHAND, SHIT ONEHAND, ACC% ONE
        dw_r2_c1, dw_r2_c2, dw_r2_c3 = st.columns(3)
        with dw_r2_c1:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND</div><div class='stat-value'>{dw['onehand']}</div></div>", unsafe_allow_html=True)
        with dw_r2_c2:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT ONEHAND</div><div class='stat-value'>{dw['shit_onehand']}</div></div>", unsafe_allow_html=True)
        with dw_r2_c3:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% ONE</div><div class='stat-value'>{dw['acc_onehand']}</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # 3ª Riga: TWOHAND, SHIT TWOHAND, ACC% TWO
        dw_r3_c1, dw_r3_c2, dw_r3_c3 = st.columns(3)
        with dw_r3_c1:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND</div><div class='stat-value'>{dw['twohand']}</div></div>", unsafe_allow_html=True)
        with dw_r3_c2:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT TWOHAND</div><div class='stat-value'>{dw['shit_twohand']}</div></div>", unsafe_allow_html=True)
        with dw_r3_c3:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% TWO</div><div class='stat-value'>{dw['acc_twohand']}</div></div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- RENDER UI: WEAPON PERFORMANCE TABLE ---
    st.markdown("<h4 style='color: #93c5fd; text-align: center;'>WEAPON PERFORMANCE</h4>", unsafe_allow_html=True)
    
    if weapon_rows_data:
        df_weapons_final = pd.DataFrame(weapon_rows_data)
    else:
        df_weapons_final = pd.DataFrame(columns=[
            "WEAPON", "TOT SHOTS", "SHOT HIT", "ACC%", "DMG", "HEADSHOT", "MAX DISTANCE", 
            "SHOT ONE", "SHOT HIT ONE", "ACC% ONE", "SHOT TWO", "SHOT HIT TWO", "ACC% TWO"
        ])

    st.dataframe(df_weapons_final, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)
