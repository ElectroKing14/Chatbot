print("Laden...")
import os
import random
import yaml

# unterdrückt Warnungen, falls GPU nicht CODA geeignet ist
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import spacy

nlp = spacy.load("de_core_news_lg")

with open("intents.yml", 'r') as f:
    intents = yaml.safe_load(f)

with open("responses.yml", 'r') as f:
    responses = yaml.safe_load(f)


def identify_intent(p_input):
    for intent in intents:
        for example in intents[intent]:
            example = nlp(example)
            for token in p_input:
                if token and token.vector_norm and example.vector_norm:
                    if token.similarity(example) > 0.7:
                        return intent
                else:
                    if token.lemma_ == example:
                        return intent
    neue_antwort(p_input)


def get_response(intent):
    if responses[intent] is not None:
        return random.choice(responses[intent])


def neue_antwort(p_input):
    print("Darauf konnte ich leider keine Antwort in meiner Datenbank finden. Du kannst aber die Datenbank erweitern, "
          "indem du ein paar Fragen beantwortest.")
    for token in p_input:
        if token.is_stop:
            continue
        print(f"Beschreibt {token} deine Frage?")
        if identify_intent(nlp(input())) == "ja":
            intents.update({token: [token, token.lemma_]})
            print(intents)
            with open("intents.yml", "w") as f:
                yaml.safe_dump(intents, f)
            print("Was würdest du dir als Antwort wünschen?")
            input2 = input()
            responses.update({token: [input2]})
            print(responses)
            with open("responses.yml", "w") as f:
                yaml.safe_dump(responses, f)
            break


def warte_auf_eingabe():
    userinput = nlp(input())
    identify_intent(userinput)


if __name__ == "__main__":
    print(intents)
    print(responses)
    print("Hallo, ich bin ein Bot, der dich bei der Einschulung deines Kindes beim EMA beraten soll. Frage mich "
          "einfach etwas.")
    while True:
        warte_auf_eingabe()
