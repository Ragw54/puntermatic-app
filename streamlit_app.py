import streamlit as st
import json
import os

# Set wide layout
st.set_page_config(page_title="Puntermatic", page_icon="🏇", layout="wide")

# ------------------------------------------------------------------------------
# CUSTOM CSS: COLOR STYLING, COMPACT TOP PADDING & ENLARGED TEXT
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Remove default top padding to push content as high as possible */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Header Styling */
    .punter-title {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        color: #1E3A8A !important; /* Deep Racing Blue */
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        line-height: 1.1 !important;
    }
    .punter-subtitle {
        font-size: 1.6rem !important;
        font-weight: 400 !important;
        color: #4B5563 !important; /* Neutral Gray */
        margin-top: 2px !important;
        margin-bottom: 15px !important;
    }
    
    /* Section Headers */
    h2, h3, .stSubheader {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }
    
    /* Selectbox Label and Larger Selectbox Input Text */
    .stSelectbox label {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1F2937 !important;
    }
    div[data-baseweb="select"] div {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
    }
    
    /* Enlarge Slider Labels & Options */
    .stSlider label {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }

    /* Enlarge Sidebar Radio Buttons & Navigation Pane */
    section[data-testid="stSidebar"] {
        width: 320px !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }
    section[data-testid="stSidebar"] input[type="radio"] {
        width: 22px !important;
        height: 22px !important;
        margin-right: 12px !important;
        cursor: pointer;
    }
    
    /* Styled Card Backgrounds for Race Ratings */
    .stExpander {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        background-color: #F9FAFB !important;
        margin-bottom: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TOP HEADER SECTION (MOVED UP & REFORMATED)
# ------------------------------------------------------------------------------
st.markdown('<div class="punter-title">PUNTERMATIC</div>', unsafe_allow_html=True)
st.markdown('<div class="punter-subtitle">Race Selection</div>', unsafe_allow_html=True)

# Initialize default session state values for all 6 core metrics
slider_keys = [
    "u_jockey", "u_trainer", "u_class", "u_barrier", "u_stats", "u_weight",
    "a_jockey", "a_trainer", "a_class", "a_barrier", "a_stats", "a_weight"
]
for k in slider_keys:
    if k not in st.session_state:
        st.session_state[k] = 1.0

if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

# Sidebar Setup
st.sidebar.header("Navigation Menu")
pages = ["📊 Live Race Fields & Ratings", "🎛️ Adjust Slider Settings"]

with st.sidebar.expander("⚙️ Master System Access"):
    admin_pin = st.text_input("Master Key Code", type="password")
    if admin_pin == "7272":
        st.session_state["admin_authenticated"] = True

if st.session_state["admin_authenticated"]:
    pages.append("🔒 Admin Calibration Panel")

selected_page = st.sidebar.radio("Select Application View", pages)

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
if selected_page == "📊 Live Race Fields & Ratings":
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
                
                # Relabeled dropdown prompt to "Select Race" (removed "Sheet")
                selected_raw_key = st.selectbox("Select Race", raw_keys, format_func=lambda x: race_display_map[x])
                
                if selected_raw_key:
                    race_horses = race_database.get(selected_raw_key, [])
                    
                    if not race_horses or len(race_horses) == 0:
                        st.warning(f"No runners found for {race_display_map[selected_raw_key]}.")
                    else:
                        race_distance = race_horses[0].get("current_distance", race_horses[0].get("Current Distance", "N/A"))
                        
                        # Display race name directly without "Field Overview:"
                        st.subheader(f"{race_display_map[selected_raw_key]}")
                        st.markdown(f"**Current Race Distance: {race_distance}m**")
                        st.write("---")
                        
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
                            card_label = f"**{item['Horse']}** | Adjusted Rating: **{item['Calculated Live Rating']:.3f}**"
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
# PAGE 2: USER CATEGORY SLIDER SETTINGS
# ------------------------------------------------------------------------------
elif selected_page == "🎛️ Adjust Slider Settings":
    st.subheader("🎛️ Category Calculation Factors")
    st.write("Adjust weighting factors (0.00 to 2.00) applied to each performance category:")
    st.divider()

    st.session_state["u_jockey"]  = st.slider("Jockey Value Multiplier", 0.0, 2.0, float(st.session_state["u_jockey"]), step=0.05)
    st.session_state["u_trainer"] = st.slider("Trainer Value Multiplier", 0.0, 2.0, float(st.session_state["u_trainer"]), step=0.05)
    st.session_state["u_class"]   = st.slider("Class Value Multiplier", 0.0, 2.0, float(st.session_state["u_class"]), step=0.05)
    st.session_state["u_barrier"] = st.slider("Barrier Value Multiplier", 0.0, 2.0, float(st.session_state["u_barrier"]), step=0.05)
    st.session_state["u_stats"]   = st.slider("Stats Value (STV) Multiplier", 0.0, 2.0, float(st.session_state["u_stats"]), step=0.05)
    st.session_state["u_weight"]  = st.slider("Weight Difference Multiplier", 0.0, 2.0, float(st.session_state["u_weight"]), step=0.05)

# ------------------------------------------------------------------------------
# PAGE 3: ADMIN CALIBRATION PANEL
# ------------------------------------------------------------------------------
elif selected_page == "🔒 Admin Calibration Panel":
    st.subheader("🔒 Master Core Calibration")
    st.write("Master system-wide baseline adjustments:")
    st.divider()

    st.session_state["a_jockey"]  = st.slider("Master Jockey Multiplier", 0.0, 2.0, float(st.session_state["a_jockey"]), step=0.05)
    st.session_state["a_trainer"] = st.slider("Master Trainer Multiplier", 0.0, 2.0, float(st.session_state["a_trainer"]), step=0.05)
    st.session_state["a_class"]   = st.slider("Master Class Multiplier", 0.0, 2.0, float(st.session_state["a_class"]), step=0.05)
    st.session_state["a_barrier"] = st.slider("Master Barrier Multiplier", 0.0, 2.0, float(st.session_state["a_barrier"]), step=0.05)
    st.session_state["a_stats"]   = st.slider("Master Stats Multiplier", 0.0, 2.0, float(st.session_state["a_stats"]), step=0.05)
    st.session_state["a_weight"]  = st.slider("Master Weight Multiplier", 0.0, 2.0, float(st.session_state["a_weight"]), step=0.05)
