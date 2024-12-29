import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import gradio as gr
from PIL import Image
import io

app = Flask(__name__)

# Ersetzen Sie 'GEMINI_API_KEY' durch Ihren tatsächlichen API-Schlüssel
api_key = 'YOUR KEY'
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,  # Angepasster Wert für top_k
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def upload_to_gemini(image):
    # Speichern Sie das Bild temporär
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Laden Sie das Bild in die Gemini API hoch
    sample_file = genai.upload_file(path=image_path, display_name="Uploaded Image")
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    # Löschen Sie die temporäre Datei
    os.remove(image_path)

    return sample_file

def chat_with_gemini(user_input, image=None):
    history = [
        {
            "role": "user",
            "parts": [
                user_input,
            ],
        },
    ]

    if image:
        sample_file = upload_to_gemini(image)
        history[0]["parts"].append(sample_file)

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    return response.text

def analyze_image(image):
    sample_file = upload_to_gemini(image)
    response = model.generate_content(["Beschreiben Sie das Bild mit einer kreativen Beschreibung. Bitte in German antworten.", sample_file])
    return response.text

# Gradio-Benutzeroberfläche
with gr.Blocks() as demo:
    gr.Markdown("## Gemini Chatbot with Image Analysis")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Enter your message", placeholder="Type your message here...")
            image_upload = gr.Image(type="pil", label="Upload an image")
            submit_btn = gr.Button("Send")
        response = gr.Textbox(label="Response", interactive=False)

    submit_btn.click(fn=chat_with_gemini, inputs=[user_input, image_upload], outputs=response)

    with gr.Row():
        analyze_btn = gr.Button("Analyze Image")
        image_analysis = gr.Textbox(label="Image Analysis", interactive=False)

    analyze_btn.click(fn=analyze_image, inputs=image_upload, outputs=image_analysis)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Starten Sie die Gradio-Benutzeroberfläche
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
    # Starten Sie die Flask-Anwendung
    app.run(debug=True, port=5000)
