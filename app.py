
import streamlit as st

from auth import create_users_table, create_user, verify_user
from orchestrator import Orchestrator


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DevTeam AI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------

create_users_table()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# --------------------------------------------------
# LOGIN / SIGN UP PAGE
# --------------------------------------------------

def show_auth_page():

    st.title("🤖 DevTeam AI")
    st.subheader("Your AI Software Development Team")

    st.write(
        "Sign in to start building software with your AI development team."
    )

    login_tab, signup_tab = st.tabs(["🔐 Login", "📝 Sign Up"])

    # ---------------- LOGIN ----------------

    with login_tab:

        st.subheader("Welcome Back")

        with st.form("login_form"):

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            login_button = st.form_submit_button(
                "Login",
                type="primary"
            )

        if login_button:

            if verify_user(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:
                st.error("Invalid username or password.")

    # ---------------- SIGN UP ----------------

    with signup_tab:

        st.subheader("Create Account")

        with st.form("signup_form"):

            new_username = st.text_input(
                "Choose a username",
                key="signup_username"
            )

            new_password = st.text_input(
                "Choose a password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="confirm_password"
            )

            signup_button = st.form_submit_button(
                "Create Account",
                type="primary"
            )

        if signup_button:

            if not new_username.strip():
                st.warning("Please enter a username.")

            elif len(new_password) < 6:
                st.warning(
                    "Password must contain at least 6 characters."
                )

            elif new_password != confirm_password:
                st.warning("Passwords do not match.")

            else:

                success, message = create_user(
                    new_username,
                    new_password
                )

                if success:
                    st.success(
                        "Account created successfully! "
                        "You can now log in."
                    )
                else:
                    st.error(message)


# --------------------------------------------------
# MAIN DEVTEAM AI PAGE
# --------------------------------------------------

def show_main_page():

    # Sidebar
    with st.sidebar:

        st.title("🤖 DevTeam AI")

        st.write(
            f"Logged in as **{st.session_state.username}**"
        )

        st.divider()

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()

    # Main content
    st.title("🤖 DevTeam AI")
    st.subheader("Your AI Software Development Team")

    st.write(
        "Describe the software you want to build. "
        "Our specialized AI agents will analyze, design, develop, "
        "test, review, and document the project."
    )

    requirement = st.text_area(
        "What would you like to build?",
        placeholder=(
            "Example: Build a Student Management System where I can "
            "add, update, delete, and search students."
        ),
        height=150
    )

    if st.button(
        "🚀 Start Development",
        type="primary"
    ):

        if requirement.strip():

            try:
                with st.spinner(
                    "🤖 Requirement Agent and Architect Agent are working..."
                ):

                    team = Orchestrator(provider="gemini")
                    result = team.run(requirement)

                st.success(
                    "✅ Requirement analysis and architecture completed!"
                )

                st.subheader("📋 Generated Requirements")
                st.markdown(result["requirements"])

                st.subheader("🏗️ Software Architecture")
                st.markdown(result["architecture"])

                st.subheader("💻 Generated Source Code")
                st.code(
                result["generated_code"],
                        language="markdown"
                )

                st.subheader("📁 Saved Project Files")

                st.success("Generated files saved successfully!")

                for filename in result["saved_files"]:
                    st.write(f"📄 {filename}")


            except Exception as e:
                st.error(f"Development failed: {e}")

        else:
            st.warning(
                "Please describe the software you want to build."
            )


# --------------------------------------------------
# APP ROUTING
# --------------------------------------------------

if st.session_state.logged_in:
    show_main_page()
else:
    show_auth_page()
