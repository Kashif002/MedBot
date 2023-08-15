import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
#import pyttsx3
import threading

from keras.models import load_model
model = load_model('Medbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                # if show_details:
                #     print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            #print(i['tag'])
            #print(tag)
            result = random.choice(i['responses'])
            break
    return result
        
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

'''def playResponce(self,msg):
        x=pyttsx3.init()
        print(msg)
        li = []
        if len(msg) > 1:
            if msg.find('--') == -1:
                b = msg.split('--')
                #print(b)
                 
        x.setProperty('rate',120)
        x.setProperty('volume',100)
        x.say(msg)
        x.runAndWait()
        print("Played Successfully......")'''

#Creating GUI with tkinter
import tkinter
from tkinter import *
from tkinter import font as size
        

def temp():
    msg = "Hi!,I am MedBot (A Medical Assistant Chatbot)"
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "Bot: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
#        res = chatbot_response(msg)
#        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

def entrytext():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("MedBot")
base.geometry("450x550")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0,font="Verdana", bg="#9AFEFF", height="65", width="120")
ChatLog.config(state=DISABLED)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, bg="#52595D", command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

temp()

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="10",relief=GROOVE, height=2,
bd=1, bg="#20B2AA", activebackground="#3c9d9b",fg='white',command=send)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="25", height="5", font="Verdana")


#Place all components on the screen
scrollbar.place(x=425,y=7, height=435)
ChatLog.place(x=6,y=6, height=435, width=420)
EntryBox.place(x=128, y=450, height=90, width=315)
SendButton.place(x=6, y=450, height=90)

base.mainloop ()