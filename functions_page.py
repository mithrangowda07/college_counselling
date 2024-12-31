import datetime
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import tempfile

def getcutoff_rank(selected_list, df):
    if all(item != "--Select--" for item in selected_list[:4]):
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch Name"] == selected_list[3])
        ]
        if not filtered_data.empty:
            # The selected category
            category = selected_list[0]
            
            # Define fallback order based on the category
            fallback_order = {
                "1R": ["1R", "1G", "GM"],
                "1K": ["1K", "1G", "GM"],
                "1G": ["1G", "GM"],
                "2AR": ["2AR", "2AG", "GM"],
                "2AK": ["2AK", "2AG", "GM"],
                "2AG": ["2AG", "GM"],
                "2BR": ["2BR", "2BG", "GM"],
                "2BK": ["2BK", "2BG", "GM"],
                "2BG": ["2BG", "GM"],
                "3AK": ["3AK", "3AG", "GM"],
                "3AR": ["3AR", "3AG", "GM"],
                "3AG": ["3AG", "GM"],
                "3BK": ["3BK", "3BG", "GM"],
                "3BR": ["3BR", "3BG", "GM"],
                "3BG": ["3BG", "GM"],
                "STK": ["STK", "STG", "GM"],
                "STR": ["STR", "STG", "GM"],
                "STG": ["STG", "GM"],
                "SCK": ["SCK", "SCG", "GM"],
                "SCR": ["SCR", "SCG", "GM"],
                "SCG": ["SCG", "GM"],
                "GMR": ["GMR","GM"],
                "GMK": ["GMK","GM"],
                # Default fallbacks for undefined categories
                "GM": ["GM"]
            }

            
            # Get the fallback order or default to just the category and GM
            fallback_categories = fallback_order.get(category, [category, "GM"])
            
            # Iterate through fallback categories to find a valid cutoff
            for fallback_category in fallback_categories:
                if fallback_category in filtered_data:
                    cutoff_rank = filtered_data[fallback_category].values[0]
                    
                    # Check if the cutoff rank is valid
                    if isinstance(cutoff_rank, (int, float)):
                        return [cutoff_rank, fallback_category]
                    elif isinstance(cutoff_rank, str) and cutoff_rank.isnumeric():
                        return [int(cutoff_rank), fallback_category]
            
            # No valid cutoff rank found in fallback categories
            return [-1, category]
        else:
            # No matching data for college and branch
            return [-1, selected_list[0]]
    else:
        # Invalid selection
        return [-1, selected_list[0]]
 
    
def getcollege_code(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch Name"] == selected_list[3])
        ]
        if not filtered_data.empty:
            college_code = filtered_data["College Code"].values[0]
            return college_code
        
        else:
            return -1
        
def getbranch_code(selected_list,df):
    if selected_list[0] != "--Select--" and selected_list[1] != "--Select--" and selected_list[2] != "--Select--" and selected_list[3] != "--Select--":
        filtered_data = df[
            (df["College Name"] == selected_list[2]) & (df["Branch Name"] == selected_list[3])
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

def generate_pdf_table(data, file_prefix="table"):
    unique_colleges = {}
    for entry in data:
        key = (entry[0], entry[3])  # Unique key based on College Code and Branch
        unique_colleges[key] = entry  # Always overwrite, keeping the latest entry
    
    # Extract the unique entries and sort them by Cutoff Rank
    sorted_colleges = sorted(unique_colleges.values(), key=lambda x: x[6])
    columns = ["College Code", "Place", "College", "Branch Name", "Branch Code", "Category", "Cutoff"]
    dataframe = pd.DataFrame(sorted_colleges, columns=columns)
    
    # Generate today's date for the filename
    today = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"{file_prefix}_{today}.pdf"
    
    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Create a table from the DataFrame
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(dataframe.columns))))
    
    # Save the table as an image
    table_image = "table_image.png"
    plt.savefig(table_image, bbox_inches="tight", dpi=300)
    plt.close(fig)  # Close the figure to release memory
    
    # Generate a PDF and save to a file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Selected Colleges and Cutoffs", ln=True, align="C")
    pdf.image(table_image, x=10, y=30, w=190)
    
    # Save PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf_path = temp_file.name
        pdf.output(pdf_path)  # Write the PDF content to the temp file
    
    return pdf_path  # Return the file path of the generated PDF