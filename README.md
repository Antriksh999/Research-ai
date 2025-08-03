# 🔬 Research Content Extractor Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rcea-antriksh-99.streamlit.app/)

An intelligent research assistant built with **Python** and **Agno** framework, leveraging Google Gemini AI to generate comprehensive academic reports. Features multi-source data gathering, automated content synthesis, and professional formatting - deployed on Streamlit Cloud for seamless accessibility and research productivity.

## ✨ Features

- 🤖 **Multi-Model Support** - Google Gemini 2.0 Flash & Ollama integration
- 📚 **Multiple Data Sources** - Wikipedia, DuckDuckGo, and Google Search
- 📄 **Academic Reports** - Professional formatting with citations
- 🔄 **Smart Model Fallback** - Auto-switches between cloud and local models
- 💾 **Export Options** - Download as Markdown files
- 🔒 **Secure API Handling** - No persistent storage of API keys
- 🎯 **User-Friendly Interface** - Intuitive Streamlit web app
- ⚡ **Cloud Ready** - Optimized for Streamlit Cloud deployment

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

### Security Notice 🔒
**API keys are never stored persistently for security.** You must enter your API key each session, or set it in Streamlit Cloud secrets for permanent deployment.

### Required API Key
You need a Google Gemini API key:

1. **Get API Key:** Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **For Streamlit Cloud:** Add to your app's secrets:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
3. **For manual entry:** Enter your API key in the sidebar (session only)

### Model Options
- **Gemini Only** (Recommended for cloud): Uses Google Gemini 2.0 Flash
- **Auto Mode**: Tries Gemini first, falls back to Ollama
- **Ollama Only**: Local models (requires local Ollama installation)

### Local Development
```bash
# Clone repository
git clone https://github.com/Antriksh999/Research-ai.git
cd Research-ai

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run locally
streamlit run app.py
```

## 🎯 Usage

1. **Configure Model**: Choose between Gemini, Auto, or Ollama mode
2. **Enter API Key**: Add your Gemini API key in the sidebar (if using Gemini)
3. **Select Search Tools**: Choose Wikipedia, DuckDuckGo, or Google Search
4. **Enter Research Topic**: Type your topic or select from examples
5. **Generate Report**: Wait for the AI to research and create your report
6. **Download**: Save your report as a Markdown file

### Example Topics
- "The impact of artificial intelligence on healthcare delivery"
- "Sustainable energy solutions for urban environments"
- "Climate change adaptation strategies in coastal cities"
- "The future of quantum computing in cybersecurity"
- "Blockchain technology applications beyond cryptocurrency"
- "Gene therapy advances in treating rare diseases"

## 📁 Project Structure

```
research-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── GITHUB_SETUP.txt   # Deployment instructions
```

## 🔧 Technical Details

- **Framework:** Streamlit
- **AI Framework:** Agno Agent Framework
- **AI Models:** Google Gemini 2.0 Flash, Ollama (local)
- **Search Tools:** Wikipedia, DuckDuckGo, Google Search
- **Language:** Python 3.8+
- **Dependencies:** See requirements.txt

## 🚀 Live Demo

Visit the live app: [Research Content Extractor Agent](https://rcea-antriksh-99.streamlit.app/)

## 🔒 Security Features

- ✅ API keys not stored in browser
- ✅ Session-only key storage
- ✅ Environment variable support
- ✅ Secure deployment ready

## 📜 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the web framework
- Agno for agent orchestration

---
