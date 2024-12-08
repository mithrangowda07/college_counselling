import streamlit as st
import pandas as pd

def page4(df):
    # Ensure GM column is numeric
    df["GM"] = pd.to_numeric(df["GM"], errors="coerce")
    df = df.dropna(subset=["GM"])  # Drop rows with NaN in GM
    
    st.write("### Best")
    
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list), key="add_category")
    
    col1, col2 = st.columns(2)
    
    # Best college for a selected branch
    with col1:
        st.write("#### Best college for selected branch")
        selected_branch = st.selectbox(
            "Select Branch",
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
                st.write(f"*College:* {best_college['College Name']}")
                st.write(f"*Cutoff:* {best_college[selected_category]}")
            else:
                st.write("No valid data available for the selected category and branch.")

    # Best branch for a selected college
    with col2:
        st.write("#### Best branch for selected College")
        selected_college = st.selectbox(
            "Select College",
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
                st.write(f"*Branch:* {best_branch['Branch Name']}")
                st.write(f"*Cutoff:* {best_branch[selected_category]}")
            else:
                st.write("No valid data available for the selected category and college.")