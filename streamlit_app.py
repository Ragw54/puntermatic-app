import streamlit as st
import json
import os

# Set wide layout
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# ------------------------------------------------------------------------------
# CLEAN CSS: SMALL LEFT-ALIGNED MENU BUTTON ABOVE PUNTERMATIC HEADER
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Pull page content up to the top */
    .block-container {
        padding-top: 0.1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Hide standard internal Streamlit header container */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* TOP ROW: LEFT MENU BUTTON & PUNTERMATIC HEADER */
    .punter-header-container {
        text-align: center !important;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
    }
    
    /* PUNTERMATIC MAIN TITLE */
    .punter-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #216bd1 !important;
        letter-spacing: 1.5px !important;
        margin-bottom: 0px !important;
        line-height: 1.1 !important;
    }
    
    /* Race Selection Label under PUNTERMATIC */
    .race-select-label {
        font-size: 1.35rem !important;
        font-weight: 400 !important;
        color: #216bd1 !important;
        margin-top: 0px !important;
        margin-bottom: 4px !important;
        text-align: center !important;
        width: 100% !important;
    }

    /* COMPACT, SMALL LEFT-ALIGNED 'MENU' BUTTON */
    .menu-button-container div.stButton > button {
        background-color: #216bd1 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border-radius: 6px !important;
        padding: 4px 12px !important;
        margin: 0 !important;
        display: inline-block !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        width: auto !important;
        min-height: unset !important;
        height: auto !important;
    }
    .menu-button-container div.stButton > button:hover {
        background-color: #1E3A8A !important;
        color: #FFD700 !important;
    }
    
    /* -------------------------------------------------------------------------
       MAIN PAGE RACE SELECTOR (3 ACROSS, CENTERED, CLEAN BUTTONS)
       ------------------------------------------------------------------------- */
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] > label {
        display: none !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 8px !important;
        width: 600px !important;
        max-width: 90vw !important;
        margin-left: auto !important;
        margin-right: auto !important;
        justify-content: center !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
        display: none !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #F1F5F9 !important;
        border: 2px solid #216bd1 !important;
        border-radius: 8px !important;
        padding: 8px 0px !important;
        text-align: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        margin: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #216bd1 !important;
        margin: 0 !important;
        text-align: center !important;
    }
    
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background-color: #216bd1 !important;
        border-color: #216bd1 !important;
    }
    div[data-testid="stMainBlockContainer"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
        color: #FFFFFF !important;
    }

    /* -------------------------------------------------------------------------
       SIDEBAR NAVIGATION STYLING (#216bd1 TEXT & CHECKBOX CIRCLES)
       ------------------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        width: 320px !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #216bd1 !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #216bd1 !important;
    }
    
    section[data-testid="stSidebar"] input[type="radio"] {
        accent-color: #216bd1 !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* -------------------------------------------------------------------------
       CATEGORY ADJUSTMENT PAGE STYLING (#216bd1 THEME & UNBOLDED TEXT)
       ------------------------------------------------------------------------- */
    .slider-header-centered {
        text-align: center !important;
        font-size: 2.2rem !important;
        font-weight: 400 !important;
        color: #216bd1 !important;
        margin-top: 0px !important;
        margin-bottom: 4px !important;
    }
    .slider-subtitle-centered {
        text-align: center !important;
        font-size: 1.25rem !important;
        font-weight: 400 !important;
        color: #216bd1 !important;
        margin-bottom: 15px !important;
    }
    
    .stSlider label p {
        font-size: 1.35rem !important;
        font-weight: 400 !important;
        color: #216bd1 !important;
    }
    
    div[data-testid="stSlider"] p,
    div[data-testid="stSlider"] span {
        color: #216bd1 !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] div {
        background-color: #216bd1 !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #216bd1 !important;
        border-color: #216bd1 !important;
    }

    .race-info-header {
        display: flex !important;
        align-items: baseline !important;
        gap: 16px !important;
        margin-top: 15px !important;
        margin-bottom: 5px !important;
    }
    .race-info-title {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #216bd1 !important;
        margin: 0 !important;
    }
    .race-info-distance {
        font-size: 1.35rem !important;
        font-weight: 400 !important;
        color: #216bd1 !important;
        margin: 0 !important;
    }

    .stExpander {
        border: 2px solid #1E3A8A !important;
        border-radius: 8px !important;
        background-color: #216bd1 !important;
        margin-bottom: 12px !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15) !important;
    }
    .stExpander > details > summary {
        background-color: #1E3A8A !important;
        color: #FFD700 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
    }
    .stExpander > details > summary * {
        color: #FFD700 !important;
    }
    
    .stExpander > details > div {
        background-color: #FFFFFF !important;
        color: #216bd1 !important;
        padding: 14px !important;
        border-bottom-left-radius: 6px !important;
        border-bottom-right-radius: 6px !important;
    }

    .stTable table th, div[data-testid="stTable"] th {
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        color: #216bd1 !important;
        background-color: #F1F5F9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State values
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Live Race Fields & Ratings"

slider_keys = [
    "u_jockey", "u_trainer", "u_class", "u_barrier", "u_stats", "u_weight",
    "a_jockey", "a_trainer", "a_class", "a_barrier", "a_stats", "a_weight"
]
for k in slider_keys:
    if k not in st.session_state:
        st.session_state[k] = 1.0

if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

# Navigation helper callback
def go_to_page(target_page):
    st.session_state["nav_page"] = target_page

# Sidebar Setup
st.sidebar.header("Navigation Menu")
pages = ["Live Race Fields & Ratings", "Navigation Menu / Settings", "Adjust Slider Settings"]

with st.sidebar.expander("⚙️ Master System Access"):
    admin_pin = st.text_input("Master Key Code", type="password")
    if admin_pin == "7272":
        st.session_state["admin_authenticated"] = True

if st.session_state["admin_authenticated"]:
    pages.append("Admin Calibration Panel")

# Sync Sidebar Radio with Session State
curr_idx = pages.index(st.session_state["nav_page"]) if st.session_state["nav_page"] in pages else 0
selected_page = st.sidebar.radio("Navigation Menu", pages, index=curr_idx, label_visibility="collapsed")
st.session_state["nav_page"] = selected_page

# ------------------------------------------------------------------------------
# TOP LEFT COMPACT 'MENU' BUTTON (PLACED ABOVE PUNTERMATIC HEADER)
# ------------------------------------------------------------------------------
if st.session_state["nav_page"] != "Navigation Menu / Settings":
    st.markdown('<div class="menu-button-container">', unsafe_allow_html=True)
    st.button("📋 Menu", on_click=go_to_page, args=("Navigation Menu / Settings",))
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# CENTERED TOP HEADER SECTION
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="punter-header-container">
        <div class="punter-title">PUNTERMATIC</div>
    </div>
""", unsafe_allow_html=True)

# Dynamic Database Locator
user_prof = os.environ.get("USERPROFILE", "")
possible_paths = [
    "Full_Puntermatic_Migration.json",
    os.path.join(user_prof, "OneDrive", "Desktop", "Full_Puntermatic_Migration.json"),
    os.path.join(user_prof, "Desktop", "Full_Puntermatic_Migration.json")
]

json_path = None
for p in possible_paths:
    if os.path.exists(p):
        json_path = p
        break

# ------------------------------------------------------------------------------
# PAGE 1: LIVE RACE FIELDS & RATINGS
# ------------------------------------------------------------------------------
if st.session_state["nav_page"] == "Live Race Fields & Ratings":
    if not json_path:
        st.error("❌ Database file `Full_Puntermatic_Migration.json` was not found.")
        st.info("Please verify that `Full_Puntermatic_Migration.json` is uploaded to your GitHub repository.")
    else:
        try:
            with open(json_path, "r") as f:
                race_database = json.load(f)
            
            raw_keys = list(race_database.keys())
            if not raw_keys:
                st.warning("JSON loaded, but no race sheets were found inside.")
            else:
                race_display_map = {k: f"Race {k.replace('R', '').replace('Temp', '')}" for k in raw_keys}
                
                # Render clean label
                st.markdown('<div class="race-select-label">Race Selection</div>', unsafe_allow_html=True)
                
                # Render 3-Column Centered Race Buttons
                selected_raw_key = st.radio(
                    "Select Race",
                    raw_keys,
                    format_func=lambda x: race_display_map[x],
                    horizontal=True
                )
                
                if selected_raw_key:
                    race_horses = race_database.get(selected_raw_key, [])
                    
                    if not race_horses or len(race_horses) == 0:
                        st.warning(f"No runners found for {race_display_map[selected_raw_key]}.")
                    else:
                        race_distance = race_horses[0].get("current_distance", race_horses[0].get("Current Distance", "N/A"))
                        
                        # Side-by-Side Row: Race Name and Distance
                        st.markdown(f"""
                            <div class="race-info-header">
                                <span class="race-info-title">{race_display_map[selected_raw_key]}</span>
                                <span class="race-info-distance">Distance: {race_distance}m</span>
                            </div>
                        """, unsafe_allow_html=True)
                        st.write("---")

                        sliders_modified = any(st.session_state[k] != 1.0 for k in slider_keys)
                        rating_label_prefix = "Adjusted Rating" if sliders_modified else "Rating"
                        
                        calculated_field = []
                        for horse in race_horses:
                            h_name = horse.get("horse_name", horse.get("excel_name", "Unknown Horse"))
                            j_name = horse.get("jockey", horse.get("Jockey Name", horse.get("Jockey", "TBA")))
                            t_name = horse.get("trainer", horse.get("Trainer Name", horse.get("Trainer", "TBA")))
                            
                            base_rat = float(horse.get("raw_total_rating", horse.get("Live Rating", horse.get("Rating", 0.0))))
                            jv_val   = float(horse.get("raw_jockey_value", horse.get("Jockey Value", 0.0)))
                            tv_val   = float(horse.get("raw_trainer_value", horse.get("Trainer Value", 0.0)))
                            cv_val   = float(horse.get("raw_class_value", horse.get("Class Value", 0.0)))
                            bv_val   = float(horse.get("raw_barrier_value", horse.get("Barrier Value", 0.0)))
                            sv_val   = float(horse.get("raw_stats_value", horse.get("Stats Value", 0.0)))
                            wv_val   = float(horse.get("raw_weight_diff", horse.get("Weight Diff Value", 0.0)))

                            live_rating = base_rat + (
                                (jv_val * st.session_state["u_jockey"] * st.session_state["a_jockey"]) +
                                (tv_val * st.session_state["u_trainer"] * st.session_state["a_trainer"]) +
                                (cv_val * st.session_state["u_class"] * st.session_state["a_class"]) +
                                (bv_val * st.session_state["u_barrier"] * st.session_state["a_barrier"]) +
                                (sv_val * st.session_state["u_stats"] * st.session_state["a_stats"]) +
                                (wv_val * st.session_state["u_weight"] * st.session_state["a_weight"])
                            )
                            
                            calculated_field.append({
                                "Horse": h_name,
                                "Jockey": j_name if str(j_name).strip() != "" else "TBA",
                                "Trainer": t_name if str(t_name).strip() != "" else "TBA",
                                "Calculated Live Rating": round(live_rating, 3),
                                "Previous_Starts": horse.get("previous_starts", horse.get("Previous_Starts", []))
                            })
                        
                        calculated_field.sort(key=lambda x: x["Calculated Live Rating"], reverse=True)
                        
                        for item in calculated_field:
                            card_label = f"**{item['Horse']}** | {rating_label_prefix}: **{item['Calculated Live Rating']:.3f}**"
                            with st.expander(card_label, expanded=False):
                                st.markdown(f"**Jockey:** {item['Jockey']} &nbsp;|&nbsp; **Trainer:** {item['Trainer']}")
                                starts = item["Previous_Starts"]
                                if starts:
                                    st.table(starts)
                                else:
                                    st.caption("No historical form data available.")
        except Exception as e:
            st.error(f"Error reading JSON database: {e}")

# ------------------------------------------------------------------------------
# PAGE 2: NAVIGATION MENU / SETTINGS PAGE
# ------------------------------------------------------------------------------
elif st.session_state["nav_page"] == "Navigation Menu / Settings":
    st.markdown('<div class="slider-header-centered">Navigation Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="slider-subtitle-centered">Select a destination below:</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.button("🏇 Live Race Fields & Ratings", on_click=go_to_page, args=("Live Race Fields & Ratings",), use_container_width=True)
    with col2:
        st.button("⚙️ Category Adjustment Sliders", on_click=go_to_page, args=("Adjust Slider Settings",), use_container_width=True)

    if st.session_state["admin_authenticated"]:
        st.write("")
        st.button("🔒 Admin Calibration Panel", on_click=go_to_page, args=("Admin Calibration Panel",), use_container_width=True)

# ------------------------------------------------------------------------------
# PAGE 3: USER CATEGORY SLIDER SETTINGS
# ------------------------------------------------------------------------------
elif st.session_state["nav_page"] == "Adjust Slider Settings":
    st.markdown('<div class="slider-header-centered">Category Adjustment</div>', unsafe_allow_html=True)
    st.markdown('<div class="slider-subtitle-centered">Category adjustment values can be adjusted from 0.00 to 2.00.</div>', unsafe_allow_html=True)
    st.divider()

    st.session_state["u_jockey"]  = st.slider("Jockey Value Multiplier", 0.0, 2.0, float(st.session_state["u_jockey"]), step=0.05)
    st.session_state["u_trainer"] = st.slider("Trainer Value Multiplier", 0.0, 2.0, float(st.session_state["u_trainer"]), step=0.05)
    st.session_state["u_class"]   = st.slider("Class Value Multiplier", 0.0, 2.0, float(st.session_state["u_class"]), step=0.05)
    st.session_state["u_barrier"] = st.slider("Barrier Value Multiplier", 0.0, 2.0, float(st.session_state["u_barrier"]), step=0.05)
    st.session_state["u_stats"]   = st.slider("Stats Value (STV) Multiplier", 0.0, 2.0, float(st.session_state["u_stats"]), step=0.05)
    st.session_state["u_weight"]  = st.slider("Weight Difference Multiplier", 0.0, 2.0, float(st.session_state["u_weight"]), step=0.05)

# ------------------------------------------------------------------------------
# PAGE 4: ADMIN CALIBRATION PANEL
# ------------------------------------------------------------------------------
elif st.session_state["nav_page"] == "Admin Calibration Panel":
    st.subheader("🔒 Master Core Calibration")
    st.write("Master system-wide baseline adjustments:")
    st.divider()

    st.session_state["a_jockey"]  = st.slider("Master Jockey Multiplier", 0.0, 2.0, float(st.session_state["a_jockey"]), step=0.05)
    st.session_state["a_trainer"] = st.slider("Master Trainer Multiplier", 0.0, 2.0, float(st.session_state["a_trainer"]), step=0.05)
    st.session_state["a_class"]   = st.slider("Master Class Multiplier", 0.0, 2.0, float(st.session_state["a_class"]), step=0.05)
    st.session_state["a_barrier"] = st.slider("Master Barrier Multiplier", 0.0, 2.0, float(st.session_state["a_barrier"]), step=0.05)
    st.session_state["a_stats"]   = st.slider("Master Stats Multiplier", 0.0, 2.0, float(st.session_state["a_stats"]), step=0.05)
    st.session_state["a_weight"]  = st.slider("Master Weight Multiplier", 0.0, 2.0, float(st.session_state["a_weight"]), step=0.05)
