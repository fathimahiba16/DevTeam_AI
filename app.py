import streamlit as st

# Page configuration
st.set_page_config(
    page_title="DevTeam AI",
    page_icon="🤖",
    layout="wide"
)

# Main heading
st.title("🤖 DevTeam AI")
st.subheader("Your AI Software Development Team")

st.write(
    "Describe the software you want to build. "
    "Our specialized AI agents will analyze, design, develop, "
    "test, review, and document the project."
)

# User input
requirement = st.text_area(
    "What would you like to build?",
    placeholder=(
        "Example: Build a Student Management System where I can "
        "add, update, delete, and search students."
    ),
    height=150
)

# Start button
if st.button("🚀 Start Development", type="primary"):

    if requirement.strip():

        st.success("Development request received!")

        st.write("### Your Requirement")
        st.write(requirement)

        st.info(
            "Next step: Requirement Agent will analyze this request."
        )

    else:
        st.warning("Please describe the software you want to build.")