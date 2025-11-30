# Image Question Answering Interface

A Streamlit application for uploading images and asking questions about them, designed to be connected to a vision-language model.

## Features

- 📤 **Image Upload**: Support for multiple image formats (PNG, JPG, JPEG, BMP, GIF)
- 💬 **Question Answering**: Text input for asking questions about uploaded images
- 📝 **Conversation History**: Track all questions and answers in a session
- ⚙️ **Model Configuration**: Configurable settings for connecting to your model API
- 🎨 **Image Preprocessing**: Optional image resizing before processing
- 💾 **Export History**: Download conversation history as text file
- 🔍 **Debug Mode**: View detailed information about the session

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Upload an Image**: Click on the file uploader and select an image from your computer
2. **Ask Questions**: Enter your question in the text input field
3. **Submit**: Click the "Submit" button to process your question
4. **View Results**: See the model's response in the conversation history
5. **Export**: Download your conversation history if needed

## Connecting to Your Model

To connect the app to your actual model, modify the section in `app.py` marked with:

```python
# TODO: Connect to your model here
```

Replace the placeholder code with your actual model API call:

```python
# Example implementation:
import requests

response = requests.post(
    model_endpoint,
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "image": base64.b64encode(img_byte_arr).decode('utf-8'),
        "question": question,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
)
answer = response.json()['answer']
```

## Configuration Options

### Model Settings
- **Model API Endpoint**: URL of your model's API
- **API Key**: Authentication key for your model
- **Temperature**: Controls randomness (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Maximum length of model responses

### Image Preprocessing
- **Resize Image**: Optionally resize images to a maximum dimension
- **Max Dimension**: Maximum width or height in pixels

### Additional Options
- **Show Debug Info**: Display session state and image information
- **Save Conversation History**: Keep history throughout the session

## File Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## License

MIT License12
