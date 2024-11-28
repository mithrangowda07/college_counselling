def category(df):
    exclusion_list = ["College Code", "Place", "College Name", "Branch ", "Branch code"]
    return [col for col in df.columns if col not in exclusion_list]

def getcutoff_rank(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch"] == selected_list[3])
        ]
        if not filtered_data.empty:
            cutoff_rank = filtered_data[selected_list[0]].values[0]
            
            # Check for numeric cutoff
            if isinstance(cutoff_rank, (int, float)):
                pass  # Valid numeric value
            elif isinstance(cutoff_rank, str) and cutoff_rank.isnumeric():
                cutoff_rank = int(cutoff_rank)
            else: 
                if "GM" in filtered_data:
                    cutoff_rank = filtered_data["GM"].values[0]
                    selected_list[0] = "GM"
                else:
                    None
            
            if cutoff_rank is not None:
                return cutoff_rank
            else:
                return 0          
        else:
            return ("No data available for the selected options.")
    else:
        return ("Please make valid selections for Category, College, and Branch.")