import pandas as pd

def transform_data():
    df = pd.read_csv("../raw_titanic.csv")

    # If Age is missing for a passenger in a certain class 
    # it gets filled with the median age of all in that class.
    df["Age"] = df.groupby(["Sex", "Pclass"])["Age"].transform(
    lambda x: x.fillna(x.median())
)
    # drop Cabin (too many missing values)
    df.drop(columns=["Cabin"], inplace=True)

    # Save cleaned dataset
    df.to_csv("../clean_titanic.csv", index=False)
    print("Data transformed and saved as clean_titanic.csv")

    # Show start and end of the DataFrame
    print("\n--- First 5 rows ---")
    print(df.head(10))
    print("\n--- Last 5 rows ---")
    print(df.tail())

if __name__ == "__main__":
    transform_data()
