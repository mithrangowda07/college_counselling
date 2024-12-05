import streamlit as st
import pandas as pd
from functions_page import getbranch_code,getcutoff_rank,getcollege_code,gettable,generate_pdf_table

def page2(df):
    if "selected_colleges" not in st.session_state:
        st.session_state["selected_colleges"] = []
    
    col1, col2 , col3 = st.columns(3)
    
    with col1:
        st.write("### Add College to the List")
        exclusion_list = ["College Code", "Place", "College Name", "Branch", "Branch code"]
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
            if st.button("Add", key="add_submit"):
                branches = sorted(df[df["College Name"] == selected_college]["Branch"].dropna().unique())
                for branch in branches:
                    selected_list = [selected_category, selected_place, selected_college, branch]
                    cutoff_rank = getcutoff_rank(selected_list, df)
                    college_code = getcollege_code(selected_list, df)
                    branch_code = getbranch_code(selected_list, df)
                    if cutoff_rank[0] != -1 and college_code != -1 and branch_code != -1:
                        selected_list = [
                            college_code,
                            selected_place,
                            selected_college,
                            branch,
                            branch_code,
                            cutoff_rank[1],
                            cutoff_rank[0],
                        ]
                        st.session_state["selected_colleges"].append(selected_list)
    
    with col2:  # Delete from the list logic
        st.write("### Delete from the List")
        if st.session_state["selected_colleges"]:
            college_list = list(set([col[2] for col in st.session_state["selected_colleges"]]))
            selected_college = st.selectbox("Select College", ["--Select--"] + sorted(college_list), key="delete_college")

            if selected_college and selected_college != "--Select--":
                branch_list = [col[3] for col in st.session_state["selected_colleges"] if col[2] == selected_college]
                selected_branch = st.selectbox(
                    "Select Branch",
                    ["--Select--"] + sorted(branch_list),
                    key="delete_branch",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Delete", key="delete_submit"):
                        st.session_state["selected_colleges"] = [
                            col for col in st.session_state["selected_colleges"]
                            if not (col[2] == selected_college and col[3] == selected_branch)
                        ]
                        st.success(f"Deleted {selected_branch} from {selected_college} successfully.")
        else:
            st.write("No selections available for deletion.")
    
    with col3:
        st.write("### Delete the College")
        if st.session_state["selected_colleges"]:
            # Extract unique college names from the selected colleges
            college_list = list(set([col[2] for col in st.session_state["selected_colleges"]]))
            selected_college = st.selectbox(
                "Select College", ["--Select--"] + sorted(college_list), key="delete_college_allbranches"
            )

            if selected_college and selected_college != "--Select--":
                # Display a confirmation button for deleting all branches of the selected college
                if st.button("Delete All Branches", key="delete_all_branches"):
                    # Filter out all entries associated with the selected college
                    st.session_state["selected_colleges"] = [
                        col for col in st.session_state["selected_colleges"]
                        if col[2] != selected_college  # Assuming [2] is the college name
                    ]
                    st.success(f"All branches of {selected_college} have been deleted successfully.")
        else:
            st.write("No colleges available for deletion.")

        
    if st.session_state["selected_colleges"]:
        selected_df = gettable(st.session_state["selected_colleges"])
        st.write("### Selected Colleges and Cutoff Details")  # Add a title
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
            
    else:
        # Create an empty DataFrame with appropriate column names
        empty_df = pd.DataFrame(columns=["College Code", "Place", "College Name", "Branch", "Branch Code", "Category", "Cutoff Rank"])
        st.write("### Selected Colleges and Cutoff Details")  # Add a title
        st.table(empty_df)