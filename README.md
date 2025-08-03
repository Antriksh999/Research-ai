# 🔬 Research Content Extractor Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

A powerful AI-powered research assistant that generates comprehensive, academic-style reports on any topic using multiple search tools and Google Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Analysis** - Google Gemini 2.0 Flash integration
- 📚 **Multiple Data Sources** - Wikipedia and DuckDuckGo search
- 📄 **Professional Reports** - Academic-style formatting
- 💾 **Export Options** - Download as Markdown or Text
- 🎯 **Easy to Use** - Simple Streamlit interface

## 🚀 Deploy on Streamlit Cloud

### Quick Deployment
1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Click "New app"**
4. **Connect your GitHub account**
5. **Select this repository**
6. **Set main file path:** `app.py`
7. **Add your API key in secrets** (see Configuration below)
8. **Click "Deploy"**

## ⚙️ Configuration

### Required API Key
You need a Google Gemini API key:

1. **Get API Key:** Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **For Streamlit Cloud:** Add to your app's secrets:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/research-ai.git
cd research-ai

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run locally
streamlit run app.py
```

## 🎯 Usage

1. Enter your research topic
2. Click generate to create a comprehensive report
3. Download or save your research report

### Example Topics
- "The impact of artificial intelligence on healthcare"
- "Sustainable energy solutions for urban environments"
- "Future of quantum computing in cybersecurity"

## 📁 Project Structure

```
research-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── reports/           # Generated reports (auto-created)
```

## 🔧 Technical Details

- **Framework:** Streamlit
- **AI Model:** Google Gemini 2.0 Flash
- **Search Tools:** Wikipedia, DuckDuckGo
- **Python:** 3.8+

## 📜 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the web framework
- Agno for agent orchestration

---
