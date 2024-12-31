import streamlit as st
import pandas as pd

# Define the file path
FILE_PATH = "cet_matrix.xlsx"

# Load the Excel file
@st.cache_data
def load_excel_file():
    """Load Excel file."""
    try:
        data = pd.read_excel(FILE_PATH, engine="openpyxl")
        data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
        return data
    except FileNotFoundError:
        st.error("The file 'seat_matrix.xlsx' was not found. Please check the file path.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Load data
df = load_excel_file()

# Fallback order dictionary
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
    "GMR": ["GMR", "GM"],
    "GMK": ["GMK", "GM"],
    # Default fallbacks for undefined categories
    "GM": ["GM"]
}

# App UI
st.title("K-CET Counselling Helper 🎓")
st.write("### Seat Matrix")

# Generate category list excluding specific columns
exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code", "SNQ", "Total"]
category_list = [col for col in df.columns if col not in exclusion_list]
selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list), key="add_category")

# Create tabs
tabs = st.tabs(["Particular College", "All Colleges"])

with tabs[0]:  # Tab 1: Particular College
    selected_college = st.selectbox(
        "Select College",
        ["--Select--"] + sorted(df["College Name"].dropna().unique()),
        disabled=(selected_category == "--Select--"),
        key="add_college",
    )

    if selected_college != "--Select--" and selected_category != "--Select--":
        fallback_categories = fallback_order.get(selected_category, [selected_category])
        filtered_data = df[(df["College Name"] == selected_college) & (df[fallback_categories].any(axis=1))]
        
        if not filtered_data.empty:
            st.write(f"##### Seat Matrix for {selected_category} in {selected_college}:")
            filtered_data = filtered_data.reset_index(drop=True)
            filtered_data.index = range(1, len(filtered_data) + 1)
            st.table(filtered_data[[ "Branch Name"] + fallback_categories + ["SNQ", "Total"]])
        else:
            st.warning(f"No data available for {selected_category} in {selected_college}.")

with tabs[1]:  # Tab 2: All Colleges
    if selected_category != "--Select--":
        fallback_categories = fallback_order.get(selected_category, [selected_category])
        all_colleges_data = df[["College Name", "Branch Name"] + fallback_categories + ["SNQ", "Total"]]
        
        st.write(f"##### Seat Matrix for {selected_category} Across All Colleges:")
        st.table(all_colleges_data)
