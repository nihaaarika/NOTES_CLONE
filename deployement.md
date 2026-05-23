# Setup & Deployment Guide

## 🖥️ Local Setup (Your Computer)

### For Windows Users

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 or higher
   - During installation, **CHECK** "Add Python to PATH"
   - Click "Install Now"

2. **Download the app**
   - Download the project folder
   - Extract it to a location you can find easily (e.g., Documents)

3. **Run the app**
   - Open the folder
   - Double-click `start.bat`
   - Your browser will open automatically
   - Your app is running! 🎉

### For Mac Users

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Download the macOS installer
   - Run it and follow the installation steps

2. **Download the app**
   - Download the project folder
   - Extract it to a location you can find

3. **Open Terminal**
   - Press Cmd + Space
   - Type "Terminal" and press Enter

4. **Run the app**
   ```bash
   cd /path/to/notion-clone
   bash start.sh
   ```
   - Your browser will open automatically

### For Linux Users

1. **Install Python** (if not already installed)
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-venv python3-pip
   ```

2. **Download and extract the app**
   ```bash
   cd ~/your-folder/notion-clone
   ```

3. **Run the app**
   ```bash
   bash start.sh
   ```

---

## ☁️ Deploy to Streamlit Cloud (Free)

This will make your app accessible from anywhere with a URL!

### Prerequisites
- GitHub account (create free at github.com)
- Git installed on your computer

### Steps

1. **Create a GitHub repository**
   - Go to github.com and sign in
   - Click "New" to create a new repository
   - Name it "notion-clone"
   - Choose "Public"
   - Click "Create repository"

2. **Upload your code**
   ```bash
   # In your project folder
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/notion-clone.git
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Connect your GitHub account
   - Select your repository (notion-clone)
   - Branch: main
   - Main file path: app.py
   - Click "Deploy"
   - Wait 2-3 minutes for deployment
   - Your app has a public URL! 🚀

4. **Share your app**
   - Copy the URL from Streamlit Cloud
   - Share with anyone!
   - They don't need Python or anything installed

### Environment Variables on Streamlit Cloud

If you want to use OpenAI API:

1. Go to your app settings on Streamlit Cloud
2. Click "Secrets"
3. Add your keys:
   ```
   OPENAI_API_KEY = "sk-your-key-here"
   ```
4. Redeploy your app

---

## 🐳 Docker Deployment

Run your app in a containerized environment.

### Prerequisites
- Docker installed (https://www.docker.com/get-started)

### Steps

1. **Build the Docker image**
   ```bash
   docker build -t notion-clone .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 notion-clone
   ```

3. **Access the app**
   - Open http://localhost:8501 in your browser

### Deploy Docker to Production

1. **Create Docker Hub account** (free at hub.docker.com)

2. **Tag your image**
   ```bash
   docker tag notion-clone YOUR-USERNAME/notion-clone:latest
   ```

3. **Push to Docker Hub**
   ```bash
   docker login
   docker push YOUR-USERNAME/notion-clone:latest
   ```

4. **Deploy to cloud services**
   - AWS, Google Cloud, Azure, Heroku all support Docker
   - Documentation varies by provider

---

## 🖱️ Create Desktop App (Windows/Mac)

Convert your app to a standalone application.

### Prerequisites
```bash
pip install pyinstaller
```

### Steps

1. **Create a launcher script** (`run_app.py`)
   ```python
   import os
   import sys
   import subprocess
   
   if __name__ == "__main__":
       os.system("streamlit run app.py")
   ```

2. **Build executable**
   ```bash
   pyinstaller --onefile --windowed run_app.py
   ```

3. **Find your app**
   - Windows: `dist/run_app.exe`
   - Mac: `dist/run_app`
   - Double-click to run!

---

## 🔧 Advanced Configuration

### Customize Streamlit Port
Edit `.streamlit/config.toml`:
```toml
[server]
port = 9000
```

Then run:
```bash
streamlit run app.py --server.port 9000
```

### Enable Wide Layout by Default
Edit `.streamlit/config.toml`:
```toml
[logger]
level = "info"

[client]
showErrorDetails = true
```

### Dark Mode
Edit `.streamlit/config.toml`:
```toml
[theme]
base = "dark"
primaryColor = "#6366f1"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#e2e8f0"
```

---

## 📊 Performance Tips

### Optimize for Production

1. **Reduce model sizes**
   - Use `distilbert` instead of `bert`
   - Use `gpt2` instead of `gpt-3`

2. **Cache expensive operations**
   ```python
   @st.cache_data
   def load_model():
       return transformer_model
   ```

3. **Limit concurrent users**
   - Streamlit Cloud: Use Pro plan for more resources
   - Self-hosted: Use gunicorn with multiple workers

4. **Database optimization**
   - Create indexes on frequently searched columns
   - Regular backups

---

## 🆘 Troubleshooting Deployment

### App won't start on Streamlit Cloud
1. Check your GitHub repository is public
2. Verify all dependencies are in requirements.txt
3. Check Streamlit Cloud logs for errors
4. Redeploy the app

### Database errors
1. Local: Delete `data/notes.db` and restart
2. Cloud: Database resets on redeployment (use backup)
3. Production: Use PostgreSQL instead of SQLite

### Memory issues
1. Reduce DataFrame sizes
2. Clear cache more frequently
3. Use cloud services with more RAM

### API key not working
1. Check key format (should start with `sk-`)
2. Verify key has sufficient balance
3. Check environment variable name matches code

---

## 🔐 Security Best Practices

1. **Never commit API keys**
   - Use `.env` for local development
   - Use Secrets on Streamlit Cloud
   - Never share `.env` files

2. **Backup your data**
   - Regular exports to JSON/CSV
   - Cloud backup solutions

3. **Database security**
   - Limit database file permissions
   - Use SQLite for local, PostgreSQL for cloud

4. **HTTPS only**
   - Always use HTTPS URLs
   - Streamlit Cloud provides this automatically

---

## 📈 Monitoring & Maintenance

### Local Development
- Regular backups of `data/notes.db`
- Monitor app performance
- Update dependencies monthly

### Production (Streamlit Cloud)
- Check deployment logs regularly
- Monitor app usage stats
- Update code when dependencies need patches

### Self-Hosted
- Monitor server resources (CPU, RAM, disk)
- Set up automated backups
- Enable access logs
- Use monitoring tools (New Relic, DataDog, etc.)

---

## 🚀 Next Steps

1. **Enhance features**
   - Add search filters
   - Implement user accounts
   - Add multi-user sync

2. **Mobile app**
   - Use Streamlit mobile or React Native
   - Create iOS/Android versions

3. **Advanced AI**
   - Fine-tune models for your use case
   - Add voice-to-text
   - Implement advanced NLP

4. **Integration**
   - Google Drive sync
   - Slack integration
   - Zapier automation

---

## 📞 Getting Help

- **Streamlit docs:** https://docs.streamlit.io
- **Python docs:** https://docs.python.org
- **GitHub Issues:** Check existing issues
- **Stack Overflow:** Tag with "streamlit"

---

Good luck with your deployment! 🎉