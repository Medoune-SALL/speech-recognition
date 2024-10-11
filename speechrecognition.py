import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np

# Fonction pour capturer l'audio avec sounddevice
def record_audio(duration=5, fs=16000):
    st.info("Enregistrement en cours...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Attendre la fin de l'enregistrement
    st.success("Enregistrement terminé.")
    return np.squeeze(audio)

# Fonction pour la transcription vocale avec sélection de l'API et de la langue
def transcribe_speech(api_choice, language):
    r = sr.Recognizer()
    # Capture audio via sounddevice
    audio_data = record_audio()

    # Convertir l'audio en AudioData utilisable par SpeechRecognition
    audio_sr = sr.AudioData(audio_data.tobytes(), 16000, 2)

    st.info("Transcription en cours...")

    try:
        if api_choice == "Google":
            text = r.recognize_google(audio_sr, language=language)
        elif api_choice == "Sphinx":
            text = r.recognize_sphinx(audio_sr, language=language)
        elif api_choice == "IBM Watson":
            # Nécessite des clés API IBM Watson
            api_key = st.text_input("Clé API IBM Watson:", type="password")
            url = st.text_input("URL du service IBM Watson:")
            if api_key and url:
                text = r.recognize_ibm(audio_sr, username="apikey", password=api_key, language=language, url=url)
            else:
                text = "Veuillez fournir les informations d'authentification pour IBM Watson."
        else:
            text = "API de reconnaissance non supportée"
        return text
    except sr.UnknownValueError:
        return "Désolé, je n'ai pas pu comprendre l'audio."
    except sr.RequestError as e:
        return f"Erreur de service API : {e}"

# Fonction principale de l'application
def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le bouton pour commencer l'enregistrement.")

    # Sélection de l'API
    api_choice = st.sidebar.selectbox("Choisissez l'API de reconnaissance vocale", ["Google", "Sphinx", "IBM Watson"])

    # Choix de la langue
    language = st.sidebar.selectbox("Choisissez la langue", ["fr-FR", "en-US", "es-ES", "de-DE"])

    # Bouton pour démarrer la transcription
    if st.button("Commencer l'enregistrement"):
        text = transcribe_speech(api_choice, language)
        st.write("Transcription : ", text)

if __name__ == "__main__":
    main()
