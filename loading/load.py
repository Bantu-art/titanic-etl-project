import pandas as pd
import sqlite3
import os

def load_data():
    # Use relative path from project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    df = pd.read_csv(os.path.join(data_dir, "clean_titanic.csv"))
    conn = sqlite3.connect(os.path.join(data_dir, "titanic.db"))
    df.to_sql("titanic_passengers", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Data loaded into titanic.db")

if __name__ == "__main__":
    load_data()
