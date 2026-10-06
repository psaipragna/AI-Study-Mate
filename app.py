import streamlit as st
import ollama

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Study Mate",
    page_icon="📚",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}
.card {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #ddd;
    background: #fafafa;
    margin-bottom: 15px;
}
.feature-title {
    font-size: 21px;
    font-weight: 600;
}
.result {
    padding: 20px;
    border-radius: 12px;
    background: #f7f7f7;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)


# ---------------- AI FUNCTION ----------------
def ask_ai(prompt):
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"


def length_prompt(length):
    return {
        "Short": "Give a short and simple answer.",
        "Medium": "Give a clear medium-length answer with important points.",
        "Long": "Give a detailed answer with examples and explanations."
    }[length]


def show_result(title, answer):
    st.markdown(f"### {title}")
    st.markdown(
        f'<div class="result">{answer}</div>',
        unsafe_allow_html=True
    )


# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 AI Study Mate")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🤖 Ask AI", "📖 Explain Topic", "📝 Quiz"]
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by Ollama + Llama 3.2")


# ==================================================
# HOME
# ==================================================
if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">📚 AI Study Mate</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your personal AI-powered study assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h2>👋 Welcome!</h2>
        <p>
        AI Study Mate helps students understand topics, ask questions,
        and practice through quizzes using local AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <div class="feature-title">🤖 Ask AI</div>
        <p>Ask questions and get simple AI-generated answers.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <div class="feature-title">📖 Explain Topic</div>
        <p>Learn difficult topics in an easy-to-understand way.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <div class="feature-title">📝 Quiz</div>
        <p>Test your knowledge with AI-generated questions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 How to use")

    st.write("1. Select a feature from the sidebar.")
    st.write("2. Enter your question or topic.")
    st.write("3. Choose the answer length if available.")
    st.write("4. Click the button and get your AI response.")


# ==================================================
# ASK AI
# ==================================================
elif page == "🤖 Ask AI":

    st.title("🤖 Ask AI")
    st.write("Ask anything related to your studies.")

    length = st.radio(
        "Answer Length",
        ["Short", "Medium", "Long"],
        horizontal=True
    )

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is artificial intelligence?"
    )

    if st.button("🚀 Ask AI", use_container_width=True):

        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                prompt = f"""
You are a helpful study assistant.

{length_prompt(length)}

Question:
{question}

Answer in a student-friendly way.
"""
                answer = ask_ai(prompt)

            show_result("📚 Answer", answer)


# ==================================================
# EXPLAIN TOPIC
# ==================================================
elif page == "📖 Explain Topic":

    st.title("📖 Explain Topic")
    st.write("Understand difficult topics in a simple way.")

    length = st.radio(
        "Explanation Length",
        ["Short", "Medium", "Long"],
        horizontal=True
    )

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Binary Search Tree"
    )

    if st.button("📖 Explain Topic", use_container_width=True):

        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Preparing explanation..."):
                prompt = f"""
You are an expert teacher helping a college student.

Explain the following topic.

Topic:
{topic}

{length_prompt(length)}

Use simple language and examples where useful.
"""
                answer = ask_ai(prompt)

            show_result("📖 Explanation", answer)


# ==================================================
# QUIZ
# ==================================================
else:

    st.title("📝 Quiz")
    st.write("Test your knowledge with an AI-generated quiz.")

    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input(
            "Quiz Topic",
            placeholder="Example: Data Structures"
        )

    with col2:
        count = st.selectbox(
            "Number of Questions",
            [5, 10, 15, 20]
        )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("📝 Generate Quiz", use_container_width=True):

        if not topic.strip():
            st.warning("Please enter a quiz topic.")
        else:
            with st.spinner("Generating quiz..."):

                prompt = f"""
Create a {count}-question multiple-choice quiz.

Topic: {topic}
Difficulty: {difficulty}

For every question provide:

Question:
A)
B)
C)
D)
Correct Answer:

Make the questions educational and accurate.
Do not add unnecessary explanations.
"""

                quiz = ask_ai(prompt)

            show_result("📝 Your Quiz", quiz)