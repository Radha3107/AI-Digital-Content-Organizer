# 🤖 AI Based Digital Content Organizer

An AI-powered digital content organization system that retrieves real-time YouTube content and automatically classifies it into meaningful categories using Machine Learning.

The project combines the **YouTube Data API v3**, **TF-IDF**, **Logistic Regression**, and a **Gradio GUI** to provide an interactive content discovery and organization platform.

---

## 📌 Project Overview

With the rapid growth of digital content, users often need to search through a large number of videos and manually identify and organize useful content.

The **AI Based Digital Content Organizer** automates this process.

The system:

1. Accepts a topic from the user.
2. Retrieves real-time YouTube videos using the YouTube Data API v3.
3. Extracts video titles and descriptions.
4. Converts textual information into numerical features using TF-IDF.
5. Classifies the content using a trained Logistic Regression model.
6. Assigns each video to a predefined category.
7. Displays the predicted category and confidence score.
8. Organizes videos category-wise through a Gradio interface.
9. Allows users to save and manage videos in a personal content library.

---

## ✨ Features

### 🔎 Real-Time Content Search
Search for topics such as:

- Python Programming
- Artificial Intelligence
- Fitness
- Travel
- Gaming
- Food
- Fashion
- Technology

The system retrieves real public YouTube videos based on the search query.

### 🤖 AI-Based Content Classification

The machine learning pipeline uses:

**TF-IDF → Logistic Regression → Category Prediction**

The system classifies content into:

- 📚 Education
- 💻 Technology
- 🏋️ Fitness
- 🍔 Food
- ✈️ Travel
- 🎬 Entertainment
- 👗 Fashion
- 🎮 Gaming

### 📊 Confidence Score

For every classified video, the system displays the model's prediction confidence.

Example:

```text
Category: Education
Confidence: 82.45%
