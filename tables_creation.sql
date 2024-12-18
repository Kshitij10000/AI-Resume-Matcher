CREATE TABLE jd_info (
    jd_id INT AUTO_INCREMENT PRIMARY KEY,  
    job_type VARCHAR(50), 
    jd_role VARCHAR(500),
    location VARCHAR(500),
    education VARCHAR(1000),
    skills_required TEXT,
    skills_preferable TEXT,
    experience_requirements TEXT,
    other_requirements TEXT,
    description TEXT,
    responsibilities MEDIUMTEXT,
    process_time DOUBLE,
    cost DOUBLE,
    server_file_name VARCHAR(255),
    active SMALLINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE resume_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_jd_id INT,
  cand_name VARCHAR(1000),
  email VARCHAR(50),
  phone VARCHAR(50),
  address VARCHAR(500),
  role VARCHAR(455),
  technical_skills TEXT,
  soft_skills TEXT,
  similar_skills TEXT,
  missing_skills TEXT,
  preferable_skills TEXT,
  required_experience VARCHAR(1000),
  score VARCHAR(10),
  recommendation varchar(1000),
  file_path VARCHAR(455),
  active SMALLINT,
  created_at DATETIME,
  FOREIGN KEY (fk_jd_id) REFERENCES jd_info(jd_id)
);

CREATE TABLE professional_experience_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_cand_id INT,
  company_name VARCHAR(1000),
  designation VARCHAR(500),
  duration VARCHAR(500),
  key_skills TEXT,
  roles_and_responsibilities TEXT,
  active SMALLINT,
  created_at DATETIME,
  FOREIGN KEY (fk_cand_id) REFERENCES resume_info(id)
);

CREATE TABLE projects_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_cand_id INT,
  project_name VARCHAR(1000),
  role VARCHAR(500),
  duration VARCHAR(500),
  environment VARCHAR(1000),
  description TEXT,
  active SMALLINT,
  created_at DATETIME,
  FOREIGN KEY (fk_cand_id) REFERENCES resume_info(id)
);



CREATE TABLE education_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_cand_id INT,
  degree_name VARCHAR(1000),
  degree_specialization VARCHAR(500),
  degree_institution VARCHAR(1000),
  passing_year VARCHAR(45),
  active SMALLINT,
  created_at DATETIME,
  FOREIGN KEY (fk_cand_id) REFERENCES resume_info(id)
); 

CREATE TABLE certification_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_cand_id INT,
  certificate_name VARCHAR(1000),
  certificate_issuing_authority VARCHAR(500),
  passing_year VARCHAR(45),
  active SMALLINT,
  created_at DATETIME,
  FOREIGN KEY (fk_cand_id) REFERENCES resume_info(id)
);  

CREATE TABLE feedback_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fk_jd_id INT,
  feedback_text TEXT,
  created_at DATETIME,
  FOREIGN KEY (fk_jd_id) REFERENCES jd_info(jd_id)
);

CREATE TABLE error_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(255),
    error_desc TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);








