<div align="center">
▶️ AI Based Digital Content Organizer
Search YouTube. Let machine learning sort it. Keep what you love.
<p> <img src="https://img.shields.io/badge/Python-3.9%2B-FF0000?style=for-the-badge&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Gradio-UI-0F0F0F?style=for-the-badge&logo=gradio&logoColor=white" alt="Gradio"> <img src="https://img.shields.io/badge/scikit--learn-ML-FF0000?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"> <img src="https://img.shields.io/badge/YouTube%20Data%20API-v3-0F0F0F?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube Data API v3"> <img src="https://img.shields.io/badge/Test%20Accuracy-97.50%25-FF0000?style=for-the-badge" alt="Test accuracy 97.50%"> </p>

An ML-powered app that retrieves real public YouTube videos for any topic, classifies them into 8 categories with a confidence score, and lets you save them to a searchable personal library.

Features · How it works · Quick start · Results · Roadmap

</div>
🎬 Demo
<!-- ➜ Add a screenshot or GIF of your running app here, e.g.: 1. Run the app, search a topic, take a screenshot. 2. Save it as docs/demo.png (or docs/demo.gif). 3. Replace the line below with: ![App demo](docs/demo.png) -->

📸 Add a screenshot or GIF of the app here (docs/demo.png).

🧠 What is this?

There is far more online video than anyone can sort by hand. Search gives you a list ranked by relevance, but it does not organize the results into categories, and bookmarking means doing all the sorting yourself.

AI Based Digital Content Organizer closes that gap in one workflow:

Retrieve real videos → Classify them with ML → Organize by category → Save to a personal library.

⚠️ Important clarification

The YouTube Data API is not the AI model. It is used only to retrieve public video data. The classification is done by our own model: TF-IDF + Logistic Regression (scikit-learn).

✨ Features
	Feature	Description
🔎	Live YouTube search	Fetches real, public video metadata for any topic you type
🤖	AI classification	TF-IDF + Logistic Regression assigns each video to one of 8 categories
📊	Confidence score	Every prediction shows how certain the model is (High / Medium / Low)
🗂️	Category-wise organization	Results grouped by category, with counts and a distribution chart
🖼️	Rich video cards	Thumbnail, title, channel, description, predicted category and a YouTube link
📚	Personal library	Save videos, search them, filter by category, avoid duplicates
📥	CSV export	Download the current search results as a .csv file
🧩	Modular code	API, classifier, training, UI and storage live in separate modules
🏷️ The 8 categories
📚 Education	💻 Technology	🏋️ Fitness	🍔 Food
✈️ Travel	🎬 Entertainment	👗 Fashion	🎮 Gaming
⚙️ How it works
🔎 User search query
🖥️ Gradio interface
▶️ YouTube Data API v3
📝 Video title + description
🧹 Text processing
🔢 TF-IDF vectorization
🤖 Logistic Regression
🏷️ Category + confidence
🗂️ Organized content
📚 Personal libraryCSV + JSON
<details> <summary><b>🔢 What is TF-IDF?</b></summary> <br/>

Computers cannot read words, so text must become numbers. TF-IDF (Term Frequency – Inverse Document Frequency) gives each word a weight:

TF: how often a word appears in this text.
IDF: how rare the word is across all texts. Common words like "video" get a low weight; distinctive words like "workout" or "itinerary" get a high one.
TF-IDF = TF × IDF

TF-IDF is a feature-extraction technique, not an AI model by itself.

</details> <details> <summary><b>🤖 What is Logistic Regression?</b></summary> <br/>

A supervised classification algorithm. It is trained on texts with known categories and learns which words point to which category. For a new video it produces a probability for each of the 8 categories (softmax). The highest probability becomes the predicted category, and it is shown as the confidence score.

Why it fits this project: it is fast, needs no GPU, works very well on sparse TF-IDF features, and gives probabilities out of the box.

</details>
🧰 Tech stack
Layer	Technology
🖥️ Frontend	Gradio
🐍 Backend / application	Python, Pandas, Requests
📡 Data retrieval	YouTube Data API v3
🤖 ML pipeline	scikit-learn: TF-IDF + Logistic Regression
💾 Storage	CSV + JSON
📁 Project structure
text
.
├── app.py                # Gradio UI, result rendering, personal-library logic
├── services/
│   └── youtube_api.py    # YouTube Data API v3 retrieval (search_youtube)
├── model/                # TF-IDF + Logistic Regression: training and classifier
├── data/                 # Training data, organized_content.csv, my_content_library.json
├── utils/                # Helper functions
├── .env                  # Your API key (never commit this file!)
└── requirements.txt
🚀 Quick start
1️⃣ Clone the repository
bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
2️⃣ Create a virtual environment and install dependencies
bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
3️⃣ Add your YouTube Data API key

Create a key in the Google Cloud Console (enable YouTube Data API v3), then create a .env file in the project root:

env
YOUTUBE_API_KEY=your_api_key_here

🔐 The key is read from .env and is never hard-coded. Make sure .env is listed in your .gitignore. <br/>(Use the exact variable name your services/youtube_api.py reads.)

4️⃣ Train the model (if a trained model is not already included)
bash
# run the training script inside the model/ folder
python model/<your_training_script>.py
5️⃣ Launch the app
bash
python app.py

Open http://localhost:7860 in your browser. 🎉

🕹️ How to use
Type a topic, for example Python programming, home workout or Japan travel.
Choose how many videos (5, 10, 15 or 20) and click 🚀 Organize Content.
Explore the results: statistics, category distribution, and video cards with the predicted category and confidence.
Click 💾 Save Current Results to My Library to keep them.
Search your library by title, channel or category, or filter by category.
Use 📥 Download Current Search CSV to export the results.
📊 Results
Model evaluation
Model	Features	Test accuracy	Test set
Logistic Regression	TF-IDF	97.50%	40 samples

📝 The test set is small, so treat this as an indication of performance, not a guarantee. No other metrics (precision, recall, F1) are claimed here.

🎥 Example demo run (one query, not universal performance)
	
Search query	Python Programming
Videos retrieved	10
Distribution	📚 Education: 9 · 💻 Technology: 1
Average AI confidence	≈ 29.9%

💡 Why is confidence lower than accuracy? They measure different things. Accuracy counts how often the top prediction is right on a prepared test split. Confidence is the probability the model gives its top choice, and with 8 categories that probability is spread out, especially for short or ambiguous real-world titles. A low confidence means the model is uncertain, not necessarily wrong. That is why the app shows it to you.

⚖️ Strengths & limitations
<table> <tr> <td width="50%" valign="top">
✅ Strengths
Automated categorization
Real-time YouTube retrieval
Simple, clean interface
Lightweight ML approach
Confidence score for every prediction
Personal content library
Modular architecture
</td> <td width="50%" valign="top">
⚠️ Limitations
Depends on title and description quality
Limited to 8 predefined categories
Text-only: does not analyze actual video or audio
YouTube API quota can limit retrieval
Low-confidence predictions for ambiguous content
Evaluated on a small (40-sample) test split
</td> </tr> </table>
🗺️ Roadmap
 🧠 Transformer / BERT-based classification
 🌍 Multilingual classification
 🏷️ Additional content categories (and an "Other" class)
 🌐 Support for more content platforms
 💬 Caption and tag-based analysis
 ⭐ Personalized recommendations
 ☁️ Cloud deployment
 🔍 Advanced search and filtering
 📱 Mobile application
 🔄 Continuous model retraining
📚 References
YouTube Data API documentation
YouTube Data API: Search: list
scikit-learn documentation
TfidfVectorizer
LogisticRegression
Gradio documentation
Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.
Sebastiani, F. (2002). Machine Learning in Automated Text Categorization. ACM Computing Surveys, 34(1).
🎓 About

Built as a Mini Project at Symbiosis Institute of Technology, Nagpur Campus (Symbiosis International (Deemed University)).

	
👩‍💻 Developer	Radhika Chaudhari, B.Tech Computer Science Engineering, Semester 5
🧑‍🏫 Guide	[Guide Name]
<div align="center"> <br/>

If you found this project useful, please give it a ⭐

Made with Python, scikit-learn and a lot of ▶️

</div>
