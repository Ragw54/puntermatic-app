import streamlit as st
import requests

# 1. FORCE THE WIDE LAYOUT FOR PERFECT CROSS-SCREEN ALIGNMENT
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# 2. INJECT CUSTOM GLOBAL THEMING (COLORS, FONTS, AND CARDS)
st.markdown("""
    <style>
    /* Force main app background color (Light slate gray look) */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Style all native dropdown selectors and basic text elements to use sharp fonts */
    h1, h2, h3, p, label {
        font-family: 'Segoe UI', Arial, sans-serif !important;
        color: #1F2937 !important;
    }
    
    /* Style your selection buttons */
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }

    /* TRANSFORM EXPANDERS: Make them look like premium white cards */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        border-left: 6px solid #1E3A8A !important; /* Premium navy-blue left accent strip */
    }

    /* Style the clickable text header inside the expander bar */
    div[data-testid="stExpander"] details summary {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        padding: 10px 5px !important;
    }

    /* Style the historical table container to blend with the card */
    div.stTable {
        background-color: #FFFFFF !important;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
FIREBASE_DB_URL = st.secrets["FIREBASE_URL"] + "races.json"

@st.cache_data(ttl=10)  # Refresh data every 10 seconds automatically
def fetch_race_data():
    try:
        response = requests.get(FIREBASE_DB_URL)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

# Fetch data from your cloud bridge
all_races = fetch_race_data()

if not all_races:
    st.error("Unable to connect to Firebase. Please check your network or database URL.")
else:
    # Create a clean tab or dropdown selector for Races R1 to R10
    race_list = sorted(list(all_races.keys()))
    selected_race = st.selectbox("Select a Race", race_list)

    st.title(f"🏇 Puntermatic - {selected_race}")
    st.write("---")

    # Get the horse records for the selected race sheet
    horses_data = all_races[selected_race]

    # ==============================================================================
    # DEEP HUNT SORTING: Checks all database variations to find the number
    # ==============================================================================
    def get_rating_value(item):
        try:
            details = item[1]
            # Look inside every key variation we've used across edits
            val = details.get("Live Rating", details.get("Live_Rating", details.get("LiveRating", 0)))
            if val is None or str(val).strip() == "" or str(val).strip().upper() == "N/A":
                return 0.0
            return float(str(val).strip())
        except (ValueError, TypeError):
            return 0.0

    # Sort the horses: highest rating goes to the top
    sorted_horses = sorted(horses_data.items(), key=get_rating_value, reverse=True)

    # Loop through each horse block in sorted order
    for horse_name, horse_details in sorted_horses:
        
        # Pull values using deep fallbacks to ensure nothing stays blank
        jockey = horse_details.get("Today's Jockey Value", horse_details.get("Todays_Jockey_Value", ""))
        trainer = horse_details.get("Today's Trainer Value", horse_details.get("Todays_Trainer_Value", ""))
        rating = horse_details.get("Live Rating", horse_details.get("Live_Rating", "N/A"))
        
        # Clean up empty strings or zero entries dynamically
        if str(jockey).strip() in ["", "None", "0", "0.0"]:
            jockey_display = "Unrated"
        else:
            jockey_display = jockey

        if str(trainer).strip() in ["", "None", "0", "0.0"]:
            trainer_display = "Unrated"
        else:
            trainer_display = trainer
            
        rating_display = str(rating).strip() if str(rating).strip() != "" else "N/A"
        
        # 2. Native text string title for the clean dropdown button style
        expander_title = f"🏇 {horse_name} | Rating: {rating_display}"
        
        # 3. Open/Close dropdown capability with hidden categories inside
        with st.expander(expander_title, expanded=False):
            
            # Put Today's Jockey and Trainer inside a dedicated shaded row bar
            st.markdown(f"""
                <div style="
                    background-color: #F8F9FA; 
                    padding: 12px 15px; 
                    border-radius: 6px; 
                    margin-top: 5px; 
                    margin-bottom: 15px; 
                    border-left: 4px solid #1E3A8A;
                ">
                    <p style="font-size: 15px; color: #4B5563; margin: 0; font-family: 'Segoe UI', Arial, sans-serif;">
                        <strong style="color: #1F2937;">Today's Jockey:</strong> {jockey_display} &nbsp;|&nbsp; 
                        <strong style="color: #1F2937;">Today's Trainer:</strong> {trainer_display}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Extract previous starts history sub-tree
            prev_starts = horse_details.get("Previous_Starts", {})
            
            if prev_starts:
                # Reconstruct the nested history dictionary into a clean list for presentation
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
                
                # Display the data grid inside the open dropdown container cleanly
                st.table(history_table)
            else:
                st.caption("No previous starts data available for this runner.")
