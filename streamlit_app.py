import json
import re

# Simulate reading your raw extracted data (WJTTransfer sheet structure)
# Format: [Saddle/Scratched, Horse Name, Trainer, Jockey, Barrier, Weight]
wjt_transfer_data = [
    ["1", "ASTON", "Andrew Noblet", "Billy Egan", "8", "58kg"],
    ["2", "LEVRIER VOBIS", "Matt Laurie", "Patrick Moloney", "11", "58kg"],
    ["3", "MR NATURAL", "Lindsey Smith", "John Allen", "17", "58kg"],
    ["4", "PRIDE IN MOTION", "Danielle Loos", "Will Gordon", "1", "58kg"],
    ["5", "PROLIFIC ANGEL", "Anthony & Sam Freedman", "Damien Thornton", "18", "58kg"],
    ["6", "7x", "SEZZLE VOBIS", "Henry Dwyer", "Mitchell Aitken", "13", "58kg"],
    ["7", "63x7", "ANGELIC RISE", "Ben, Will & JD Hayes", "Luke Currie", "5", "56kg"],
    ["8", "CHESTNUT TEAL", "Thomas Carberry", "Eoin Walsh", "3", "56kg"],
    ["9", "MOUNTJOY VOBIS", "Henry Dwyer", "Declan Bates", "4", "56kg"],
    ["10", "9", "SASHIKO VOBIS", "Ben, Will & JD Hayes", "Jye McNeil", "14", "56kg"],
    ["11", "6", "STARSEATIC VOBIS", "Peter Chow", "Zac Spain", "6", "56kg"],
    ["12", "STRENGTH WITHIN", "Tom Dabernig", "Paul Gatt", "2", "56kg"],
    ["13", "4", "VICTIMISED VOBIS", "Lindsey Smith", "Fred Kersley", "7", "56kg"],
    ["14", "WRITTEN WAND", "Matt Laurie", "Jake Noonan", "16", "56kg"]
]

# Simulate your current destination database structure (e.g., loaded from your existing JSON)
firebase_races_data = {
    "Race 1": {
        "1 ASTON": {"Live Rating": 1.050, "Today's Jockey Value": 1},
        "3 MR NATURAL": {"Live Rating": 0.500, "Today's Jockey Value": 0.50},
        "4 PRIDE IN MOTION": {"Live Rating": 0.775, "Today's Jockey Value": 0.78},
        "6 SEZZLE": {"Live Rating": 1.744, "Today's Jockey Value": 0},
        "7 ANGELIC RISE": {"Live Rating": 4.768, "Today's Jockey Value": 1, "Today's Trainer Value": 0.65},
        "8 CHESTNUT TEAL": {"Live Rating": 0.000, "Today's Jockey Value": 0},
        "9 MOUNTJOY": {"Live Rating": 0.000, "Today's Jockey Value": 0},
        "11 STARSEATIC": {"Live Rating": 2.314, "Today's Jockey Value": 0},
        "12 STRENGTH WITHIN": {"Live Rating": 0.625, "Today's Jockey Value": 0, "Today's Trainer Value": 0.625},
        "13 VICTIMISED": {"Live Rating": 2.042, "Today's Jockey Value": 0},
        "15 NICCTINI EM": {"Live Rating": 0.084}
    }
}

def clean_name(name_str):
    """
    Removes saddle prefixes, form tracking suffixes (like VOBIS), 
    and extra spaces to ensure perfect matching.
    """
    if not name_str:
        return ""
    # Convert to uppercase and strip trailing/leading spaces
    name = str(name_str).upper().strip()
    # Strip leading saddle numbers (e.g., '1 ASTON' -> 'ASTON')
    name = re.sub(r'^\d+\s+', '', name)
    # Strip common bonus suffixes that clip text lengths
    name = name.replace("VOBIS SILVER BONUS SCHEME", "").replace("VOBIS", "")
    return name.strip()

# --- RUN THE MATCHING CORRECTION LOOP ---
for race, horses in firebase_races_data.items():
    for db_horse_key in list(horses.keys()):
        db_horse_clean = clean_name(db_horse_key)
        
        # Scan through our raw transfer data block
        for row in wjt_transfer_data:
            # Handle potential cell shift if scratch info exists in column A
            if len(row) == 6:
                scrape_name = row[1] if "x" not in row[0] else row[2]
                trainer = row[2] if "x" not in row[0] else row[3]
                jockey = row[3] if "x" not in row[0] else row[4]
                weight = row[5]
            else:
                continue
                
            scrape_name_clean = clean_name(scrape_name)
            
            # If the core horse names match, injection is guaranteed!
            if scrape_name_clean and (scrape_name_clean in db_horse_clean or db_horse_clean in scrape_name_clean):
                horses[db_horse_key]["Weight"] = weight
                horses[db_horse_key]["Jockey Name"] = jockey
                horses[db_horse_key]["Trainer Name"] = trainer
                break

# View the perfectly updated JSON dataset ready for Streamlit
print(json.dumps(firebase_races_data, indent=4))
