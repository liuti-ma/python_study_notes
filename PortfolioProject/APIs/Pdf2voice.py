import os
import PyPDF2
from google.cloud import texttospeech
import boto3

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def text_to_speech(text, output_file="output.mp3"):
    """Convert text to speech using Google Cloud Text-to-Speech API."""
    # Initialize the client
    client = texttospeech.TextToSpeechClient()

    # Set the text input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Change language code as needed
        name="en-US-Wavenet-D",  # Choose a voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio saved to {output_file}")



def text_to_speech_polly(text, output_file="output.mp3"):
    """Convert text to speech using Amazon Polly."""
    polly = boto3.client("polly", region_name="us-west-2")
    response = polly.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    with open(output_file, "wb") as out:
        out.write(response["AudioStream"].read())
    print(f"Audio saved to {output_file}")
def main():
    # Path to the PDF file
    pdf_path = "example.pdf"  # Replace with your PDF file path

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    print("Extracted text:", text[:500])  # Print first 500 characters for debugging

    # Convert text to speech
    text_to_speech(text, output_file="output.mp3")

if __name__ == "__main__":
    main()