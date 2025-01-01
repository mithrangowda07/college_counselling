import streamlit as st

# Title of the app
st.title("🎓 CounselMate: Your College Admission Assistant")

st.subheader("✨ Welcome to CounselMate!")
st.write("Simplify your post-exam counseling process for exams like JEE and CET.")
st.write("Use the navigation above to learn more about us.")


st.subheader("ℹ️ About Us")
st.markdown("""
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

# # About Us button
# st.sidebar.markdown(
#     '<a href="https://about-us.streamlit.app/" class="sidebar-button" target="_self">ℹ️ About Us</a>',
#     unsafe_allow_html=True,
# )

# Home button
st.sidebar.markdown(
    '<a href="https://home-page-counsel-mate.streamlit.app/" class="sidebar-button" target="_self">🏠 Home</a>',
    unsafe_allow_html=True,
)

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
