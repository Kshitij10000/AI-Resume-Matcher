import streamlit as st 
import database

def new_user_page():
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        width: 100%;
    }
    .stForm {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])  # Adjusted column widths to reduce the middle column
    with col2:
        st.markdown("<h1 style='text-align: center;'>Create a New Account</h1>", unsafe_allow_html=True)
        with st.form(key='signup_form'):
            st.markdown("<div class='stForm'>", unsafe_allow_html=True)
            name = st.text_input("Name")
            username = st.text_input("Username")
            email = st.text_input("Email ID")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Sign Up")
            st.markdown("</div>", unsafe_allow_html=True)

            if submit_button:
                try:
                    if database.user_signup_input(name, username, email, password):
                        st.success("Account created successfully! Redirecting to login page...")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.warning("User Already Exists")
                except Exception as e:
                    st.error(f"Failed to create account due to: {e}")

        if st.button("Back to Login"):
            st.session_state.show_signup = False
            st.rerun()
