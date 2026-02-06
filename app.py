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

# Quiz Data
QUIZZES = {
    "ramadan": {
        "title": "مسابقة رمضان - Ramadan Quiz",
        "questions": [
            {
                "ar": "ما معنى محيبس؟",
                "en": "What is the meaning of Muhaybes?",
                "options": [
                    {"ar": "لعبة رمضانية", "en": "A Ramadan game", "correct": True},
                    {"ar": "حلوى", "en": "A dessert", "correct": False},
                    {"ar": "تحية", "en": "A greeting", "correct": False},
                    {"ar": "صلاة", "en": "A prayer", "correct": False}
                ]
            },
            {
                "ar": "ما اسم المسحراتي في دولة المغرب؟",
                "en": "What is the name of the Mesaharati in Morocco?",
                "options": [
                    {"ar": "النفار", "en": "Al-Naffar", "correct": True},
                    {"ar": "المسحراتي", "en": "Al-Mesaharati", "correct": False},
                    {"ar": "الطبال", "en": "Al-Tabbal", "correct": False},
                    {"ar": "المنادي", "en": "Al-Munadi", "correct": False}
                ]
            },
            {
                "ar": "ما هو اكثر تقليد رمضاني مشهور في مصر؟",
                "en": "What is the most famous Ramadan tradition in Egypt?",
                "options": [
                    {"ar": "فانوس رمضان", "en": "Ramadan Lantern", "correct": True},
                    {"ar": "مدفع رمضان", "en": "Ramadan Cannon", "correct": False},
                    {"ar": "خيمة رمضان", "en": "Ramadan Tent", "correct": False},
                    {"ar": "موائد الرحمن", "en": "Charity Tables", "correct": False}
                ]
            },
            {
                "ar": "ما اسم احتفال رمضان بالكويت؟",
                "en": "What is the name of Ramadan celebration in Kuwait?",
                "options": [
                    {"ar": "القرقيعان", "en": "Gergean", "correct": True},
                    {"ar": "الناصفة", "en": "Al-Nasfa", "correct": False},
                    {"ar": "الحية بية", "en": "Haya Baya", "correct": False},
                    {"ar": "القرنقعوه", "en": "Garan'oh", "correct": False}
                ]
            },
            {
                "ar": "كم عدد أيام شهر رمضان؟",
                "en": "How many days is Ramadan?",
                "options": [
                    {"ar": "29 أو 30 يوم", "en": "29 or 30 days", "correct": True},
                    {"ar": "28 يوم", "en": "28 days", "correct": False},
                    {"ar": "31 يوم", "en": "31 days", "correct": False},
                    {"ar": "27 يوم", "en": "27 days", "correct": False}
                ]
            }
        ]
    },
    "chinese": {
        "title": "مسابقة السنة الصينية - Chinese New Year Quiz",
        "questions": [
            {
                "ar": "متى يحدث عيد الربيع؟",
                "en": "When does the Spring Festival happen?",
                "options": [
                    {"ar": "أول يوم في السنة القمرية", "en": "First day of Lunar New Year", "correct": True},
                    {"ar": "1 يناير", "en": "January 1st", "correct": False},
                    {"ar": "في فصل الربيع", "en": "In Spring season", "correct": False},
                    {"ar": "15 فبراير", "en": "February 15th", "correct": False}
                ]
            },
            {
                "ar": "ما اسم الوحش الذي كان يهاجم القرى؟",
                "en": "What's the name of the monster?",
                "options": [
                    {"ar": "نيان", "en": "Nian", "correct": True},
                    {"ar": "تنين", "en": "Dragon", "correct": False},
                    {"ar": "فينيكس", "en": "Phoenix", "correct": False},
                    {"ar": "شي", "en": "Xi", "correct": False}
                ]
            },
            {
                "ar": "لماذا كان القرويون يستخدمون الألعاب النارية؟",
                "en": "Why were the villagers using fireworks?",
                "options": [
                    {"ar": "لإخافة الوحش", "en": "To scare away the monster", "correct": True},
                    {"ar": "للاحتفال", "en": "For celebration", "correct": False},
                    {"ar": "للإضاءة", "en": "For lighting", "correct": False},
                    {"ar": "للتواصل", "en": "For communication", "correct": False}
                ]
            },
            {
                "ar": "ما اللون الذي يرمز للحظ في الثقافة الصينية؟",
                "en": "What color symbolizes luck in Chinese culture?",
                "options": [
                    {"ar": "الأحمر", "en": "Red", "correct": True},
                    {"ar": "الأصفر", "en": "Yellow", "correct": False},
                    {"ar": "الأخضر", "en": "Green", "correct": False},
                    {"ar": "الأزرق", "en": "Blue", "correct": False}
                ]
            },
            {
                "ar": "ما هو الطعام التقليدي في عيد الربيع؟",
                "en": "What is the traditional food during Spring Festival?",
                "options": [
                    {"ar": "الزلابية (دامبلينغ)", "en": "Dumplings", "correct": True},
                    {"ar": "الأرز", "en": "Rice", "correct": False},
                    {"ar": "النودلز", "en": "Noodles", "correct": False},
                    {"ar": "السوشي", "en": "Sushi", "correct": False}
                ]
            }
        ]
    }
}

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
