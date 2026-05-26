# 🔒 Secret Diary

A professional, feature-rich diary app built with Streamlit. Keep your thoughts safe with password protection.

## Features

- 📝 **Journaling** - Write with custom fonts (100+ Google Fonts), colors, and background themes
- 💬 **Secret Talk** - Record voice notes and transcriptions
- ✨ **Manifestations** - Track and manage your goals
- 📅 **Everyday Notes** - Quick daily notes with date selection
- 💳 **Billing** - Subscription management (coming soon)

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## First Time Setup

1. Create account (name → email → phone → password)
2. Password must be 8+ characters with uppercase + digit
3. Login on subsequent sessions with email + password

## Project Structure

```
.
├── app.py                    # Main entry point (setup/login/routing)
├── modules/
│   └── database.py          # SQLite database handler
├── pages/
│   ├── journaling.py        # Rich text editor with styling
│   ├── secret_talk.py       # Voice notes
│   ├── manifestations.py     # Goal tracker
│   ├── everyday_notes.py     # Daily notes
│   └── billing.py           # Billing info
├── requirements.txt
├── config.toml
├── start.sh                 # Linux/Mac launcher
└── start.bat                # Windows launcher
```

## Tech Stack

- **Frontend**: Streamlit
- **Database**: SQLite
- **Security**: bcrypt (password hashing)
- **Styling**: Custom CSS + Google Fonts

## Database Schema

- **users** - User accounts with hashed passwords
- **journal_entries** - Journal with font/color/theme customization
- **voice_notes** - Voice recordings with transcriptions
- **manifestations** - Goals and aspirations
- **everyday_notes** - Daily notes by date

## Deployment

Run as standalone app:
```bash
./start.sh        # Linux/Mac
./start.bat       # Windows
```

---

Made with ❤️ for personal journaling and manifestation.
