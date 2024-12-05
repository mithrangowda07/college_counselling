import streamlit as st
import pandas as pd

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

#Sidebar
st.sidebar.image('rvce_logo.jpg', width=230)
st.sidebar.title("Navigator")
pagelist = ["Home","Normal Sort","College","Branch"]
app = st.sidebar.radio("Select Page", pagelist)
st.sidebar.markdown("""
    <div style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; color: #f58067;">
        Created by:<br>
        1. Mithra N Gowda
    </div>
""", unsafe_allow_html=True)

if app == pagelist[0]:
    st.title("K-CET Counselling Helper")
    
elif app == pagelist[1]:
    from page1 import page1
    page1(df)
    
elif app == pagelist[2]:
    from page2 import page2
    page2(df)
    
elif app == pagelist[3]:
    from page3 import page3
    page3(df)