import pandas as pd
import os

def extract_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    
    # Use absolute path
    data_dir = "/home/bantu/dataProjects/titanic_pipeline/data"
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(f"{data_dir}/raw_titanic.csv", index=False)
    print("✅ Data extracted and saved as raw_titanic.csv")

if __name__ == "__main__":
    extract_data()
