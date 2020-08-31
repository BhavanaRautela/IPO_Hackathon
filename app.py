from flask import Flask
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize(audio)

    except:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        print()

    return response


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    ascii_banner = "Impact Players"
    return ascii_banner


@app.route('/transcript/', methods=['GET', 'POST'])
def transcript():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Say something: ")
    #time.sleep(5000)
    guess = recognize_speech_from_mic(recognizer, microphone)
    return guess["transcription"]

if __name__ == "__main__":
    app.run(debug=True)
