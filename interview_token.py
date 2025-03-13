import re
import os
import json
import spacy
import nltk
from nltk.corpus import stopwords
from langdetect import detect

nlp_sv = spacy.load("sv_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

nltk.download("stopwords")
swedish_stopwords = set(stopwords.words("swedish"))
english_stopwords = set(stopwords.words("english"))

def detect_language(text):
    """"Detect the language of a given text."""
    try:
        return detect(text)
    except:
        return "unknown"
    
def preprocess_text(text, language):
    """"Tokenizes, removes stopwords, and lemmatizes text based on language"""
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = text.lower()  # Convert to lowercase

    if language == "sv":
        doc = nlp_sv(text)
        stopwords_set = swedish_stopwords
    else:
        doc = nlp_en(text)
        stopwords_set = english_stopwords

    tokens = [token.lemma_ for token in doc if token.text not in stopwords_set and len(token.text) > 2]

    exclude_words = {"speaker", "speak", "speaking", "spoken", "speaks"}  # add more variations if needed

    tokens = [token.lemma_ for token in doc if token.text not in stopwords_set and len(token.text) > 2 and token.text not in exclude_words]

    return tokens

input_folder = r"MY_FOLDER"
output_folder = r"NEW_FOLDER"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure data is a list of dictionaries (or a list of strings)
        if isinstance(data, list):
            if isinstance(data[0], dict):  # Checking if the first element is a dictionary
                text = " ".join([segment["text"] for segment in data if isinstance(segment, dict) and "text" in segment])
            elif isinstance(data[0], str):  # If the list consists of strings
                text = " ".join(data)
            else:
                raise ValueError("Unknown format in 'data' elements")
        else:
            raise ValueError("Expected 'data' to be a list, but found a different structure")


        lang = detect_language(text)

        tokenized_text = preprocess_text(text, lang)

        output_file = os.path.join(output_folder, filename)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(tokenized_text, f, ensure_ascii=False, indent=4)

        print(f"Processed: {filename} (Detcted language: {lang})")

print ("Tokenization completed for all files")