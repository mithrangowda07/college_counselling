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
# Add CSS styling for uniform button sizes
st.sidebar.markdown(
    """
    <style>
    .sidebar-button {
        display: block;
        text-align: center;
        height: 40px; /* Set uniform height */
        line-height: 40px; /* Vertically center text */
        width: 75%; /* Full width */
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px; /* Space between buttons */
        border-radius: 8px; /* Rounded corners */
        background-color: #f0f2f6; /* Button background color */
        color: black; /* Text color */
        text-decoration: none; /* Remove underline from links */
        border: 1px solid #ccc; /* Button border */
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .sidebar-button:hover {
        background-color: #e0e3e8; /* Change color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image("find.gif", use_container_width=True)

# Sidebar menu
st.sidebar.write("# Menu")

# About Us button
st.sidebar.markdown(
    '<a href="https://about-us.streamlit.app/" class="sidebar-button" target="_self">ℹ️ About Us</a>',
    unsafe_allow_html=True,
)

# # Home button
# st.sidebar.markdown(
#     '<a href="https://home-page-counsel-mate.streamlit.app/" class="sidebar-button" target="_self">🏠 Home</a>',
#     unsafe_allow_html=True,
# )

# Advance Sort button
st.sidebar.markdown(
    '<a href="https://efficient-college-and-branch-comparison-tool.streamlit.app/" class="sidebar-button" target="_self">🔄 Advance Sort</a>',
    unsafe_allow_html=True,
)

# Seat Matrix button
st.sidebar.markdown(
    '<a href="https://kcet-seat-matrix.streamlit.app/" class="sidebar-button" target="_self">📊 Seat Matrix</a>',
    unsafe_allow_html=True,
)

# Best button
st.sidebar.markdown(
    '<a href="https://best-college-branch-for-kcet.streamlit.app/" class="sidebar-button" target="_self">💎 Best</a>',
    unsafe_allow_html=True,
)

# Chat Box button
st.sidebar.markdown(
    '<a href="https://chat-box-for-kcet-counselling.streamlit.app/" class="sidebar-button" target="_self">🤖 Chat Box</a>',
    unsafe_allow_html=True,
)

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
