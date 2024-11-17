from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel 
from dotenv import load_dotenv
from typing import List, Dict, Optional
from langchain_community.callbacks.manager import get_openai_callback

load_dotenv()

class ProfessionalExperience(BaseModel):
    company_name: Optional[str] = None
    designation: Optional[str] = None
    duration: Optional[str] = None
    key_skills: Optional[List[str]] = []
    roles_and_responsibilities: Optional[List[str]] = []

class Project(BaseModel):
    project_name: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    environment: Optional[str] = None
    description: Optional[str] = None

class Education(BaseModel):
    degree_name: Optional[str] = None
    degree_specialization: Optional[str] = None
    degree_institution: Optional[str] = None
    passing_year: Optional[str] = None

class Certification(BaseModel):
    certificate_name: Optional[str] = None
    certificate_issuing_authority: Optional[str] = None  
    passing_year: Optional[str] = None  

class StructuredResume(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None  
    technical_skills: Optional[List[str]] = []
    soft_skills: Optional[List[str]] = []
    professional_experience: Optional[List[ProfessionalExperience]] = None
    projects: Optional[List[Project]] = None
    education: Optional[List[Education]] = None
    certifications: Optional[List[Certification]] = None

resume_template = """ 

 

Background: 

 

You are a seasoned and accomplished recruiter with extensive experience spanning over a decade,  

specializing in both technical and non-technical recruitment across diverse industries.  

Armed with a profound understanding of human resources and talent acquisition,  

you have honed your skills in deciphering intricate resumes and aligning them with the organization's strategic goals. 

 

Objective: 

 

Your main goal is to review the resumes thoroughly and identify key features like name, technical_skills,projects, professional_experience, education and certificates from Resume.  

Focus on extracting specific details from each section of the Resume to understand the core requirements.  

With this information, you'll refine and structure the Resume to clearly outline the Resume in a user-friendly format. 

 

Concise Responses: 

 

Respond directly to each question using information strictly from the provided Resume. 

Ensure all answers are concise and based solely on the content provided in the Resume. 

give all outputs in propercase. 

 

Instructions: 

1. Extract the candidate's name and address from the resume (if mentioned). 

2. Skills Extraction -  

    Identify Essential Skills: Begin by identifying all key skills listed within the resume, noting common abbreviations and variations (e.g., "Machine Learning" as "ML", "JavaScript" as "JS"). This ensures a thorough recognition of skills during the extraction process. 

    Comprehensive Document Analysis: Conduct an exhaustive analysis of the entire resume. This includes the skills section, work experience, projects, and any other segments where skills might be explicitly or implicitly mentioned. 

    Skill Normalization: Standardize the identified skills to maintain consistency and reduce redundancy: 

    Convert all skill mentions to a unified format. 

    Resolve common abbreviations to their full terms, and separate compound skills into individual elements. 

    Duplicate Removal: Implement strategies to ensure that each skill is noted only once in the list, thus maintaining a unique set of skills. 

    Implementation Flexibility: 

    Do not restrict the process to predefined methods.
    Employ the best available techniques which could include advanced NLP tools, machine learning models for text analysis, regular expressions, and semantic analysis to deliver the most accurate and inclusive results. 
    Adapt dynamically to the specifics of the resume content and the nuanced requirements of the skill set being analyzed. 

    
    Final Output: 

    Compile an exhaustive list of unique skills that includes all pertinent technical and soft skills depicted in the resume. 
    This list should comprehensively reflect the candidate's capabilities. 


    Recheck Point: 

    Quality Assurance Review: After the initial skill list compilation, perform a detailed review to verify each skill for accuracy and completeness: 
    Inspect the skill list to detect any overlooked skills, incorrect categorizations, or redundancies. 
    Confirm that all variations and abbreviations have been accurately captured and standardized. 
    Ensure no duplicates are present and that the list accurately represents the candidate's skills. 

    
    Adjustment and Immediate Updates: 

    Immediate List Update: If the recheck identifies any missing skills, incorrect entries, or needs for re-categorization, update the skill list promptly.
    This involves adding missing skills, correcting any mislabeled or incorrectly formatted entries, and removing duplicates. 

    Process Enhancement: Refine the skill extraction process based on the outcomes of the recheck.
    This could include adjusting NLP tool parameters, updating regular expressions, or improving the list of recognized abbreviations and variations to prevent similar issues in future extractions. 

    

3. Document the candidate's professional experience, including: 

   - Company name 
   - Designation (job title) 
   - Duration of employment (if mentioned) 
   - Key technical skills used in each experience (use the extracted normalized skills list) 
   - Roles and responsibilities (if mentioned in bullet points or descriptions) 

 

4. Capture the project details, including: 

   - Project name 
   - Role in the project 
   - Duration (if mentioned) 
   - Development environment (if mentioned) 
   - Brief description of the project 

 

5. Extract the candidate's educational qualifications, including: 

   - Degree name 
   - Specialization (if mentioned) 
   - Institution name 
   - Passing year 

 

6. Identify any certifications obtained by the candidate, including: 

   - Certificate name 
   - Issuing authority (if mentioned) 
   - Passing year (if mentioned) 

 

7. Provide the output in the following JSON format, ensuring that all the fields are populated with the extracted information or "null" if the information is not available: 

 
**Note:** Give output in JSON format and Aslo keep output in proper format. 

%%Resume: 
{resume} 

%%OUTPUT_INSTRUCTIONS: 
{format_instructions} 

%%ANSWER: 

""" 

 

# Updated format instructions 

format_instructions = """ 

Please populate the following data structure with the extracted information: 

{ 

  "name": "", 

  "address": "",   

  "technical_skills": [ 
    "" 
  ], 

  "professional_experience": [ 
    { 
      "company_name": "", 
      "designation": "", 
      "duration": "", 
      "key_technical_skills": [ 
        "" 
      ], 
      "roles_and_responsibilities": [ 
        "", 
        "" 
      ] 
    } 
  ], 

  "projects": [ 
    { 
      "project_name": "", 
      "role": "", 
      "duration": "", 
      "environment": "", 
      "description": "" 
    } 
  ], 

  "education": [ 
    { 
      "degree_name": "", 
      "degree_specialization": "", 
      "degree_institution": "", 
      "passing_year": "" 
    } 
  ], 

  "certifications": [ 
    { 
      "certificate_name": "", 
      "certificate_issuing_authority": "",  
      "passing_year": ""                 
    } 
  ] 

} 

""" 
import asyncio
# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=StructuredResume)

prompt =  PromptTemplate(
    template=resume_template,
    input_variables=["resume"],  # Correct input variables
    partial_variables={"format_instructions": format_instructions},
)





# Async function to structure resumes
async def structure_resumes(resume_docs: Dict[str, str]) -> Dict[str, StructuredResume]:
    structured_resumes = {}
    with get_openai_callback() as rc:
        model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")
        chain = prompt | model | parser
        
        # Create a list of dictionaries as needed for `abatch`
        formatted_inputs = [{"resume": content.page_content} for filename, content in resume_docs.items()]
        
        # Processing each resume with the chain
        formatted_resumes = await chain.abatch(formatted_inputs)
        
        # Mapping formatted resumes back to their filenames
        for filename, structured_resume in zip(resume_docs.keys(), formatted_resumes):
            structured_resumes[filename] = structured_resume

    return structured_resumes, rc.total_cost

# async def process_resume_async(model, parser, resume_text: str, idx: int) -> Dict[str, StructuredResume]:
#     chain = prompt | model | parser
#     structured_resume = await chain.ainvoke({"resume": resume_text})
#     return f"resume_{idx+1}", structured_resume