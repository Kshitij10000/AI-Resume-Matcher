import streamlit as st 
import database

def login_id_page():
    
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
    .bottom-create-account {
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 2, 3])  # Adjusted column widths to reduce the middle column
    with col2:
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
        with st.form(key='login_form'):
            st.markdown("<div class='stForm'>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")
            st.markdown("</div>", unsafe_allow_html=True)

            if submit_button:
                verification = database.check_user_in_database(username, password)
                if verification:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.warning("Login Failed. Check if your username/password is correct. If you don't have an account, create a new account.")

        st.markdown("<div class='bottom-create-account'>", unsafe_allow_html=True)
        if st.button("Create a New Account"):
            st.session_state.show_signup = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
