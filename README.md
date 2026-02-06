# 51Talk MENA Live Quiz System
## Annual Gathering 2026

A real-time quiz system for 500+ employees with live winner detection, built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [Deployment](#-deployment)
- [Usage Guide](#-usage-guide)
  - [Admin Mode](#1-admin-mode)
  - [Presentation Mode](#2-presentation-mode)
  - [Player Mode](#3-player-mode)
- [Event Day Workflow](#-event-day-workflow)
- [Quiz Content](#-quiz-content)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Technical Details](#-technical-details)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏆 **First Correct Wins** | Automatically detects the fastest correct answer |
| 📊 **Real-time Updates** | Live response tracking with auto-refresh |
| 📺 **Presentation Mode** | Big screen view for projector display |
| 🌐 **Bilingual** | Full Arabic + English support |
| 📱 **Mobile Friendly** | Optimized for smartphone answering |
| 👥 **500+ Users** | Handles large audiences |
| 💰 **100% Free** | No paid subscriptions required |
| 🚀 **Easy Setup** | Deploy in under 5 minutes |

---

## 🎬 Demo

### Three Views

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ADMIN                PRESENTATION              PLAYER         │
│   (Your Laptop)        (Big Screen)             (Phones)        │
│                                                                 │
│   ┌───────────┐        ┌───────────┐          ┌───────────┐    │
│   │ Controls  │        │           │          │   ┌───┐   │    │
│   │ Questions │   ──►  │  Question │    ◄──   │   │📱│   │    │
│   │ Responses │        │  Winner   │          │   └───┘   │    │
│   │ Stats     │        │  Stats    │          │  Answer   │    │
│   └───────────┘        └───────────┘          └───────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Testing

```bash
# Clone the repository
git clone https://github.com/ahmedalsadeqhr/51talk-quiz.git
cd 51talk-quiz

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Access the Views

| Mode | URL |
|------|-----|
| Player | http://localhost:8501 |
| Admin | http://localhost:8501?mode=admin |
| Presentation | http://localhost:8501?mode=present |

---

## ☁️ Deployment

### Deploy to Streamlit Cloud (Recommended)

1. **Fork/Push to GitHub**
   - Ensure `app.py` and `requirements.txt` are in your repository

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"

3. **Configure**
   - Repository: `your-username/51talk-quiz`
   - Branch: `master`
   - Main file: `app.py`

4. **Deploy**
   - Click "Deploy!"
   - Wait 1-2 minutes

5. **Your URLs**
   ```
   https://your-app-name.streamlit.app              (Player)
   https://your-app-name.streamlit.app?mode=admin   (Admin)
   https://your-app-name.streamlit.app?mode=present (Presentation)
   ```

### Alternative: Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku master
```

---

## 📖 Usage Guide

### 1. Admin Mode

**URL:** `your-app.streamlit.app?mode=admin`

The control center for managing the quiz.

#### Interface Overview

```
┌────────────────────────────────────────────────────────────┐
│  🎯 Quiz Admin Dashboard                                   │
├──────────────┬─────────────────────────────────────────────┤
│              │                                             │
│  📋 Quiz     │  ┌─────────────────────────────────────┐   │
│  Selection   │  │        Current Question              │   │
│              │  │                                       │   │
│  • Ramadan   │  │   ما معنى محيبس؟                     │   │
│  • Chinese   │  │   What is the meaning of Muhaybes?   │   │
│              │  └─────────────────────────────────────┘   │
│  📡 Broadcast│                                             │
│              │  ┌─────────────────────────────────────┐   │
│  [🚀 START]  │  │  🏆 WINNER: Ahmed (2.34s)            │   │
│  [⏹ STOP]   │  └─────────────────────────────────────┘   │
│              │                                             │
│  [🗑 Clear]  │  Total: 45  ✓ Correct: 12  ✗ Wrong: 33    │
│              │                                             │
│  📱 Link     │  📊 Live Responses                         │
│  [Copy URL]  │  1. 🏆 Ahmed - Correct - 2.34s             │
│              │  2. ✓ Sara - Correct - 3.12s               │
│              │  3. ✗ Omar - Wrong - 1.89s                 │
│  🔄 Auto-    │  4. ✓ Fatima - Correct - 4.56s             │
│  refresh ✓   │  ...                                        │
│              │                                             │
└──────────────┴─────────────────────────────────────────────┘
```

#### Controls

| Control | Function |
|---------|----------|
| **Quiz Selection** | Choose between Ramadan or Chinese New Year quiz |
| **Question Selection** | Select which question (1-5) to display |
| **🚀 START Question** | Broadcast question to all players |
| **⏹ STOP Question** | End the current question |
| **🗑 Clear Responses** | Reset all answers for current question |
| **📱 Player Link** | Copy URL for players to join |
| **🔄 Auto-refresh** | Automatically update responses every 2 seconds |

---

### 2. Presentation Mode

**URL:** `your-app.streamlit.app?mode=present`

Optimized for projection on big screens (7m x 3m recommended).

#### Active Question View

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      🔴 LIVE                                    │
│           🎯 مسابقة رمضان - Ramadan Quiz                        │
│                  Question 1 of 5                                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                     ما معنى محيبس؟                              │
│                                                                 │
│              What is the meaning of Muhaybes?                   │
│                                                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                   🏆 WINNER! 🏆                                 │
│                                                                 │
│                      Ahmed                                      │
│                                                                 │
│                   ⚡ 2.34 seconds                               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│      [ 45 ]           [ 12 ]           [ 33 ]                  │
│      Total          ✓ Correct        ✗ Wrong                   │
│                                                                 │
│                    🏅 Top Correct Answers                       │
│                    🥇 Ahmed - 2.34s                             │
│                    🥈 Sara - 3.12s                              │
│                    🥉 Fatima - 4.56s                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Waiting Screen

When no question is active:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                                                                 │
│                   🎯 51Talk MENA Quiz                           │
│                   Annual Gathering 2026                         │
│                                                                 │
│                          ⏳                                     │
│                                                                 │
│              Waiting for the next question...                   │
│              في انتظار السؤال التالي                            │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3. Player Mode

**URL:** `your-app.streamlit.app` (default)

Mobile-optimized interface for participants.

#### Registration Screen

```
┌─────────────────────┐
│                     │
│   🎯 Live Quiz      │
│   مسابقة مباشرة     │
│                     │
│   Fastest correct   │
│   answer wins!      │
│                     │
├─────────────────────┤
│                     │
│   Enter your name   │
│   أدخل اسمك         │
│                     │
│   ┌───────────────┐ │
│   │  Your name    │ │
│   └───────────────┘ │
│                     │
│   ┌───────────────┐ │
│   │ Join Quiz     │ │
│   │ انضم للمسابقة │ │
│   └───────────────┘ │
│                     │
└─────────────────────┘
```

#### Question Screen

```
┌─────────────────────┐
│                     │
│  Ramadan Quiz       │
│  Question 1/5       │
│                     │
│  ⏱ Time: 15s       │
│  ████████░░░░░░░░  │
│                     │
├─────────────────────┤
│                     │
│   ما معنى محيبس؟    │
│                     │
│   What is the       │
│   meaning of        │
│   Muhaybes?         │
│                     │
├─────────────────────┤
│                     │
│ ┌─────────────────┐ │
│ │ A. لعبة رمضانية │ │
│ │    Ramadan game │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ B. حلوى         │ │
│ │    A dessert    │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ C. تحية         │ │
│ │    A greeting   │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ D. صلاة         │ │
│ │    A prayer     │ │
│ └─────────────────┘ │
│                     │
└─────────────────────┘
```

---

## 🎪 Event Day Workflow

### Before the Event

1. **Test the system** with a few colleagues
2. **Set up screens:**
   - Laptop for Admin
   - Projector for Presentation mode
3. **Prepare prizes** for winners
4. **Print backup QR codes** (optional)

### During the Event

```
Step 1: Admin selects Quiz (Ramadan/Chinese New Year)
           │
           ▼
Step 2: Admin selects Question (1-5)
           │
           ▼
Step 3: Admin clicks "🚀 START Question"
           │
           ├──► Presentation screen shows question
           │
           ▼
Step 4: Announce "Scan the QR code to answer!"
           │
           ▼
Step 5: Players scan QR → Enter name → Answer
           │
           ▼
Step 6: Winner appears on Presentation screen
           │
           ▼
Step 7: Admin announces winner, gives prize
           │
           ▼
Step 8: Admin clicks "🗑 Clear Responses"
           │
           ▼
Step 9: Repeat from Step 2 for next question
```

### Timing Suggestions

| Segment | Duration |
|---------|----------|
| Question display | 5 seconds |
| Answer time | 20 seconds |
| Winner announcement | 30 seconds |
| Prize giving | 1 minute |
| **Total per question** | **~2 minutes** |
| **Full quiz (5 questions)** | **~10 minutes** |

---

## 📝 Quiz Content

### Ramadan Quiz (Arabic Focus)

| # | Question (AR) | Question (EN) | Answer |
|---|---------------|---------------|--------|
| 1 | ما معنى محيبس؟ | What is the meaning of Muhaybes? | لعبة رمضانية (A Ramadan game) |
| 2 | ما اسم المسحراتي في دولة المغرب؟ | What is the Mesaharati called in Morocco? | النفار (Al-Naffar) |
| 3 | ما هو اكثر تقليد رمضاني مشهور في مصر؟ | Most famous Ramadan tradition in Egypt? | فانوس رمضان (Ramadan Lantern) |
| 4 | ما اسم احتفال رمضان بالكويت؟ | Ramadan celebration name in Kuwait? | القرقيعان (Gergean) |
| 5 | كم عدد أيام شهر رمضان؟ | How many days is Ramadan? | 29 أو 30 يوم (29 or 30 days) |

### Chinese New Year Quiz (English Focus)

| # | Question (EN) | Question (AR) | Answer |
|---|---------------|---------------|--------|
| 1 | When does the Spring Festival happen? | متى يحدث عيد الربيع؟ | First day of Lunar New Year |
| 2 | What's the name of the monster? | ما اسم الوحش؟ | Nian |
| 3 | Why were villagers using fireworks? | لماذا استخدموا الألعاب النارية؟ | To scare away the monster |
| 4 | What color symbolizes luck? | ما لون الحظ؟ | Red |
| 5 | Traditional Spring Festival food? | الطعام التقليدي؟ | Dumplings |

---

## ⚙️ Customization

### Adding New Questions

Edit the `QUIZZES` dictionary in `app.py`:

```python
QUIZZES = {
    "your_quiz_id": {
        "title": "Your Quiz Title - عنوان المسابقة",
        "questions": [
            {
                "ar": "السؤال بالعربية",
                "en": "Question in English",
                "options": [
                    {"ar": "الإجابة الصحيحة", "en": "Correct answer", "correct": True},
                    {"ar": "إجابة خاطئة", "en": "Wrong answer", "correct": False},
                    {"ar": "إجابة خاطئة", "en": "Wrong answer", "correct": False},
                    {"ar": "إجابة خاطئة", "en": "Wrong answer", "correct": False}
                ]
            },
            # Add more questions...
        ]
    }
}
```

### Changing Timer Duration

Find this line in the player mode section:

```python
remaining = max(0, 20 - int(elapsed))  # Change 20 to desired seconds
```

### Customizing Colors

Edit the CSS in the `st.markdown("""<style>...</style>""")` section:

```css
/* Main colors */
--primary-gold: #FFD700;
--background-dark: #1a1a2e;
--correct-green: #00ff00;
--wrong-red: #ff6b6b;
```

### Adding Sound Effects

Streamlit doesn't support audio natively, but you can:
1. Play sounds from the presentation computer separately
2. Use browser extensions for sound effects

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **App won't start** | Check Python version (3.8+), reinstall requirements |
| **Database errors** | Delete `quiz_responses.db` to reset |
| **Responses not showing** | Enable auto-refresh checkbox in admin |
| **Players see "waiting"** | Make sure admin clicked START |
| **Slow performance** | Check internet connection, reduce refresh rate |

### Database Reset

```bash
# Delete the database file to start fresh
rm quiz_responses.db
# or on Windows
del quiz_responses.db
```

### Logs

```bash
# View Streamlit logs
streamlit run app.py --logger.level=debug
```

### Testing Multiple Users

Open multiple browser tabs/incognito windows to simulate multiple players.

---

## 🔬 Technical Details

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Streamlit App                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│   │   Admin     │   │   Present   │   │   Player    │       │
│   │   Mode      │   │   Mode      │   │   Mode      │       │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘       │
│          │                 │                 │               │
│          └────────────┬────┴────────────────┘               │
│                       │                                      │
│                       ▼                                      │
│              ┌─────────────────┐                            │
│              │   SQLite DB     │                            │
│              │                 │                            │
│              │  • responses    │                            │
│              │  • active_q     │                            │
│              └─────────────────┘                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Database Schema

```sql
-- Responses table
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,           -- Player name
    quiz TEXT,           -- Quiz ID (ramadan/chinese)
    question INTEGER,    -- Question number (0-4)
    correct INTEGER,     -- 1 = correct, 0 = wrong
    time_ms INTEGER,     -- Response time in milliseconds
    timestamp TEXT       -- ISO format timestamp
);

-- Active question table
CREATE TABLE active_question (
    id INTEGER PRIMARY KEY,
    quiz TEXT,           -- Current quiz ID
    question INTEGER,    -- Current question number
    active INTEGER,      -- 1 = active, 0 = inactive
    start_time TEXT      -- When question was activated
);
```

### File Structure

```
51talk-quiz/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── quiz_responses.db  # SQLite database (created at runtime)
```

---

## 📄 License

MIT License - Feel free to modify and use for your events!

---

## 🙏 Credits

- **Built for:** 51Talk MENA Annual Gathering 2026
- **Framework:** [Streamlit](https://streamlit.io)
- **Developed with:** Claude AI

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Contact the event organizers

---

*Made with ❤️ for 51Talk MENA*
