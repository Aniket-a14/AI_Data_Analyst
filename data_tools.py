import pandas as pd

def load_dataset(file_path: str):
    """
    Load a CSV file into a Pandas DataFrame.
    Returns the DataFrame if successful, or an error message as a string.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return f"Error loading dataset: {e}"

#this block of code is used to load the dataset from the csv file
#it returns the dataframe if successful, or an error message as a string
#the dataframe is then used in the agent.py file to execute the code



