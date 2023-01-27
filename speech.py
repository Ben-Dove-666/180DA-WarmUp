import speech_recognition as sr
#print(sr.__version__)

r = sr.Recognizer()
mic = sr.Microphone()

#print(sr.Microphone.list_microphone_names())

i = 0
while (i<10):
    with mic as source:
        print("please say something")
        audio = r.listen(source)

        print(r.recognize_google(audio))