import pyttsx3
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["conversation"]
collection = db["qa_pairs"]

# Load conversation data from text file into a DataFrame
data = pd.read_csv("dialogs.txt", sep='\t', header=None)
data.columns = ["question", "answer"]

# Initialize text-to-speech engine
engine = pyttsx3.init()

def save_qa_pair(question, answer):
    """Save question-answer pair to MongoDB."""
    collection.insert_one({"question": question, "answer": answer})

def get_answer(question):
    """Retrieve answer from conversation data."""
    return data.loc[data["question"] == question, "answer"].values[0]

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        try:
            # Input question
            question = input("Ask a question: ")

            # Retrieve answer from MongoDB if exists, otherwise from conversation data
            saved_answer = collection.find_one({"question": question})
            if saved_answer:
                answer = saved_answer["answer"]
            else:
                answer = get_answer(question)
                save_qa_pair(question, answer)

            print(f"Answer: {answer}")
            speak(answer)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
