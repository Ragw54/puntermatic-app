import streamlit as st
import requests

# 1. FORCE THE WIDE LAYOUT FOR PERFECT CROSS-SCREEN ALIGNMENT
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# 2. INJECT CUSTOM STREAMLIT APP OVERRIDES
st.markdown("""
    <style>
    /* Force main app background color (Light slate gray look) */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Global font enforcement */
    h1, h2, h3, p, label {
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }

    /* CENTER & STYLE THE DROPDOWN HEADER LABEL */
    div[data-testid="stSelectbox"] label p {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #175cad !important; 
        text-align: center !important;
        display: block !important;
        margin-bottom: 5px !important;
    }
    
    /* ENFORCE DROPDOWN MENU TEXT COLOR AND SIZE (FIXES image_2.png issue) */
    div[data-testid="stSelectbox"] [data-baseweb="select"] div {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #175cad !important; /* MATCHES SELECT A RACE COLOR */
        text-align: center !important;
    }

    /* Align select box container to the center column design */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        max-width: 400px !important;
        margin: 0 auto !important;
    }

    /* CENTER AND UPCASE THE MAIN PUNTERMATIC HEADER IN #175cad */
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
    
    /* CENTER AND COLOR THE SUB-TITLE TO #175cad */
    .sub-title {
        font-size: 32px !important; 
        font-weight: 800 !important;
        color: #175cad !important; 
        text-align: center !important;        
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }

    /* OVERHAUL HORSE PANELS: BACKGROUND #175cad */
    div[data-testid="stExpander"] {
        background-color: #175cad !important; /* Horse background color restored */
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 6px !important; 
        padding: 0px !important;
        overflow: visible !important;
    }

    /* HIDE the default plain text Streamlit expander summary row entirely */
    div[data-testid="stExpander"] details summary span {
        display: none !important;
    }

    /* Style the clickable AREA (the underlying trigger bar) */
    div[data-testid="stExpander"] details summary {
        padding: 12px 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    
    /* Make the interactive expansion arrow white to match the theme */
    div[data-testid="stExpander"] details summary svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* Expander Inner Content Container (The white block that opens) */
    div[data-testid="stExpander"] details div[data-testid="stVerticalBlock"] {
        background-color: #FFFFFF !important; 
        padding: 15px !important;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        margin-top: 0px !important;
    }

    /* ENFORCE HORIZONTAL SCROLLING FOR PREVIOUS STARTS HISTORY TABLE */
    div.stTable {
        background-color: #FFFFFF !important;
        margin-top: 5px;
        overflow-x: auto !important; 
        display: block !important;
        width: 100% !important;
    }
    
    /* Centered horizontal divider line layout */
    hr {
        max-width: 600px !important;
        margin: 10px auto 20px auto !important;
        border-color: #175cad !important;
        opacity: 0.3;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
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
    st.error("Unable to connect to Firebase database URL.")
else:
    race_list = sorted(list(all_races.keys()))
    
    # 1. UPPERCASE & Centered Main Title
    st.markdown(f'<h1 class="main-title">PUNTERMATIC</h1>', unsafe_allow_html=True)
    
    # 2. Centered Selection Box with Matching Blue Typography Layout
    selected_race = st.selectbox("Select a Race", race_list, key="race_selector_centered_v4")

    # 3. Centered Race Number (e.g., R1) in Blue
    st.markdown(f'<h2 class="sub-title">{selected_race}</h2>', unsafe_allow_html=True)
    st.write("---")

    horses_data = all_races[selected_race]

    # Deep ranking sort mechanism
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

    # Render sorted runners list
    for horse_name, horse_details in sorted_horses:
        
        jockey = horse_details.get("Today's Jockey Value", horse_details.get("Todays_Jockey_Value", ""))
        trainer = horse_details.get("Today's Trainer Value", horse_details.get("Todays_Trainer_Value", ""))
        rating = horse_details.get("Live Rating", horse_details.get("Live_Rating", "N/A"))
        
        if str(jockey).strip() in ["", "None", "0", "0.0"]:
            jockey_display = "Unrated"
        else:
            jockey_display = jockey

        if str(trainer).strip() in ["", "None", "0", "0.0"]:
            trainer_display = "Unrated"
        else:
            trainer_display = trainer
            
        rating_display = str(rating).strip() if str(rating).strip() != "" else "N/A"
        
        # Unique tracking key to fix the expansion toggle drop bug completely
        unique_key = f"panel_{selected_race}_{horse_name.replace(' ', '_')}"
        
        # FIXED: Expander now only acts as the opening TRIGGER for the internal history.
        # It's actual plain-text title parameter is blank to prevent code leak (image_1.png).
        with st.expander("", expanded=False):
            
            # THE FIX: Bypassing st.expander restrictions by injecting custom HEADER HTML inside the panel!
            # This absolute-positioned block recreates the blue header row and places the styled text perfectly.
            st.markdown(f"""
                <div style="
                    position: absolute;
                    top: -42px;
                    left: 45px;
                    pointer-events: none;
                    z-index: 999;
                    font-family: 'Segoe UI', Arial, sans-serif;
                ">
                    <span style="font-size: 19px; font-weight: 800; color: #FFFFFF;">{horse_name}</span>
                    <span style="font-size: 19px; font-weight: 800; color: #FFFFFF;"> &nbsp;|&nbsp; Rating: </span>
                    <span style="font-size: 19px; font-weight: 800; color: #FFFF00;">{rating_display}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Connection summary information row block
            st.markdown(f"""
                <div style="
                    background-color: #F8F9FA; 
                    padding: 12px 15px; 
                    border-radius: 6px; 
                    margin-top: 5px; 
                    margin-bottom: 15px; 
                    border-left: 4px solid #175cad;
                ">
                    <p style="font-size: 15px; color: #4B5563; margin: 0;">
                        <strong style="color: #1F2937;">Today's Jockey:</strong> {jockey_display} &nbsp;|&nbsp; 
                        <strong style="color: #1F2937;">Today's Trainer:</strong> {trainer_display}
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
                st.caption("No previous starts data available for this runner.")
