import pandas as pd

def extract_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    df.to_csv("../raw_titanic.csv", index=False)
    print("✅ Data extracted and saved as raw_titanic.csv")

if __name__ == "__main__":
    extract_data()
