import streamlit as st
import pandas as pd
from app1 import category,getcutoff_rank,getcollege_code,getbranch_code,generate_csv_file,gettable
from pdf_download import generate_pdf_table

# Define the file path
FILE_PATH = r"C:\Users\mithr\Desktop\3rd Sem\DTL\cet_colg_data.xlsx"

# Load the Excel file
@st.cache_data
def load_excel_file():
    """Load Excel file."""
    try:
        data = pd.read_excel(FILE_PATH, engine="openpyxl")
        data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_excel_file()

st.title("K-CET Counselling Helper")

if df is None:
    st.error("Unable to load the data. Please check the file.")
else:
    required_columns = {"Place", "College Name","Branch"}
    if not required_columns.issubset(df.columns):
        st.error(f"Missing required columns: {required_columns - set(df.columns)}")
    else:
        app_mode1 = st.selectbox("Choose **Start** to enter the college sorting or **End** to end the session.", ["--Select--", "Start"])
        if "selected_colleges" not in st.session_state:
            st.session_state["selected_colleges"] = []
        if app_mode1 == "Start":
            category_list = category(df)
            selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list))
            selected_place = st.selectbox(
                "Select Place", 
                ["--Select--"] + sorted(df["Place"].dropna().unique()), 
                disabled=(selected_category == "--Select--")
            )
            if selected_place and selected_place != "--Select--":
                selected_college = st.selectbox(
                    "Select College",
                    ["--Select--"] + sorted(df[df["Place"] == selected_place]["College Name"].dropna().unique())
                )
                if selected_college and selected_college != "--Select--":
                    selected_branch = st.selectbox(
                        "Select Branch",
                        ["--Select--"] + sorted(df[df["College Name"] == selected_college]["Branch"].dropna().unique())    
                    )
                    
                    selected_list = [selected_category,selected_place,selected_college,selected_branch]
                    if st.button("Submit"):
                        cutoff_rank = getcutoff_rank(selected_list,df)
                        college_code = getcollege_code(selected_list,df)
                        branch_code = getbranch_code(selected_list,df)
                        if cutoff_rank[0] == -1 or college_code == -1 or branch_code == -1:
                            st.error("No data available for the selected options.\nPlease make valid selections for Category, College, and Branch.")
                        else:
                            st.success(f"Cutoff Rank: {cutoff_rank[0]}")
                            if cutoff_rank[1] == "GM":
                                selected_category = cutoff_rank[1]
                                
                            selected_list = [college_code,selected_place,selected_college,selected_branch,branch_code,selected_category,cutoff_rank[0]]
                            st.session_state["selected_colleges"].append(selected_list)
                                
                    if st.button("Show the sorted list"):
                        if st.session_state["selected_colleges"]:
                            # Use a dictionary to keep the latest entry for each unique college and branch
                            newlist = st.session_state["selected_colleges"]
                            selected_df = gettable(newlist)
                            st.write("Selected Colleges and Cutoffs:")
                            st.table(selected_df)

                            
                            try:
                                csv, file_name = generate_csv_file(selected_df)  # Call the function
                                st.download_button(
                                    label="Download as CSV",
                                    data=csv,
                                    file_name=file_name,
                                    mime="text/csv"
                                )
                            except ValueError as e:
                                st.error(str(e))
                            
                            try:
                                # Generate the PDF file
                                data = st.session_state["selected_colleges"]
                                columns = ["College Code", "Place", "College", "Branch", "Branch Code", "Category", "Cutoff"]
                                df1 = pd.DataFrame(data, columns=columns)
                                pdf_buffer, file_name = generate_pdf_table(df1)

                                # Display the download button for the PDF
                                st.download_button(
                                    label="Download as PDF",
                                    data=pdf_buffer,
                                    file_name=file_name,
                                    mime="application/pdf"
                                )
                            except ValueError as e:
                                st.error(str(e))




        if st.button("End"):
            st.success("Session ended successfully!")
            st.session_state["selected_colleges"].clear()