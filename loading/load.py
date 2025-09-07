import pandas as pd
import sqlite3

def load_data():
    # Use absolute paths
    data_dir = "/home/bantu/dataProjects/titanic_pipeline/data"
    df = pd.read_csv(f"{data_dir}/clean_titanic.csv")
    conn = sqlite3.connect(f"{data_dir}/titanic.db")
    df.to_sql("titanic_passengers", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Data loaded into titanic.db")

if __name__ == "__main__":
    load_data()
