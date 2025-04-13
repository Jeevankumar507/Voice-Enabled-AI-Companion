## 🤖 Personal AI Companion • Your Thought Partner

Welcome to your **Personal Growth AI Companion** — a confidential and calming space to engage in self-reflective conversations. Built using **Streamlit**, **OpenAI**, and **Azure Cognitive Services**, this app listens to your voice, understands your emotions, and responds with empathy and clarity.

![App Screenshot](https://drive.google.com/uc?id=1Hw0E2sdGzETD3v86q5H5wTBeuKQYXNJF)  


---

### 🎩🎮 Demo
<video controls src="20250413-1812-03.5154571.mp4" title="AI Companion Demo"></video>
[View on Google Drive](https://drive.google.com/file/d/1Hw0E2sdGzETD3v86q5H5wTBeuKQYXNJF/view?usp=sharing)
---

### ✨ Features

- 🎙️ **Voice Recognition** — Powered by Azure Speech API
- 💬 **Empathetic AI Responses** — Using Google Gemini (OpenAI-compatible) APIs
- 🔊 **Text-to-Speech** — AI speaks back with soothing voice feedback
- 🧠 **Personality Customization** — Tailor your AI's tone and style
- 🌿 **Growth-Focused Prompts** — Ideal for introspection and self-coaching

---

### 🚀 How It Works

1. **Start a Voice Session**  
   Speak naturally and let your companion listen and understand your thoughts.

2. **Thoughtful AI Replies**  
   The AI responds with short, growth-oriented insights and questions.

3. **Audio Playback**  
   Your AI buddy reads out its responses for a more natural interaction.

4. **Custom Instructions**  
   You can guide the AI’s personality (e.g., "respond like a wise monk", or "use nature metaphors").

---

### 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io)
- **AI Model**: Google Gemini via OpenAI-compatible endpoints
- **Voice Recognition**: [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/)
- **Text-to-Speech**: Azure Speech SDK
- **Environment Variables**: `python-dotenv`

---

### 🔐 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ai-companion.git
   cd ai-companion
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   ```env
   AZURE_SPEECH_KEY=your_azure_key
   GOOGLE_API_KEY=your_openai_compatible_key
   ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

---

### ✅ Example Prompts

- "What should I focus on for personal growth this week?"
- "Help me reframe a recent challenge."
- "I feel stuck in my career — what can I do?"

---

### 📁 Folder Structure
```
├── app.py               # Main Streamlit App
├── .env                 # API keys and config (not committed)
├── README.md            # You're here!
└── requirements.txt     # Python dependencies
```

---

### 📄 License

This project is for **educational and personal use only**. Attribution appreciated. Not for commercial deployment without consent.

---

### 🙏 Acknowledgements

- [Streamlit](https://streamlit.io)
- [Azure Speech Services](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Google Gemini / OpenAI Compatible APIs](https://ai.google.dev)

