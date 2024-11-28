import io
import datetime
import pandas as pd

def category(df):
    exclusion_list = ["College Code", "Place", "College Name", "Branch ", "Branch code"]
    return [col for col in df.columns if col not in exclusion_list]

def getcutoff_rank(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch"] == selected_list[3])
        ]
        if not filtered_data.empty:
            change_category = None
            cutoff_rank = filtered_data[selected_list[0]].values[0]
            
            # Check for numeric cutoff
            if isinstance(cutoff_rank, (int, float)):
                pass  # Valid numeric value
            elif isinstance(cutoff_rank, str) and cutoff_rank.isnumeric():
                cutoff_rank = int(cutoff_rank)
            else: 
                if "GM" in filtered_data:
                    cutoff_rank = filtered_data["GM"].values[0]
                    change_category = "GM"
                    if (isinstance(cutoff_rank, (int, float))):
                        pass
                    else:
                        cutoff_rank = 0
                else:
                    None
            
            if cutoff_rank is not None:
                return [cutoff_rank, change_category]
            else:
                return [-1, change_category]         
        else:
            return [-1, change_category] 
    else:
        return [-1, change_category] 
    
def getcollege_code(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch"] == selected_list[3])
        ]
        if not filtered_data.empty:
            college_code = filtered_data["College Code"].values[0]
            return college_code
        
        else:
            return -1
        
def getbranch_code(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch"] == selected_list[3])
        ]
        if not filtered_data.empty:
            branch_code = filtered_data["Branch code"].values[0]
            return branch_code
        
        else:
            return -1
        
def gettable(newlist):
    unique_colleges = {}
    for entry in newlist:
        key = (entry[0], entry[3])  # Unique key based on College Code and Branch
        unique_colleges[key] = entry  # Always overwrite, keeping the latest entry
    
    # Extract the unique entries and sort them by Cutoff Rank
    sorted_colleges = sorted(unique_colleges.values(), key=lambda x: x[6])
    
    selected_df = pd.DataFrame(
        sorted_colleges,
        columns=["College Code", "Place", "College", "Branch", "Branch Code","Category", "Cutoff"]
    )
    
    # Reset the index to start from 1
    selected_df.index = range(1, len(selected_df) + 1)
    
    return selected_df
        
def generate_csv_file(dataframe: pd.DataFrame, file_prefix: str = "selected_colleges") -> tuple:
    """
    Generates a CSV file from the provided DataFrame and returns its content along with the filename.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame to be converted to a CSV file.
    - file_prefix (str): Prefix for the filename. Defaults to "selected_colleges".

    Returns:
    - tuple: A tuple containing the CSV content as bytes and the filename.
    """
    if dataframe is None or dataframe.empty:
        raise ValueError("The provided DataFrame is empty. Please ensure there is data to generate a CSV.")
    
    csv_content = dataframe.to_csv(index=False).encode("utf-8")
    today = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"{file_prefix}_{today}.csv"
    
    return csv_content, file_name
