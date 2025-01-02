import streamlit as st
import pandas as pd

# Define the file path
FILE_PATH = "cet_matrix.xlsx"

# Custom CSS for background and font
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .stSelectbox {
        font-size: 16px;
    }
    .tabs-container {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the Excel file with a progress bar
@st.cache_data
def load_excel_file():
    """Load Excel file."""
    with st.spinner("Loading data... Please wait"):
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

# App Title
st.title("🎓 CounselMate: Your College Admission Assistant")
st.write("### 🔍 Explore Seat Matrix and Make Informed Choices")

# Collapsible disclaimer section
with st.expander("📢 **Disclaimer**"):
    st.write(
        """
        - The seat matrix displayed is based on available data.
        - Actual results may vary during counselling.
        - Use this app for reference and decision-making.
        """
    )

# Dropdown and tab section
st.write("---")  # Separator line for better layout
col1, col2 = st.columns([1, 2])
with col1:
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code", "SNQ", "Total"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("📊 Select Category", ["--Select--"] + sorted(category_list), key="add_category")

# Tabs
st.write("---")
tabs = st.tabs(["🏫 College Analysis", "📚 Branch Analysis"])

# Tab 1: College Analysis
with tabs[0]:
    st.write("#### 🏅 Explore Particular Colleges")
    selected_college = st.selectbox(
        "🔽 Select College",
        ["--Select--"] + sorted(df["College Name"].dropna().unique()),
        disabled=(selected_category == "--Select--"),
        key="add_college",
    )

    if selected_college != "--Select--" and selected_category != "--Select--":
        fallback_categories = fallback_order.get(selected_category, [selected_category])
        filtered_data = df[(df["College Name"] == selected_college) & (df[fallback_categories].any(axis=1))]

        if not filtered_data.empty:
            st.success(f"🎓 Showing seat matrix for **{selected_category}** in **{selected_college}**:")
            filtered_data = filtered_data.reset_index(drop=True)
            filtered_data.index = range(1, len(filtered_data) + 1)
            st.table(filtered_data[[ "Branch Name"] + fallback_categories + ["SNQ", "Total"]])
        else:
            st.error("🚫 No data available for the selected category and college.")

# Tab 2: Branch Analysis
with tabs[1]:
    st.write("#### 🏅 Explore All Colleges")
    if selected_category != "--Select--":
        fallback_categories = fallback_order.get(selected_category, [selected_category])
        all_colleges_data = df[["College Name", "Branch Name"] + fallback_categories + ["SNQ", "Total"]]

        st.success(f"Displaying seat matrix for **{selected_category}** across all colleges:")
        st.dataframe(all_colleges_data)

st.sidebar.image("find.gif", use_container_width=True)

st.sidebar.write("# ℹ️ About Us")
st.sidebar.markdown("""
Welcome to **CounselMate: Your College Admission Assistant**, your trusted guide for simplifying the post-exam counseling process for exams like JEE and CET.  

#### What We Offer:  
1. **College Recommendations:** Enter your rank to discover colleges matching your cutoff.  
2. **Advanced Sorting:** Prioritize colleges by creating and refining your custom list.  
3. **Best Branch Finder:** Identify the ideal branch and college for your aspirations.  
4. **Seat Matrix Insights:** Stay updated on seat availability across colleges.  
5. **Chatbot Support:** Get instant guidance and answers to your queries.  

At **CounselMate: Your College Admission Assistant**, we make your counseling journey effortless and efficient.  
**Let’s shape your future together!**
""")