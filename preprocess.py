import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download stopwords once (first time only)
nltk.download('stopwords')

# Load dataset
df = pd.read_csv("dataset/spam.csv", encoding="latin-1")

# Keep only useful columns
df = df[['v1', 'v2']]
df.columns = ['label', 'text']

# Convert labels to numbers
df['label'] = df['label'].map({
    'ham': 0,
    'spam': 1
})

# NLP setup
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Preprocessing function
def preprocess_text(text):
    text = text.lower()                      # lowercase
    text = re.sub('[^a-zA-Z]', ' ', text)   # remove punctuation/numbers
    words = text.split()                    # tokenize

    words = [
        ps.stem(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

# Process all messages
corpus = []

for text in df['text']:
    processed_text = preprocess_text(text)
    corpus.append(processed_text)

# Add processed column
df['processed_text'] = corpus

# Print sample output
print(df.head())

# Save cleaned dataset
df.to_csv("dataset/cleaned_spam.csv", index=False)

print("\nPreprocessing completed successfully!")
print("Saved as dataset/cleaned_spam.csv")