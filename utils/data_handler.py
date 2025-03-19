import pandas as pd #type:ignore
import os
from datetime import datetime
from config.config import CANDIDATE_DATA_FILE

def save_candidate_data(candidate_info):
    data = candidate_info.copy()

    if "tech_stack" in data and isinstance(data["tech_stack"], list):
        data["tech_stack"] = ", ".join(data["tech_stack"])

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_new = pd.DataFrame([data])

    if os.path.exists(CANDIDATE_DATA_FILE):
        df_existing = pd.read_csv(CANDIDATE_DATA_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(CANDIDATE_DATA_FILE, index=False)
    else:
        df_new.to_csv(CANDIDATE_DATA_FILE, index=False)

    return True

def get_candidate_data():
    if os.path.exists(CANDIDATE_DATA_FILE):
        return pd.read_csv(CANDIDATE_DATA_FILE)
    else:
        return pd.DataFrame()