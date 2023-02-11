import os
import random
import yaml

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import spacy

nlp = spacy.load("de_core_news_lg")

with open("intents.yml", 'r') as f:
    intents = yaml.load(f, yaml.Loader)

with open("responses.yml", 'r') as f:
    responses = yaml.load(f, yaml.Loader)


def identify_intent(p_input):
    for intent in intents:
        for example in intent:
            for token in p_input:
                if token in example:
                    if p_input.similarity(nlp(example)) > 0.7:
                        return intent
                if token.lemma_.similarity(nlp(example)) > 0.7:
                    return intent
    neue_antwort(p_input)



def get_response(intent):
    for response in responses:
        if response[intent] is not None:
            return random.choice(response[intent])


def neue_antwort(p_input):
    print("Darauf konnte ich leider keine Antwort in meiner Datenbank finden. Du kannst aber eine Antwort hinzufügen,"
          "die dich zufrieden stellen würde.")
    print("Gewünschte Antwort:", end="")
    input2 = input()
    if identify_intent(input2) == "Ablehnung":
        warte_auf_eingabe()



def warte_auf_eingabe():
    userinput = nlp(input())
    ausgabe(userinput)


def ausgabe(userinput):
    print(get_response(identify_intent(userinput)))
