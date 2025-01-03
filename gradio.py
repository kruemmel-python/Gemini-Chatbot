import os
import google.generativeai as genai
import gradio as gr
from PIL import Image

# Ersetzen Sie 'GEMINI_API_KEY' durch Ihren tatsächlichen API-Schlüssel
api_key = 'AIzaSyCQ0xd71zVQgtIBHTl6MfOrs3KKQTStySU'
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
    sample_file = genai.upload_file(path=image_path, display_name="Hochgeladenes Bild")
    print(f"Hochgeladene Datei '{sample_file.display_name}' as: {sample_file.uri}")

    # Löschen Sie die temporäre Datei
    os.remove(image_path)

    return sample_file

def chat_with_gemini(user_input, image=None):
    if not user_input.strip():
        return "Bitte geben Sie eine Nachricht ein."

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
    response_text = chat_session.send_message(user_input).text

    # Extrahiere den Python-Code aus der Antwort
    if "```python" in response_text and "```" in response_text:
        start_index = response_text.find("```python") + 9
        end_index = response_text.find("```", start_index)
        python_code = response_text[start_index:end_index].strip()
        return python_code
    else:
        return response_text

def analyze_image(image):
    if image is None:
        return "Bitte laden Sie ein Bild hoch."

    sample_file = upload_to_gemini(image)
    response = model.generate_content(["Beschreiben Sie das Bild mit einer kreativen Beschreibung. Bitte in German antworten.", sample_file])
    response_text = response.text

    # Extrahiere den Python-Code aus der Antwort
    if "```python" in response_text and "```" in response_text:
        start_index = response_text.find("```python") + 9
        end_index = response_text.find("```", start_index)
        python_code = response_text[start_index:end_index].strip()
        return python_code
    else:
        return response_text

# Gradio-Benutzeroberfläche
with gr.Blocks() as demo:
    gr.Markdown("## Gemini Chatbot mit Bildanalyse")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Geben Sie Ihre Nachricht ein", placeholder="Geben Sie hier Ihre Nachricht ein...")
            image_upload = gr.Image(type="pil", label="Bild hochladen")
            submit_btn = gr.Button("Senden")
        response = gr.Code(label="Antwort", language="python", interactive=False)

    submit_btn.click(fn=chat_with_gemini, inputs=[user_input, image_upload], outputs=response)

    with gr.Row():
        analyze_btn = gr.Button("Bild analysieren")
        image_analysis = gr.Code(label="Bildanalyse", language="python", interactive=False)

    analyze_btn.click(fn=analyze_image, inputs=image_upload, outputs=image_analysis)

# Starten Sie die Gradio-Benutzeroberfläche
if __name__ == '__main__':
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
