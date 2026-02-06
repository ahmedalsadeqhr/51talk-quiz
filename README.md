# 51Talk Quiz - Streamlit Version
## Quick Deploy Guide

---

## Deploy to Streamlit Cloud (FREE - 3 Minutes)

### Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Name it: `51talk-quiz`
3. Make it **Public**
4. Click **Create repository**

### Step 2: Upload Files

1. Click **"uploading an existing file"**
2. Drag these files:
   - `app.py`
   - `requirements.txt`
3. Click **Commit changes**

### Step 3: Deploy on Streamlit

1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Select your repository: `your-username/51talk-quiz`
4. Main file: `app.py`
5. Click **Deploy!**

Wait 1-2 minutes... Your app is live! 🎉

---

## URLs

After deployment, you'll get a URL like:
`https://your-app-name.streamlit.app`

### Admin Dashboard:
```
https://your-app-name.streamlit.app?mode=admin
```

### Player Page:
```
https://your-app-name.streamlit.app
```

### Direct Question Link:
```
https://your-app-name.streamlit.app?quiz=ramadan&q=0
```

---

## How to Run the Quiz

### Admin (You):
1. Open: `your-url?mode=admin`
2. Select quiz (Ramadan or Chinese New Year)
3. Select question number
4. Click **🚀 START Question**
5. Share the player URL or QR code
6. Watch responses come in real-time!
7. Winner is shown automatically
8. Click **Clear Responses** → Next question

### Players (500 Employees):
1. Open: `your-url`
2. Enter name
3. Wait for question (or scan direct QR)
4. Tap answer
5. First correct wins!

---

## Features

- ✅ **Real-time responses** - See answers as they come
- ✅ **Winner detection** - First correct answer highlighted
- ✅ **Bilingual** - Arabic + English
- ✅ **Mobile-friendly** - Works on all phones
- ✅ **Auto-refresh** - Updates every 2 seconds
- ✅ **No setup** - Just deploy and use
- ✅ **FREE hosting** - Streamlit Cloud

---

## Local Testing

```bash
cd streamlit_quiz
pip install -r requirements.txt
streamlit run app.py
```

Open:
- Player: http://localhost:8501
- Admin: http://localhost:8501?mode=admin

---

## Quiz Content

### Ramadan Quiz (5 Questions - Arabic)
1. ما معنى محيبس؟
2. ما اسم المسحراتي في المغرب؟
3. ما أشهر تقليد رمضاني في مصر؟
4. ما اسم احتفال رمضان بالكويت؟
5. كم عدد أيام رمضان؟

### Chinese New Year Quiz (5 Questions - English)
1. When does Spring Festival happen?
2. What's the monster's name?
3. Why use fireworks?
4. Lucky color?
5. Traditional food?

---

## Troubleshooting

### App won't deploy
- Make sure files are named exactly: `app.py`, `requirements.txt`
- Repository must be public

### Responses not showing
- Enable auto-refresh checkbox in admin
- Check that admin URL has `?mode=admin`

### Players see "waiting"
- Make sure you clicked START in admin
- Players need to refresh if they joined before START

---

## Cost

**$0** - Streamlit Cloud free tier includes:
- Unlimited apps
- 1GB resources
- Perfect for 500 users

---

*51Talk MENA Annual Gathering 2026*
