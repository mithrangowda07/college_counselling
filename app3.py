import streamlit as st
import pandas as pd

# File paths
FILE_PATH1 = "cet_colg_data.xlsx"

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

# Load Excel File with a progress bar
@st.cache_data
def load_excel_file(FILE_PATH):
    """Load Excel file."""
    with st.spinner("Loading data... Please wait"):
        try:
            data = pd.read_excel(FILE_PATH, engine="openpyxl")
            data.columns = data.columns.str.strip()  # Clean column names
            return data
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None

df = load_excel_file(FILE_PATH1)

# App Title
st.title("🎓 CounselMate: Your College Admission Assistant")
st.write("### 🔍 Explore the Best College and Branch Options for Your Rank")

# Collapsible disclaimer section
with st.expander("📢 **Disclaimer**"):
    st.write(
        """
        - The results shown in this app are **based on previous year cutoff data**.
        - The actual college selections during counselling will vary depending on your preferences and seat availability.
        - Use this tool as a reference to make informed decisions.
        """
    )

# Dropdown and tab section
st.write("---")  # Separator line for better layout
col1, col2, col3 = st.columns(3)
with col1:
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("📊 Select Category", ["--Select--"] + sorted(category_list), key="category_select")

# Tabs
tabs = st.tabs(["🏫 College Recommendations", "📚 Branch Recommendations"])

# Tab 1: College Recommendations
with tabs[0]:
    st.write("#### 🏅 Discover the Best Colleges for Your Selected Branch")
    selected_branch = st.selectbox(
        "🔽 Select Branch",
        ["--Select--"] + sorted(df["Branch Name"].dropna().unique()),
        key="select_branch",
    )
    if selected_branch != "--Select--" and selected_category != "--Select--":
        filtered_data = df[df["Branch Name"] == selected_branch].copy()
        
        # Exclude rows where the selected category has invalid values
        filtered_data[selected_category] = pd.to_numeric(
            filtered_data[selected_category], errors="coerce"
        )
        filtered_data = filtered_data.dropna(subset=[selected_category])
        
        if not filtered_data.empty:
            best_college = (
                filtered_data.sort_values(by=selected_category, ascending=True)
                .iloc[0]  # College with the lowest GM value (best)
            )
            st.success(f"🎓 **College:** {best_college['College Name']}")
            st.info(f"📈 **Cutoff Rank:** {best_college[selected_category]}")
        else:
            st.error("🚫 No valid data available for the selected category and branch.")

# Tab 2: Branch Recommendations
with tabs[1]:
    st.write("#### 🏅 Discover the Best Branches in Your Selected College")
    selected_college = st.selectbox(
        "🔽 Select College",
        ["--Select--"] + sorted(df["College Name"].dropna().unique()),
        key="select_college",
    )
    if selected_college != "--Select--" and selected_category != "--Select--":
        filtered_data = df[df["College Name"] == selected_college].copy()
        
        # Exclude rows where the selected category has invalid values
        filtered_data[selected_category] = pd.to_numeric(
            filtered_data[selected_category], errors="coerce"
        )
        filtered_data = filtered_data.dropna(subset=[selected_category])
        
        if not filtered_data.empty:
            best_branch = (
                filtered_data.sort_values(by=selected_category, ascending=True)
                .iloc[0]  # Branch with the lowest GM value (best)
            )
            st.success(f"📚 **Branch:** {best_branch['Branch Name']}")
            st.info(f"📈 **Cutoff Rank:** {best_branch[selected_category]}")
        else:
            st.error("🚫 No valid data available for the selected category and college.")
            
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