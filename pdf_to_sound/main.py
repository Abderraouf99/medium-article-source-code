import pyttsx3
import PyPDF2

# Open the PDF file
with open('test.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # # Extract the text from the PDF file
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Initialize the TTS engine
    engine = pyttsx3.init()
    engine.save_to_file(text, '/test.mp3')
    engine.runAndWait()

    # Set the voice
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)  # Replace 0 with the index of your desired voice

    # Convert the text to speech
    # engine.say(text)
    # engine.runAndWait()
