import time

import spacy
from spacy.matcher import Matcher
from spacytextblob.spacytextblob import SpacyTextBlob
from textblob_de import TextBlobDE
from GUI import App
import threading
from datetime import datetime
from time import sleep


@spacy.registry.misc("spacytextblob.de_blob")
def create_de_blob():
    return TextBlobDE


config = {
    "blob_only": True,
    "custom_blob": {"@misc": "spacytextblob.de_blob"}
}

nlp = spacy.load("de_core_news_lg")
nlp.add_pipe("spacytextblob", config=config)
ruler = nlp.add_pipe("entity_ruler")
matcher = Matcher(nlp.vocab)

namen = []
preis = 5
spende = 0
datum = None
email = None

pattern = [
    {
        "label": "DATUM",
        "pattern": [
            {
                "SHAPE": "dd.dd.dddd"
            },
        ]
    }
]
ruler.add_patterns(pattern)


def get_name():
    app.insert_text("Chatbot: Wie heißen Sie?")
    pattern2 = [
        {
            "LOWER": "prof.",
            "OP": "?"
        },
        {
            "LOWER": "dr.",
            "OP": "?"
        },
        {
            "LOWER": "herr",
            "OP": "?"
        },
        {
            "POS": "PROPN",
            "OP": "{2,}"
        }
    ]
    matcher.add("NAME", [pattern2], greedy="LONGEST")
    matches = matcher(nlp(app.get_input()), as_spans=True)
    if not matches:
        app.insert_text("Chatbot: Für die Ausstellung der Tickets benötige ich Vor- und Nachname. Können Sie bitte "
                        "beides angeben?")
        matches = get_name()
    namen.append(matches[0].text)
    return matches


def get_namen():
    app.insert_text("Chatbot: Listen Sie bitte die Personen auf:")
    matches = matcher(nlp(app.get_input()), as_spans=True)
    if not matches:
        app.insert_text("Chatbot: Listen Sie bitte die Personen auf und achten Sie bitte auf Vor- und "
                        "Nachnamen.")
        get_namen()
    for match in matches:
        namen.append(match.text)

    s = f"Chatbot: Alles klar. Sie"
    for name in namen:
        if namen[-1] == name:
            s += f" und {name}"
        elif namen[0] == name:
            continue
        else:
            s += f", {name}"
    s += " werden das Konzert besuchen."
    app.insert_text(s)


def get_datum():
    global datum
    app.insert_text("Chatbot: Bitte geben Sie nun das Datum des Konzerts an.")
    for ent in nlp(app.get_input()).ents:
        if ent.label_ == "DATUM":
            datum = ent.text
            if datetime.strptime(datum, "%d.%m.%Y") < datetime.today():
                app.insert_text("Chatbot: Es scheint als sei ihr Datum in der Vergangenheit. Bitte geben Sie ein "
                                "aktuelles Datum an.")
                get_datum()
            else:
                app.insert_text(f"Chatbot: Alles klar. Der {datum} wird wohl der große Tag sein.")
    if datum is None:
        app.insert_text("Chatbot: Leider konnte ich kein Datum erkennen. Bitte versuchen Sie es nochmal.")
        get_datum()


def get_spende():
    global spende
    app.insert_text("Chatbot: Wieviel möchten Sie spenden?")
    pattern3 = [
        {"LIKE_NUM": True},
        {"TEXT": "€", "OP": "?"}
    ]
    matcher.add("GELDANZAHL", [pattern3])
    matches = matcher(nlp(app.get_input()), as_spans=True)
    if not matches:
        app.insert_text("Chatbot: Leider konnte ich keine Zahl erkennen. Können Sie es erneut versuchen?")
        get_spende()
    try:
        spende = int(matches[0].text.replace("€", ""))
    except ValueError:
        app.insert_text("Chatbot: Es scheint so als hätten Sie eine Kommazahl eingegeben. Bitte beschränken Sie sich "
                        "auf ganze Zahlen.")
        get_spende()
    app.insert_text("Chatbot: Vielen Dank für ihre großzügige Spende!")


def get_email():
    global email
    app.insert_text("Chatbot: Bitte geben Sie ihre Email an, um die Rechnung und die Tickets zu erhalten.")
    pattern4 = [{"LIKE_EMAIL": True}]
    matcher.add("EMAIL", [pattern4])
    matches = matcher(nlp(app.get_input()), as_spans=True)
    if not matches:
        app.insert_text("Chatbot: Ich konnte keine Email erkennen. Haben Sie sich vielleicht vertippt?")
        get_email()
    email = matches[0].text


def get_bewertung():
    app.insert_text("Chatbot: Danke. Bitte bewerten Sie nun den Chatbot, damit er verbessert werden kann")
    doc = nlp(app.get_input())
    bewertung = doc._.blob.polarity
    if bewertung < 0:
        app.insert_text("Chatbot: Das ist schade zu hören. Bitte schlagen Sie vor, was verbessert werden kann.")
        with open("Verbesserungsvorschläge.txt", "w") as f:
            f.write(app.get_input())
        app.insert_text("Chatbot: Ich habe ihr Feedback notiert. Nun zur Ausgabe:")


def ausgabe():
    app.insert_text(f"Chatbot: Hier sind die Tickets für den {datum}")
    for name in namen:
        app.insert_text(f"Chatbot: Ticket für {name} ({preis}€)")
    app.insert_text(f"Chatbot: Spende: {spende}€")
    app.insert_text(f"Chatbot: Gesamtpreis: {preis * len(namen) + spende}€")
    app.insert_text(f"Chatbot: Die Rechnung und die Tickets werden Ihnen ({email}) sofort zugesendet.")


def chat():
    app.insert_text("Chatbot: Hallo. Möchten Sie Tickets für Emazing Rock kaufen?")
    if app.user_consent():
        get_name()
        app.insert_text(f"Chatbot: {namen[0]}, möchten Sie noch weitere Personen mitbringen?")
        if app.user_consent():
            get_namen()
        matcher.remove("NAME")
        get_datum()
        app.insert_text("Chatbot: Möchten Sie eine Spende zum Preis hinzufügen?")
        if app.user_consent():
            get_spende()
            matcher.remove("GELDANZAHL")
        get_email()
        get_bewertung()
        ausgabe()
        time.sleep(10)
        app.insert_text("Chatbot: Ich schließe mich nun in 10 Sekunden.")
        time.sleep(10)
        app.close()
    else:
        app.insert_text("Chatbot: Warum sind Sie dann hier?")
        time.sleep(5)
        chat()


if __name__ == "__main__":
    app = App()
    chat_thread = threading.Thread(target=chat)
    chat_thread.start()
    app.run()
