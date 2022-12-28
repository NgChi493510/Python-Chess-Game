import speech_recognition as sr

def recogVoice():
    r = sr.Recognizer()
    text = ''
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source);
        r.energy_threshold += 100
        print("Threshold: ", r.energy_threshold)
        print("Speak: ")
        audio = r.listen(source, phrase_time_limit=3)
        try:
            text = r.recognize_google(audio, language="en-US")
            print("Said -->: {}".format(text))
        except:
            print("Error, Speak again!")
    return text

def extract_xy(text_from_voice):
    if verify_input(text_from_voice):
        varX = ('a','b','c','d','e','f','g','h')
        x, y = text_from_voice[0], int(text_from_voice[1])
        x = x.lower()
        if x not in varX:
            print("Invalid Input.")
            return (0, 0)
        if y < 1 or y > 8:
            print("Invalid Input.")
            return (0, 0)
        x1 = int(varX.index(x)) + 1
        return (x1,y)
    else:
        return (0,0)

def verify_input(input):

    if input == '':
        return False
    elif len(input) == 2:
        try:
            sec = int(input[1])
        except ValueError:
            return False
        return True

if __name__ == "__main__":
    print("Final result: ", extract_xy(recogVoice()))
