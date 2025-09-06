import pandas as pd

def transform_data():
    df = pd.read_csv("../data/raw_titanic.csv")

    # If Age is missing for a passenger in a certain class 
    # it gets filled with the median age of all in that class.
    df["Age"] = df.groupby(["Sex", "Pclass"])["Age"].transform(
    lambda x: x.fillna(x.median())
)
    # drop Cabin (too many missing values)
    df.drop(columns=["Cabin"], inplace=True)

    # Since there are only two missing Embarked coulumn, I am filling
    # them with the most common
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    # For clean read I have moved surname from the name column and 
    # created a new column for it
    df["Surname"] = df["Name"].str.split(",").str[0].str.strip()

    # For a clean name read I have also moved Surname column to before Name
    col_index = df.columns.get_loc("Name")  
    surname_col = df.pop("Surname")          
    df.insert(col_index, "Surname", surname_col)  

    # strip the name column of the surname and the comma
    df["Name"] = df["Name"].str.split(",").str[1].str.strip()

    df["TicketPrefix"] = (
    df["Ticket"]
    .str.replace(r"\d+", "", regex=True)   # remove numbers
    .str.replace(r"[./]", "", regex=True) # remove dots/slashes
    .str.strip()                          # clean spaces
)
    df["TicketPrefix"] = df["TicketPrefix"].replace("", "None")  # mark empty as None

    # Reorder: TicketPrefix comes before Ticket
    cols = list(df.columns)
    ticket_idx = cols.index("Ticket")
    cols.remove("TicketPrefix")
    cols.insert(ticket_idx, "TicketPrefix")
    df = df[cols]

    # df["Ticket"] = df["Ticket"].str.split(" ").str[1].str.strip()


    # Save cleaned dataset
    df.to_csv("../data/clean_titanic.csv", index=False)
    print("Data transformed and saved as clean_titanic.csv")

    # Show start and end of the DataFrame
    print("\n--- First 5 rows ---")
    print(df.head(10))
    print("\n--- Last 5 rows ---")
    print(df.tail())

if __name__ == "__main__":
    transform_data()
