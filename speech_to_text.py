# speech_to_text.py - Voice Input Feature for Resume Builder
# Unique Speech-to-Text functionality powered by browser API and AI enhancement

import streamlit as st
import streamlit.components.v1 as components

def create_voice_input_button(key_suffix=""):
    """
    Create a voice input button that uses browser's Speech Recognition API
    Returns the transcribed text when user speaks
    """
    
    # Custom HTML/JS component for speech recognition
    speech_component = f"""
    <div style="margin: 10px 0;">
        <button id="voiceBtn_{key_suffix}" 
                style="background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
                       color: white;
                       border: none;
                       border-radius: 8px;
                       padding: 10px 20px;
                       font-weight: 600;
                       cursor: pointer;
                       box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
                       transition: all 0.3s ease;">
            🎤 Click to Speak
        </button>
        <span id="status_{key_suffix}" style="margin-left: 15px; font-size: 14px; color: #666;"></span>
    </div>
    
    <script>
    (function() {{
        const btn = document.getElementById('voiceBtn_{key_suffix}');
        const status = document.getElementById('status_{key_suffix}');
        
        // Check if browser supports speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {{
            status.innerHTML = '❌ Speech recognition not supported in this browser';
            btn.disabled = true;
            return;
        }}
        
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-IN'; // Indian English, can be changed
        
        let finalTranscript = '';
        let isListening = false;
        
        btn.addEventListener('click', function() {{
            if (!isListening) {{
                recognition.start();
                isListening = true;
                btn.innerHTML = '🔴 Listening... (Click to Stop)';
                btn.style.background = 'linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%)';
                status.innerHTML = '🎧 Listening...';
            }} else {{
                recognition.stop();
                isListening = false;
                btn.innerHTML = '🎤 Click to Speak';
                btn.style.background = 'linear-gradient(90deg, #f093fb 0%, #f5576c 100%)';
                status.innerHTML = '✅ Done';
                
                // Send transcript back to Streamlit
                if (finalTranscript) {{
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: finalTranscript
                    }}, '*');
                }}
            }}
        }});
        
        recognition.onresult = function(event) {{
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {{
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {{
                    finalTranscript += transcript + ' ';
                }} else {{
                    interimTranscript += transcript;
                }}
            }}
            
            status.innerHTML = '🎤 ' + (interimTranscript || finalTranscript.slice(-50));
        }};
        
        recognition.onerror = function(event) {{
            console.error('Speech recognition error:', event.error);
            status.innerHTML = '❌ Error: ' + event.error;
            isListening = false;
            btn.innerHTML = '🎤 Click to Speak';
            btn.style.background = 'linear-gradient(90deg, #f093fb 0%, #f5576c 100%)';
        }};
        
        recognition.onend = function() {{
            if (isListening) {{
                // Auto-restart if manually stopped by browser
                recognition.start();
            }}
        }};
    }})();
    </script>
    """
    
    # Render the component
    result = components.html(speech_component, height=80)
    return result


def get_voice_input_instructions():
    """Display helpful instructions for voice input"""
    return """
    ### 🎤 Voice Input Tips:
    
    **How to use:**
    1. Click the "🎤 Click to Speak" button
    2. Start speaking clearly
    3. Click again to stop recording
    4. Your text will automatically appear below
    
    **Best Practices:**
    - Speak clearly and at a moderate pace
    - Pause briefly between sentences
    - Use punctuation commands: say "comma", "period", "new line"
    - Works best in quiet environment
    - Supports English (Indian accent optimized)
    
    **What you can dictate:**
    - Work experience descriptions
    - Project details
    - Professional summary
    - Skills and achievements
    """


def enhance_voice_text_with_ai(text, ai_assistant, context="work_experience"):
    """
    Enhance voice-transcribed text using AI to make it professional
    
    Args:
        text: Raw transcribed text from voice input
        ai_assistant: AI assistant instance
        context: Type of content (work_experience, summary, project, etc.)
    
    Returns:
        Enhanced professional text
    """
    
    if not ai_assistant or not ai_assistant.enabled:
        return text
    
    try:
        if context == "work_experience":
            prompt = f"""Convert this voice-transcribed work experience into professional bullet points:

Raw voice input: "{text}"

Requirements:
- Create 2-4 bullet points
- Start each with strong action verbs
- Include metrics/numbers where applicable
- Make it ATS-friendly
- Keep the core information accurate

Return only the bullet points, nothing else."""

        elif context == "summary":
            prompt = f"""Convert this voice-transcribed text into a professional summary:

Raw voice input: "{text}"

Requirements:
- Create a 3-4 line professional summary
- Highlight key strengths and experience
- Make it compelling and concise
- Use professional language

Return only the summary, nothing else."""

        elif context == "project":
            prompt = f"""Convert this voice-transcribed project description into professional text:

Raw voice input: "{text}"

Requirements:
- Create 2-3 sentences describing the project
- Include technologies used
- Mention impact/results
- Make it clear and professional

Return only the description, nothing else."""

        else:
            return text
        
        # Get AI enhancement
        enhanced = ai_assistant.generate_content(prompt)
        return enhanced if enhanced else text
        
    except Exception as e:
        print(f"Error enhancing voice text: {e}")
        return text


def create_voice_input_section(field_name, ai_assistant=None, context="general"):
    """
    Create a complete voice input section with button and text area
    
    Args:
        field_name: Name of the field being filled
        ai_assistant: Optional AI assistant for enhancement
        context: Context for AI enhancement
    
    Returns:
        tuple: (voice_button_result, text_area_widget)
    """
    
    st.markdown(f"### 🎤 Voice Input for {field_name}")
    
    # Info box
    with st.expander("ℹ️ How to use Voice Input", expanded=False):
        st.markdown(get_voice_input_instructions())
    
    # Voice input button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        voice_result = create_voice_input_button(key_suffix=field_name.replace(" ", "_"))
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if ai_assistant and ai_assistant.enabled:
            st.success("✨ AI Enhancement Available")
        else:
            st.info("💬 Voice-to-Text Only")
    
    return voice_result


# Language options for speech recognition
SUPPORTED_LANGUAGES = {
    "English (India)": "en-IN",
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN"
}


def create_advanced_voice_input(key_suffix="", language="en-IN", ai_enhance=False, ai_assistant=None, context="general"):
    """
    Advanced voice input with language selection and AI enhancement
    
    Args:
        key_suffix: Unique identifier for this input
        language: Language code for speech recognition
        ai_enhance: Whether to enhance with AI
        ai_assistant: AI assistant instance
        context: Context for content type
    
    Returns:
        Transcribed and optionally AI-enhanced text
    """
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Voice button
        voice_result = create_voice_input_button(key_suffix=key_suffix)
    
    with col2:
        # Language selector
        selected_lang = st.selectbox(
            "Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=0,
            key=f"lang_{key_suffix}"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if ai_enhance and ai_assistant and ai_assistant.enabled:
            if st.button("✨ Enhance with AI", key=f"enhance_{key_suffix}"):
                if voice_result:
                    enhanced = enhance_voice_text_with_ai(voice_result, ai_assistant, context)
                    return enhanced
    
    return voice_result


def get_voice_input_widget(label, key, ai_assistant=None, context="general", placeholder="Click 🎤 to speak or type here..."):
    """
    Complete voice input widget with text area
    Combines voice input button with editable text area
    
    Args:
        label: Label for the text area
        key: Unique key for the widget
        ai_assistant: Optional AI assistant
        context: Context for AI enhancement
        placeholder: Placeholder text
    
    Returns:
        Text content (either voice transcribed or manually typed)
    """
    
    st.markdown(f"**{label}**")
    
    # Voice input row
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        voice_btn_clicked = st.button(f"🎤 Voice Input", key=f"voice_btn_{key}")
    
    with col2:
        if ai_assistant and ai_assistant.enabled:
            ai_enhance = st.checkbox("✨ AI Enhance", value=True, key=f"ai_check_{key}")
        else:
            ai_enhance = False
    
    with col3:
        lang_options = ["English (India)", "English (US)", "Hindi"]
        selected_lang = st.selectbox("Lang", lang_options, label_visibility="collapsed", key=f"lang_{key}")
    
    # Text area for input/output
    text_value = st.text_area(
        label,
        value=st.session_state.get(f"{key}_text", ""),
        placeholder=placeholder,
        height=100,
        key=f"textarea_{key}",
        label_visibility="collapsed"
    )
    
    # Store in session state
    st.session_state[f"{key}_text"] = text_value
    
    # Show voice input instructions
    if voice_btn_clicked:
        st.info("🎤 **Voice Input Active**: Speak clearly into your microphone. Your speech will be transcribed and appear in the text area above.")
        with st.expander("📝 Voice Input Tips"):
            st.markdown("""
            - Speak naturally and clearly
            - Pause between sentences
            - Say punctuation: "comma", "period", "new line"
            - Works best in quiet environment
            - Click the button again to stop
            """)
    
    return text_value
