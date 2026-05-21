import streamlit as st
import requests

# Set mobile-first page layout configurations
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="centered")

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# Tell the app to fetch your real URL straight from the Streamlit Secrets box
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
        
        # 2. Design the Visible Header Row
        header_text = f"**{horse_name}** | Rating: `{rating}`"
        
        # 3. Create the Native Expandable Container (The Dropdown Box)
        with st.expander(header_text):
            # Display today's extra live parameters clearly
            st.markdown(f"**Today's Jockey:** {jockey} | **Today's Trainer:** {trainer}")
            
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
