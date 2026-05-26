import streamlit as st
import requests
import re

# 1. FORCE THE WIDE LAYOUT FOR PERFECT CROSS-SCREEN ALIGNMENT
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# ==============================================================================
# PRIVATE ACCESS CONFIGURATION (ADMIN USER LOCK)
# ==============================================================================
# Change this to your true email address
ALLOWED_USERS = [
    "ragw54@gmail.com"
]

# Initialize login tracking token states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Web API function to securely verify credentials via Firebase REST Authentication
def firebase_auth(email, password, action="signInWithPassword"):
    API_KEY = st.secrets["FIREBASE_API_KEY"] 
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{action}?key={API_KEY}"
    
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            error_msg = response.json().get("error", {}).get("message", "Authentication Failed")
            return False, error_msg
    except Exception as e:
        return False, str(e)

# ==============================================================================
# INJECT DESIGN LAYOUT OVERRIDES (GLOBAL APP STYLING)
# ==============================================================================
st.markdown("""
    <style>
    .stApp {
        background-color: #F3F4F6;
    }
    h1, h2, h3, p, label {
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    div[data-testid="stSelectbox"] label p {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #175cad !important; 
        text-align: center !important;
        display: block !important;
        margin-bottom: 5px !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] div {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #175cad !important; 
        text-align: center !important;
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        max-width: 400px !important;
        margin: 0 auto !important;
        border-color: #175cad !important;
    }
    .main-title {
        font-size: 48px !important;
        font-weight: 900 !important;
        color: #175cad !important; 
        text-transform: uppercase !important; 
        text-align: center !important;        
        margin-top: -30px !important;
        margin-bottom: 10px !important;
        padding-top: 0px !important;
    }
    .sub-title {
        font-size: 32px !important; 
        font-weight: 800 !important;
        color: #175cad !important; 
        text-align: center !important;        
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] details summary {
        background-color: #175cad !important; 
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stExpander"] {
        margin-bottom: 8px !important; 
        padding: 0px !important;
    }
    div[data-testid="stExpander"] details summary {
        padding: 12px 15px !important;
    }
    div[data-testid="stExpander"] details summary p,
    div[data-testid="stExpander"] details summary span,
    div[data-testid="stExpander"] details[open] summary p,
    div[data-testid="stExpander"] details[open] summary span {
        font-size: 19px !important;
        font-weight: 800 !important; 
        color: #FFFFFF !important;   
        opacity: 1.0 !important;
        display: inline-block !important;
    }
    div[data-testid="stExpander"] details summary svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stExpander"] details div[data-testid="stVerticalBlock"] {
        background-color: #FFFFFF !important; 
        padding: 15px !important;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        margin-top: 0px !important;
    }
    div.stTable {
        background-color: #FFFFFF !important;
        margin-top: 5px;
        overflow-x: auto !important; 
        display: block !important;
        width: 100% !important;
    }
    hr {
        max-width: 600px !important;
        margin: 10px auto 20px auto !important;
        border-color: #175cad !important;
        opacity: 0.3;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# DISPLAY AUTHENTICATION GATEKEEPER SCREEN
# ==============================================================================
if not st.session_state.logged_in:
    st.markdown("<br><h1 style='text-align: center; color: #175cad;'>PUNTERMATIC DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4B5563;'>Secure Single-User Data Environment</p><br>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        auth_tab, signup_tab = st.tabs(["🔒 Account Login", "📝 Register User"])
        
        with auth_tab:
            st.write(" ")
            login_email = st.text_input("Email Address", key="login_email_input").strip().lower()
            login_password = st.text_input("Password", type="password", key="login_pass_input")
            st.write(" ")
            
            if st.button("Log In", type="primary", use_container_width=True):
                if login_email not in ALLOWED_USERS:
                    st.error("Access Denied: This account is not authorized to access this dashboard.")
                else:
                    success, result = firebase_auth(login_email, login_password, "signInWithPassword")
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = login_email
                        st.success("Access Granted! Loading your workspace...")
                        st.rerun()
                    else:
                        st.error(f"Login Failed: {result.replace('_', ' ')}")
                    
        with signup_tab:
            st.write(" ")
            new_email = st.text_input("Enter Email Address", key="signup_email_input").strip().lower()
            new_password = st.text_input("Create Password (Min 6 Characters)", type="password", key="signup_pass_input")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_input")
            st.write(" ")
            
            if st.button("Register Authorized Account", use_container_width=True):
                if new_email not in ALLOWED_USERS:
                    st.error("Registration Blocked: Email address is not on the authorized developer list.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    success, result = firebase_auth(new_email, new_password, "signUp")
                    if success:
                        st.success("Account created successfully! You can now switch to the Login tab.")
                    else:
                        st.error(f"Registration Failed: {result.replace('_', ' ')}")

    st.stop()

# ==============================================================================
# MAIN APPLICATION INTERFACE (RUNS ONLY IF ACCESS GRANTED)
# ==============================================================================
with st.sidebar:
    st.write(f"Workspace Identity:")
    st.code(st.session_state.user_email)
    st.write(" ")
    if st.button("Log Out of Dashboard", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

FIREBASE_DB_URL = st.secrets["FIREBASE_URL"] + "races.json"

@st.cache_data(ttl=10)
def fetch_race_data():
    try:
        response = requests.get(FIREBASE_DB_URL)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

all_races = fetch_race_data()

if not all_races:
    st.error("Unable to connect to your Firebase database URL endpoint.")
else:
    race_list = sorted(list(all_races.keys()))
    
    # 1. RACES Header layout
    st.markdown(f'<h1 class="main-title">RACES</h1>', unsafe_allow_html=True)
    
    selected_race = st.selectbox("Select a Race", race_list, key="race_selector_final_v4")

    st.markdown(f'<h2 class="sub-title">{selected_race}</h2>', unsafe_allow_html=True)
    st.write("---")

    horses_data = all_races[selected_race]

    def get_rating_value(item):
        try:
            details = item[1]
            val = details.get("Live Rating", details.get("Live_Rating", details.get("LiveRating", 0)))
            if val is None or str(val).strip() == "" or str(val).strip().upper() == "N/A":
                return 0.0
            return float(str(val).strip())
        except (ValueError, TypeError):
            return 0.0

    sorted_horses = sorted(horses_data.items(), key=get_rating_value, reverse=True)

    for horse_name, horse_details in sorted_horses:
        
        # Pulling data points dynamically from your newly structured JSON keys
        jockey_name = horse_details.get("Jockey", horse_details.get("Jockey Name", "TBA")) 
        trainer_name = horse_details.get("Trainer", horse_details.get("Trainer Name", "TBA"))
        weight_val = horse_details.get("Weight", "N/A")
        
        jockey_val = horse_details.get("Today's Jockey Value", horse_details.get("Todays_Jockey_Value", ""))
        trainer_val = horse_details.get("Today's Trainer Value", horse_details.get("Todays_Trainer_Value", ""))
        rating = horse_details.get("Live Rating", horse_details.get("Live_Rating", "N/A"))
        
        jockey_val_display = "Unrated" if str(jockey_val).strip() in ["", "None", "0", "0.0"] else jockey_val
        trainer_val_display = "Unrated" if str(trainer_val).strip() in ["", "None", "0", "0.0"] else trainer_val
        rating_display = str(rating).strip() if str(rating).strip() != "" else "N/A"
        
        expander_title = f"{horse_name}  |  Rating: :rainbow[{rating_display}]"
        
        with st.expander(expander_title, expanded=False):
            st.markdown(f"""
                <style>
                div[data-testid="stExpander"] details summary p span,
                div[data-testid="stExpander"] details summary span span {{
                    color: #FFFF00 !important;
                    background: none !important;
                    -webkit-text-fill-color: #FFFF00 !important;
                }}
                </style>
                
                <div style="
                    background-color: #F8F9FA; 
                    padding: 12px 15px; 
                    border-radius: 6px; 
                    margin-top: 5px; 
                    margin-bottom: 15px; 
                    border-left: 4px solid #175cad;
                    line-height: 1.6;
                ">
                    <p style="font-size: 15px; color: #4B5563; margin: 0;">
                        <strong style="color: #1F2937;">Jockey:</strong> {jockey_name}<br>
                        <strong style="color: #1F2937;">Trainer:</strong> {trainer_name}<br>
                        <strong style="color: #1F2937;">Weight:</strong> {weight_val}<br>
                        <strong style="color: #1F2937;">Jockey Value:</strong> {jockey_val_display}<br>
                        <strong style="color: #1F2937;">Trainer Value:</strong> {trainer_val_display}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            prev_starts = horse_details.get("Previous_Starts", {})
            if prev_starts:
                history_table = []
                for start_id in sorted(prev_starts.keys()):
                    start_data = prev_starts[start_id]
                    history_table.append({
                        "Form": start_data.get("Form", ""),
                        "Dist": start_data.get("Distance", ""),
                        "Class": start_data.get("Class", ""),
                        "Wgt": start_data.get("Weight", ""),
                        "Barr": start_data.get("Barrier", ""),
                        "Track": start_data.get("Track_Status", "")
                    })
                st.table(history_table)
            else:
                st.caption("No historical run data files mapped for this selection.")
