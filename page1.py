import streamlit as st
import pandas as pd
from functions_page import getbranch_code, getcutoff_rank, getcollege_code, gettable, generate_pdf_table

def page1(df):
    if "selected_data" not in st.session_state:
        st.session_state["selected_data"] = []
    
    # Side-by-side Add and Delete Buttons
    col1, col2 = st.columns(2)
    
    with col1:  # Add to the list logic
        st.write("### Add to the List")
        exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code"]
        category_list = [col for col in df.columns if col not in exclusion_list]
        selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list), key="add_category")
        selected_place = st.selectbox(
            "Select Place",
            ["--Select--"] + sorted(df["Place"].dropna().unique()),
            disabled=(selected_category == "--Select--"),
            key="add_place",
        )
        if selected_place and selected_place != "--Select--":
            selected_college = st.selectbox(
                "Select College",
                ["--Select--"] + sorted(df[df["Place"] == selected_place]["College Name"].dropna().unique()),
                key="add_college",
            )
            if selected_college and selected_college != "--Select--":
                selected_branch = st.selectbox(
                    "Select Branch",
                    ["--Select--"] + sorted(df[df["College Name"] == selected_college]["Branch Name"].dropna().unique()),
                    key="add_branch",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Add", key="add_submit"):
                        selected_list = [selected_category, selected_place, selected_college, selected_branch]
                        cutoff_rank = getcutoff_rank(selected_list, df)
                        college_code = getcollege_code(selected_list, df)
                        branch_code = getbranch_code(selected_list, df)
                        
                        if cutoff_rank[0] == -1 or college_code == -1 or branch_code == -1:
                            st.error("No data available for the selected options. Please make valid selections.")
                        else:
                            st.success(f"Cutoff Rank for the selected option: {cutoff_rank[0]}")
                            selected_list = [
                                college_code,
                                selected_place,
                                selected_college,
                                selected_branch,
                                branch_code,
                                cutoff_rank[1], #selected_category
                                cutoff_rank[0],
                            ]
                            st.session_state["selected_data"].append(selected_list)

    with col2:  # Delete from the list logic
        st.write("### Delete from the List")
        if st.session_state["selected_data"]:
            college_list = list(set([col[2] for col in st.session_state["selected_data"]]))
            selected_college = st.selectbox("Select College", ["--Select--"] + sorted(college_list), key="delete_college")

            if selected_college and selected_college != "--Select--":
                branch_list = [col[3] for col in st.session_state["selected_data"] if col[2] == selected_college]
                selected_branch = st.selectbox(
                    "Select Branch",
                    ["--Select--"] + sorted(branch_list),
                    key="delete_branch",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Delete", key="delete_submit"):
                        st.session_state["selected_data"] = [
                            col for col in st.session_state["selected_data"]
                            if not (col[2] == selected_college and col[3] == selected_branch)
                        ]
                        st.success(f"Deleted {selected_branch} from {selected_college} successfully.")
        else:
            st.write("No colleges available for deletion.")

    # Display selected colleges table
    if st.session_state["selected_data"]:
        selected_df = gettable(st.session_state["selected_data"])
        st.write("### Selected Colleges and Cutoff Details")
        st.table(selected_df)

        # Download PDF of the table
        try:
            pdf_path = generate_pdf_table(st.session_state["selected_data"])
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            st.download_button(
                label="Download as PDF",
                data=pdf_data,
                file_name="colleges_table.pdf",
                mime="application/pdf",
            )
        except ValueError as e:
            st.error(str(e))
    else:
        # Empty table placeholder
        empty_df = pd.DataFrame(columns=["College Code", "Place", "College Name", "Branch", "Branch Code", "Category", "Cutoff Rank"])
        st.write("### Selected Colleges and Cutoff Details")
        st.table(empty_df)
