import streamlit as st
import pandas as pd
import database


def past_report():
        def dict_to_list(a):
            result = []
            for i in a:
                result.append(i)
            return result

        all_jd = dict_to_list(database.fetch_all_recent_job_roles())
        option_to_id = {f"Role: {item['jd_role']} (ID: {item['jd_id']})": item['jd_id'] for item in all_jd}
        selected_option = st.selectbox("Choose a Job Role:", list(option_to_id.keys()))
        jd_id = option_to_id[selected_option]

        report = database.extract_all_data_for_jd_id(jd_id)

        if report:
            column_names = [
                "id", "cand_name", "email", "phone", "address", "role", "technical_skills",
                "soft_skills", "similar_skills", "missing_skills", "preferable_skills",
                "required_experience", "score", "recommendation", "file_path", "active",
                "created_at", "companies", "designations", "projects", "degrees", "certificates"
            ]
            df = pd.DataFrame(report, columns=column_names)
            
            # Set default as an empty list for no initial selection
            cols = st.multiselect('Select columns to display', df.columns, default=[])
            
            # Only display the DataFrame if there are columns selected
            if cols:
                st.dataframe(df[cols])

            # Download button for CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download CSV", data=csv, file_name="report.csv", mime='text/csv')
        else:
            st.write("No data found for the selected job role.")
