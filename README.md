# Gemini Chatbot

Dieses Projekt ist ein einfacher Chatbot, der die Gemini-2.0-Flash-Exp-Modell von Google Generative AI verwendet. Der Chatbot ist mit Gradio erstellt, einer benutzerfreundlichen Bibliothek zum Erstellen von Benutzeroberflächen für maschinelle Lernmodelle.

## Inhalt

- [Installation](#installation)
- [API-Schlüssel](#api-schlüssel)
- [Verwendung](#verwendung)
- [Lizenz](#lizenz)

## Installation

1. Klonen Sie das Repository:

    ```bash
    git clone https://github.com/IhrBenutzername/gemini-chatbot.git
    cd gemini-chatbot
    ```

2. Installieren Sie die erforderlichen Pakete:

    ```bash
    pip install -r requirements.txt
    ```

## API-Schlüssel

Um den Chatbot zu verwenden, benötigen Sie einen API-Schlüssel von Google AI Studio. Hier sind die Schritte, um einen API-Schlüssel zu erhalten:

1. Besuchen Sie [Google AI Studio API Key](https://aistudio.google.com/apikey).
2. Melden Sie sich mit Ihrem Google-Konto an.
3. Folgen Sie den Anweisungen, um einen neuen API-Schlüssel zu erstellen.
4. Kopieren Sie den API-Schlüssel und ersetzen Sie `'YOUR KEY'` in der Datei `app.py` durch Ihren tatsächlichen API-Schlüssel.

## Verwendung

1. Starten Sie die Gradio-Benutzeroberfläche:

    ```bash
    python app.py
    ```

2. Öffnen Sie Ihren Webbrowser und navigieren Sie zu `http://localhost:7860`, um die Benutzeroberfläche zu sehen.
3. Geben Sie Ihre Nachricht in das Textfeld ein und klicken Sie auf "Send", um mit dem Chatbot zu interagieren.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der [LICENSE](LICENSE)-Datei.

---
