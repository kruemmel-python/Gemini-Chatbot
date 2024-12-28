import os
import google.generativeai as genai
import gradio as gr

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

# Initialize chat history
chat_history = []

def chat_with_gemini(user_input, history):
    global chat_history
    # Ensure user input is not empty
    if not user_input.strip():
        return history, "Bitte geben Sie eine Nachricht ein."

    # Add user input to chat history
    chat_history.append({"role": "user", "parts": [user_input]})

    # Send chat history to the model
    response = model.generate_content(chat_history)

    # Add model response to chat history
    chat_history.append({"role": "model", "parts": [response.text]})

    # Update the chat history display
    history.append((user_input, response.text))
    return history, ""

# Gradio-Benutzeroberfläche
with gr.Blocks() as demo:
    gr.Markdown("## Gemini Chatbot")
    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Enter your message", placeholder="Type your message here...")
            submit_btn = gr.Button("Send")

    submit_btn.click(fn=chat_with_gemini, inputs=[user_input, chatbot], outputs=[chatbot, user_input])

if __name__ == '__main__':
    # Starten Sie die Gradio-Benutzeroberfläche
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
