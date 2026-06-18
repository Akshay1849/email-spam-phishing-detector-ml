import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# Step 1: Load cleaned dataset
# -----------------------------
df = pd.read_csv("dataset/cleaned_spam.csv")

# Remove NaN / empty rows
df = df.dropna(subset=['processed_text'])
df['processed_text'] = df['processed_text'].astype(str)
df = df[df['processed_text'].str.strip() != ""]

print("Dataset loaded successfully")
print("Rows:", len(df))

# -----------------------------
# Step 2: Features and labels
# -----------------------------
X = df['processed_text']
y = df['label']

# -----------------------------
# Step 3: Convert text to numbers (TF-IDF)
# -----------------------------
vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(X).toarray()

# -----------------------------
# Step 4: Split dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Step 5: Train model
# -----------------------------
model = MultinomialNB()
model.fit(X_train, y_train)

# -----------------------------
# Step 6: Prediction
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Step 7: Evaluation
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

# -----------------------------
# Step 8: Save model + vectorizer
# -----------------------------
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel saved successfully!")
print("Vectorizer saved successfully!")

# -----------------------------
# Step 9: Custom test
# -----------------------------
sample = ["free entry claim prize now"]
sample_vector = vectorizer.transform(sample).toarray()
prediction = model.predict(sample_vector)

print("\nCustom Message:", sample[0])

if prediction[0] == 1:
    print("Prediction: SPAM")
else:
    print("Prediction: HAM")