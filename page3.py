import streamlit as st
import pandas as pd
from functions_page import getbranch_code,getcutoff_rank,getcollege_code,gettable,generate_pdf_table

def page3(df):
    if "selected_branch" not in st.session_state:
        st.session_state["selected_branch"] = []
    
    col1, col2 ,col3 = st.columns(3)
    
    with col1:
        st.write("### Add Branch to the List")
        exclusion_list = ["College Code", "Place", "College Name", "Branch", "Branch code"]
        category_list = [col for col in df.columns if col not in exclusion_list]
        selected_category = st.selectbox("Select Category", ["--Select--"] + sorted(category_list), key="add_category")
        selected_branch = st.selectbox(
            "Select Branch",
            ["--Select--"] + sorted(df["Branch"].dropna().unique()),
            disabled=(selected_category == "--Select--"),
            key="add_branch",
        )
        if selected_branch and selected_branch != "--Select--":
            selected_place = st.selectbox(
                "Select place",
                ["--Select--"] + sorted(df[df["Branch"] == selected_branch]["Place"].dropna().unique()),
                key="add_place",
            )
            if selected_place and selected_place != "--Select--":
                filtered_df = df[(df["Place"] == selected_place) & (df["Branch"] == selected_branch)]
                selected_college = st.selectbox(
                    "Select College",
                    ["--Select--"] + sorted(filtered_df["College Name"].dropna().unique()),
                )
                if selected_college and selected_college != "--Select--":
                    if st.button("Add", key="add_submit"):
                        selected_list = [selected_category, selected_place, selected_college, selected_branch]
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
                            st.session_state["selected_branch"].append(selected_list)
                            
    with col2:  # Delete from the list logic
        st.write("### Delete from the List")
        if st.session_state["selected_branch"]:
            college_list = list(set([col[2] for col in st.session_state["selected_branch"]]))
            selected_college = st.selectbox("Select College", ["--Select--"] + sorted(college_list), key="delete_college")

            if selected_college and selected_college != "--Select--":
                branch_list = [col[3] for col in st.session_state["selected_branch"] if col[2] == selected_college]
                selected_branch = st.selectbox(
                    "Select Branch",
                    ["--Select--"] + sorted(branch_list),
                    key="delete_branch",
                )
                if selected_branch and selected_branch != "--Select--":
                    if st.button("Delete", key="delete_submit"):
                        st.session_state["selected_branch"] = [
                            col for col in st.session_state["selected_branch"]
                            if not (col[2] == selected_college and col[3] == selected_branch)
                        ]
                        st.success(f"Deleted {selected_branch} from {selected_college} successfully.")
        else:
            st.write("No selections available for deletion.")
            
    with col3:
        st.write("### Delete the College")
        if st.session_state["selected_branch"]:
            # Extract unique college names from the selected colleges
            branch_list = list(set([col[3] for col in st.session_state["selected_branch"]]))
            selected_branch = st.selectbox(
                "Select Branch", ["--Select--"] + sorted(branch_list), key="delete_branches_allcolleges"
            )

            if selected_branch and selected_branch != "--Select--":
                # Display a confirmation button for deleting all branches of the selected college
                if st.button("Delete All colleges", key="delete_all_colleges"):
                    # Filter out all entries associated with the selected college
                    st.session_state["selected_branch"] = [
                        col for col in st.session_state["selected_branch"]
                        if col[3] != selected_branch  # Assuming [3] is the college name
                    ]
                    st.success(f"All colleges of {selected_branch} have been deleted successfully.")
        else:
            st.write("No colleges available for deletion.")
                        
    if st.session_state["selected_branch"]:
        selected_df = gettable(st.session_state["selected_branch"])
        st.write("### Selected Colleges and Cutoff Details")  # Add a title
        st.table(selected_df)

        try:
            # Generate the PDF file and get the file path
            pdf_path = generate_pdf_table(st.session_state["selected_branch"])

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