import mysql.connector
import json
import os 
from datetime import datetime

db_config = {
    'user': 'admin',
    'password': 'WHqqCKcpOa6PGQwKVIz3',
    'host': 'cre-database.clskaom22sd7.us-east-1.rds.amazonaws.com',
    'port': 3306,
    'database': 'cre'
}



def insert_error_log(method_name, error_desc):
    """Function to log errors into the database."""
    error_insert_query = """
    INSERT INTO error_info (method_name, error_desc, created_at)
    VALUES (%s, %s, NOW())
    """
    error_data_tuple = (method_name, error_desc)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(error_insert_query, error_data_tuple)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Failed to log error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def check_user_in_database(username, password):
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor()
            # Corrected the SQL query to use proper SQL syntax for WHERE conditions
            cursor.execute("SELECT 1 FROM login_users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return bool(result)  # Returns True if user exists with the given username and password, False otherwise
    except mysql.connector.Error as err:
        insert_error_log("error is occurring while checking user credentials", str(err))
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()


def user_signup_input(name, username, email, password):
    """Function to save user data into the database and handle exceptions."""
    userdata_insert_query = """
    INSERT INTO login_users (name, username, email, password, current_datetime, active)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    current_datetime = datetime.now()  # Get current datetime

    user_data_tuple = (name, username, email, password, current_datetime, 1)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(userdata_insert_query, user_data_tuple)
        conn.commit()
        return True  # Return True when signup is successful
    except mysql.connector.Error as err:
        if 'duplicate entry' in str(err).lower():  # Adjust the error check as per your DBMS
            return False  # Return False if user already exists
        else:
            raise  # Re-raise the exception for any other errors
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def check_job_role_in_database(job_role):
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor()
            # Ensure the query checks against `jd_role` not `jd_id`
            cursor.execute("SELECT 1 FROM jd_info WHERE jd_role = %s", (job_role,))
            result = cursor.fetchone()
            return bool(result)  # Returns True if a job role exists, False otherwise
    except mysql.connector.Error as err:
        insert_error_log("error is occuring while checking job role", str(err))
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

def fetch_all_recent_job_roles():
    query = """
    SELECT jd_id, jd_role, created_at FROM jd_info
    ORDER BY created_at DESC
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        insert_error_log("error occured while fetching job role", str(err))
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_jd_data_into_db(jd_data, process_time, cost, jd_role, sever_name, job_type):
    jd_json = jd_data

    data = json.loads(jd_json)

    server_file_name = sever_name 
    
    if 'experience_requirements' in data and data['experience_requirements']:
        formatted_experience = '; '.join([
            f"{exp['designation']} in {exp['skill']} for {exp['years']} years"
            for exp in data['experience_requirements']
        ])
    else:
        formatted_experience = None
        

    # Check for empty lists or missing keys and set to None if so
    skills_required = ', '.join(data.get('skills_required', [])) if data.get('skills_required', []) else None
    skills_preferable = ', '.join(data.get('skills_preferable', [])) if data.get('skills_preferable', []) else None
    other_requirements = ', '.join(data.get('other_requirements', [])) if data.get('other_requirements', []) else None
    location = data.get('location', None)
    if location == "":
        location = None
    # SQL statement for inserting data
    insert_query = """
    INSERT INTO jd_info (job_type, jd_role, location, education, skills_required, skills_preferable, experience_requirements, other_requirements, description, responsibilities, process_time, cost, server_file_name, active, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """

    # Prepare the data tuple
    data_tuple = (
        job_type,
        jd_role,
        location,
        data.get('education', None),
        skills_required,
        skills_preferable,
        formatted_experience,
        other_requirements,
        data.get('description', None),
        data.get('responsibilities', None),
        process_time,  # Real value for process_time
        cost,          # Real value for cost
        server_file_name,
        1,  # Example value for active (1 means active)
    )

    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(insert_query, data_tuple)
        conn.commit()
        jd_id = cursor.lastrowid 
         # Retrieve the last inserted id
        return jd_id

    except mysql.connector.Error as err:
        insert_error_log("Error occured while inserting \"Jd_info\" data", str(err))
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            





def insert_resume_data_into_db( data, fk_jd_id, report_data, file_path):
    """Insert resume data into the database."""
    try:
        # Open database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Preparing the data
        technical_skills_str = ', '.join(data['technical_skills']) if 'technical_skills' in data else None
        soft_skills_str = ', '.join(data['soft_skills']) if 'soft_skills' in data else None
        similar_skills_str = ', '.join(skill['name'] for skill in report_data['similar_skills']) if 'similar_skills' in report_data else None
        missing_skills_str = ', '.join(skill['name'] for skill in report_data['missing_skills']) if 'missing_skills' in report_data else None
        preferable_skills_str = ', '.join(skill['name'] for skill in report_data['preferable_skills']) if 'preferable_skills' in report_data else None
        required_experience_str = ', '.join(f"{exp['title']} at {exp['organization']} for {exp['years']} years" for exp in report_data['experiences']) if 'experiences' in report_data else None
        file_path = file_path[:-5]  # Assuming you're trimming the file path as needed

        # SQL query
        resume_insert_query = """
        INSERT INTO resume_info (fk_jd_id, cand_name, email, phone, address, role, technical_skills, soft_skills, similar_skills, missing_skills, preferable_skills, required_experience, score, recommendation, file_path, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        resume_data_tuple = (
            fk_jd_id,
            data['name'],
            data['email'],
            data['phone'],
            data['address'],
            report_data.get('role', None),
            technical_skills_str,
            soft_skills_str,
            similar_skills_str,
            missing_skills_str,
            preferable_skills_str,
            required_experience_str,
            report_data.get('score', None),
            report_data.get('recommendation', None),
            file_path,
            1  # Active status
        )

        # Executing the query
        cursor.execute(resume_insert_query, resume_data_tuple)
        conn.commit()
        
        return cursor.lastrowid

    except mysql.connector.Error as err:
        insert_error_log("Error occured while inserting resume_info", str(err))
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            

def insert_professional_experience(cand_id, experiences):
    """Insert professional experiences into the database."""
    try:
        # Open database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        exp_insert_query = """
        INSERT INTO professional_experience_info (fk_cand_id, company_name, designation, duration, key_skills, roles_and_responsibilities, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        for experience in experiences:
            exp_data_tuple = (
                cand_id,
                experience['company_name'],
                experience['designation'],
                experience['duration'],
                ', '.join(experience.get('key_skills', [])),
                ', '.join(experience.get('roles_and_responsibilities', [])),
                1  # Active status
            )
            # Execute insert operation for each experience
            cursor.execute(exp_insert_query, exp_data_tuple)
            conn.commit()

        
        return True

    except mysql.connector.Error as err:
        insert_error_log("Error has occured while inserting professional_experience", str(err))
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
           

def insert_projects(cand_id, projects):
    """Insert project data into the database."""
    try:
        # Open database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        project_insert_query = """
        INSERT INTO projects_info (fk_cand_id, project_name, role, duration, environment, description, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        for project in projects:
            project_tuple = (
                cand_id,
                project['project_name'],
                project['role'],
                project['duration'],
                project['environment'],
                project['description'],
                1  # Active status
            )
            # Execute insert operation for each project
            cursor.execute(project_insert_query, project_tuple)
            conn.commit()

        
        return True

    except mysql.connector.Error as err:
        insert_error_log("Error occured while inserting projects_info", str(err))
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            

def insert_education( cand_id, education_entries):
    """Insert education data into the database."""
    try:
        # Open database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        education_insert_query = """
        INSERT INTO education_info (fk_cand_id, degree_name, degree_specialization, degree_institution, passing_year, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        for education in education_entries:
            education_tuple = (
                cand_id,
                education['degree_name'],
                education['degree_specialization'],
                education['degree_institution'],
                education['passing_year'],
                1  # Active status
            )
            # Execute insert operation for each education entry
            cursor.execute(education_insert_query, education_tuple)
            conn.commit()

        
        return True

    except mysql.connector.Error as err:
        insert_error_log("Error occured while inserting education_info", str(err))
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            

def insert_certifications(cand_id, certifications):
    """Insert certification data into the database."""
    try:
        # Open database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        certification_insert_query = """
        INSERT INTO certification_info (fk_cand_id, certificate_name, certificate_issuing_authority, passing_year, active, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        for certification in certifications:
            certification_tuple = (
                cand_id,
                certification['certificate_name'],
                certification['certificate_issuing_authority'],
                certification['passing_year'],
                1  # Active status
            )
            # Execute insert operation for each certification
            cursor.execute(certification_insert_query, certification_tuple)
            conn.commit()

        
        return True

    except mysql.connector.Error as err:
        insert_error_log("Error occured while inserting certifications_info", str(err))
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            


def process_resume_files(folder_path, jd_id, resumes_final_report, raw_resume_paths):
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)  # Correct usage to form the file path
            raw_resume_path = os.path.join(raw_resume_paths, filename)  # Form the path to the raw resume
            with open(file_path, 'r') as file:
                resume_data = json.load(file)
                resume_id = filename[:-5]  # Assuming the identifier is the filename without '.json'
                report_data = resumes_final_report.get(resume_id)
                if report_data:
                    cand_id = insert_resume_data_into_db(resume_data, jd_id, report_data, raw_resume_path)
                    insert_professional_experience(cand_id, resume_data.get('professional_experience', []))
                    insert_projects(cand_id, resume_data.get('projects', []))
                    insert_education(cand_id, resume_data.get('education', []))
                    insert_certifications(cand_id, resume_data.get('certifications', []))





def get_feedback(feedback,fk_jd_id):
    feedback_query = """
    INSERT INTO feedback_info(fk_jd_id, feedback_text, created_at)
    VALUES(%s, %s, NOW())
    """
    feedback_tuple = (
        fk_jd_id,
        feedback
    )

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(feedback_query, feedback_tuple)
    conn.commit()

    cursor.close()
    conn.close()

def fetch_resumes_by_job_role(job_role):
    # Database connection configuration
   

    # SQL Query
    query = """
    SELECT
        r.cand_name AS Name,
        r.role AS Role,
        r.similar_skills AS SimilarSkills,
        r.missing_skills AS MissingSkills,
        r.required_experience AS RequiredExperience,
        r.recommendation AS Recommendation,
        r.score AS Score,
        r.file_path AS FilePath 
    FROM
        resume_info r
    JOIN
        jd_info j ON r.fk_jd_id = j.jd_id
    WHERE
        j.jd_role = %s
    AND
        r.active = 1
    AND
        j.active = 1;
    """

    try:
        # Establishing the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Using dictionary cursor to return data as dictionaries

        # Executing the query
        cursor.execute(query, (job_role,))  # The job_role is passed as a tuple

        # Fetching all rows from the query result
        result = cursor.fetchall()

        return result

    except mysql.connector.Error as err:
        insert_error_log("error while fetching the data", str(err))
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def fetch_cost_and_process_time_by_job_role(job_role):
    # Database connection configuration

    # SQL Query
    query = """
    SELECT
        j.cost AS Cost,
        j.process_time AS ProcessTime
    FROM
        jd_info j
    WHERE
        j.jd_role = %s
    AND
        j.active = 1;
    """

    try:
        # Establishing the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Using dictionary cursor to return data as dictionaries

        # Executing the query
        cursor.execute(query, (job_role,))  # The job_role is passed as a tuple

        # Fetching all rows from the query result
        result = cursor.fetchall()

        return result

    except mysql.connector.Error as err:
        insert_error_log("error occured while fetching cost and time", str(err))
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_fk_jd_id(jd_role):
    query = """
    SELECT jd_id FROM jd_info WHERE jd_role = %s
    """
    try:
        # Establishing the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()  # Regular cursor since only one value is fetched

        # Executing the query
        cursor.execute(query, (jd_role,))  # Ensuring jd_role is passed as a tuple

        # Fetching the first row from the query result
        result = cursor.fetchone()

        return result[0] if result else None  # Return the jd_id or None if no rows are returned

    except mysql.connector.Error as err:
        insert_error_log("error occured while fetching jd_role", str(err))
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()




def extract_all_data_for_jd_id(jd_id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor()
            # Updated SQL query without feedback info
            query = """
                SELECT
                ri.id, ri.cand_name, ri.email, ri.phone, ri.address, ri.role,
                ri.technical_skills, ri.soft_skills, ri.similar_skills,
                ri.missing_skills, ri.preferable_skills, ri.required_experience,
                ri.score, ri.recommendation, ri.file_path, ri.active, ri.created_at,
                GROUP_CONCAT(DISTINCT pei.company_name SEPARATOR ', ') AS companies,
                GROUP_CONCAT(DISTINCT pei.designation SEPARATOR ', ') AS designations,
                GROUP_CONCAT(DISTINCT proj.project_name SEPARATOR ', ') AS projects,
                GROUP_CONCAT(DISTINCT edu.degree_name SEPARATOR ', ') AS degrees,
                GROUP_CONCAT(DISTINCT cert.certificate_name SEPARATOR ', ') AS certificates
                FROM resume_info ri
                LEFT JOIN professional_experience_info pei ON pei.fk_cand_id = ri.id AND pei.active = 1
                LEFT JOIN projects_info proj ON proj.fk_cand_id = ri.id AND proj.active = 1
                LEFT JOIN education_info edu ON edu.fk_cand_id = ri.id AND edu.active = 1
                LEFT JOIN certification_info cert ON cert.fk_cand_id = ri.id AND cert.active = 1
                WHERE ri.fk_jd_id = %s AND ri.active = 1
                GROUP BY ri.id;

            """
            cursor.execute(query, (jd_id,))  # Pass jd_id as a tuple
            result = cursor.fetchall()  # Use fetchall to get all matching rows
            return result if result else None  
    except mysql.connector.Error as err:
        insert_error_log("error is occurring while extracting data for report", str(err))
        return None
    finally:
        if cursor:  # Ensuring cursor is defined before trying to close it
            cursor.close()# Ensure cursor is always closed; this is safe inside finally

