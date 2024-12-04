import io
import datetime
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd

def category(df):
    exclusion_list = ["College Code", "Place", "College Name", "Branch", "Branch code"]
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

def generate_pdf_table(data, file_prefix="table"):
    unique_colleges = {}
    for entry in data:
        key = (entry[0], entry[3])  # Unique key based on College Code and Branch
        unique_colleges[key] = entry  # Always overwrite, keeping the latest entry
    
    # Extract the unique entries and sort them by Cutoff Rank
    sorted_colleges = sorted(unique_colleges.values(), key=lambda x: x[6])
    columns = ["College Code", "Place", "College", "Branch", "Branch Code", "Category", "Cutoff"]
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

    # Generate a PDF with the table image
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Selected Colleges and Cutoffs", ln=True, align="C")
    pdf.image(table_image, x=10, y=30, w=190)

    # Write PDF to an in-memory BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)  # Output the PDF content to the buffer
    pdf_buffer.seek(0)  # Reset buffer pointer to the beginning

    return pdf_buffer, file_name