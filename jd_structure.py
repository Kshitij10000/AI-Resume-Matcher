from typing import List, Dict, Optional
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback

load_dotenv()


class JdExperience(BaseModel):
    skill: Optional[str] = Field(default=None, description="Specific skill or technology mentioned in the experience requirement")
    designation: Optional[str] = Field(default=None, description="Role designation associated with the experience requirement")
    years: Optional[str] = Field(default=None, description="Number of years of experience required for the skill")

class JdStructured(BaseModel):
    role: Optional[str] = Field(default=None, description="Role of the job description")
    location: str = Field(default="Location not specified", description="Geographical location of the job or 'Location not specified'")
    education: Optional[str] = Field(default=None, description="Education qualifications in the format: 'Degree, Major, Year of Graduation, University/College Percentage'")
    skills_required: List[str] = Field(default_factory=list, description="Primary skills required for the role, separated and without duplicates")
    skills_preferable: List[str] = Field(default_factory=list, description="Secondary skills for the role, separated and without duplicates")
    experience_requirements: List[JdExperience] = Field(default_factory=list, description="Experience level required for each skill")
    other_requirements: List[str] = Field(default_factory=list, description="Other skills required for the role, such as interpersonal abilities, communication, teamwork")
    description: str = Field(default="Description not provided", description="Description of the role mentioned in the job description or 'Description not provided'")
    responsibilities: str = Field(default="Responsibilities not provided", description="Responsibilities associated with the role or 'Responsibilities not provided'")



# Define the prompt template for job description processing
jd_template = """

Background:

You are a seasoned and accomplished recruiter with extensive experience spanning over a decade,
focusing on both technical and non-technical roles as specified by the job type: {job_type}. recruitment across diverse industries.
Armed with a profound understanding of human resources and talent acquisition,
you have honed your skills in deciphering intricate job descriptions and aligning them with the organization's strategic goals.

Objective:

Your main goal is to review the job description thoroughly and identify key skills, experience, and qualifications needed for the position.
Focus on extracting specific details from each section of the job description to understand the core requirements.
With this information, you'll refine and structure the job description to clearly outline the job's expectations in a user-friendly format.

Concise Responses:

Respond directly to each question using information strictly from the provided job description.
Ensure all answers are concise and based solely on the content provided in the documents.

Instructions:

1. Job Role and Technical/Non-Technical Classification:

- Understand the job title and description to determine the job role and whether it's technical or non-technical.
  You can use pre-defined lists of technical keywords or leverage sentiment analysis techniques.

2. Location Extraction:

- Extract the relevant location given in the job description for location of work.

3. Education Extraction:

- Extract the education details from the job description concisely and efficiently.

4. Skills Extraction:

    Identify Essential Skills:
    Start by identifying all crucial skills from the job description, paying close attention to include common abbreviations and variations (e.g., "Machine Learning" as "ML", "JavaScript" as "JS") to ensure these are specifically recognized during the extraction process.

    Comprehensive Document Analysis: 
    Analyze the entire resume document thoroughly. This includes the skills section, work experience, projects, and any other relevant areas where skills might be mentioned or implied.

    Skill Normalization:
    Normalize the identified skills to maintain consistency and avoid duplicates. This includes converting all skill mentions to a standard format, resolving common abbreviations to their full forms, and separating compound skills into individual components.

    Duplicate Removal: 
    Implement mechanisms to ensure that each skill is recorded only once, maintaining a unique set of skills.

    Implementation Flexibility:
    The extraction process is not limited to predefined functions or methods. 
    Instead, leverage the best available techniques, which may include advanced NLP tools, machine learning models for text classification, regular expressions, and semantic analysis to achieve the most accurate and comprehensive results.
    The method chosen should dynamically adapt to the specificities of the document and the job description to maximize accuracy and relevance of the skills extracted.

    Final Output:
    Compile a finalized list of unique skills, ensuring that it includes all relevant technical and soft skills as required by the job description. 
    This list should be exhaustive and reflect a precise mapping of the candidate's capabilities to the job requirements.

    Recheck Point:
    Quality Assurance Review: After compiling the initial list of skills, conduct a thorough review to recheck each skill for accuracy and completeness. 
    This review should:
    Re-examine the skill list to identify any missed skills, incorrect categorizations, or redundancies.
    Confirm that all common abbreviations and variations have been captured and correctly normalized.
    Ensure no duplicates exist, and that the list reflects a complete and accurate representation of the required skills.

    Adjustment and Immediate Updates:
    Immediate List Update: If the recheck identifies missing skills, incorrect entries, or any need for re-categorization, update the skill list immediately. 
    This includes adding missed skills, correcting any mislabeled or improperly formatted entries, and removing duplicates.

    Process Enhancement: Based on the outcomes of the recheck, refine the skill extraction process to prevent similar issues in future cycles. 
    This may involve adjusting the parameters used in NLP tools, updating regular expressions, or enhancing the list of recognized abbreviations and variations.

5. Skill Filtering based on Role:

    Role Classification: Determine if the job is technical or non-technical based on the job description to guide the filtering process.

    Skill Prioritization:

    Technical Roles: Prioritize technical skills from the all_skills list, such as programming languages and engineering methodologies, using a predefined list to ensure consistency.

    Non-Technical Roles: Focus on soft skills and other relevant non-technical skills from all_skills, like interpersonal and management skills, guided by a predefined list.

    Organized Skill Documentation:

    Document the relevant filtered skills under 'Skills Required' tailored to the role classification.

    Maintain repeatability and consistency in skill selection to ensure reliability across similar job designations.

    Classify essential skills as 'Skills Required' and additional, beneficial technical skills as 'Skills Preferable', depending on their necessity and relevance to the role type..

6. Experience Extraction:

- Look for keywords or phrases related to experience requirements (e.g., "3 years of experience", "Senior", "Entry-level").

- Extract the experience level and duration (if specified) and store them in the `experience_requirements` list.

7. Job Description and Responsibility Extraction:

- Identify sections in the job description labeled "Job Description" or "Responsibilities" (or similar variations).

- Extract the text content from these sections and store them in the `description` and `responsibilities` fields, respectively.

Note: Give output in JSON format and Propercase.

Specific Areas of Analysis:
-----------------
You should remove the duplicate skills , you are adding same skills again. 
you should be strict with removing duplicate skills

Make sure to follow each step mentioned in Skills Extraction and Skill Filtering based on Role section.

%%JOB_DESCRIPTION:

{job_description}

%%OUTPUT_INSTRUCTIONS:

{format_instructions}

%%ANSWER:

"""

format_instructions = """

Please populate the following data structure with the extracted information:

{

"role": "{role}",
"location": "{location}",
"education": "{education}",
"skills_required": [{% for skill in skills_required %}"{{ skill }}"{% if not loop.last %},{% endif %}{% endfor %}],
"skills_preferable": [{% for skill in skills_preferable %}"{{ skill }}"{% if not loop.last %},{% endif %}{% endfor %}],
"experience_requirements": [
    {% for exp in experience_requirements %}
    {
        "skill": "{{ exp.skill }}",
        "designation": "{{ exp.designation }}",
        "years": "{{ exp.years }}"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
],
"other_requirements": [{% for requirement in other_requirements %}"{{ requirement }}"{% if not loop.last %},{% endif %}{% endfor %}],
"description": "{{ job_description }}",
"responsibilities": "{{ responsibilities }}"
}
"""

# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=JdStructured)

prompt = PromptTemplate(
    template=jd_template,
    input_variables=["job_description"],
    partial_variables={
        "format_instructions": format_instructions},
)

def get_jd_structured(jd: str, job_type: str) -> Dict:
    with get_openai_callback() as jc:
        model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")
        chain = prompt | model | parser
        structured_jd = chain.invoke({"job_description": jd, "job_type": job_type})
        
    return structured_jd, jc.total_cost