import streamlit as st
import pandas as pd
from functions_page import getbranch_code, getcutoff_rank, getcollege_code, gettable, generate_pdf_table

# File paths
FILE_PATH1 = "cet_colg_data.xlsx"

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f7f9fc;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 8px 12px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stSelectbox {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load Excel File
@st.cache_data
def load_excel_file(FILE_PATH):
    """Load Excel file."""
    try:
        data = pd.read_excel(FILE_PATH, engine="openpyxl")
        data.columns = data.columns.str.strip()  # Clean column names
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_excel_file(FILE_PATH1)

# Title and introduction
st.title("🎓 CounselMate: Your College Admission Assistant")
st.write("### Explore Colleges and Branches Based on Cutoff Ranks")

# Collapsible disclaimer section
with st.expander("📢 **Disclaimer**"):
    st.write(
        """
        - The results shown in this app are based on the previous year's cutoff data and are **indicative only**.
        - The actual college selections depend on your real-time preferences and seat availability.
        - Use this app as a **reference tool** to make informed decisions.
        - Developers are not responsible for decisions made based on this app.
        """
    )

# Initialize session state
if "selected_data" not in st.session_state:
    st.session_state["selected_data"] = []

# Dropdown setup
st.write("---")  # Horizontal separator for cleaner layout
col1, col2 = st.columns([2, 2])
with col1:
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("📊 Select Category", ["--Select--"] + sorted(category_list), key="category_select")

with col2:
    selected_place = st.selectbox(
        "📍 Select Place",
        ["--Select--"] + sorted(df["Place"].dropna().unique()),
        disabled=(selected_category == "--Select--"),
        key="place_select",
    )

# Tabs
tabs = st.tabs(["🏫 Branch-Level Options", "📚 College-Level Options"])

# Tab 1: Branch-Level Options
with tabs[0]:
    st.write("###  Add or Remove Branch-Level Data")
    col1, col2 = st.columns(2)

    # Add to List
    with col1:
        st.write("#### ➕ Add to the List")
        if selected_place and selected_place != "--Select--":
            selected_college = st.selectbox(
                "🏫 Select College",
                ["--Select--"] + sorted(df[df["Place"] == selected_place]["College Name"].dropna().unique()),
                key="college_select_normal",
            )
            if selected_college and selected_college != "--Select--":
                selected_branch = st.selectbox(
                    "📚 Select Branch",
                    ["--Select--"] + sorted(df[df["College Name"] == selected_college]["Branch Name"].dropna().unique()),
                    key="branch_select_normal",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Add Branch", key="add_button_normal"):
                        selected_list = [selected_category, selected_place, selected_college, selected_branch]
                        cutoff_rank = getcutoff_rank(selected_list, df)
                        college_code = getcollege_code(selected_list, df)
                        branch_code = getbranch_code(selected_list, df)

                        if cutoff_rank[0] == -1 or college_code == -1 or branch_code == -1:
                            st.error("🚫 No data available for the selected options.")
                        else:
                            st.success(f"✅ Added! Cutoff Rank: {cutoff_rank[0]}")
                            st.session_state["selected_data"].append([
                                college_code, selected_place, selected_college, selected_branch, branch_code, cutoff_rank[1], cutoff_rank[0]
                            ])

    # Delete from List
    with col2:
        st.write("#### 🚮 Remove from the List")
        if st.session_state["selected_data"]:
            college_list = list(set([col[2] for col in st.session_state["selected_data"]]))
            selected_college = st.selectbox("🏫 Select College", ["--Select--"] + sorted(college_list), key="delete_college")

            if selected_college and selected_college != "--Select--":
                branch_list = [col[3] for col in st.session_state["selected_data"] if col[2] == selected_college]
                selected_branch = st.selectbox(
                    "📚 Select Branch",
                    ["--Select--"] + sorted(branch_list),
                    key="delete_branch",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Remove Branch", key="delete_button"):
                        st.session_state["selected_data"] = [
                            col for col in st.session_state["selected_data"]
                            if not (col[2] == selected_college and col[3] == selected_branch)
                        ]
                        st.success(f"✅ Removed {selected_branch} from {selected_college} successfully.")
        else:
            st.info("ℹ️ No colleges available for deletion.")

# Tab 2: College-Level Options
with tabs[1]:
    st.write("###  Add or Remove College-Level Data")
    col1, col2, col3 = st.columns(3)

    # Add College
    with col1:
        st.write("#### ➕ Add College")
        if selected_place and selected_place != "--Select--":
            selected_college = st.selectbox(
                "🏫 Select College",
                ["--Select--"] + sorted(df[df["Place"] == selected_place]["College Name"].dropna().unique()),
                key="college_select_college_tab",
            )
            if st.button("Add College", key="add_college_button"):
                branches = sorted(df[df["College Name"] == selected_college]["Branch Name"].dropna().unique())
                for branch in branches:
                    selected_list = [selected_category, selected_place, selected_college, branch]
                    cutoff_rank = getcutoff_rank(selected_list, df)
                    college_code = getcollege_code(selected_list, df)
                    branch_code = getbranch_code(selected_list, df)
                    if cutoff_rank[0] != -1 and college_code != -1 and branch_code != -1:
                        st.session_state["selected_data"].append([
                            college_code, selected_place, selected_college, branch, branch_code, cutoff_rank[1], cutoff_rank[0]
                        ])
                        
    with col2:
        st.write("#### 🚮 Remove from the List")
        if st.session_state["selected_data"]:
            college_list = list(set([col[2] for col in st.session_state["selected_data"]]))
            selected_college = st.selectbox("🏫 Select College", ["--Select--"] + sorted(college_list), key="delete_coll")

            if selected_college and selected_college != "--Select--":
                branch_list = [col[3] for col in st.session_state["selected_data"] if col[2] == selected_college]
                selected_branch = st.selectbox(
                    "📚 Select Branch",
                    ["--Select--"] + sorted(branch_list),
                    key="delete_bran",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Remove Branch", key="delete_button"):
                        st.session_state["selected_data"] = [
                            col for col in st.session_state["selected_data"]
                            if not (col[2] == selected_college and col[3] == selected_branch)
                        ]
                        st.success(f"✅ Removed {selected_branch} from {selected_college} successfully.")
        else:
            st.info("ℹ️ No colleges available for deletion.")

    # Delete College
    with col3:
        st.write("#### 🚮 Remove College")
        if st.session_state["selected_data"]:
            college_list = list(set([col[2] for col in st.session_state["selected_data"]]))
            selected_college = st.selectbox("🏫 Select College", ["--Select--"] + sorted(college_list), key="delete_all_college")
            if selected_college and selected_college != "--Select--":
                if st.button("Remove All Branches", key="delete_all_button"):
                    st.session_state["selected_data"] = [
                        col for col in st.session_state["selected_data"] if col[2] != selected_college
                    ]
                    st.success(f"✅ Removed all branches of {selected_college} successfully.")
        else:
            st.info("ℹ No colleges available for deletion.")

# Display Selected Data
st.write("---")
st.write("### 🎯 Selected Colleges and Cutoff Details")
if st.session_state["selected_data"]:
    selected_df = gettable(st.session_state["selected_data"])
    st.table(selected_df)

    try:
        pdf_path = generate_pdf_table(st.session_state["selected_data"])
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        st.download_button(
            label="📥 Download as PDF",
            data=pdf_data,
            file_name="colleges_table.pdf",
            mime="application/pdf",
        )
    except ValueError as e:
        st.error(f"⚠️ Error generating PDF: {e}")
else:
    st.info("ℹ️ No data selected yet.")
