# 🎯 Getting Started Guide

**Welcome!** This guide will get you from zero to a running app in 5 minutes.

---

## 📋 What You Need

- A computer (Windows, Mac, or Linux)
- Python 3.8 or higher (free from python.org)
- That's it! Everything else is included.

---

## 🚀 5-Minute Quick Start

### Step 1: Install Python

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download "Python 3.11" (or newer)
3. Run the installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"

**Mac:**
1. Go to https://www.python.org/downloads/
2. Download "Python 3.11 for macOS"
3. Run the installer
4. Follow the steps

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

### Step 2: Download the App

1. Download the `notion-clone` folder
2. Extract it to a location you can find (like Documents)
3. Open the folder

### Step 3: Run the App

**Windows:**
- Double-click `start.bat`
- Your browser will open automatically

**Mac/Linux:**
- Open Terminal
- Type: `cd /path/to/notion-clone`
- Type: `bash start.sh`
- Press Enter

### Step 4: Wait for App to Start
```
⠙ Running on local URL:  http://localhost:8501
```

### Step 5: Use the App!
Your browser opens automatically. Start creating notes! 🎉

---

## ❓ Troubleshooting

### "Python not found"
- You didn't install Python or didn't check "Add to PATH"
- Restart your computer after installing Python
- Try `python3` instead of `python`

### "Port 8501 is already in use"
- Close other apps using Streamlit
- Or use a different port: `streamlit run app.py --server.port 9000`

### "ModuleNotFoundError"
- The dependencies didn't install properly
- Try: `pip install -r requirements.txt`
- Then: `streamlit run app.py`

### "Permission denied" (Mac/Linux)
- Make the script executable: `chmod +x start.sh`
- Then: `bash start.sh`

---

## 🎓 How to Use the App

### 📝 Notes
1. Click **"✨ New Note"**
2. Type a title and content
3. Pick a color
4. Add tags (optional)
5. Click **"💾 Save Note"**

### ✓ Todo List
1. Click **"➕ Add New Task"**
2. Enter task details
3. Set priority and due date
4. Click **"💾 Add Task"**
5. Check off when done

### 📖 Diary
1. Pick a date
2. Write your entry
3. Select your mood
4. Click **"💾 Save Entry"**
5. View past entries in timeline

### ✨ AI Assistant
1. Go to **"✨ AI Assistant"**
2. Choose a feature (Continue, Brainstorm, etc.)
3. Paste or write some text
4. Click the action button
5. Get AI suggestions!

### ⚙️ Settings
1. Go to **"⚙️ Settings"**
2. Change theme, colors, font size
3. Export your data
4. View statistics

---

## 💾 Your Data is Safe

- ✅ All data saved locally on YOUR computer
- ✅ No cloud sync (unless you deploy)
- ✅ You can export anytime
- ✅ Never shared with anyone

To backup:
1. Go to Settings → Data
2. Click "Export as JSON"
3. Save the file somewhere safe

---

## 🌐 Share Your App (Optional)

Want to share with others? Deploy to cloud for free!

### Streamlit Cloud (Easiest)

1. **Push to GitHub** (instructions in DEPLOYMENT.md)
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Click "Deploy"
6. Get a public URL instantly!

Anyone can use it without installing anything. 🚀

---

## 📱 Use on Phone

The app works on phones too!

1. Deploy to Streamlit Cloud (see above)
2. Open the URL on your phone
3. Use just like on desktop

---

## 🔑 Optional: AI Features

The app works great without this, but for better AI:

1. Get OpenAI API key at https://platform.openai.com
2. In Settings → AI Settings, add your key
3. AI features now use advanced models

(This costs money, so it's completely optional)

---

## 📚 Learn More

- **How to use:** See README.md
- **Deploy to web:** See DEPLOYMENT.md
- **File structure:** See FILE_STRUCTURE.md
- **Project overview:** See PROJECT_SUMMARY.md

---

## 🎓 Customization Examples

### Change the theme color
1. Go to Settings
2. Click "Accent Color"
3. Pick a new color
4. Click "Save"

### Export your notes
1. Go to Settings → Data
2. Click "Export as JSON" or "Export as CSV"
3. Download and save

### Add more features
Edit the Python files and restart the app!

---

## 🆘 Still Need Help?

### Step-by-step video
(Create your own YouTube tutorial!)

### Common issues
- **App won't start:** Close and run again, clear cache
- **Can't find file:** Extract the folder properly
- **Lost data:** Check data/notes.db exists
- **Can't save:** Check folder permissions

### Restart the app
1. Press Ctrl+C in terminal
2. Run start.sh or start.bat again

---

## 🎯 Your First Session

**Suggested 10-minute walkthrough:**

1. ✅ Create a note (2 min)
2. ✅ Create a todo (2 min)
3. ✅ Write a diary entry (3 min)
4. ✅ Try AI assistant (2 min)
5. ✅ Change theme (1 min)

That's it! You now know how to use everything. 🎉

---

## 🚀 What's Next?

After running the app:

1. **Create content** - Add your own notes, todos, diary
2. **Customize** - Change colors, fonts, themes
3. **Deploy** - Share with friends on Streamlit Cloud
4. **Extend** - Add your own features (Python knowledge needed)

---

## 💡 Pro Tips

1. **Search is powerful** - Use it to find notes quickly
2. **Colors organize** - Use different colors for different types
3. **Tags organize further** - Tag by project or topic
4. **Export regularly** - Backup your data
5. **Dark mode helps** - Easier on eyes at night

---

## 📊 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|------------|
| Python | 3.8 | 3.11+ |
| RAM | 2 GB | 4 GB+ |
| Disk | 500 MB | 1 GB |
| Network | Optional | For deployment |
| Browser | Chrome/Firefox | Latest version |

---

## 🎓 Learn by Doing

Best way to learn:

1. **Create a note** - Just try it
2. **Delete it** - Oops, gone forever (just kidding, you can undo)
3. **Try something** - Click buttons, see what happens
4. **Break something** - It's fine, restart the app
5. **Fix it** - You just learned!

No way to break it permanently. Experiment!

---

## 🔐 Data Security

Your data:
- Lives only on your computer
- Never sent to external servers (unless you add API key)
- You own it completely
- You can export it anytime
- You can delete it anytime

No ads, tracking, or data collection. Pure privacy. ✅

---

## 💬 Keyboard Shortcuts

Standard Streamlit shortcuts:

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Stop the app |
| Cmd+R | Refresh page |
| F12 | Developer tools |
| Ctrl+L | Clear console |

---

## 🎨 Customization Ideas

Once comfortable, try:

1. Change the app title
2. Add custom colors
3. Add new note categories
4. Change mood options
5. Add priority levels

See Python code comments for where to modify!

---

## 📞 Getting Help

1. **Check README.md** - User guide
2. **Check DEPLOYMENT.md** - Setup guide
3. **Check FILE_STRUCTURE.md** - File organization
4. **Check Streamlit docs** - https://docs.streamlit.io
5. **Google the error** - Usually has a solution

---

## 🎉 You're Ready!

Now go run the app and enjoy! You've got a powerful productivity tool at your fingertips.

**Next step: Run `start.bat` (Windows) or `bash start.sh` (Mac/Linux)**

---

### Questions?
- It's all in the other .md files
- Or Google the specific problem
- Streamlit docs are excellent

**Happy note-taking!** 📝✨

---

Made with ❤️ for beginners