import streamlit as st
import speech_recognition as sr
import os

# Fonction pour la transcription vocale avec sélection de l'API et de la langue
def transcribe_speech(api_choice, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio_text = r.listen(source)
        st.info("Transcription en cours...")

        try:
            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            elif api_choice == "IBM Watson":
                # Nécessite des clés API IBM Watson
                api_key = st.text_input("Clé API IBM Watson:", type="password")
                url = st.text_input("URL du service IBM Watson:")
                if api_key and url:
                    text = r.recognize_ibm(audio_text, username="apikey", password=api_key, language=language, url=url)
                else:
                    text = "Veuillez fournir les informations d'authentification pour IBM Watson."
            else:
                text = "API de reconnaissance non supportée"
            return text
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas pu comprendre l'audio."
        except sr.RequestError as e:
            return f"Erreur de service API : {e}"

# Fonction pour enregistrer le texte transcrit dans un fichier
def save_transcription(text):
    file_path = st.text_input("Nom du fichier pour enregistrer la transcription (ex: transcription.txt):")
    if file_path and st.button("Enregistrer la transcription"):
        with open(file_path, "w") as f:
            f.write(text)
        st.success(f"Transcription enregistrée dans {file_path}")

# Fonction principale de l'application
def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le microphone pour commencer à parler.")

    # Sélection de l'API
    api_choice = st.sidebar.selectbox("Choisissez l'API de reconnaissance vocale", ["Google", "Sphinx", "IBM Watson"])

    # Choix de la langue
    language = st.sidebar.selectbox("Choisissez la langue", ["fr-FR", "en-US", "es-ES", "de-DE"])

    # Bouton pour démarrer la transcription
    if st.button("Commencer l'enregistrement"):
        text = transcribe_speech(api_choice, language)
        st.write("Transcription : ", text)

        # Fonctionnalité pour enregistrer le texte transcrit
        save_transcription(text)

if __name__ == "__main__":
    main()
