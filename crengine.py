import streamlit as st
import json
import datetime
import pandas as pd
import streamlit as st
from dataload import *
from jd_structure import *
from resume_structure import *
from resume_matching import *
import os
from io import BytesIO
import asyncio
import database
import base64



def candidate_recommendation_engine():
    st.header("AI Powered Candidate Recommendation Engine", divider="rainbow")

    if 'is_matching' not in st.session_state:
        st.session_state['is_matching'] = False
    if 'viewing_role_report' not in st.session_state:
        st.session_state['viewing_role_report'] = False
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files'] = False
    if 'selected_role' not in st.session_state:
        st.session_state['selected_role'] = None
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 0  # starting index for pages
    if 'cards_per_page' not in st.session_state:
        st.session_state['cards_per_page'] = 10

    job_role_exists = False
    job_role_input = st.sidebar.text_input("Job Role", key="job_role_input").strip()
    if job_role_input:
        job_role_exists = database.check_job_role_in_database(job_role_input)
        if job_role_exists:
            st.sidebar.warning("Job role already exists in the database. Please try a different name.")

    job_type = st.sidebar.selectbox("Select Job Type", ["Technical", "Non-Technical"], key="job_type") if not job_role_exists else None

    st.session_state["jd_id"] = job_role_input

    with st.sidebar:
        with st.form("combined_form", clear_on_submit=True):
            jds = st.file_uploader("Upload Job Description (JD)", type=["docx"], accept_multiple_files=False, key="form_jds") if not job_role_exists else None
            resumes = st.file_uploader("Upload Resumes", type=["ZIP"], key="form_resumes") if not job_role_exists else None
            start_matching = st.form_submit_button("Match Resumes")

    if start_matching:
        st.session_state['is_matching'] = True
        st.session_state['viewing_role_report'] = False
        st.session_state['selected_role'] = None

    def show_recent_job_roles_with_data_fetch():
        st.sidebar.subheader("Recent Job Roles")
        recent_roles = database.fetch_all_recent_job_roles()

        if recent_roles and not st.session_state['is_matching']:
            roles_options = [f"{role['jd_role']} ({role['created_at'].strftime('%Y-%m-%d')})" for role in recent_roles]
            selected_role = st.sidebar.selectbox("Select a Job Role", roles_options, key='selected_role_dropdown')

            selected_role_data = next((role for role in recent_roles if f"{role['jd_role']} ({role['created_at'].strftime('%Y-%m-%d')})" == selected_role), None)

            if selected_role_data:
                st.session_state['selected_role'] = selected_role_data['jd_role']
                st.session_state['is_matching'] = False
                st.session_state['viewing_role_report'] = True
                st.session_state['uploaded_files'] = False
        else:
            st.sidebar.warning("No recent data found")

    if not st.session_state['uploaded_files'] and not st.session_state['selected_role'] and not st.session_state['is_matching']:
        st.warning("Please upload job description (JD) and resumes to get the latest report or access recent files if any.")
    show_recent_job_roles_with_data_fetch()

    Report_cards, feedback_tab = st.tabs(["Score Cards", "Feedback Tab"])

    # Helper functions
    def create_download_button(file_path):
        """Generate a download button for resumes. Handles cases where file_path might be None."""
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as file:
                filedata = file.read()
            encoded_data = base64.b64encode(filedata).decode()
            filename = os.path.basename(file_path)
            download_button = f'<a download="{filename}" href="data:application/pdf;base64,{encoded_data}" style="text-decoration: none; color: white; background-color: #FF4B4B; padding: 8px 15px; border-radius: 5px; margin: 5px;">Download Resume</a>'
        else:
            download_button = "File not available"
        return download_button

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        return processed_data

    # Define functions for pagination
    def show_page(page_index, data):
        start_index = page_index * st.session_state['cards_per_page']
        end_index = start_index + st.session_state['cards_per_page']
        return data[start_index:end_index]

    def next_page():
        st.session_state['current_page'] += 1

    def previous_page():
        if st.session_state['current_page'] > 0:
            st.session_state['current_page'] -= 1

    with Report_cards:
        if 'selected_role' in st.session_state and not st.session_state['is_matching'] and st.session_state['viewing_role_report']:
            reportdata = database.fetch_resumes_by_job_role(st.session_state['selected_role'])
            process_time_and_cost = database.fetch_cost_and_process_time_by_job_role(st.session_state['selected_role'])
            st.session_state["process_time"] = process_time_and_cost[0]['ProcessTime']
            st.session_state["cost"] = process_time_and_cost[0]['Cost']

            if reportdata and process_time_and_cost:
                df = pd.DataFrame(reportdata)
                df = df.sort_values(by='Score', ascending=False)
                st.markdown(f"<h3 style='font-size:26px;'>Quick Recommendations For Role: {st.session_state['selected_role']}</h3>", unsafe_allow_html=True)
                st.success(f'Processed in Time: {st.session_state["process_time"]:.2f} seconds')
                st.info(f'Cost: {st.session_state["cost"]:.2f} $')
                st.download_button(
                    label="Download Report",
                    data=to_excel(df),
                    file_name="candidate_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                total_cards = len(df)
                total_pages = (total_cards + st.session_state['cards_per_page'] - 1) // st.session_state['cards_per_page']  # calculate the total number of pages

                df_subset = show_page(st.session_state['current_page'], df)

                for index, row in df_subset.iterrows():  # Use df_subset instead of df
                    candidate_name = row.get('Name')  # Using .get() avoids KeyError if 'Name' is not a key in the dictionary
                    if candidate_name is not None:
                        candidate_name = candidate_name.upper()
                    else:
                        candidate_name = "Name Not Found"
                    job_role = row.get('Role', 'Default Role') 
                    similar_skills = row.get('SimilarSkills', [])
                    missing_skills = row.get('MissingSkills', [])
                    experiences = row.get('RequiredExperience', [])
                    score = str(row.get('Score', 0)) 
                    recommendation = row.get('Recommendation', 'No recommendation available')
                    file_path = row.get('FilePath')
                    if file_path:
                        download_button = create_download_button(file_path)
                        
                    else:
                        download_button = "No file available"  # Or disable the button
                        
                    card_html = f"""
                        <div style="display: flex; flex-direction: column; justify-content: space-between; padding: 20px; margin: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: #f5f5f5; transition: box-shadow 0.3s ease;">
                            <div style="display: flex; justify-content: space-between;">
                                <div style="flex: 1;">
                                    <h4>{candidate_name}</h4>
                                    <p><strong>Role:</strong> {job_role}</p>
                                    <p><strong>Similar Skills:</strong> {similar_skills}</p>
                                    <p><strong>Missing Skills:</strong> {missing_skills}</p>
                                    <p><strong>Experiences:</strong> {experiences}</p>
                                    <p><strong>Candidate Summary:</strong> {recommendation}</p>
                                    <div style="align-self: flex-start;">
                                        {download_button}
                                    </div>
                                </div>
                                <div class="progress-bar" style="width: 100px; height: 100px; position: relative;">
                                    <svg viewBox="0 0 100 100" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;">
                                        <!-- Background circle -->
                                        <circle cx="50" cy="50" r="45" fill="none" stroke="#eee" stroke-width="10"/>
                                        <!-- Progress circle -->
                                        <circle cx="50" cy="50" r="45" fill="none" stroke="LightGreen" stroke-width="10" 
                                                stroke-dasharray="283" stroke-dashoffset="{283 - (283 * float(score) / 100)}" 
                                                transform="rotate(-90 50 50)"/>
                                        <!-- Text inside circle -->
                                        <text x="50" y="50" text-anchor="middle" dominant-baseline="central" font-size="24" fill="black">{score}%</text>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                if st.session_state['current_page'] > 0:
                    col1.button("Previous", on_click=previous_page)
                if st.session_state['current_page'] < total_pages - 1:
                    col3.button("Next", on_click=next_page)

                col2.write(f"Page {st.session_state['current_page'] + 1} of {total_pages}")

                with feedback_tab:
                    st.subheader("Feedback For Current Resumes", divider="rainbow")
                    with st.form("feedback", clear_on_submit=True):
                        user_comments = st.text_area("Feedback")
                        submit_feedback = st.form_submit_button("Submit Feedback")
                        if submit_feedback:
                            fk_jd_id = database.get_fk_jd_id(st.session_state['selected_role'])
                            database.get_feedback(user_comments, fk_jd_id)
                            st.toast("Feedback received", icon="👍")
                            message_placeholder = st.empty()
                            message_placeholder.text("Feedback submitted successfully!")
                            import time
                            time.sleep(5)
                            message_placeholder.empty()
            else:
                st.error("No candidates found for the selected role.")

        elif st.session_state['is_matching']:
            if not jds:
                st.warning("Please upload a job description (JD).")
            elif not job_role_input:
                st.warning("Please input the job role.")
            elif not resumes:
                st.warning("Please upload resumes.")
            else:
                st.session_state["uploaded_files"] = True
                st.session_state["start_time"] = datetime.datetime.now()
                
                # Define processing stages and corresponding text
                stages = [
                    ("Resumes are being processed...", 0.0),
                    ("Job Description is being processed...", 0.4),
                    ("Looking for candidates...", 0.6)
                ]
                # Display a single progress bar for all stages
                progress_bar = st.progress(0.0)
                stage_text_placeholder = st.empty()

                # Process each stage
                for stage_index, (stage_text, progress_value) in enumerate(stages, start=1):
                    progress_bar.progress(progress_value)
                    stage_text_placeholder.markdown(f'<p style="font-size: 24px;">{stage_text}</p>', unsafe_allow_html=True)

                    if stage_index == 1:
                        resume_docs, folder_path , resume_raw_path = process_text_resumes(resumes)
                        structured_resumes, cost1 = asyncio.run(structure_resumes(resume_docs))
                        resumes_json =  save_structured_resumes_as_json(structured_resumes, folder_path)
                    elif stage_index == 2:
                        jd_docs = save_and_get_text_jd(jds, folder_path)
                        structured_jd, cost2 = get_jd_structured(jd_docs.page_content, job_type)
                        jd_json = json.dumps(structured_jd.dict())
                        save_jd(jd_json, structured_jd.role, folder_path)
                    elif stage_index == 3:
                        resumes_final_report, cost3 = asyncio.run(
                        match_resumes_with_jd(structured_resumes, jd_json))
                
                #ALL SESSIONS TO STORE ALL INFORMATION NEEDED FURTHER TO DISPLAY
                st.session_state["stop_time"] = datetime.datetime.now()       
                st.session_state["cost"] = cost1 + cost2 + cost3
                st.session_state["resumes_report"] = resumes_final_report
                st.session_state["resume_raw_path"] = resume_raw_path
                st.session_state["folder_path"] = folder_path
                st.session_state["jd_role"] = structured_jd.role
                st.session_state["jd"] = json.dumps(structured_jd.dict())
                st.session_state["process_time"] = (st.session_state["stop_time"] - st.session_state["start_time"]).total_seconds()
                
                # CODE TO SAVE IN DATABASE
                fk_jd_id = database.insert_jd_data_into_db(st.session_state["jd"], st.session_state["process_time"], st.session_state["cost"], st.session_state["jd_id"], st.session_state["folder_path"], job_type)
                st.session_state["fk_jd_id"] = fk_jd_id        
                database.process_resume_files(resumes_json, st.session_state["fk_jd_id"], st.session_state["resumes_report"], st.session_state["resume_raw_path"])
                stage_text_placeholder.empty()
                progress_bar.empty()
                st.session_state["is_matching"] = False
                st.toast("Matching Resumes Completed!")
                st.rerun()