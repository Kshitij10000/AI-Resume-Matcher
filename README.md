# AI-Powered Resume Recommendation Application

This project is an AI-driven application that assists in identifying the best candidate for a job description by analyzing resumes. It leverages the capabilities of OpenAI and a relational database to achieve efficient candidate matching.

## Table of Contents

1.  [Features](#features)
2.  [Requirements](#requirements)
3.  [Installation](#installation)
4.  [Setup](#setup)
5.  [Usage](#usage)
6.  [Contributing](#contributing)

---

## Features

-   **AI-powered resume analysis:** Utilizes OpenAI's API to extract relevant skills and keywords from resumes.
-   **Job description matching:** Analyzes job descriptions and prioritizes resumes that best align with the requirements.
-   **Streamlit integration:** Provides a user-friendly interface for interacting with the application.

---

## Requirements

-   Python 3.8 or higher
-   OpenAI API Key (see [Setup](#setup))
-   streamlit (install with `pip install streamlit`)
-   Database Libraries:
    *   `SQLAlchemy` (for database interaction)
    *   `mysql-connector-python` (for MySQL databases, or choose another connector as per your database)
-   Other requirements are listed in the `requirements.txt` file

---

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/your-username/your_project_name.git
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    *   Linux/macOS: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate.bat`
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Setup

1.  **Obtain your OpenAI API Key:**
    *   Create an OpenAI account and obtain your API key at: [https://openai.com/api/]
2.  **Set up Environment Variables:**
    *   Create a file named `.env` in the project's root directory. This file is used to store sensitive information (like your API key) and is excluded from version control by being listed in `.gitignore`. Add the following line, replacing `YOUR_OPENAI_API_KEY` with your actual key:

        ```
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        ```
3.  **Configure your Database:**
    *   Ensure your database is running (e.g MySQL)
    *   Create a database (e.g., `resume_db`)
    *   Create a user that has the privileges to access the database
    *   Open the `database.py` file.
    *   Update the database connection details in this file (e.g. host, user, password and database name). Example configurations will be provided in the file's comments.

---

## Usage

1.  Run the application:
    ```bash
    streamlit run main.py
    ```
2.  The Streamlit interface will open in your browser. Follow the instructions on the page to upload a job description and a ZIP file containing the candidate resumes.

---
## Contributing
We welcome contributions to the project. To contribute, please follow these steps:
1.  Fork the repository.
2.  Create a new branch.
3.  Make your changes
4.  Submit a Pull Request.

---

## Licence

This project is licensed under the MIT Licence.
