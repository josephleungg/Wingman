import speech_recognition as sr
import pyttsx3

# speech to text util function

# initialize the recognizer from speech recognition
r = sr.Recognizer()

# function to listen to microphone and return the text
def record_text():
    while(True):
        try:
            with sr.Microphone() as source2:

                # prepare the recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for user's input
                audio2 = r.listen(source2)

                # uses google to recognize the audio
                MyText = r.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print("could not request results; {0}".format(e))
        
        except sr.UnknownValueError:
            print("unknown error occured")

    return

def output_text(text):
    f = open("output.txt", "a")
    f.write(text + "\n")
    f.close()

    return

while(True):
    text = record_text()

    # testing if it is recognizing the text or voice prompt
    if(text.lower() == "hello wingman"):
        print("Wingman: " + text)
        message = record_text()
        print("User: " + message)
    elif(text):
        print(text)
        print("text is working")

    # output_text(text)