import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NIT Jalandhar AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BACKEND
# =========================================================

from chatbot import ask_question


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   MAIN APP
===================================================== */

.stApp {
    background-color: #f7f8fc !important;
}


/* =====================================================
   FORCE ALL NORMAL TEXT BLACK
===================================================== */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown div,
.stMarkdown li,
.stMarkdown strong,
.stMarkdown em {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}

section[data-testid="stSidebar"] * {
    color: #000000 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] span {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   SIDEBAR BUTTON
===================================================== */

section[data-testid="stSidebar"] .stButton button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #f1f5f9 !important;
    color: #000000 !important;
}


/* =====================================================
   HEADER
===================================================== */

.main-header {
    background: linear-gradient(
        135deg,
        #123c69,
        #1d5fa7
    );

    padding: 25px 30px;

    border-radius: 18px;

    margin-bottom: 25px;

    box-shadow:
        0px 5px 20px rgba(0, 0, 0, 0.08);
}

.main-header h1 {
    color: #ffffff !important;
    margin: 0 !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

.main-header p {
    color: #ffffff !important;
    margin-top: 8px !important;
    font-size: 15px !important;
}


/* =====================================================
   WELCOME CARD
===================================================== */

.welcome-card {
    background-color: #ffffff !important;

    padding: 25px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    margin-top: 15px;

    margin-bottom: 20px;

    box-shadow:
        0px 3px 12px rgba(0, 0, 0, 0.04);
}

.welcome-card h2,
.welcome-card h3,
.welcome-card h4,
.welcome-card p {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   EXAMPLE QUESTIONS
===================================================== */

.example-question {
    background-color: #ffffff !important;

    color: #000000 !important;

    padding: 13px 16px;

    border-radius: 10px;

    margin: 8px 0;

    border: 1px solid #e2e8f0;

    font-size: 15px;

    opacity: 1 !important;
}

.example-question * {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   CHAT MESSAGE - IMPORTANT
===================================================== */

[data-testid="stChatMessage"] {
    color: #000000 !important;
    opacity: 1 !important;
}


/* Chat message content */

[data-testid="stChatMessageContent"] {
    color: #000000 !important;
    opacity: 1 !important;
}


/* Everything inside chat message */

[data-testid="stChatMessageContent"] * {
    color: #000000 !important;
    opacity: 1 !important;
}


/* Markdown inside chat */

[data-testid="stChatMessageContent"]
[data-testid="stMarkdownContainer"] {
    color: #000000 !important;
    opacity: 1 !important;
}


/* Paragraph */

[data-testid="stChatMessageContent"] p {
    color: #000000 !important;
    opacity: 1 !important;

    font-size: 16px !important;

    line-height: 1.6 !important;
}


/* Lists */

[data-testid="stChatMessageContent"] ul,
[data-testid="stChatMessageContent"] ol {
    color: #000000 !important;
}

[data-testid="stChatMessageContent"] li {
    color: #000000 !important;
    opacity: 1 !important;

    font-size: 15px !important;

    line-height: 1.6 !important;
}


/* Bold */

[data-testid="stChatMessageContent"] strong {
    color: #000000 !important;
    opacity: 1 !important;
}


/* Headings */

[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3,
[data-testid="stChatMessageContent"] h4,
[data-testid="stChatMessageContent"] h5,
[data-testid="stChatMessageContent"] h6 {
    color: #000000 !important;
    opacity: 1 !important;
}


/* =====================================================
   USER CHAT MESSAGE
===================================================== */

[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    color: #000000 !important;
}


/* =====================================================
   CHAT INPUT
===================================================== */

[data-testid="stChatInput"] {
    background-color: #ffffff !important;
}

[data-testid="stChatInput"] > div {
    background-color: #ffffff !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;

    color: #000000 !important;

    -webkit-text-fill-color: #000000 !important;

    caret-color: #000000 !important;

    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #555555 !important;

    -webkit-text-fill-color: #555555 !important;

    opacity: 1 !important;
}


/* =====================================================
   BUTTONS
===================================================== */

.stButton button {
    background-color: #ffffff !important;

    color: #000000 !important;

    -webkit-text-fill-color: #000000 !important;

    border: 1px solid #d1d5db !important;

    border-radius: 10px !important;

    font-weight: 600 !important;

    opacity: 1 !important;
}

.stButton button:hover {
    background-color: #f1f5f9 !important;

    color: #000000 !important;
}


/* =====================================================
   SPINNER
===================================================== */

.stSpinner {
    color: #000000 !important;
}


/* =====================================================
   ERROR / EXPANDER
===================================================== */

[data-testid="stExpander"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

[data-testid="stExpander"] * {
    color: #000000 !important;
}


/* =====================================================
   CODE
===================================================== */

code {
    color: #000000 !important;
}


/* =====================================================
   HIDE STREAMLIT BRANDING
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🎓 NIT Jalandhar")

    st.markdown("### AI Admission Assistant")

    st.divider()

    st.markdown("### 💡 Ask about")

    st.markdown("""
- 🎓 Admissions
- 💰 Fees
- 🏠 Hostels
- 📚 Courses
- 📄 Documents
- ✅ Eligibility
- 📝 Counselling
- 🏫 Campus information
""")

    st.divider()

    st.markdown("### ⚙️ Chat")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.markdown("**Powered by NVIDIA AI + RAG**")

    st.caption(
        "Answers are generated from the available "
        "NIT Jalandhar college documents."
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
<div class="main-header">
    <h1>🎓 NIT Jalandhar AI Assistant</h1>
    <p>
        Ask questions about admissions, fees, hostels,
        courses, eligibility, documents and counselling.
    </p>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="welcome-card">',
        unsafe_allow_html=True
    )

    st.markdown("## 👋 Hello!")

    st.markdown(
        "I'm the NIT Jalandhar admission assistant. "
        "Ask me anything related to college admission information."
    )

    st.markdown("### Try asking:")

    st.markdown(
        """
<div class="example-question">
💬 hostels available for boys?
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="example-question">
💬 What documents are required for physical reporting?
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="example-question">
💬 What hostel facilities are available?
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="example-question">
💬 hostel available for girls?
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.markdown(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.markdown(
                message["content"]
            )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask your question about NIT Jalandhar..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    question = question.strip()

    if question:

        # =================================================
        # SAVE USER MESSAGE
        # =================================================

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # =================================================
        # DISPLAY USER MESSAGE
        # =================================================

        with st.chat_message("user"):

            st.markdown(
                question
            )


        # =================================================
        # GENERATE AI ANSWER
        # =================================================

        with st.chat_message("assistant"):

            with st.spinner(
                "🔎 Searching college documents..."
            ):

                try:

                    answer = ask_question(
                        question
                    )

                    if not isinstance(
                        answer,
                        str
                    ):
                        answer = str(answer)


                    # -------------------------------------
                    # DISPLAY ANSWER
                    # -------------------------------------

                    st.markdown(
                        answer
                    )


                    # -------------------------------------
                    # SAVE ANSWER
                    # -------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )


                except Exception as e:

                    error_message = (
                        "⚠️ Sorry, something went wrong "
                        "while processing your question."
                    )

                    st.error(
                        error_message
                    )


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )


                    # -------------------------------------
                    # TECHNICAL ERROR
                    # -------------------------------------

                    with st.expander(
                        "🔧 Technical Error"
                    ):

                        st.code(
                            str(e)
                        )