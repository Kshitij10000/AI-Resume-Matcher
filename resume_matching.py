import os
from typing import List, Optional

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class EducationInfo(BaseModel):
    degree: Optional[str] = Field(
        description="Degree pursued by the candidate (e.g., Bachelor of Science in Computer Science)."
    )
    completion_year: Optional[str] = Field(
        description="Year of degree completion (if available)."
    )
    percentage: Optional[str] = Field(
        description="Percentage obtained in the degree program (if available)."
    )


class SkillInfo(BaseModel):
    name: Optional[str] = Field(
        description="Name of the skill."
    )
    category: Optional[str] = Field(
        description="Category of the skill (e.g., Programming Language, Tool)."
    )


class ExperienceInfo(BaseModel):
    organization: Optional[str] = Field(
        description="Name of the company."
    )
    title: Optional[str] = Field(
        description="Title of the job role."
    )
    years: Optional[str] = Field(
        description="Years of experience in the job role.If not found return NULL"
    )


class ResumeMatchingInfo(BaseModel):
    role: Optional[str] = Field(
        description="Role specified in the job description."
    )
    candidate: Optional[str] = Field(
        description="Name of the candidate from the resume."
    )
    location: Optional[str] = Field(
        description="Location specified in the job description (if applicable)."
    )
    education: Optional[List[EducationInfo]] = Field(
        default=None,
        description="List of education qualifications."
    )
    similar_skills: Optional[List[SkillInfo]] = Field(
        default=None,
        description="List of skills from the resume that match the required skills in the job description."
    )
    missing_skills: Optional[List[SkillInfo]] = Field(
        default=None,
        description="List of skills from the job description that are missing in the candidate's resume."
    )
    preferable_skills: Optional[List[SkillInfo]] = Field(
        default=None,
        description="List of skills from the resume that match the preferable skills in the job description."
    )
    experiences: Optional[List[ExperienceInfo]] = Field(
        default=None,
        description="List of relevant job role experiences listed in the resume that align with the job description."
    )
    validation: Optional[str] = Field(
        description="validation on score. total breakdown of point allocationa and sum of scoring."
    )
    score: Optional[str] = Field(
        description="Matching score indicating the relevance and match between the resume and job description (0% to 100%)."
    )
   
    recommendation: Optional[str] = Field(
        description="Hiring recommendation based on the analysis of the resume and job description."
    )


class ListResumeMatchingInfo(BaseModel):
    jds_report: List[ResumeMatchingInfo] = Field(
        description="Resume matching information for each job description."
    )


# Define the updated prompt template
resume_template = """
Background:
You are an experienced recruiter specializing in technical roles with a keen eye for skill alignment between job descriptions and candidate resumes.  
With years of experience, you excel in identifying the right candidates for organizations, fulfilling their demands.  
You are adept at reading resumes and job descriptions,  
having previously worked in a large multinational corporation where you extracted skills and experience from resumes to match with job descriptions and developed a scoring system (0 to 100) for rating candidates.  
Your expertise lies in crafting meaningful and perfect recommendation summaries for candidate hiring. 

Objective:
Your objective is to meticulously compare the skills listed in the job description with those found in the candidate's resume,  
categorizing them into "similar_skills" and "missing_skills" based on similar matches.  
Find relevant experience according to job requirements and excel in scoring resumes by analyzing job descriptions and resumes.  
You will provide a recommendation summary for any candidate, which is precise. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

Instructions:
//////////////
%%Candidate Name:
Extract the candidate's name from the resume.

%%Role Identification:
Identify the specific role from the job description and document it under the "role" section in the report.

%%Education Details:
Extract candidate education information from the resume.

%%Skills Matching:
////////////// 

Skills Matching Instructions: 

Understand the Job Role: 

Review the JOB_DESCRIPTIONS to clearly understand the role and its specific skill requirements. 
Only consider skills directly related to this job role for matching. 

Skill Matching Process: 

Direct Skill Comparison: 

Compare the normalized and pre-extracted skills from the resume with the "skills_required" listed in the JOB_DESCRIPTIONS. 
Use both exact and semantic matching techniques to assess equivalency, accounting for variations and synonyms previously normalized (e.g., "ML" for "Machine Learning"). 

Categorization of Skills: 

Similar Skills: If a skill from "skills_required" directly matches or is semantically equivalent to any skill on the extracted resume list, categorize this under "similar_skills". 
Missing Skills: If a skill from "skills_required" is absent from the resume's skill list, categorize it under "missing_skills". 

Ensure Comprehensive Coverage: 

Make sure all skills listed in "skills_required" are evaluated against the resume's skill set to maintain completeness. 

Recheck Mechanism: 

(a) Accuracy Check: After the initial categorization, review both "similar_skills" and "missing_skills" to ensure each skill from "skills_required" has been accurately categorized. 
Check for any discrepancies or misclassifications. 

(b) Completeness Check: Verify that the total count of "similar_skills" and "missing_skills" matches the count in "skills_required". 
If there are any inconsistencies or if any skill is unaccounted for, repeat the comparison and categorization process until accuracy and completeness are achieved. 

Important Notes: 

Adhere strictly to the skills listed in "skills_required" of the JOB_DESCRIPTIONS when comparing with the extracted resume skills. 

The sum of "similar_skills" and "missing_skills" should precisely match the number of skills specified in "skills_required". 

Example for Context: 

If "skills_required" lists a total of 24 skills and the resume's extracted skills match or are equivalent to 16 of these, categorize those 16 under "similar_skills". 
The remaining 8, not found on the resume's list, should be categorized under "missing_skills". 
Ensure the sum of both categories equals 24, reflecting the total in "skills_required". 

%%Preferable Skills Identification:

Assess and match the candidate's resume for listed and autonomously identified relevant skills for the job role. 

Direct Comparison: Match skills from the candidate's resume with "skills_preferable" from the JOB_DESCRIPTIONS. 

Semantic Analysis: Autonomously evaluate additional skills on the resume to determine their relevance to the role based on job context. 

Documentation: 

Listed Matches: Record directly matched skills in the "similar_preferred_skills" section. 

Additional Skills: Include relevant skills identified through semantic analysis that are beneficial for the role. 

Recheck Mechanism: 
Verify the accuracy of all matched and autonomously identified skills, making adjustments as necessary. 

%%Experience Matching:
Compare required experience with resume experience in a properly formatted manner. 
Use standard capitalization (no all lower or upper case): start sentences with a capital letter, capitalize proper nouns such as company names and job titles, 
and maintain a standard text structure. Extract relevant experience from JOB_DESCRIPTIONS and prioritize it in the response. 
If experience matches, list it first followed by other experiences. Consider elements like company name, job title, and years of experience for a thorough comparison.


%%Matching Score Calculation:

Calculate a matching score based on the alignment of skills and experience between a candidate's resume and a job description. 
Follow precise scoring instructions outlined below to ensure accurate evaluation.

**Categories and Point Allocation:**

    1. **Required Skills Assessment:**
    - For each skill in the candidate's profile:
        Determine the relevance to the job role:
          If the skill is highly relevant to the job role, assign 4 points.
          If the skill is moderately relevant but not directly related to the job role, assign 2 points.
    - Sum up the points from all relevant skills to calculate the total score for similar skills assessment.
    - Maximum Cap: Ensure that the total points awarded for similar skills assessment do not exceed 44 points. if score goes beyond 44, round of to 44.

    2. **Preferable Skills Assessment:**
    - For each skill in the candidate's preferable skills list:
        - Assign 1 point if the skill is present.
    - Sum up the points from all present preferable skills to calculate the total score for preferable skills assessment.
    - Maximum Cap: Ensure that the total points awarded for preferable skills assessment do not exceed 6 points. if socre goes beyond 6, round of to 6.

    **Example:**
      Candidate's Skills:Required Skills: DevOps, HTML, Python, Machine Learning, Deep Learning
      Preferable Skills: R, Data Wrangling
      Job Role: Data Scientist
      Skill Relevance Assessment:
      Highly Relevant Skills (4 points each): Python, Machine Learning, Deep Learning
      Total: 3 skills * 4 points/skill = 12 points
      Moderately Relevant Skills (2 points each): HTML , DevOps
      Total: 2 skills * 2 points/skill = 4 points
      Total Points for Required Skills Assessment: 16 points
      Preferable Skills Assessment:
      Present Preferable Skills (1 point each): R, Data Wrangling
      Total: 2 skills * 1 point/skill = 2 points
      Total Points for Preferable Skills Assessment: 2 points
      Total Matching Score:
      Total Score = Total Points from Required Skills + Total Points from Preferable Skills
      Total Score = 16 (Required skills) + 2 (preferable skills) = 18 points
      so now we got 18 out 50.

2. **Experience Alignment:** 
    Undertsand the Experience requirements of Job Description and check the same Experience in Resumes: 
    Roles with Specified Limited Experience (e.g., "1-2 years required"): 
    Award 25 points for candidates who meet the exact experience requirement. 
    This emphasizes roles targeting those with specific limited experience. 
    Roles with No Upper Experience Limit or targeting more experienced candidates: 
    Base Points: Award 25 points for meeting the minimum required experience as stated in the job description. 
    Additional Experience: Award 2 point for each additional year of relevant experience beyond the minimum, with a maximum cap of 20 additional points, ensuring the total for this category does not exceed 50 points. 
    Roles for Freshers or Very Low Experience Requirements: 
    Meeting Minimum Requirement: If the role explicitly targets freshers, award 25 points for up to 1 year of experience or no experience as suited for the role. 
    **Maximum Cap:** 
      Ensure that the total points awarded for experience in any scenario do not exceed 50 points. 
      This cap prevents the experience category from disproportionately influencing the overall score, maintaining balance with other evaluation criteria. 
    **Example:** 
      For a role requiring at least 3 years of experience: 
      lets consider a scenario were a candidate have 8 years of experience.
      Base Points: 25 points for meeting the 3-year minimum. 
      Additional Experience: 2 point for each year beyond the minimum, up to a total of 20 additional points, ensuring the total for this category is capped at 50 points. 
      Result: first 3 years 25 points, 4th year 2 points, 5th year 2 points, 6th year 2 points, 7th year 2 points, 8th year 2 points, total= 35 points.

**Process:**
- Review the candidate's resume and job description thoroughly.
- Understand the job role to determine skill relevance.
- For each category (Skill Relevance and Experience Alignment), assign points based on the criteria met.
- Sum up the points from all categories to calculate the overall matching score, ranging from 0 to 100.
- Ensure a comprehensive evaluation that accurately reflects the candidate's qualifications.

**Validation with Calculation Process:**
- Utilize the above categories and scoring method to assign points accurately.
- Follow the calculation process as outlined to derive the "Matching Score."
- Document the process for validation purposes.

%%Hiring Recommendation: 

Provide a detailed hiring summary based on the comprehensive analysis of the candidate's RESUME and JOB_DESCRIPTIONS.  
Evaluate the candidate's qualifications, experience, and skills to provide a nuanced recommendation. 
Format the output as a review on the candidate's suitability for the role, considering their strengths, weaknesses, and potential areas for development.  
Highlight whether the candidate is a strong fit for the position, requires additional training or support to excel, or may not be recommended for the role. 

 
Consider the following aspects in your summary: 
- Evaluate the candidate's technical skills, aligning them with the job requirements. 
- Assess the candidate's professional experience and how it matches the demands of the role. 
- Identify any missing skills or areas where the candidate may need further training or development. 
- Highlight specific strengths or experiences that make the candidate a valuable asset. 
- Provide insights on potential tasks or roles where the candidate's abilities can be effectively utilized, even if not for the immediate position. 

The recommendation should be concise, precise, and based on a thorough analysis of the candidate's profile in relation to the job expectations. 
Give at most 6 lines of recommendation. 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

Specific Areas of Analysis: 

You are analyzing each skill from the job description against the skills listed in the resume to identify exact matches (similar_skills) and missing skills (missing_skills). 
The total number of "similar_skills" and "missing_skills" should match the number of skills specified in the skills_required section of the job description. 
Specific Areas of Analysis:
Compare each job skill against resume skills to identify "similar_skills" and "missing_skills".

%%RESUME:
{resume}

%%JOB_DESCRIPTIONS:
{job_description}

%%OUTPUT_INSTRUCTIONS:
{format_instructions}

%%ANSWER:
"""


format_instructions = """
Please populate the following data structure with the extracted information:
{
  "candidate_name": "Candidate's Name",
  "role": "Role identified from the job description",
  "education": [
    {
      "degree": "Degree name",
      "completion_year": "Year of completion (if available)",
      "marks": "Marks obtained (if available)"
    },
    {
      "degree": "Another degree name",
      "completion_year": "Year of completion (if available)",
      "marks": "Marks obtained (if available)"
    },
    ...
  ],
  "skills": {
    "similar_skills": [
      "Skill 1",
      "Skill 2",
      ...
    ],
    "missing_skills": [
      "Missing Skill 1",
      "Missing Skill 2",
      ...
    ],
    "preferable_skills": [
      "Preferable Skill 1",
      "Preferable Skill 2",
      ...
    ]
  },
  "experience": [
    {
      "organization": "Company name",
      "title": "Job Title",
      "years": "Years of experience"
    },
    {
      "organization": "Another Company name",
      "title": "Another Job Title",
      "years": "Years of experience"
    },
    ...
  ],
  "validation": "Give a validation on score , tell calculated method to get the score validation",
  "score": "Matching score percentage (0% to 100%)",
  "recommendation": "Hiring recommendation with reasons"
}
"""

# # Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=ListResumeMatchingInfo)

prompt = PromptTemplate(
    template=resume_template,
    input_variables=["job_descriptions", "resume"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()},
)


import asyncio
from typing import List, Dict, Tuple


async def match_resumes_with_jd(resumes: Dict[str, str], job_description: str) -> Tuple[Dict[str, str], float]:
    
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")
    chain = prompt | model | parser
    report = {}
    results = []
    
    with get_openai_callback() as cb:
        # Create input data preserving both filename and content
        inputs = [{"job_description": job_description, "resume": content, "filename": filename} for filename, content in resumes.items()]
        matched_resumes = await chain.abatch(inputs)
        
        # Assume that 'matched_resumes' returns a list of structured responses corresponding to the inputs
        for input_data, resume_response in zip(inputs, matched_resumes):
            filename = input_data["filename"]
            results.append((filename, resume_response))

        total_cost = cb.total_cost  # Calculate total cost after all resumes are processed

        # Form the report based on filenames
        for filename, response in results:
            # Assuming 'response' has an attribute 'jds_report' that can be serialized as a dictionary
            report[filename] = response.jds_report[0].dict() if response.jds_report else "No data"

    return report, total_cost

# async def process_resume_jd_match_async(model, chain, resume_content: str, job_description: str, idx: int):
#     response = chain.invoke({"job_description": job_description, "resume": resume_content})
#     return f"resume_{idx+1}", response
