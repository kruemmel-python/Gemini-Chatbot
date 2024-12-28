import os
import google.generativeai as genai
import gradio as gr

# Konfigurieren Sie den API-Schlüssel
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Lädt die angegebene Datei zu Gemini hoch.

    Siehe https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Erstellen Sie das Modell
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-1219",
    generation_config=generation_config,
)

# Initialisieren Sie den Chat-Verlauf
chat_history = []

def chat_with_gemini(user_input, image, history):
    global chat_history
    # Stellen Sie sicher, dass die Benutzereingabe nicht leer ist
    if not user_input.strip():
        return history, "Bitte geben Sie eine Nachricht ein."

    # Laden Sie das Bild hoch, falls vorhanden
    if image:
        file = upload_to_gemini(image.name, mime_type=image.type)
        chat_history.append({"role": "user", "parts": [file, user_input]})
    else:
        chat_history.append({"role": "user", "parts": [user_input]})

    # Senden Sie den Chat-Verlauf an das Modell
    response = model.generate_content(chat_history)

    # Fügen Sie die Modellantwort zum Chat-Verlauf hinzu
    chat_history.append({"role": "model", "parts": [response.text]})

    # Aktualisieren Sie die Anzeige des Chat-Verlaufs
    history.append((user_input, response.text))
    return history, ""

# Gradio-Benutzeroberfläche
with gr.Blocks() as demo:
    gr.Markdown("## Gemini Chatbot")
    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Enter your message", placeholder="Type your message here...")
            image_input = gr.File(label="Upload an image", type="file")
            submit_btn = gr.Button("Send")

    submit_btn.click(fn=chat_with_gemini, inputs=[user_input, image_input, chatbot], outputs=[chatbot, user_input])

if __name__ == '__main__':
    # Starten Sie die Gradio-Benutzeroberfläche
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
