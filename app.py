import streamlit as st

st.set_page_config(
    page_title="AI IT Support Agent",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ AI IT Support Agent")
st.caption("Agentic AI Workflow Portfolio | Prototype V1")

st.info(
    "This demonstration uses fictional IT support scenarios. "
    "No real employee or client information is collected."
)

st.subheader("How can I help you today?")

issue = st.selectbox(
    "Select your IT support issue:",
    [
        "Choose an issue",
        "I cannot log into my account",
        "I cannot access SharePoint",
        "I need a software licence"
    ]
)

knowledge_base = {
    "I cannot log into my account": (
        "1. Confirm your username is correct.\n\n"
        "2. Check whether your password has expired.\n\n"
        "3. Try signing in through your organization's approved login page.\n\n"
        "4. If you are still unable to log in, contact IT support."
    ),
    "I cannot access SharePoint": (
        "1. Confirm you are signed into the correct account.\n\n"
        "2. Check whether you have been granted access to the site.\n\n"
        "3. Ask the site owner to verify your permissions.\n\n"
        "4. If access is still denied, contact IT support."
    ),
    "I need a software licence": (
        "1. Identify the software you need.\n\n"
        "2. Check whether your organization already provides it.\n\n"
        "3. Obtain any required manager approval.\n\n"
        "4. Submit a software access request to IT."
    )
}

if issue != "Choose an issue":

    st.subheader("Recommended troubleshooting steps")

    st.write(knowledge_base[issue])

    st.divider()

    resolved = st.radio(
        "Did these steps resolve your issue?",
        ["Select an answer", "Yes", "No"]
    )

    if resolved == "Yes":
        st.success("Great! Your support request is resolved.")

    elif resolved == "No":
        st.warning("This issue may require human IT support.")

        description = st.text_area(
            "Please describe what happened:"
        )

        if st.button("Create support ticket"):
            if description.strip():
                st.success("Demo support ticket created successfully!")
                st.write("**Category:**", issue)
                st.write("**Description:**", description)
                st.write("**Status:** Escalated to IT Support")
            else:
                st.error("Please provide a description before creating a ticket.")

st.divider()

st.caption(
    "Portfolio demonstration | Streamlit + Python | "
    "Future integration: Microsoft Copilot Studio and Power Automate"
)
