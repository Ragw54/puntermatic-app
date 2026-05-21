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

    # Loop through each horse block sequentially
    for horse_name, horse_details in horses_data.items():
        
        # 1. Capture today's variables
        jockey = horse_details.get("Todays_Jockey_Value", "N/A")
        trainer = horse_details.get("Todays_Trainer_Value", "N/A")
        rating = horse_details.get("Live_Rating", "N/A")
        
        # Handle formatting for blank cells coming from Excel
        jockey_display = jockey if jockey else 'Not Listed'
        trainer_display = trainer if trainer else 'Not Listed'
        
        # 2. Design the New Custom HTML Mobile-Responsive Card Container
        st.markdown(f"""
            <div style="
                background-color: #FFFFFF; 
                border-radius: 12px; 
                padding: 20px; 
                margin-top: 25px;
                margin-bottom: 5px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
                border-left: 6px solid #1E3A8A;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 22px; font-weight: 700; color: #111827; letter-spacing: 0.5px;">🏇 {horse_name}</span>
                    <span style="background-color: #10B981; color: white; padding: 6px 14px; border-radius: 8px; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(16,185,129,0.2);">
                        {rating}
                    </span>
                </div>
                <hr style="border: 0; border-top: 1px solid #E5E7EB; margin: 12px 0;">
                <p style="font-size: 15px; color: #4B5563; margin: 0; font-family: 'Segoe UI', Arial, sans-serif;">
                    <strong style="color: #1F2937;">Today's Jockey:</strong> {jockey_display} &nbsp;|&nbsp; 
                    <strong style="color: #1F2937;">Today's Trainer:</strong> {trainer_display}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. Extract and display previous starts history table directly below the card header
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
            
            # Display the data grid seamlessly underneath the card header element
            st.table(history_table)
        else:
            st.caption("No previous starts data available for this runner.")
