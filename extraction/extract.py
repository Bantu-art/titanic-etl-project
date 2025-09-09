import pandas as pd
import os

def extract_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    
    # Use relative path from project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "raw_titanic.csv"), index=False)
    print("✅ Data extracted and saved as raw_titanic.csv")

if __name__ == "__main__":
    extract_data()
