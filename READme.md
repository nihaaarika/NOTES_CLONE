# 📔 Notion Clone - Professional Note-Taking App

A beautiful, feature-rich note-taking and productivity application built with Python and Streamlit. Keep your notes, manage your todos, maintain your diary, and get AI-powered writing suggestions—all in one elegant place.

## ✨ Features

### 📝 Notes
- Create rich text notes with custom colors
- Tag system for organization
- Pin important notes
- Search and filter functionality
- Grid or list view options

### ✓ Todo List
- Create tasks with due dates
- Priority levels (high, medium, low)
- Task categories
- Mark tasks as complete
- Track progress with statistics

### 📖 Diary
- Personal journaling with date navigation
- Mood tracking (happy, sad, neutral, excited, stressed, calm)
- Tag your entries
- View past entries timeline
- Statistics and insights

### ✨ AI Writing Assistant
- Continue writing with AI suggestions
- Brainstorm ideas on any topic
- Check grammar and style
- Summarize long texts
- Generate catchy titles
- Fallback templates + OpenAI API support

### 🎨 Customization
- Light/Dark/Auto themes
- Custom accent colors
- Font size adjustment
- Auto-save option

### 💾 Data Management
- Export as JSON or CSV
- Local SQLite database
- Backup and restore
- Data statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the repository**
```bash
cd notion-clone
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Notes
1. Click **"✨ New Note"** to create a note
2. Add a title, content, and optional tags
3. Choose a color for visual organization
4. Click **"💾 Save Note"** to save
5. Use search to find notes by title or content
6. Pin important notes to keep them at the top

### Todo List
1. Click **"➕ Add New Task"**
2. Enter task details: title, priority, due date, category
3. Organize by priority or category
4. Check off tasks when complete
5. View statistics and pending tasks

### Diary
1. Select a date using the date picker
2. Write your entry
3. Select your mood
4. Add tags for easy searching
5. View your mood distribution and word count
6. Browse past entries in the timeline

### AI Assistant
1. Navigate to **"✨ AI Assistant"**
2. Choose from 5 features:
   - **Continue Writing** - Finish your thoughts
   - **Brainstorm** - Generate ideas
   - **Grammar Check** - Improve your writing
   - **Summarize** - Condense long texts
   - **Generate Title** - Create catchy titles

### Settings
- **Appearance** - Customize theme and colors
- **Data** - Export, backup, and manage your data
- **About** - Learn about the app
- **Advanced** - Database and system info

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory for optional settings:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

If you add an OpenAI API key, the AI Assistant will use higher-quality models instead of fallback templates.

## 📁 Project Structure

```
notion-clone/
├── app.py                      # Main application file
├── database.py                 # SQLite database handler
├── ai_generator.py            # AI text generation module
├── pages/
│   ├── notes.py              # Notes management
│   ├── todos.py              # Todo list management
│   ├── diary.py              # Diary/journaling
│   ├── ai_assistant.py       # AI features
│   └── settings.py           # App settings
├── data/
│   └── notes.db              # SQLite database (created on first run)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🎯 Key Classes

### NotesDatabase (`database.py`)
Manages all data persistence:
- `create_note()` - Create a new note
- `get_all_notes()` - Retrieve all notes
- `update_note()` - Update existing note
- `delete_note()` - Delete a note
- And similar methods for todos and diary entries

### AITextGenerator (`ai_generator.py`)
Handles AI-powered text generation:
- `generate_continuation()` - Continue writing
- `brainstorm_ideas()` - Generate brainstorm items
- `check_grammar()` - Grammar checking
- `summarize()` - Text summarization
- `generate_title()` - Title generation

Supports multiple backends:
- **OpenAI API** - Best quality (requires API key)
- **Local Transformers** - Good quality, offline
- **Templates** - Quick fallbacks

## 🎨 Design Features

### Professional Aesthetics
- Clean, modern interface
- Gradient accents
- Smooth animations
- Responsive layout
- Dark/Light mode support

### Color Scheme
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Accent: `#ec4899` (Pink)
- Customizable via settings

### Typography
- Custom Geist font family
- Clear hierarchy
- Readable line heights
- Monospace for code

## 💡 Tips & Best Practices

### For Notes
- Use tags to organize by topic
- Color-code by importance or project
- Pin your most important notes
- Use the search function frequently

### For Todos
- Set realistic due dates
- Use priorities wisely
- Group similar tasks in categories
- Review completed tasks for motivation

### For Diary
- Write regularly for better insights
- Use mood tracking to identify patterns
- Tag entries by topic (work, personal, health)
- Review past entries for reflection

### For AI Assistant
- Provide context for better results
- Use appropriate tone settings
- Try multiple times for variations
- Combine suggestions with your own writing

## 🐛 Troubleshooting

### App won't start
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run again
streamlit run app.py
```

### Database issues
- Delete `data/notes.db` to reset database
- Settings → Advanced → Repair Database
- Use Settings → Data to export before deleting

### AI features not working
- Check internet connection for API calls
- Verify OpenAI API key if using paid features
- Use fallback template mode if API is unavailable

### Streamlit bugs
- Clear browser cache (Ctrl+Shift+Del)
- Restart Streamlit (Ctrl+C, then `streamlit run app.py`)
- Update Streamlit: `pip install --upgrade streamlit`

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Click "Deploy"

### Deploy Locally with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t notion-clone .
docker run -p 8501:8501 notion-clone
```

### Create Desktop App

Using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile app.py
# Creates standalone .exe or .app file
```

## 📊 Database Schema

### Notes Table
- `id` - Primary key
- `title` - Note title
- `content` - Note body
- `tags` - JSON array of tags
- `color` - Hex color code
- `pinned` - Boolean flag
- `created_at` - Timestamp
- `updated_at` - Timestamp

### Todos Table
- `id` - Primary key
- `title` - Task title
- `description` - Task details
- `completed` - Boolean flag
- `due_date` - Date
- `priority` - low/medium/high
- `category` - Text category
- `created_at` - Timestamp
- `updated_at` - Timestamp

### Diary Entries Table
- `id` - Primary key
- `entry_date` - Date (unique)
- `title` - Entry title
- `content` - Entry body
- `mood` - Mood indicator
- `tags` - JSON array
- `created_at` - Timestamp
- `updated_at` - Timestamp

## 🔐 Privacy & Security

- **Local Storage** - All data stored locally in SQLite
- **No Cloud Sync** - Your data stays on your machine
- **No Tracking** - No analytics or tracking features
- **Optional API** - Only if you choose to enable AI features

## 📝 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - App framework
- [Python](https://www.python.org/) - Programming language
- [SQLite](https://www.sqlite.org/) - Database
- [OpenAI](https://openai.com/) - AI API (optional)
- [Hugging Face](https://huggingface.co/) - ML models

## 📧 Support & Feedback

Have suggestions or found a bug? Feel free to:
- Create an issue on GitHub
- Reach out via email
- Submit feature requests

---

**Happy note-taking! 📝✨**

Made with ❤️ for productivity enthusiasts