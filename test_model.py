import pickle

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

sample = ["free money claim now"]

sample_vector = vectorizer.transform(sample).toarray()
prediction = model.predict(sample_vector)

if prediction[0] == 1:
    print("SPAM")
else:
    print("HAM")