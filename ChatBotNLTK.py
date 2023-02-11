from nltk.chat.util import Chat
import json

with open("daten.json", 'r') as f:
    daten = json.load(f)

chatbot = Chat(daten)

print("Hallo. Ich bin ein Chatbot programmiert mit NLTK. Frage mich einfach etwas zum Thema [].")
while True:
    try:
        antwort = chatbot.respond(input())
        if antwort is None:
            print("Das habe ich nicht verstanden. Kannst du das wiederholen?")
        else:
            print(antwort)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
