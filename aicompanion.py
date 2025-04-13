import streamlit as st
from openai import OpenAI
import azure.cognitiveservices.speech as speechsdk
from typing import Optional
import html
import base64
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# Configure page settings
st.set_page_config(
    page_title="Personal AI Comapnion • Your Thought Companion",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "## Your Personal Growth Partner\nHarness AI for meaningful conversations"
    }
)

# Configuration - Replace with your actual credentials
AZURE_SPEECH_KEY = os.environ.get('AZURE_SPEECH_KEY')
AZURE_REGION = "eastus"
OPENAI_API_KEY = os.environ.get('GOOGLE_API_KEY')
OPENAI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"  # Update if using different provider

DEFAULT_SYSTEM_PROMPT = """Act as a compassionate life coach who:
1. Asks thoughtful questions to spark self-reflection 🌱
2. Offers balanced perspectives without judgment 
3. Provides concise insights (1-2 lines maximum)
4. Always focuses on personal growth and empowerment"""

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

def recognize_speech() -> Optional[str]:
    """Capture audio and return transcribed text"""
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.toast("🔇 No speech detected", icon="⚠️")
    return None

def generate_response(prompt: str) -> str:
    """Generate AI response with safety handling"""
    try:
        with st.spinner('Crafting thoughtful response...'):
            response = client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=[
                    {"role": "system", "content": st.session_state.system_prompt+"Dont spell the special symbols if you refering points ,then specify as pint 1 and 2 and so on"},
                    {"role": "user", "content": prompt+"Dont spell the special symbols if you refering points ,then specify as pint 1 and 2 and so on"}
                ],
                temperature=0.7,
                max_tokens=150,
                stream=False
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error("⚠️ Error generating response. Please try again.")
        return "I'm having trouble responding right now. Could you rephrase that?"

def text_to_speech(text: str) -> Optional[bytes]:
    """Convert text to speech with error handling"""
    try:
        text = text.replace("*", "")
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        st.toast("🔇 Audio synthesis failed", icon="⚠️")
        return None
    except Exception as e:
        st.error("⚠️ Error generating audio. Check speech service configuration.")
        return None

# Enhanced CSS styling
st.markdown(f"""
<style>
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}}

.message-animation {{
    animation: messageEntrance 0.4s ease-out;
}}

@keyframes messageEntrance {{
    0% {{ opacity: 0; transform: translateY(20px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

.user-message {{
    align-self: flex-end;
    background: rgba(99, 102, 241, 0.1);
    padding: 15px;
    border-radius: 15px 0 15px 15px;
    max-width: 70%;
    margin-left: 15%;
    border: 1px solid #6366f1;
    box-shadow: 4px 4px 15px rgba(99, 102, 241, 0.2);
    transition: all 0.3s ease;
}}

.ai-message {{
    align-self: flex-start;
    background: rgba(30, 41, 59, 0.4);
    padding: 15px;
    border-radius: 0 15px 15px 15px;
    max-width: 70%;
    margin-right: 15%;
    border: 1px solid #475569;
    box-shadow: -4px 4px 15px rgba(71, 85, 105, 0.2);
    transition: all 0.3s ease;
}}

.message-content {{
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 20px;
    border-radius: 12px;
}}

.timestamp {{
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 8px;
    text-align: right;
}}

.thinking-indicator {{
    background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
    background-size: 200% 100%;
    animation: shimmer 2s infinite linear;
    height: 4px;
    border-radius: 2px;
    margin: 15px 0;
    width: 60%;
}}

@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

@media (max-width: 768px) {{
    .chat-container {{
        padding: 10px;
    }}
    
    .user-message, .ai-message {{
        max-width: 85%;
        margin-left: 5%;
        margin-right: 5%;
    }}
}}
</style>
""", unsafe_allow_html=True)

# App Layout
left_col, right_col = st.columns([3, 9])

with left_col:
    st.markdown("### 🧠 Personality Studio")
    st.caption("Shape your AI's communication style:")
    
    new_instructions = st.text_area(
        "**How should your companion respond?**\n\nExamples:\n- 'Use metaphors from nature'\n- 'Respond like a wise mentor'\n- 'Focus on emotional intelligence'",
        value=st.session_state.system_prompt,
        height=250,
        help="Pro Tip: Use adjectives and specific scenarios for best results"
    )
    
    if st.button("✨ Activate New Personality", use_container_width=True):
        st.session_state.system_prompt = new_instructions
        st.toast("Personality updated! Your AI companion is evolving...", icon="✅")

with right_col:
    # Header Section
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #6366f1; margin-bottom: 8px;'>AI Comapanion</h1>
        <div style='display: flex; justify-content: center; gap: 8px; align-items: center;'>
            <span style='color: #94a3b8;'>Current Mode:</span>
            <div class='status-pill'>Active Listener</div>
            <div class='status-pill'>Empathy Focus</div>
        </div>
        <p style='color: #94a3b8; margin-top: 12px;'>Your confidential space for growth-oriented conversations 🌿</p>
    </div>
    """, unsafe_allow_html=True)

    # Interaction Section
    with st.container():
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("🎙️ Start Voice Session", 
                       use_container_width=True,
                       help="Hold spacebar to record your thoughts",
                       type="primary"):
                user_input = recognize_speech()
                if user_input:
                    safe_input = html.escape(user_input)
                    timestamp = datetime.now().strftime("%H:%M")
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": safe_input,
                        "timestamp": timestamp
                    })
                    
                    # Generate response with loading indicator
                    with st.empty():
                        st.markdown("<div class='thinking-indicator'></div>", unsafe_allow_html=True)
                        ai_response = generate_response(user_input)
                    
                    # Process audio response
                    audio_data = text_to_speech(ai_response)
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8') if audio_data else None
                    timestamp = datetime.now().strftime("%H:%M")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": html.escape(ai_response),
                        "audio": audio_base64,
                        "timestamp": timestamp
                    })

        with col3:
            if st.button("🔄 New Conversation", 
                       use_container_width=True,
                       help="Start fresh (existing conversation will be archived)"):
                st.session_state.messages = []
                st.toast("Clean slate created! What's on your mind?", icon="🧹")

    # Chat Display
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align: center; padding: 40px; color: #64748b;'>
                <h3>Conversation Canvas</h3>
                <p>Your dialogue will appear here<br>
                Try starting with:</p>
                <ul style='list-style: none; padding: 0;'>
                    <li>• "What's one growth area I should focus on?"</li>
                    <li>• "Help me reframe this challenge..."</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <br>
                    <div class='message-animation'>
                        <div class='user-message'>
                            <div class='message-content'>
                                <p class='user-heading'>👤 You</p>
                                <p class='message-text'>{message['content']}</p>
                                <div class='timestamp'>{message['timestamp']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    audio_element = ""
                    if message.get("audio"):
                        audio_element = f"""
                        <div style='margin-top: 15px;'>
                            <audio controls style='width: 100%;'>
                                <source src="data:audio/wav;base64,{message['audio']}" type="audio/wav">
                            </audio>
                        </div>
                        """
                    st.markdown(f"""
                    <br>
                    <div class='message-animation'>
                        <div class='ai-message'>
                            <div class='message-content'>
                                <p class='ai-heading'>🤖 Your Buddy Ai response</p>
                                <p class='message-text'>{message['content']}</p>
                                <div class='timestamp'>{message['timestamp']}</div>
                            </div>
                        </div>
                    </div>
                           
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)