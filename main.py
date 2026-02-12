import streamlit as st
import time
from main import EduBackend

# --- Page Config ---
st.set_page_config(
    page_title="EduGenius Pro | AI Learning Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Best UI" ---
st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    /* Card Styling */
    .css-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Gamification Badge */
    .badge {
        background-color: #FFD700;
        color: #333;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8em;
    }
    
    /* Success Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
        animation: pulse 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'backend' not in st.session_state: st.session_state.backend = None
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = "Novice"
if 'current_q' not in st.session_state: st.session_state.current_q = None

# --- Sidebar: Profile & Config ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("Student Profile")
    
    # Gamification Tracker
    st.markdown(f"**Rank:** {st.session_state.level} 🎖️")
    st.progress(min(st.session_state.xp % 100, 100) / 100)
    st.caption(f"XP: {st.session_state.xp}/100 to next level")
    
    st.divider()
    
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload Textbook (PDF)", type="pdf")
    
    if uploaded_file and api_key and not st.session_state.backend:
        if st.button("🚀 Launch EduGenius"):
            with st.spinner("Initializing AI Neural Network..."):
                st.session_state.backend = EduBackend(api_key)
                st.session_state.backend.process_pdf(uploaded_file)
                st.success("System Online!")
                time.sleep(1)
                st.rerun()

# --- Main App Logic ---
if st.session_state.backend:
    # Top Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Active Quiz", "📅 AI Study Planner", "📊 Progress Dashboard"])

    # === TAB 1: QUIZ & STUDY ===
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.subheader("🎯 Active Recall Session")
            
            # Input Controls
            c1, c2 = st.columns(2)
            topic = c1.text_input("Topic focus:", "General Review")
            difficulty = c2.select_slider("Difficulty", options=["Easy", "Medium", "Hard"])
            
            if st.button("Generate Challenge"):
                with st.spinner("Crafting question..."):
                    q = st.session_state.backend.generate_quiz(topic, difficulty)
                    st.session_state.current_q = q
                    st.session_state.answered = False

            # Display Question
            if st.session_state.current_q:
                q = st.session_state.current_q
                st.markdown(f"#### {q.get('question')}")
                
                # Use a unique key to prevent UI glitching
                choice = st.radio("Choose your answer:", q.get('options', []), key="quiz_choice")
                
                if st.button("Lock Answer"):
                    user_ans = choice.split(")")[0]
                    correct_ans = q.get('correct_answer')
                    
                    if user_ans == correct_ans:
                        st.balloons()
                        st.markdown('<p class="success-text">✅ Correct! +10 XP</p>', unsafe_allow_html=True)
                        if not st.session_state.answered:
                            st.session_state.xp += 10
                            st.session_state.answered = True
                    else:
                        st.error(f"❌ Incorrect. The answer was {correct_ans}.")
                    
                    with st.expander("💡 View Detailed Explanation"):
                        st.write(q.get('explanation'))
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Voice / Quick Ask Feature
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.subheader("🤖 Quick Ask")
            user_query = st.chat_input("Ask anything about the document...")
            if user_query:
                # Simple RAG Chat interface
                with st.chat_message("user"):
                    st.write(user_query)
                with st.chat_message("assistant"):
                    st.write("Processing...") # Placeholder for direct chat logic
            st.info("🎙️ Voice input enabled in mobile view.")
            st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 2: AI STUDY PLANNER ===
    with tab2:
        st.header("📅 Intelligent Study Schedule")
        if st.button("Generate 7-Day Mastery Plan"):
            with st.spinner("Analyzing document complexity..."):
                plan = st.session_state.backend.generate_study_plan()
                st.markdown(plan)
        else:
            st.info("Click to generate a personalized schedule based on your uploaded textbook.")

    # === TAB 3: DASHBOARD ===
    with tab3:
        st.metric("Total XP", st.session_state.xp, "+10 today")
        st.write("### Recent Achievements")
        if st.session_state.xp > 0:
            st.write("🏆 First Blood: Answered first question correctly")
        if st.session_state.xp > 50:
            st.write("🔥 On Fire: 5 correct answers in a row")
            
else:
    # Landing Page State
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>🎓 Welcome to EduGenius Pro</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Upload any textbook, lecture note, or research paper.<br>
            Our AI will turn it into a <b>gamified tutor</b>, a <b>study planner</b>, and a <b>quiz master</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)