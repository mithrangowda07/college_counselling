import streamlit as st
import pandas as pd
from functions_page import getbranch_code,getcutoff_rank,getcollege_code,gettable,generate_pdf_table

def page3(df):
    if "selected_colleges" not in st.session_state:
        st.session_state["selected_colleges"] = []
    
    exclusion_list = ["College Code", "Place", "College Name", "Branch", "Branch code"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list))
    selected_place = st.selectbox(
        "Select Place",
        ["--Select--"] + sorted(df["Place"].dropna().unique()),
        disabled=(selected_category == "--Select--"),
    )
    if selected_place and selected_place != "--Select--":
        selected_branch = st.selectbox(
            "Select Branch",
            ["--Select--"] + sorted(df[df["Place"] == selected_place]["Branch"].dropna().unique()),
        )
        if selected_branch and selected_branch != "--Select--":
            filtered_df = df[(df["Place"] == selected_place) & (df["Branch"] == selected_branch)]
            selected_college = st.selectbox(
                "Select College",
                ["--Select--"] + sorted(filtered_df["College Name"].dropna().unique()),
            )
            if selected_college and selected_college != "--Select--":
                selected_list = [selected_category, selected_place, selected_college, selected_branch]
                if st.button("Submit"):
                    cutoff_rank = getcutoff_rank(selected_list, df)
                    college_code = getcollege_code(selected_list, df)
                    branch_code = getbranch_code(selected_list, df)
                    if cutoff_rank[0] == -1 or college_code == -1 or branch_code == -1:
                        st.error("No data available for the selected options. Please make valid selections.")
                    else:
                        st.success(f"Cutoff Rank for the selected option: {cutoff_rank[0]}")
                        if cutoff_rank[1] == "GM":
                            selected_category = "GM"
                        selected_list = [
                            college_code,
                            selected_place,
                            selected_college,
                            selected_branch,
                            branch_code,
                            selected_category,
                            cutoff_rank[0],
                        ]
                        st.session_state["selected_colleges"].append(selected_list)
            if st.button("Show the list"):
                if st.session_state["selected_colleges"]:
                    selected_df = gettable(st.session_state["selected_colleges"])
                    st.write("Selected Colleges and Cutoffs:")
                    st.table(selected_df)

                try:
                    # Generate the PDF file and get the file path
                    pdf_path = generate_pdf_table(st.session_state["selected_colleges"])

                    # Read the file back into memory
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()

                    # Display the download button for the PDF
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_data,
                        file_name="colleges_table.pdf",
                        mime="application/pdf",
                    )
                except ValueError as e:
                    st.error(str(e))