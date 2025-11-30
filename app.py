import streamlit as st
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Image Question Answering",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state first
if 'image' not in st.session_state:
    st.session_state.image = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'theme' not in st.session_state:
    st.session_state.theme = "Purple Gradient"

# Theme configurations
THEMES = {
    "Purple Gradient": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "gradient": "linear-gradient(120deg, #667eea 0%, #764ba2 100%)",
        "card_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "Ocean Blue": {
        "primary": "#2E3192",
        "secondary": "#1BFFFF",
        "gradient": "linear-gradient(120deg, #2E3192 0%, #1BFFFF 100%)",
        "card_gradient": "linear-gradient(135deg, #2E3192 0%, #1BFFFF 100%)"
    },
    "Sunset Orange": {
        "primary": "#f12711",
        "secondary": "#f5af19",
        "gradient": "linear-gradient(120deg, #f12711 0%, #f5af19 100%)",
        "card_gradient": "linear-gradient(135deg, #f12711 0%, #f5af19 100%)"
    },
    "Forest Green": {
        "primary": "#134E5E",
        "secondary": "#71B280",
        "gradient": "linear-gradient(120deg, #134E5E 0%, #71B280 100%)",
        "card_gradient": "linear-gradient(135deg, #134E5E 0%, #71B280 100%)"
    },
    "Rose Pink": {
        "primary": "#ec008c",
        "secondary": "#fc6767",
        "gradient": "linear-gradient(120deg, #ec008c 0%, #fc6767 100%)",
        "card_gradient": "linear-gradient(135deg, #ec008c 0%, #fc6767 100%)"
    },
    "Dark Mode": {
        "primary": "#BB86FC",
        "secondary": "#03DAC6",
        "gradient": "linear-gradient(120deg, #BB86FC 0%, #03DAC6 100%)",
        "card_gradient": "linear-gradient(135deg, #BB86FC 0%, #03DAC6 100%)"
    }
}

# Get current theme colors
theme = THEMES[st.session_state.theme]

# Custom CSS for better styling with dynamic theme
st.markdown(f"""
    <style>
    /* Main title styling */
    .main-title {{
        font-size: 3rem;
        font-weight: 700;
        background: {theme['gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }}
    
    /* Card-like containers */
    .stContainer {{
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Upload section styling */
    .uploadedFile {{
        border: 2px dashed {theme['primary']};
        border-radius: 10px;
        padding: 20px;
    }}
    
    /* Button styling */
    .stButton>button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* Chat history styling */
    .chat-message {{
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .question {{
        color: {theme['primary']};
        font-weight: 600;
        margin-bottom: 8px;
    }}
    
    .answer {{
        color: #333;
        line-height: 1.6;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: #f8f9fa;
    }}
    
    /* Info boxes */
    .stAlert {{
        border-radius: 10px;
        border-left: 4px solid {theme['primary']};
    }}
    
    /* Image container */
    .image-container {{
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin: 20px 0;
    }}
    
    /* Input fields */
    .stTextInput>div>div>input {{
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 1rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: {theme['primary']};
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* Divider styling */
    hr {{
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {theme['primary']}, transparent);
    }}
    </style>
""", unsafe_allow_html=True)

# Title and description with custom styling
st.markdown('<h1 class="main-title">🖼️ Image Question Answering</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image and ask intelligent questions about its content</p>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

# Left column - Image upload and display
with col1:
    st.markdown("### 📤 Image Upload")
    st.markdown("---")
    
    # File uploader with custom styling
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['png', 'jpg', 'jpeg', 'bmp', 'gif'],
        help="Upload an image file to analyze",
        label_visibility="collapsed"
    )
    
    # Display uploaded image
    if uploaded_file is not None:
        # Read and display image
        image = Image.open(uploaded_file)
        st.session_state.image = image
        
        # Image container with custom styling
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Image info in an attractive format
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("📐 Dimensions", f"{image.size[0]} × {image.size[1]}")
        with col_info2:
            st.metric("📁 Format", image.format)
        
        st.markdown("")  # Spacing
        
        # Option to clear image
        if st.button("🗑️ Clear Image", use_container_width=True, type="secondary"):
            st.session_state.image = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown(f"""
            <div style="text-align: center; padding: 60px 20px; background: {theme['card_gradient']}; border-radius: 15px; color: white;">
                <h2>👆 Drop your image here</h2>
                <p style="font-size: 1.1rem; margin-top: 10px;">or click to browse</p>
            </div>
        """, unsafe_allow_html=True)

# Right column - Question answering
with col2:
    st.markdown("### 💬 Ask Questions")
    st.markdown("---")
    
    if st.session_state.image is not None:
        # Question input with better styling
        question = st.text_input(
            "Ask a question about the image:",
            placeholder="e.g., What is shown in this image? Describe the main elements...",
            key="question_input",
            label_visibility="collapsed"
        )
        
        st.markdown("")  # Spacing
        
        # Submit button
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            submit_button = st.button("🚀 Submit Question", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("🔄 Clear History", use_container_width=True, type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Process question
        if submit_button and question:
            with st.spinner("🤔 Analyzing image and generating response..."):
                # Prepare image for model
                img_byte_arr = io.BytesIO()
                st.session_state.image.save(img_byte_arr, format=st.session_state.image.format or 'PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # TODO: Connect to your model here
                # Example model connection point:
                # response = your_model.predict(image=img_byte_arr, question=question)
                
                # Placeholder response (replace with actual model response)
                response = f"[Model Response] This is a placeholder response for: '{question}'"
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': response
                })
                st.rerun()
        
        st.markdown("")  # Spacing
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 📝 Conversation History")
            st.markdown("")
            
            # Display in reverse order (newest first)
            for idx, chat in enumerate(reversed(st.session_state.chat_history)):
                st.markdown(f"""
                    <div class="chat-message">
                        <div class="question">❓ Question {len(st.session_state.chat_history) - idx}</div>
                        <div style="margin-left: 20px; margin-bottom: 12px;">{chat['question']}</div>
                        <div class="question">💡 Answer</div>
                        <div class="answer" style="margin-left: 20px;">{chat['answer']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: center; padding: 40px 20px; background: #f0f2f6; border-radius: 15px; margin-top: 20px;">
                    <h3 style="color: {theme['primary']};">💡 Ready to Start!</h3>
                    <p style="color: #666; font-size: 1.1rem;">Type your question above and click Submit</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: #fff3cd; border-radius: 15px; border: 2px dashed #ffc107;">
                <h3 style="color: #856404;">⚠️ No Image Uploaded</h3>
                <p style="color: #856404; font-size: 1.1rem; margin-top: 10px;">Please upload an image on the left to start asking questions</p>
            </div>
        """, unsafe_allow_html=True)

# Sidebar - Model configuration and settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    
    # Theme selector
    st.markdown("### 🎨 Theme")
    selected_theme = st.selectbox(
        "Choose your theme",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed"
    )
    
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.markdown("---")
    
    # Model configuration section
    with st.expander("🤖 Model Configuration", expanded=True):
        model_endpoint = st.text_input(
            "Model API Endpoint",
            placeholder="https://api.example.com/predict",
            help="Enter your model API endpoint"
        )
        
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Enter your API key",
            help="Your model API key (if required)"
        )
        
        temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Control randomness in model responses"
        )
        
        max_tokens = st.number_input(
            "📏 Max Tokens",
            min_value=50,
            max_value=2000,
            value=500,
            step=50,
            help="Maximum length of model response"
        )
    
    # Image preprocessing options
    with st.expander("🎨 Image Preprocessing", expanded=False):
        resize_image = st.checkbox(
            "Resize Image",
            value=False,
            help="Resize image before sending to model"
        )
        
        if resize_image:
            max_size = st.number_input(
                "Max Dimension (px)",
                min_value=128,
                max_value=2048,
                value=512,
                step=128,
                help="Maximum width or height"
            )
    
    # Additional settings
    with st.expander("📊 Additional Options", expanded=False):
        show_debug = st.checkbox(
            "Show Debug Info",
            value=False,
            help="Display debug information"
        )
        
        save_history = st.checkbox(
            "Save Conversation History",
            value=True,
            help="Keep conversation history during session"
        )
    
    # Export functionality
    if st.session_state.chat_history and save_history:
        st.markdown("---")
        st.markdown("### 💾 Export Data")
        history_text = "\n\n".join([
            f"Q: {chat['question']}\nA: {chat['answer']}"
            for chat in st.session_state.chat_history
        ])
        st.download_button(
            label="📥 Download History",
            data=history_text,
            file_name="conversation_history.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )
    
    # Stats
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📈 Session Stats")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Questions", len(st.session_state.chat_history))
        with col_stat2:
            if st.session_state.image:
                st.metric("Image", "✓")
            else:
                st.metric("Image", "✗")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #888; font-size: 0.9rem;'>
        <p style='margin: 0;'>Built with ❤️ using <strong>Streamlit</strong></p>
        <p style='margin: 5px 0 0 0;'>Upload an image and start asking intelligent questions</p>
    </div>
""", unsafe_allow_html=True)

# Debug information
if 'show_debug' in locals() and show_debug:
    with st.expander("🔍 Debug Information"):
        st.write("Session State:", st.session_state)
        if st.session_state.image:
            st.write("Image Mode:", st.session_state.image.mode)
            st.write("Image Size:", st.session_state.image.size)
st.markdown("demo")