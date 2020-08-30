# from datetime import time
# from flask_restful import Resource, Api
# from flask_httpauth import HTTPBasicAuth
# import win32security
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
# run_with_ngrok(app)
# api = Api(app, prefix="/api/v1")
# auth = HTTPBasicAuth()


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

# @auth.verify_password
# def verify(username,password):
#     username = "bhavanarautela"
#     password = "Password@123"
#     # query_parameters = request.args
#     # system_domain = query_parameters.get("Domain")
#     if not (username and password):
#         return False
#     else:
#         try:
#             sign_on_status = bool(win32security.LogonUser(username, "ktrainind", password,win32security.LOGON32_LOGON_NETWORK,win32security.LOGON32_PROVIDER_DEFAULT))
#         except:
#             sign_on_status=False
#         return sign_on_status

#
# class PrivateResource(Resource):
#     #@auth.login_required
#     def get(self):
#         recognizer = sr.Recognizer()
#         microphone = sr.Microphone()
#         print("Say something: ")
#         time.sleep(5000)
#         guess = recognize_speech_from_mic(recognizer, microphone)
#         return guess["transcription"]


# private = PrivateResource()
# api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
