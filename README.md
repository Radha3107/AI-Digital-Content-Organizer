<div align="center"> <img src="https://capsule-render.vercel.app/api?type=waving&height=230&color=0:FF0000,50:EC4899,100:7C3AED&section=header&text=AI%20Digital%20Content%20Organizer&fontSize=40&fontColor=ffffff&fontAlignY=38&desc=Search%20YouTube.%20Let%20ML%20sort%20it.%20Keep%20what%20you%20love.&descSize=18&descAlignY=58" alt="AI Digital Content Organizer" width="100%"/> <br/> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/> <img src="https://img.shields.io/badge/Gradio-F97316?style=for-the-badge" alt="Gradio"/> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/> <img src="https://img.shields.io/badge/YouTube_API_v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube API"/> <img src="https://img.shields.io/badge/Accuracy-97.5%25-22C55E?style=for-the-badge" alt="Accuracy 97.5%"/>

<br/><br/>

</div>
✨ What it does
<table align="center"> <tr> <td align="center" width="25%"> <h1>🔎</h1> <b>Retrieve</b><br/> <sub>Fetch real, public YouTube videos for any topic</sub> </td> <td align="center" width="25%"> <h1>🤖</h1> <b>Classify</b><br/> <sub>TF-IDF + Logistic Regression picks 1 of 8 categories</sub> </td> <td align="center" width="25%"> <h1>🗂️</h1> <b>Organize</b><br/> <sub>Group results by category with a confidence score</sub> </td> <td align="center" width="25%"> <h1>📚</h1> <b>Save</b><br/> <sub>Build a searchable personal library</sub> </td> </tr> </table>

💡 Note: the YouTube Data API only retrieves video data. The AI is our own TF-IDF + Logistic Regression model.

<br/>
🎬 Demo

📸 Add a screenshot or GIF here: save it as docs/demo.png and replace this line with ![Demo](docs/demo.png)

<br/>
🏷️ Categories
<div align="center"> <img src="https://img.shields.io/badge/📚_Education-3B82F6?style=for-the-badge" alt="Education"/> <img src="https://img.shields.io/badge/💻_Technology-8B5CF6?style=for-the-badge" alt="Technology"/> <img src="https://img.shields.io/badge/🏋️_Fitness-EF4444?style=for-the-badge" alt="Fitness"/> <img src="https://img.shields.io/badge/🍔_Food-F59E0B?style=for-the-badge" alt="Food"/> <br/> <img src="https://img.shields.io/badge/✈️_Travel-06B6D4?style=for-the-badge" alt="Travel"/> <img src="https://img.shields.io/badge/🎬_Entertainment-EC4899?style=for-the-badge" alt="Entertainment"/> <img src="https://img.shields.io/badge/👗_Fashion-D946EF?style=for-the-badge" alt="Fashion"/> <img src="https://img.shields.io/badge/🎮_Gaming-22C55E?style=for-the-badge" alt="Gaming"/> </div> <br/>
⚙️ How it works
🔎 Search topic
▶️ YouTube API
📝 Title + description
🔢 TF-IDF
🤖 Logistic Regression
🏷️ Category + confidence
📚 My Library

<sub>TF-IDF turns text into numbers by weighting distinctive words higher. Logistic Regression is a supervised classifier that turns those numbers into a probability for each category. The top one is the prediction, and its probability is the confidence score.</sub>

<br/>
🚀 Quick start

1. Clone and install

bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt

2. Add your YouTube API key in a .env file

env
YOUTUBE_API_KEY=your_api_key_here

3. Run

bash
python app.py

Open http://localhost:7860 🎉

<br/>
📊 Results
<div align="center">
🎯 Test accuracy	🧪 Test set	🧠 Model
97.50%	40 samples	TF-IDF + Logistic Regression
</div> <details> <summary><b>🎥 See an example demo run</b></summary> <br/>

Search: Python Programming → 10 videos retrieved

📚 Education	💻 Technology	🧠 Avg. confidence
9 videos	1 video	≈ 29.9%

This is a single example run, not a general performance measure. Confidence is lower than accuracy because the model spreads probability across 8 categories. Low confidence means uncertain, not necessarily wrong.

</details> <br/>
🧰 Built with
	
🖥️ Interface	Gradio
🐍 Backend	Python · Pandas · Requests
📡 Data	YouTube Data API v3
🤖 ML	scikit-learn
💾 Storage	CSV + JSON
<details> <summary><b>📁 Project structure</b></summary>
text
.
├── app.py              # Gradio UI + personal library
├── services/           # YouTube API retrieval
├── model/              # TF-IDF + Logistic Regression
├── data/               # Datasets, CSV export, library JSON
├── utils/              # Helpers
└── .env                # API key (never commit!)
</details> <br/>
🔭 Limitations & roadmap
<table> <tr> <td width="50%" valign="top">

⚠️ Limitations

Uses title and description only, not video or audio
8 predefined categories
API quota can limit searches
Small (40-sample) test set
</td> <td width="50%" valign="top">

🗺️ Coming next

BERT / Transformer classifier
Multilingual support
More categories and platforms
Cloud deployment and mobile app
</td> </tr> </table> <details> <summary><b>📚 References</b></summary> <br/>
YouTube Data API · Search: list
scikit-learn · TfidfVectorizer · LogisticRegression
Gradio docs
Manning, Raghavan & Schütze (2008). Introduction to Information Retrieval. Cambridge University Press.
Sebastiani (2002). Machine Learning in Automated Text Categorization. ACM Computing Surveys, 34(1).
</details> <br/> <div align="center">

Made by Radhika Chaudhari · B.Tech CSE, Semester 5<br/> Symbiosis Institute of Technology, Nagpur · Guide: [Guide Name]

⭐ If you like it, give it a star!

<img src="https://capsule-render.vercel.app/api?type=waving&height=120&color=0:7C3AED,50:EC4899,100:FF0000&section=footer" alt="" width="100%"/> </div>
