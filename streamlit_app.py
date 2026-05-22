import streamlit as st
import requests

# 1. FORCE THE WIDE LAYOUT FOR PERFECT CROSS-SCREEN ALIGNMENT
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# 2. INJECT CLEAN GLOBAL OVERRIDES (NO ABSOLUTE POSITIONING)
st.markdown("""
    <style>
    /* Force main app background color */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Global font enforcement */
    h1, h2, h3, p, label {
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }

    /* COLOR THE DROPDOWN HEADER LABEL TO SIGNATURE BLUE & MAKE IT BOLD */
    div[data-testid="stSelectbox"] label p {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #175cad !important; 
        margin-bottom: 5px !important;
    }
    
    /* Perfect spacing for the moved dropdown position */
    div[data-testid="stSelectbox"] {
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }

    /* TIGHTEN MAIN HEADER MARGINS */
    .main-title {
        font-size: 46px !important;
        font-weight: 900 !important;
        color: #111827 !important;
        margin-top: -40px !important;
        margin-bottom: 0px !important;
        padding-top: 0px !important;
    }
    
    .sub-title {
        font-size: 30px !important; 
        font-weight: 800 !important;
        color: #4B5563 !important;
        margin-top: 5px !important;
        margin-bottom: 15px !important;
    }

    /* OVERHAUL HORSE PANELS: BACKGROUND #175cad, REMOVE SHADOWS */
    div[data-testid="stExpander"] {
        background-color: #175cad !important;
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 6px !important; 
        padding: 0px !important;
    }

    /* Restore and style the clickable native header text */
    div[data-testid="stExpander"] details summary {
        padding: 12px 15px !important;
    }

    /* Make the horse name portion bold and clean white */
    div[data-testid="stExpander"] details summary span p {
        font-size: 19px !important;
        font-weight: 800 !important; 
        color: #FFFFFF !important;   
    }
    
    /* TARGET EVERY RED TEXT VALUE INSIDE THE EXPANDER SUMMARY AND FORCE IT YELLOW */
    /* Markdown colored strings render as HTML color elements behind the scenes */
    div[data-testid="stExpander"] details summary span p span[style*="color: red"],
    div[data-testid="stExpander"] details summary span p color[color="red"] {
        color: #FFFF00 !important;
    }

    /* Make the interactive expansion arrow white to match the theme */
    div[data-testid="stExpander"] details summary svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* Expander Inner Content Container */
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
    
    /* Subtle divider line adjustment */
    hr {
        margin-top: 5px !important;
        margin-bottom: 15px !important;
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
    
    # 1. Puntermatic Title at the absolute top
    st.markdown(f'<h1 class="main-title">Puntermatic</h1>', unsafe_allow_html=True)
    
    # 2. Select box colored blue sitting in between the text headers
    selected_race = st.selectbox("Select a Race", race_list, key="race_selector_v3")

    # 3. R1 header sitting two text sizes lower
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
        
        # FIX STAINED TEXT TAGS: We pass a clear Markdown text string to the title parameter.
        # We flag the rating value with a standard ":red[]" markdown wrapper. 
        # Our custom CSS block intercepting from the top swaps that red tag into bright bright yellow!
        expander_title = f"{horse_name}  |  Rating: :red[{rating_display}]"
        
        with st.expander(expander_title, expanded=False):
            
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
