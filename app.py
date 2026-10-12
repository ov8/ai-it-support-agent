import hmac

import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI IT Support Agent",
    page_icon="🛠️",
    layout="centered",
)

st.title("🛠️ AI IT Support Agent")
st.caption("Conversational AI Portfolio | Prototype V2")

st.info(
    "This is a fictional IT support demonstration. "
    "Do not enter real passwords, patient data, "
    "personal information, or confidential work information."
)

# --------------------------------------------------
# 1. PRIVATE DEMO ACCESS
# --------------------------------------------------

def check_password():
    if st.session_state.get("authenticated", False):
        return True

    entered_password = st.text_input(
        "Enter demo access password:",
        type="password",
    )

    if st.button("Unlock demo"):
        if hmac.compare_digest(
            entered_password,
            st.secrets["DEMO_PASSWORD"],
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False


if not check_password():
    st.stop()


# --------------------------------------------------
# 2. GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-2.5-flash"


# --------------------------------------------------
# 3. FICTIONAL IT KNOWLEDGE BASE
# --------------------------------------------------

KNOWLEDGE_BASE = """
You are supporting a fictional organization called
Northstar Services.

Approved troubleshooting guidance:

ISSUE: ACCOUNT LOGIN
- Confirm the employee is using the correct username.
- Check whether the password has expired.
- Direct the employee to the approved password reset process.
- Never request passwords or MFA codes.
- Escalate account lockouts or unresolved authentication failures.

ISSUE: SHAREPOINT ACCESS
- Confirm the employee is using the correct organizational account.
- Determine whether the problem affects one folder or the entire site.
- Check whether the employee has requested access from the site owner.
- Do not claim to grant permissions.
- Escalate unresolved access problems.

ISSUE: SOFTWARE LICENSING
- Ask which software is required.
- Determine whether the employee already has an approved licence.
- Explain that manager approval may be required.
- Do not claim to purchase or provision software.
- Escalate licensing requests to the appropriate IT team.
"""


# --------------------------------------------------
# 4. SYSTEM INSTRUCTIONS
# --------------------------------------------------

SYSTEM_INSTRUCTIONS = f"""
You are a professional, helpful IT support assistant
for Northstar Services, a fictional organization.

Your responsibilities:
1. Understand the employee's IT problem.
2. Identify the likely issue category.
3. Ask relevant clarifying questions.
4. Provide troubleshooting instructions using
   the approved knowledge base.
5. Determine whether the issue is resolved.
6. If unresolved, offer human IT support escalation.

Rules:
- Use only the approved knowledge base for technical guidance.
- Do not invent organizational policies or procedures.
- Never ask for passwords, MFA codes, or sensitive information.
- Do not claim to access real systems or employee records.
- Do not claim to create real support tickets.
- Ask one or two questions at a time.
- Keep responses concise and understandable.
- If information is missing, ask for clarification.
- If you cannot resolve an issue, recommend escalation.

APPROVED KNOWLEDGE BASE:
{KNOWLEDGE_BASE}
"""


# --------------------------------------------------
# 5. CONVERSATION HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 6. CONVERSATIONAL AI
# --------------------------------------------------

user_input = st.chat_input(
    "Describe your IT support issue..."
)

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            conversation = [
                {
                    "role": message["role"],
                    "parts": [
                        {"text": message["content"]}
                    ],
                }
                for message in st.session_state.messages
            ]

            response = client.models.generate_content(
                model=MODEL,
                contents=conversation,
                config={
                    "system_instruction": SYSTEM_INSTRUCTIONS,
                    "temperature": 0.3,
                },
            )

            answer = response.text or (
                "I couldn't generate a response. "
                "Please try again."
            )

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception:
            st.error(
                "The AI service is temporarily unavailable. "
                "Please try again later."
            )


# --------------------------------------------------
# 7. DEMO ESCALATION
# --------------------------------------------------

st.divider()
st.subheader("Human IT Support Escalation")

st.caption(
    "This creates a simulated ticket only. "
    "No real IT support system is connected."
)

if st.button("Prepare demo support ticket"):
    st.session_state.ticket_pending = True

if st.session_state.get("ticket_pending", False):
    st.warning(
        "Please review and approve this simulated escalation."
    )

    if st.button("Approve simulated ticket"):
        st.success(
            "Demo support ticket approved. "
            "Status: Escalated to Human IT Support."
        )
        st.session_state.ticket_pending = False


# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Prototype V2 | Streamlit + Gemini | "
    "Next: Agentic workflows, tool calling, "
    "intelligent routing and automated ticket creation."
)
