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
from streamlit_navigation_bar import st_navbar
from crengine import candidate_recommendation_engine
from report import past_report
from chat_with_sql import chat_with_sql_database
from exam import exam1
from mail import auto_email_sender
from login_page import login_id_page
from create_new_user_page import new_user_page
from home_page import home_content
from about_page import about_page_content


st.set_page_config(
    page_title="Nirmaan.HR",
    layout="wide",
    initial_sidebar_state="expanded",
)


def login_page():
    login_id_page()

def registration_page():
    new_user_page()

def home_page():
    home_content()
    
def ai_candidate_recommender():
    candidate_recommendation_engine()

def test_maker():
    exam1()

def send_mail():
    auto_email_sender()

def chat_bot():
    chat_with_sql_database()

def report_page():
    past_report()

def about_us():
    about_page_content()



def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False

    if st.session_state.show_signup:
        registration_page()
    elif not st.session_state['logged_in']:
        login_page()
    else:
        page = st_navbar(["Home", "CRE", "SkillAssess", "CandidateConnect","RecruitaBot", "Report", "About Us"])

        page_functions = {
            "Home": home_page,
            "CRE": ai_candidate_recommender,
            "SkillAssess": test_maker,
            "CandidateConnect": send_mail,
            "RecruitaBot": chat_bot,
            "Report": report_page, 
            "About Us": about_us
        }


        if page in page_functions:
            page_functions[page]()


if __name__ == "__main__":
    main()