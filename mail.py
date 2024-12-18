import streamlit as st
import mysql.connector
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def auto_email_sender():
    def send_emails(recipient_emails):
        sender_email = "ajinkyabhandare200210@gmail.com"
        sender_password = "gioy ebdr szue hjww"  # If using 2-Step Verification, use an App Password
        subject = "Congratulations! You've Been Shortlisted"
        body = '''Dear candidate,

    We are thrilled to inform you that you have been shortlisted for the [Program Name] program!  Your application stood out among a competitive pool, and we are excited to learn more about you.

    To proceed to the next stage of the selection process, please follow these steps:

    Click on the link below to access the next steps form: [Link to Form]
    Complete the form by [Date and Time].
    Verify your continued interest in the program by [Date and Time].
    We encourage you to review the attached program information document for further details.  [Optional: If there's an additional step]  Following this step, you will be notified if you have been selected for an interview.

    Thank you again for your interest in the [Program Name] program.  We look forward to hearing from you soon.

    Sincerely,
    Team
    '''
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        context = smtplib.ssl.create_default_context()
        
        def send_email(sender_email, recipient_email, subject, body):
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)  # Secure the connection
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
        for email in recipient_emails:
            if email is not None:
                send_email(sender_email, email, subject, body)
                print(f"Email sent to {email}")

    # Database configuration
    db_config = {
        'user': 'admin',
        'password': 'WHqqCKcpOa6PGQwKVIz3',
        'host': 'cre-database.clskaom22sd7.us-east-1.rds.amazonaws.com',
        'port': 3306,
        'database': 'cre'
    }

    def fetch_top_rows_desc_by_score(jd_id, top_count):
        query = """
        SELECT *
        FROM resume_info
        WHERE fk_jd_id = %s
        ORDER BY CAST(score AS SIGNED) DESC
        LIMIT %s
        """
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (jd_id, top_count))  # Pass parameters as a tuple
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

  
    st.title('Send email to Candidates')

    col1, col2 = st.columns(2)

    jd_id = col1.number_input('Enter Job Role ID:', min_value=1)
    top_count = col2.number_input('Enter Number of Top Candidates:', min_value=1, max_value=10)

    if st.button('Fetch Top Candidates'):
            data = fetch_top_rows_desc_by_score(jd_id, top_count)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
                email_list = df['email'].tolist()
                st.session_state.email_list = email_list 
            else:
                st.write("No data found for the specified job role ID and top count.")

    if st.button('Send Mail to Shortlisted Candidates'):
            if 'email_list' in st.session_state:
                send_emails(st.session_state.email_list)
                st.markdown("Mail has been sent to the shortlisted candidates.")
            else:
                st.write("No shortlisted candidates to send emails to.")

    