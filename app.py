from flask import Flask, render_template, request
from textblob import TextBlob
from googletrans import Translator

app = Flask(__name__)
translator = Translator()
variabile_colore = "#00ccff"

def backend(text):
    try:
        type_language = translator.detect(str(text))

        if type_language.lang != "en":
            text_translated = translator.translate(str(text), dest="en")
            text_blob = TextBlob(text_translated.text)
        else:
            text_blob = TextBlob(str(text))

        text_corrected = text_blob.correct()
        sentiment = text_corrected.sentiment.polarity

        if sentiment > 0.5:
            sentimento = "positive"
        elif sentiment > 0:
            sentimento = "neutral"
        else:
            sentimento = "negative"

        return {
            "sentimento": sentimento,
            "lingua": type_language.lang,
            "testo_corretto": text_corrected.string
        }

    except Exception as e:
        return {"errore": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        text = request.form.get("text", "")
        result = backend(text)
    return render_template("index.html", result=result, colore=variabile_colore)

@app.route('/all-functions')
def all_functions():
    return render_template('all-functions.html')

if __name__ == "__main__":
    app.run(debug=True)
