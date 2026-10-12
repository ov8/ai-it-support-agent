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

MODEL = "gemini-3.1-flash-lite"


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
- Never say you have escalated an issue unless the application confirms it.
- When escalation is appropriate, explain that the application will prepare a simulated escalation for human review and approval. Do not instruct the user to click "Prepare demo support ticket" when you have included the escalation marker.
- Explain that a human must approve the simulated ticket before its status changes.
- When you determine that human IT support is needed, include the exact marker [ESCALATION_RECOMMENDED] at the very end of your response.
- Only include this marker when escalation is genuinely appropriate.

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
            if "[ESCALATION_RECOMMENDED]" in answer:
                st.session_state.ticket_pending = True

                answer = answer.replace(
                    "[ESCALATION_RECOMMENDED]", ""
                ).strip()

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            import logging
            logging.exception("Gemini API request failed")

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
    if not st.session_state.messages:
        st.warning("Please describe an IT issue in the chat first.")
    else:
        with st.spinner("Gemini is preparing your support ticket..."):
            try:
                transcript = "\n".join(
                    f"{message['role']}: {message['content']}"
                    for message in st.session_state.messages
                )

                ticket_prompt = f"""
                Analyze this fictional IT support conversation.

                Prepare a concise support ticket with these fields:

                **Issue category:**
                **Issue summary:**
                **Troubleshooting completed:**
                **Current status:**
                **Recommended IT team:**
                **Reason for escalation:**

                Rules:
                - Use only information supported by the conversation.
                - Do not invent troubleshooting steps.
                - If information is missing, write "Not provided".
                - Choose an appropriate IT team based on the issue.
                - Do not claim a real ticket has been created.
                - Do not include passwords or sensitive information.

                CONVERSATION:
                {transcript}
                """

                ticket_response = client.models.generate_content(
                    model=MODEL,
                    contents=ticket_prompt,
                    config={
                        "temperature": 0.2,
                    },
                )

                ticket_text = ticket_response.text

                if not ticket_text:
                    raise ValueError("Gemini returned an empty ticket.")

                st.session_state.ticket_summary = ticket_text
                st.session_state.ticket_pending = True
                st.session_state.ticket_approved = False

            except Exception:
                import logging
                logging.exception("Ticket generation failed")

                st.error(
                    "Unable to generate the support ticket. "
                    "Please try again."
                )

if st.session_state.get("ticket_pending", False):
    st.warning(
        "Please review and approve this simulated escalation."
    )

if st.session_state.get("ticket_summary"):
    st.markdown("### AI-Generated Support Ticket")
    st.markdown(st.session_state.ticket_summary)
else:
    st.error("No ticket was generated. Please try preparing the ticket again.")

    if st.button("Approve simulated ticket"):
        st.session_state.ticket_approved = True
        st.session_state.ticket_pending = False

if st.session_state.get("ticket_approved", False):
    st.success(
        "Demo support ticket approved. "
        "Status: Escalated to Human IT Support."
    )


# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Prototype V2 | Streamlit + Gemini | "
    "Next: Agentic workflows, tool calling, "
    "intelligent routing and automated ticket creation."
)
