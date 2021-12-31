import streamlit_authenticator as stauth
from menu import *

# Function for login. User is prompted to enter a username and password.
# If user successfully logs in, the menu function will be displayed and the program functionality will
# be displayed to the user.
def login():
    names = ['Test User']
    usernames = ['tester']
    passwords = ['testing!']
    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                        'cookie', 'signature_key', cookie_expiry_days=0)
    name, authentication_status = authenticator.login('Login', 'sidebar')
    if authentication_status is None:
        st.warning('Please enter your username and password')
        return authentication_status
    else:
        if authentication_status:
            menu()
            return authentication_status
        elif not authentication_status:
            st.error('Username/password is incorrect')
            return authentication_status
