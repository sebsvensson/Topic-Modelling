import json
import os
from top2vec import Top2Vec

def load_documents(folder_path):
    print(f"Loading documents from {folder_path}...")
    documents = []
    for filename in os.listdir(folder_path):
        try:
            print(f"Checking file: {filename}")  # See which files are being checked
            if filename.endswith(".json"):
                print(f"Found JSON file: {filename}")  # Check if it's a valid JSON file
                with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                    
                    word_list = json.load(file)
                    
                    # Ensure word_list is a list of strings
                    if isinstance(word_list, list) and all(isinstance(word, str) for word in word_list):
                        documents.extend(word_list)  # Flattening into a single list of strings
                        print(f"Loaded document from {filename}: {word_list[:10]}...")  # Preview first 10 words
                    else:
                        print(f"Skipping file {filename}, it's not a list of strings.")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
    print(f"Total documents loaded: {len(documents)}")
    return documents

def run_top2vec(documents, embedding_model="universal-sentence-encoder"):
    model = Top2Vec(documents, embedding_model=embedding_model)
    return model

def display_topics(model, num_topics=5, num_words=10):
    topics, word_scores, _ = model.get_topics(num_topics)
    for i, words in enumerate(topics):
        print(f"Topic {i+1}: {', '.join(words[:num_words])}")

if __name__ == "__main__":
    folder_path = r"MY_FOLDER"  # Set your folder path
    documents = load_documents(folder_path)

    if isinstance(documents, list) and all(isinstance(word, str) for word in documents):
        print(f"Documents loaded successfully: {len(documents)} words.")
        print(f"First few words: {documents[:10]}...")  # Preview first 10 words
        model = run_top2vec(documents)
        display_topics(model)
    else:
        print("Error: Documents are not in the correct format. Please check the loaded data.")
