# AI Multitool with Google Gemini + Streamlit

A Streamlit app that:
- 🖼️ Generates AI images from text prompts
- 📄 Summarizes PDFs in English and Hindi
- 🎥 Summarizes YouTube videos

## Tech Stack
- Python
- Streamlit
- Google Gemini API (via google-genai)

## 🔐 Setup (Local)
```bash
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
streamlit run app.py
