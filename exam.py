import streamlit as st
import mysql.connector
import os
import asyncio
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit.components.v1 as components
from resume_structure import structure_resumes
from jd_structure import get_jd_structured

load_dotenv()

def exam1():
    # Database configuration
    db_config = {
        'user': 'admin',
        'password': 'WHqqCKcpOa6PGQwKVIz3',
        'host': 'cre-database.clskaom22sd7.us-east-1.rds.amazonaws.com',
        'port': 3306,
        'database': 'cre'
    }

    # Set the OpenAI API key as an environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # OpenAI LLM client initialization
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")

    def get_data_from_database(query):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            if not results:
                st.warning(f"No results found for query: {query}")
            return results
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def generate_exam_from_openai(resume_info, jd_info):
        try:
            prompt_template = PromptTemplate(
                input_variables=["resume_info", "jd_info"],
                template=(
                    "Generate an assessment exam based on the following resume information: {resume_info} and job description: {jd_info}"
                    "Provide atleast 15 questions with a mix of the following types: multiple-choice questions (MCQs), short answer questions, long answer questions, coding questions, and scenario-based questions."
                    "Ensure the questions are equally divided into easy, medium, and hard levels."
                    "The HTML code should be well-structured, visually appealing, and look like a professional exam interface."
                    "Include necessary CSS for styling to make it look polished and clean"
                    "Strictly omit any markdown or 'html' & any extra texts, words at the start or end of the response."
                ),
            )

            chain = LLMChain(llm=llm, prompt=prompt_template)
            response = chain.run({"resume_info": resume_info, "jd_info": jd_info})
            return response.strip()
        except Exception as e:
            st.error(f"Error generating exam from OpenAI API: {e}")
            return None

    async def main_async(resume_id, jd_id):
        try:
            resume_query = f"SELECT * FROM resume_info WHERE id='{resume_id}'"
            jd_query = f"SELECT * FROM jd_info WHERE jd_id='{jd_id}'"
            
            resume_info = get_data_from_database(resume_query)
            jd_info = get_data_from_database(jd_query)
            
            if resume_info and jd_info:
                resume_content = resume_info[0]
                structured_resumes, resume_cost = await structure_resumes({"resume": resume_content})
                structured_jd, jd_cost = get_jd_structured(jd_info[0]['description'], jd_info[0]['job_type'])
                exam_content = generate_exam_from_openai(structured_resumes["resume"], structured_jd)
                return exam_content
            else:
                st.error("No data found for the given IDs.")
                return None
        except Exception as e:
            st.error(f"Error in main_async: {e}")
            return None

    st.title("Automated Test Generation")

    # Fetch job descriptions for the dropdown
    jobs_query = "SELECT jd_id, jd_role FROM jd_info"
    jobs = get_data_from_database(jobs_query)
    
    if jobs:
        job_options = {job['jd_role']: job['jd_id'] for job in jobs}

        st.sidebar.title("Configuration")
        selected_job = st.sidebar.selectbox("Select Job Description", options=list(job_options.keys()))

        if selected_job:
            fk_jd_id = job_options[selected_job]

            # Fetch candidates who applied for the selected job description
            candidates_query = f"""
                SELECT id, cand_name, score 
                FROM resume_info 
                WHERE fk_jd_id='{fk_jd_id}' 
                ORDER BY score DESC
            """
            candidates = get_data_from_database(candidates_query)
            
            if candidates:
                candidate_options = {f"{cand['cand_name']} (Score: {cand['score']})": cand['id'] for cand in candidates}
                selected_candidate = st.sidebar.selectbox("Select Candidate", options=list(candidate_options.keys()))

                if st.sidebar.button("Generate Exam"):
                    st.session_state.exam_content = asyncio.run(main_async(candidate_options[selected_candidate], fk_jd_id))
                    st.session_state.selected_candidate = selected_candidate

        if "exam_content" in st.session_state and st.session_state.exam_content:
            if st.session_state.exam_content.strip() == "":
                st.error("Received empty response from OpenAI API.")
            else:
                try:
                    st.subheader(f"Candidate: {st.session_state.selected_candidate.split(' (')[0]}")
                    # Display the HTML content using Streamlit components
                    components.html(st.session_state.exam_content, height=800, scrolling=True)
                    if st.button("Submit Exam"):
                        st.session_state.submitted = True
                except Exception as e:
                    st.error(f"Error displaying exam content: {e}")
                    st.text(st.session_state.exam_content)  # Display raw content for debugging

        if st.session_state.get("submitted"):
            st.success("Test successfully submitted!")
    else:
        st.error("Failed to fetch job descriptions from the database.")
