import streamlit as st
import sqlite3
import time
import json
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="51Talk Quiz",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database setup
DB_PATH = "quiz_responses.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quiz TEXT,
            question INTEGER,
            correct INTEGER,
            time_ms INTEGER,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS active_question (
            id INTEGER PRIMARY KEY,
            quiz TEXT,
            question INTEGER,
            active INTEGER,
            start_time TEXT
        )
    ''')
    # Initialize active_question if empty
    c.execute("SELECT COUNT(*) FROM active_question")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO active_question VALUES (1, '', 0, 0, '')")
    conn.commit()
    conn.close()

init_db()

# Quiz Data - Load from JSON file
QUIZZES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quizzes.json")

def load_quizzes():
    if os.path.exists(QUIZZES_FILE):
        with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_quizzes(data):
    with open(QUIZZES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

QUIZZES = load_quizzes()

# Database functions
def get_active_question():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT quiz, question, active, start_time FROM active_question WHERE id=1")
    row = c.fetchone()
    conn.close()
    if row:
        return {"quiz": row[0], "question": row[1], "active": row[2], "start_time": row[3]}
    return None

def set_active_question(quiz, question, active):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE active_question SET quiz=?, question=?, active=?, start_time=? WHERE id=1",
              (quiz, question, 1 if active else 0, datetime.now().isoformat() if active else ""))
    conn.commit()
    conn.close()

def submit_response(name, quiz, question, correct, time_ms):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO responses (name, quiz, question, correct, time_ms, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (name, quiz, question, 1 if correct else 0, time_ms, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_responses(quiz, question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT name, correct, time_ms, timestamp
        FROM responses
        WHERE quiz=? AND question=?
        ORDER BY correct DESC, time_ms ASC
    """, (quiz, question))
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "correct": r[1], "time_ms": r[2], "timestamp": r[3]} for r in rows]

def clear_responses(quiz, question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM responses WHERE quiz=? AND question=?", (quiz, question))
    conn.commit()
    conn.close()

def has_responded(name, quiz, question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM responses WHERE name=? AND quiz=? AND question=?", (name, quiz, question))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: #FFD700;
        margin: 0;
    }
    .main-header p {
        color: #aaa;
        margin: 5px 0 0 0;
    }
    .question-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #FFD700;
        margin: 20px 0;
    }
    .question-text-ar {
        font-size: 1.8em;
        color: white;
        text-align: right;
        direction: rtl;
        margin-bottom: 10px;
    }
    .question-text-en {
        font-size: 1.2em;
        color: #aaa;
        text-align: left;
    }
    .winner-box {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .winner-box h2 {
        color: #1a1a2e;
        margin: 0;
        font-size: 2em;
    }
    .winner-box p {
        color: #333;
        margin: 10px 0 0 0;
        font-size: 1.2em;
    }
    .stat-box {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stat-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #FFD700;
    }
    .stat-label {
        color: #aaa;
    }
    .stButton > button {
        width: 100%;
        padding: 15px;
        font-size: 1.2em;
        font-weight: bold;
        border-radius: 10px;
    }
    div[data-testid="stVerticalBlock"] > div:has(> div.stButton) button {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        border: 2px solid #444;
    }
    div[data-testid="stVerticalBlock"] > div:has(> div.stButton) button:hover {
        border-color: #FFD700;
        color: #FFD700;
    }

    /* Presentation Mode Styles */
    .present-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        border: 3px solid #FFD700;
    }
    .present-header h1 {
        color: #FFD700;
        font-size: 3em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .present-header p {
        color: #aaa;
        font-size: 1.5em;
        margin: 10px 0 0 0;
    }
    .present-question {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 60px;
        border-radius: 25px;
        border: 4px solid #FFD700;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(255,215,0,0.2);
    }
    .present-question-ar {
        font-size: 3.5em;
        color: white;
        text-align: center;
        direction: rtl;
        margin-bottom: 20px;
        line-height: 1.4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .present-question-en {
        font-size: 2em;
        color: #aaa;
        text-align: center;
    }
    .present-winner {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 60px;
        border-radius: 25px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(255,215,0,0.4);
        animation: winner-pulse 2s ease-in-out infinite;
    }
    @keyframes winner-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    .present-winner h1 {
        color: #1a1a2e;
        font-size: 4em;
        margin: 0;
    }
    .present-winner h2 {
        color: #333;
        font-size: 5em;
        margin: 20px 0;
    }
    .present-winner p {
        color: #555;
        font-size: 2em;
        margin: 0;
    }
    .present-stats {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 30px 0;
    }
    .present-stat {
        background: rgba(255,255,255,0.1);
        padding: 30px 50px;
        border-radius: 15px;
        text-align: center;
    }
    .present-stat-value {
        font-size: 4em;
        font-weight: bold;
        color: #FFD700;
    }
    .present-stat-label {
        font-size: 1.5em;
        color: #aaa;
    }
    .present-waiting {
        text-align: center;
        padding: 100px;
    }
    .present-waiting h1 {
        font-size: 4em;
        color: #FFD700;
        margin-bottom: 20px;
    }
    .present-waiting p {
        font-size: 2em;
        color: #aaa;
    }
    .present-qr {
        background: white;
        padding: 30px;
        border-radius: 20px;
        display: inline-block;
        margin: 20px;
    }
    .present-live {
        display: inline-block;
        background: #00ff00;
        color: #000;
        padding: 10px 30px;
        border-radius: 30px;
        font-size: 1.5em;
        font-weight: bold;
        animation: blink 1s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# Get mode from URL params
params = st.query_params
mode = params.get("mode", "player")
quiz_param = params.get("quiz", None)
q_param = params.get("q", None)

# Initialize session state
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "answered" not in st.session_state:
    st.session_state.answered = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# =====================
# PRESENTATION MODE (Big Screen)
# =====================
if mode == "present":
    # Get active question
    active = get_active_question()

    if active and active["active"] and active["quiz"] in QUIZZES:
        quiz_id = active["quiz"]
        q_idx = active["question"]
        quiz_data = QUIZZES[quiz_id]
        question = quiz_data["questions"][q_idx]

        # Header
        st.markdown(f"""
        <div class="present-header">
            <span class="present-live">🔴 LIVE</span>
            <h1>🎯 {quiz_data['title']}</h1>
            <p>Question {q_idx + 1} of {len(quiz_data['questions'])}</p>
        </div>
        """, unsafe_allow_html=True)

        # Question Display
        st.markdown(f"""
        <div class="present-question">
            <div class="present-question-ar">{question['ar']}</div>
            <div class="present-question-en">{question['en']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Get responses
        responses = get_responses(quiz_id, q_idx)
        correct_responses = [r for r in responses if r["correct"]]
        wrong_responses = [r for r in responses if not r["correct"]]

        # Winner Display
        if correct_responses:
            winner = correct_responses[0]
            st.markdown(f"""
            <div class="present-winner">
                <h1>🏆 WINNER! 🏆</h1>
                <h2>{winner['name']}</h2>
                <p>⚡ {winner['time_ms']/1000:.2f} seconds</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()

        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="present-stat">
                <div class="present-stat-value">{len(responses)}</div>
                <div class="present-stat-label">Total Responses</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="present-stat">
                <div class="present-stat-value" style="color: #00ff00;">{len(correct_responses)}</div>
                <div class="present-stat-label">✓ Correct</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="present-stat">
                <div class="present-stat-value" style="color: #ff6b6b;">{len(wrong_responses)}</div>
                <div class="present-stat-label">✗ Wrong</div>
            </div>
            """, unsafe_allow_html=True)

        # Top 5 Leaderboard (if we have correct responses)
        if len(correct_responses) > 1:
            st.markdown("### 🏅 Top Correct Answers")
            for i, r in enumerate(correct_responses[:5]):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                st.markdown(f"**{medal} {r['name']}** - {r['time_ms']/1000:.2f}s")

    else:
        # Waiting screen
        st.markdown("""
        <div class="present-waiting">
            <h1>🎯 51Talk MENA Quiz</h1>
            <p>Annual Gathering 2026</p>
            <br><br>
            <h1>⏳</h1>
            <p>Waiting for the next question...</p>
            <p style="color: #666;">في انتظار السؤال التالي</p>
        </div>
        """, unsafe_allow_html=True)

    # Auto-refresh every 1 second for presentation
    time.sleep(1)
    st.rerun()

# =====================
# ADMIN MODE
# =====================
elif mode == "admin":
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Quiz Admin Dashboard</h1>
        <p>51Talk MENA - Annual Gathering 2026</p>
    </div>
    """, unsafe_allow_html=True)

    admin_tab1, admin_tab2 = st.tabs(["📡 Control Panel", "✏️ Edit Questions"])

    # ---- CONTROL PANEL TAB ----
    with admin_tab1:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.subheader("📋 Quiz Selection")
            selected_quiz = st.selectbox(
                "Choose Quiz",
                options=list(QUIZZES.keys()),
                format_func=lambda x: QUIZZES[x]["title"]
            )

            quiz_data = QUIZZES[selected_quiz]
            selected_q = st.selectbox(
                "Choose Question",
                options=list(range(len(quiz_data["questions"]))),
                format_func=lambda x: f"Question {x+1}: {quiz_data['questions'][x]['en'][:30]}..."
            )

            st.divider()

            # Broadcast controls
            st.subheader("📡 Broadcast")

            active = get_active_question()
            is_active = active and active["active"] and active["quiz"] == selected_quiz and active["question"] == selected_q

            if is_active:
                st.success("🟢 LIVE - Question is active!")
                if st.button("⏹ STOP Question", type="secondary"):
                    set_active_question("", 0, False)
                    st.rerun()
            else:
                if st.button("🚀 START Question", type="primary"):
                    set_active_question(selected_quiz, selected_q, True)
                    st.rerun()

            if st.button("🗑 Clear Responses"):
                clear_responses(selected_quiz, selected_q)
                st.rerun()

            st.divider()

            # QR Code / Link
            st.subheader("📱 Player Link")
            base_url = st.text_input("Your Streamlit URL", value="https://your-app.streamlit.app")
            player_url = f"{base_url}?quiz={selected_quiz}&q={selected_q}"
            st.code(player_url, language=None)

            # Auto-refresh
            st.divider()
            auto_refresh = st.checkbox("🔄 Auto-refresh (2s)", value=True)
            if auto_refresh:
                time.sleep(2)
                st.rerun()

        with col2:
            question = quiz_data["questions"][selected_q]

            # Current Question Display
            st.markdown(f"""
            <div class="question-box">
                <div class="question-text-ar">{question['ar']}</div>
                <div class="question-text-en">{question['en']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Correct Answer
            correct_opt = next(o for o in question["options"] if o["correct"])
            st.success(f"✓ Correct Answer: {correct_opt['ar']} - {correct_opt['en']}")

            # Get responses
            responses = get_responses(selected_quiz, selected_q)
            correct_responses = [r for r in responses if r["correct"]]
            wrong_responses = [r for r in responses if not r["correct"]]

            # Winner Display
            if correct_responses:
                winner = correct_responses[0]
                st.markdown(f"""
                <div class="winner-box">
                    <h2>🏆 WINNER</h2>
                    <p>{winner['name']} ({winner['time_ms']/1000:.2f}s)</p>
                </div>
                """, unsafe_allow_html=True)

            # Stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total Responses", len(responses))
            with col_b:
                st.metric("✓ Correct", len(correct_responses))
            with col_c:
                st.metric("✗ Wrong", len(wrong_responses))

            # Responses Table
            st.subheader("📊 Live Responses")
            if responses:
                for i, r in enumerate(responses):
                    icon = "🏆" if i == 0 and r["correct"] else ("✓" if r["correct"] else "✗")
                    color = "green" if r["correct"] else "red"
                    st.markdown(f"**{i+1}. {icon} {r['name']}** - :{color}[{'Correct' if r['correct'] else 'Wrong'}] - {r['time_ms']/1000:.2f}s")
            else:
                st.info("No responses yet. Click START to begin!")

    # ---- EDIT QUESTIONS TAB ----
    with admin_tab2:
        # Reload quizzes fresh for editing
        edit_quizzes = load_quizzes()

        st.subheader("📝 Question Editor")

        # --- Add New Quiz ---
        with st.expander("➕ Add New Quiz"):
            new_quiz_id = st.text_input("Quiz ID (lowercase, no spaces)", placeholder="e.g. general_knowledge", key="new_quiz_id")
            new_quiz_title = st.text_input("Quiz Title (Arabic - English)", placeholder="e.g. ثقافة عامة - General Knowledge", key="new_quiz_title")
            if st.button("Create Quiz", key="btn_create_quiz"):
                qid = new_quiz_id.strip().lower().replace(" ", "_")
                if qid and new_quiz_title.strip():
                    if qid in edit_quizzes:
                        st.error(f"Quiz '{qid}' already exists!")
                    else:
                        edit_quizzes[qid] = {"title": new_quiz_title.strip(), "questions": []}
                        save_quizzes(edit_quizzes)
                        st.success(f"Quiz '{new_quiz_title.strip()}' created!")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.error("Please fill in both Quiz ID and Title.")

        st.divider()

        # --- Select Quiz to Edit ---
        if not edit_quizzes:
            st.warning("No quizzes found. Create one above.")
        else:
            edit_quiz_id = st.selectbox(
                "Select Quiz to Edit",
                options=list(edit_quizzes.keys()),
                format_func=lambda x: edit_quizzes[x]["title"],
                key="edit_quiz_select"
            )

            eq_data = edit_quizzes[edit_quiz_id]

            # Edit quiz title
            col_title, col_del = st.columns([4, 1])
            with col_title:
                updated_title = st.text_input("Quiz Title", value=eq_data["title"], key="edit_quiz_title")
            with col_del:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑 Delete Quiz", key="btn_del_quiz", type="secondary"):
                    del edit_quizzes[edit_quiz_id]
                    save_quizzes(edit_quizzes)
                    st.success("Quiz deleted!")
                    time.sleep(0.5)
                    st.rerun()

            if updated_title != eq_data["title"]:
                eq_data["title"] = updated_title
                save_quizzes(edit_quizzes)

            st.divider()

            # --- Edit Questions ---
            questions = eq_data["questions"]

            for q_idx, q in enumerate(questions):
                with st.expander(f"Question {q_idx + 1}: {q['en'][:50]}{'...' if len(q['en']) > 50 else ''}", expanded=False):
                    # Question text
                    q_ar = st.text_input("Question (Arabic)", value=q["ar"], key=f"q_ar_{edit_quiz_id}_{q_idx}")
                    q_en = st.text_input("Question (English)", value=q["en"], key=f"q_en_{edit_quiz_id}_{q_idx}")

                    # Options
                    st.markdown("**Answer Options:**")
                    correct_index = 0
                    for oi, opt in enumerate(q["options"]):
                        if opt["correct"]:
                            correct_index = oi
                            break

                    option_labels = []
                    for oi, opt in enumerate(q["options"]):
                        c1, c2 = st.columns(2)
                        with c1:
                            opt_ar = st.text_input(f"Option {oi+1} (Arabic)", value=opt["ar"], key=f"opt_ar_{edit_quiz_id}_{q_idx}_{oi}")
                        with c2:
                            opt_en = st.text_input(f"Option {oi+1} (English)", value=opt["en"], key=f"opt_en_{edit_quiz_id}_{q_idx}_{oi}")
                        option_labels.append(f"{opt_en} / {opt_ar}")

                    # Correct answer selector
                    new_correct = st.radio(
                        "Correct Answer",
                        options=list(range(len(q["options"]))),
                        index=correct_index,
                        format_func=lambda x: f"Option {x+1}: {option_labels[x]}",
                        key=f"correct_{edit_quiz_id}_{q_idx}",
                        horizontal=True
                    )

                    col_save, col_delete = st.columns(2)
                    with col_save:
                        if st.button(f"💾 Save Question {q_idx + 1}", key=f"btn_save_q_{edit_quiz_id}_{q_idx}", type="primary"):
                            # Update question text
                            questions[q_idx]["ar"] = q_ar
                            questions[q_idx]["en"] = q_en
                            # Update options
                            for oi in range(len(questions[q_idx]["options"])):
                                questions[q_idx]["options"][oi]["ar"] = st.session_state[f"opt_ar_{edit_quiz_id}_{q_idx}_{oi}"]
                                questions[q_idx]["options"][oi]["en"] = st.session_state[f"opt_en_{edit_quiz_id}_{q_idx}_{oi}"]
                                questions[q_idx]["options"][oi]["correct"] = (oi == new_correct)
                            save_quizzes(edit_quizzes)
                            st.success(f"Question {q_idx + 1} saved!")
                            time.sleep(0.5)
                            st.rerun()
                    with col_delete:
                        if st.button(f"🗑 Delete Question {q_idx + 1}", key=f"btn_del_q_{edit_quiz_id}_{q_idx}", type="secondary"):
                            questions.pop(q_idx)
                            save_quizzes(edit_quizzes)
                            st.success(f"Question {q_idx + 1} deleted!")
                            time.sleep(0.5)
                            st.rerun()

            # --- Add New Question ---
            st.divider()
            st.subheader("➕ Add New Question")

            new_q_ar = st.text_input("New Question (Arabic)", key="new_q_ar", placeholder="اكتب السؤال بالعربية")
            new_q_en = st.text_input("New Question (English)", key="new_q_en", placeholder="Write the question in English")

            st.markdown("**Answer Options:**")
            new_opts = []
            for oi in range(4):
                nc1, nc2 = st.columns(2)
                with nc1:
                    nopt_ar = st.text_input(f"New Option {oi+1} (Arabic)", key=f"new_opt_ar_{oi}", placeholder="الخيار بالعربية")
                with nc2:
                    nopt_en = st.text_input(f"New Option {oi+1} (English)", key=f"new_opt_en_{oi}", placeholder="Option in English")
                new_opts.append({"ar": nopt_ar, "en": nopt_en})

            new_correct_opt = st.radio(
                "Correct Answer for New Question",
                options=[0, 1, 2, 3],
                format_func=lambda x: f"Option {x+1}",
                key="new_correct_opt",
                horizontal=True
            )

            if st.button("➕ Add Question", key="btn_add_q", type="primary"):
                if new_q_ar.strip() and new_q_en.strip() and all(o["ar"].strip() and o["en"].strip() for o in new_opts):
                    new_question = {
                        "ar": new_q_ar.strip(),
                        "en": new_q_en.strip(),
                        "options": [
                            {"ar": new_opts[i]["ar"].strip(), "en": new_opts[i]["en"].strip(), "correct": (i == new_correct_opt)}
                            for i in range(4)
                        ]
                    }
                    questions.append(new_question)
                    save_quizzes(edit_quizzes)
                    st.success("Question added!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Please fill in all fields (question text + all 4 options in both languages).")

# =====================
# PLAYER MODE
# =====================
elif mode == "player" or mode not in ["admin", "present"]:
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Live Quiz - مسابقة مباشرة</h1>
        <p>Fastest correct answer wins! - أسرع إجابة صحيحة تفوز!</p>
    </div>
    """, unsafe_allow_html=True)

    # Check for direct link with quiz param
    if quiz_param and q_param is not None:
        direct_quiz = quiz_param
        direct_q = int(q_param)
    else:
        # Check active question
        active = get_active_question()
        if active and active["active"]:
            direct_quiz = active["quiz"]
            direct_q = active["question"]
        else:
            direct_quiz = None
            direct_q = None

    # Registration
    if not st.session_state.player_name:
        st.subheader("Enter your name - أدخل اسمك")
        name = st.text_input("Your Name - اسمك", placeholder="Enter your name here")
        if st.button("Join Quiz - انضم للمسابقة", type="primary"):
            if name.strip():
                st.session_state.player_name = name.strip()
                st.session_state.answered = False
                st.session_state.start_time = time.time()
                st.rerun()
            else:
                st.error("Please enter your name - الرجاء إدخال اسمك")

    # Quiz
    elif direct_quiz and direct_quiz in QUIZZES:
        quiz_data = QUIZZES[direct_quiz]
        question = quiz_data["questions"][direct_q]

        # Check if already answered
        if has_responded(st.session_state.player_name, direct_quiz, direct_q):
            st.success("✓ Answer Submitted! - تم إرسال الإجابة!")
            st.info("Waiting for next question... - في انتظار السؤال التالي")

            # Auto-check for new question
            time.sleep(3)
            st.rerun()
        else:
            # Show question
            st.markdown(f"**{quiz_data['title']}** - Question {direct_q + 1}/5")

            st.markdown(f"""
            <div class="question-box">
                <div class="question-text-ar">{question['ar']}</div>
                <div class="question-text-en">{question['en']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Timer display
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                remaining = max(0, 20 - int(elapsed))
                st.progress(remaining / 20, f"⏱ Time: {remaining}s")

            # Options
            import random
            if f"shuffled_{direct_quiz}_{direct_q}" not in st.session_state:
                options = question["options"].copy()
                random.shuffle(options)
                st.session_state[f"shuffled_{direct_quiz}_{direct_q}"] = options

            options = st.session_state[f"shuffled_{direct_quiz}_{direct_q}"]

            cols = st.columns(2)
            for i, opt in enumerate(options):
                with cols[i % 2]:
                    label = f"{chr(65+i)}. {opt['ar']}\n{opt['en']}"
                    if st.button(label, key=f"opt_{i}", use_container_width=True):
                        # Calculate response time
                        response_time = int((time.time() - st.session_state.start_time) * 1000) if st.session_state.start_time else 20000

                        # Submit response
                        submit_response(
                            st.session_state.player_name,
                            direct_quiz,
                            direct_q,
                            opt["correct"],
                            response_time
                        )

                        if opt["correct"]:
                            st.balloons()
                            st.success("🎉 Correct! - صحيح!")
                        else:
                            st.error("❌ Wrong! - خطأ!")

                        time.sleep(1.5)
                        st.rerun()

    else:
        # Waiting for question
        st.info(f"👋 Welcome, **{st.session_state.player_name}**!")
        st.warning("⏳ Waiting for the host to start a question...")
        st.caption("في انتظار السؤال من المضيف...")

        # Auto-refresh to check for active question
        time.sleep(2)
        st.rerun()

    # Footer
    st.markdown("---")
    st.caption("51Talk MENA - Annual Gathering 2026")
