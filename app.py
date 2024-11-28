import streamlit as st
import pandas as pd
from app1 import category,getcutoff_rank

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
        app_mode1 = st.selectbox("Choose **Start** to enter the college sorting or **End** to end the session.", ["--Select--", "Start", "End"])
        if "selected_colleges" not in st.session_state:
            st.session_state["selected_colleges"] = []
        if app_mode1 == "Start":
            category_list = category(df)
            selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list))
            selected_place = st.selectbox("Select Place", ["--Select--"]+sorted(df["Place"].dropna().unique()))
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
                        st.success(cutoff_rank)

        elif app_mode1 == "End":
            st.success("Session ended successfully!")
            st.session_state["selected_colleges"].clear()