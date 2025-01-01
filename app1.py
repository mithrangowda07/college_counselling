import streamlit as st
import pandas as pd

# File paths
FILE_PATH1 = "cet_colg_data.xlsx"

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

# Rank Range Logic
def get_rank_range(rank):
    """Determine the rank range based on user rank."""
    if rank <= 1000:
        return rank * 0.0, 3000  # 100% below and above
    elif rank <= 5000:
        return rank * 0.0, 5000  # 100% below and above
    elif rank <= 10000:
        return rank * 0.0, rank * 2.0  # 100% below and above
    elif rank <= 35000:
        return rank * 0.7, rank * 1.5  # 70% to 50%
    elif rank <= 75000:
        return rank * 0.5, rank * 1.35  # 50% to 35%
    else:
        return rank * 0.35, rank * 1.1  # 35% to rank

# Title
st.title("🎓 CounselMate: Your College Admission Assistant")
st.write("### College List Based on Rank")
with st.expander("📢 **Disclaimer**"):
    st.write(
        """
        - The seat matrix displayed is based on available data.
        - Actual results may vary during counselling.
        - Use this app for reference and decision-making.
        """
    )

# User Inputs
col1, col2 = st.columns(2)
with col1:
    user_rank = st.text_input("Enter Your CET Rank")
    user_rank = int(user_rank) if user_rank.isdigit() else st.warning("Please enter a valid rank.")
    
with col2:
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("📊 Select Category", ["--Select--"] + sorted(category_list), key="category_select")

selected_branches = st.multiselect(
        "🔽 Select Branches",
        sorted(df["Branch Name"].dropna().unique()),
        key="select_branch",
    )

# Process Inputs and Display Results
if user_rank and selected_branches:
    # Filter data for the selected branches
    filtered_data = df[df["Branch Name"].isin(selected_branches)].copy()

    # Ensure the GM column is numeric
    filtered_data["GM"] = pd.to_numeric(filtered_data["GM"], errors="coerce")
    filtered_data = filtered_data.dropna(subset=["GM"])  # Exclude invalid GM values

    # Get the rank range
    lower_limit, upper_limit = get_rank_range(user_rank)

    # Filter based on the rank range
    filtered_data = filtered_data[
        (filtered_data["GM"] >= lower_limit) & (filtered_data["GM"] <= upper_limit)
    ]

    # Sort by GM column
    filtered_data = filtered_data.sort_values(by="GM")

    # Display results
    if not filtered_data.empty:
        st.write(
            f"### Colleges Matching Your Rank:)"
        )
        display_data = filtered_data[["College Name", "Place", "Branch Name", "GM"]].rename(
            columns={
            "College Name": "College",
            "Place": "Location",
            "Branch Name": "Branch",
            "GM": "Cutoff Rank",
            }
        )
        display_data.index = range(1, len(display_data) + 1)
        st.table(display_data)
    else:
        st.error("🚫 No colleges found matching your criteria. Try adjusting your inputs.")
else:
    st.info("ℹ️ Please enter your rank and select branches to view matching colleges.")


st.sidebar.write("# Menu")
# URL to redirect to
url = "https://best-college-branch-for-kcet.streamlit.app/"  # Replace this with your desired link



# Custom CSS to position the "About Us" button
st.markdown("""
    <style>
    .top-right-button {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Create the About Us button
if st.sidebar.button("ℹ️ About Us"):
    st.markdown("""
    ## About Us  
    Welcome to **CounselMate: Your College Admission Assistant**, your trusted guide for simplifying the post-exam counseling process for exams like JEE and CET.  

    ### What We Offer:  
    1. **College Recommendations:** Enter your rank to discover colleges matching your cutoff.  
    2. **Advanced Sorting:** Prioritize colleges by creating and refining your custom list.  
    3. **Best Branch Finder:** Identify the ideal branch and college for your aspirations.  
    4. **Seat Matrix Insights:** Stay updated on seat availability across colleges.  
    5. **Chatbot Support:** Get instant guidance and answers to your queries.  

    At **CounselMate: Your College Admission Assistant**, we make your counseling journey effortless and efficient.  
    **Let’s shape your future together!**
    """)
    
    # Button with link
if st.sidebar.button("🔄 Advance Sort"):
    # Use Streamlit's experimental rerun functionality to redirect
    st.experimental_set_query_params(redirect_url=url)
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url={url}">
    """, unsafe_allow_html=True)
# # Menu items
# menu_items = [
#     {"icon": "🏠", "label": "Home"},
#     {"icon": "🏛️", "label": "Know About Cluster"},
#     {"icon": "📊", "label": "Seat Matrix"},
#     {"icon": "🔄", "label": "Advance Sort"},
# ]
