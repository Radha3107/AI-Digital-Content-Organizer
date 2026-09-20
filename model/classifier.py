import pickle


MODEL_PATH = "model/content_classifier.pkl"


# Load trained model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


def classify_content(text):
    """
    Classify digital content into one of the trained categories.
    Returns category and confidence.
    """

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities)

    return prediction, confidence


# Run standalone tests only when this file is executed directly
if __name__ == "__main__":

    test_contents = [
        "Complete Python programming tutorial with projects",
        "Best home workout for building muscle",
        "Easy chicken pasta recipe for dinner",
        "Top places to visit in Goa this summer",
        "Latest smartphone technology review",
        "Best outfit ideas for college students",
        "Minecraft survival gameplay and tips",
        "Best new movies to watch this weekend"
    ]

    print("\nAI Digital Content Organizer")
    print("============================\n")

    for content in test_contents:

        category, confidence = classify_content(content)

        print(f"Content: {content}")
        print(f"Category: {category}")
        print(f"Confidence: {confidence:.2%}")
        print("-" * 60)