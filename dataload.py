import os
from io import BytesIO
import dataclean
import utils
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import (Docx2txtLoader,PyPDFLoader)
from langchain_community.document_loaders.unstructured import \
    UnstructuredFileLoader
import json

def extract_text(path):
    if not path:
        return
    extension = os.path.splitext(path)[1]
    if extension == ".docx":
        docs = Docx2txtLoader(path).load()  # Load .docx files as StructuredDocuments
    elif extension == ".pdf":
        docs = PyPDFLoader(path).load()  # Load .pdf files as StructuredDocuments
    else:
        docs = UnstructuredFileLoader(path, mode="single").load()
    page_content = "\n".join([doc.page_content for doc in docs])
    return Document(page_content=page_content, metadata=docs[0].metadata)

def process_text_resumes(resume):
    with BytesIO(resume.getvalue()) as uploaded_resume_zip:
        resume_folder_name = utils.get_clean_file_name(resume.name)
        folder_path = f"./data/{resume_folder_name}"
        resume_raw_path = f"{folder_path}/resume/raw/"
        utils.process_zip_file(uploaded_resume_zip, resume_raw_path)
        
        resumes_docs = {}  # Using a dictionary to store documents with filenames as keys

        for file_name in os.listdir(resume_raw_path):
            file_path = os.path.join(resume_raw_path, file_name)
            text = extract_text(file_path)
           # text.page_content = dataclean.clean_resume(text.page_content)
           # text.page_content = dataclean.remove_stopwords(text.page_content)
            resumes_docs[file_name] = text  # Store the processed Document object with the filename as key

        return resumes_docs, folder_path , resume_raw_path

def serialize_structured_resume(resume):
    """Converts a StructuredResume instance into a dictionary for JSON serialization."""
    return {
        'name': resume.name,
        'email': resume.email,
        'phone': resume.phone,
        'address': resume.address,
        'technical_skills': resume.technical_skills,
        'soft_skills': resume.soft_skills,
        'professional_experience': [
            {
                'company_name': exp.company_name,
                'designation': exp.designation,
                'duration': exp.duration,
                'key_skills': exp.key_skills,
                'roles_and_responsibilities': exp.roles_and_responsibilities
            } for exp in (resume.professional_experience or [])
        ],
        'projects': [
            {
                'project_name': proj.project_name,
                'role': proj.role,
                'duration': proj.duration,
                'environment': proj.environment,
                'description': proj.description
            } for proj in (resume.projects or [])
        ],
        'education': [
            {
                'degree_name': edu.degree_name,
                'degree_specialization': edu.degree_specialization,
                'degree_institution': edu.degree_institution,
                'passing_year': edu.passing_year
            } for edu in (resume.education or [])
        ],
        'certifications': [
            {
                'certificate_name': cert.certificate_name,
                'certificate_issuing_authority': cert.certificate_issuing_authority,
                'passing_year': cert.passing_year
            } for cert in (resume.certifications or [])
        ]
    }


def save_structured_resumes_as_json(structured_resumes, folder_path):
    """Saves structured resume data as JSON files in the specified directory."""
    structured_path = os.path.join(folder_path, 'resume', 'structured')
    os.makedirs(structured_path, exist_ok=True)
    for file_name, resume in structured_resumes.items():
        resume_data = serialize_structured_resume(resume)  # Serialize the resume to a dictionary
        json_filename = f"{file_name}.json"
        json_filepath = os.path.join(structured_path, json_filename)
        with open(json_filepath, 'w') as json_file:
            json.dump(resume_data, json_file, indent=4)  # Save the dictionary as JSON
    return structured_path


def save_and_get_text_jd(jd, folder_path):

    jd_raw_path = f"{folder_path}/jd/raw"
    os.makedirs(jd_raw_path, exist_ok=True)
    jd_raw_path = f"{jd_raw_path}/{jd.name}"
    with open(jd_raw_path, "w+b") as uploaded_jd:
        uploaded_jd.write(jd.getvalue())
    # st.write(uploaded_jd.name)
    docs = extract_text(jd_raw_path)
    # docs.page_content = dataclean.remove_stopwords(text=docs.page_content)
    return docs



def save_jd(jd_json, name, folder_path):
    if not jd_json:
        return  # Do nothing if JD JSON is not provided

    jd_path = os.path.join(folder_path, "jd", "structured")
    os.makedirs(jd_path, exist_ok=True)

    # Sanitize the role name to remove invalid characters
    sanitized_name = name.replace('/', '_')  #
    # Save the structured job description in JSON format within the "jd" folder
    jd_raw_path = os.path.join(jd_path, f"{sanitized_name}.json")
    with open(jd_raw_path, "w+t") as structured_jd:
        structured_jd.write(jd_json)


