import pandas as pd
from pathlib import Path
import random

random.seed(2026)

categories = {
    "Education": {
        "topics": ["Python programming", "Java programming", "data structures", "algorithms", "database management", "computer networks", "operating systems", "machine learning", "artificial intelligence", "web development", "cybersecurity", "cloud computing", "compiler design", "discrete mathematics", "software engineering", "SQL", "JavaScript", "C programming", "data science", "programming fundamentals"],
        "formats": ["tutorial", "full course", "complete guide", "lecture", "study guide", "concept explanation", "practice session", "exam preparation", "hands-on tutorial", "project tutorial"],
        "contexts": ["for beginners", "from scratch", "with practical examples", "with real projects", "step by step", "for college students", "with coding exercises", "for interview preparation"]
    },

    "Technology": {
        "topics": ["artificial intelligence", "generative AI", "smartphones", "laptops", "robotics", "cloud technology", "cybersecurity technology", "virtual reality", "electric vehicles", "computer processors", "AI tools", "software technology", "computer hardware", "future technology", "internet technology", "wearable technology", "automation", "5G technology", "technology trends", "emerging technologies"],
        "formats": ["technology news", "latest trends", "product review", "technology explained", "future predictions", "innovation report", "comparison", "hands-on review", "industry update", "technology guide"],
        "contexts": ["you should know", "in 2026", "explained simply", "for everyday users", "with real examples", "for beginners", "in the real world", "and what it means for the future"]
    },

    "Fitness": {
        "topics": ["home workout", "strength training", "muscle building", "weight loss", "morning yoga", "cardio workout", "abs workout", "leg workout", "upper body workout", "bodyweight exercises", "flexibility training", "gym workout", "beginner fitness", "mobility exercises", "workout routine", "fitness motivation", "healthy fitness habits", "full body workout", "stretching routine", "functional training"],
        "formats": ["workout", "routine", "training plan", "exercise guide", "fitness tutorial", "beginner session", "workout challenge", "training session", "fitness tips", "exercise tutorial"],
        "contexts": ["for beginners", "at home", "without equipment", "for building strength", "for a healthy lifestyle", "step by step", "for busy people", "with proper form"]
    },

    "Food": {
        "topics": ["pasta", "pizza", "chocolate cake", "Indian breakfast", "biryani", "chicken recipe", "vegetarian recipe", "healthy salad", "homemade burger", "rice recipe", "dessert", "soup", "sandwich", "noodle recipe", "quick snacks", "healthy dinner", "breakfast ideas", "baking", "Indian curry", "easy lunch"],
        "formats": ["easy recipe", "quick recipe", "step by step recipe", "cooking tutorial", "homemade recipe", "beginner cooking guide", "healthy recipe", "traditional recipe", "15 minute recipe", "simple cooking idea"],
        "contexts": ["at home", "for beginners", "with simple ingredients", "for a quick dinner", "without an oven", "on a budget", "with easy instructions", "for busy days"]
    },

    "Travel": {
        "topics": ["Goa", "Mumbai", "Delhi", "Dubai", "Singapore", "Paris", "London", "Europe", "India", "Thailand", "Japan", "Bali", "Kerala", "Rajasthan", "weekend trips", "solo travel", "budget travel", "beach destinations", "mountain destinations", "international travel"],
        "formats": ["travel guide", "travel vlog", "destination guide", "trip planning guide", "travel tips", "tourist guide", "itinerary", "travel documentary", "budget travel guide", "destination review"],
        "contexts": ["for first-time visitors", "on a budget", "for a weekend trip", "with a complete itinerary", "for solo travelers", "with local tips", "for your next vacation", "with places to visit"]
    },

    "Entertainment": {
        "topics": ["new movies", "Bollywood movies", "Hollywood movies", "web series", "music releases", "movie trailers", "comedy movies", "action movies", "romantic movies", "Netflix series", "celebrity interviews", "movie reviews", "music videos", "popular songs", "entertainment news", "movie recommendations", "TV series", "film analysis", "celebrity news", "weekend entertainment"],
        "formats": ["review", "trailer", "recommendation", "reaction", "interview", "analysis", "news update", "watchlist", "top picks", "discussion"],
        "contexts": ["you should watch", "this week", "of the year", "for the weekend", "explained", "with spoilers", "without spoilers", "for movie fans"]
    },

    "Fashion": {
        "topics": ["college outfits", "summer fashion", "winter outfits", "streetwear", "casual outfits", "formal outfits", "jeans styling", "wardrobe essentials", "fashion trends", "accessories", "minimalist fashion", "party outfits", "office outfits", "everyday fashion", "sneaker styling", "color combinations", "outfit ideas", "clothing trends", "fashion styling", "capsule wardrobe"],
        "formats": ["styling guide", "outfit ideas", "fashion tips", "lookbook", "fashion tutorial", "style guide", "trend report", "outfit inspiration", "wardrobe guide", "fashion haul"],
        "contexts": ["for college students", "for beginners", "on a budget", "for everyday wear", "for the new season", "with affordable pieces", "for a modern look", "step by step"]
    },

    "Gaming": {
        "topics": ["Minecraft", "Valorant", "GTA", "Fortnite", "Call of Duty", "PlayStation games", "Xbox games", "PC gaming", "mobile games", "open world games", "multiplayer games", "gaming laptops", "gaming PCs", "game releases", "gaming accessories", "game walkthroughs", "competitive gaming", "survival games", "role playing games", "gaming setup"],
        "formats": ["gameplay", "beginner guide", "review", "walkthrough", "tips and tricks", "gaming news", "setup guide", "game analysis", "gameplay highlights", "gaming tutorial"],
        "contexts": ["for beginners", "you should try", "in 2026", "with tips and tricks", "for new players", "with the best settings", "for competitive players", "with a complete guide"]
    }
}

templates = [
    "{topic} {format} {context}",
    "Complete {topic} {format} {context}",
    "{topic}: {format} {context}",
    "Best {topic} {format} {context}",
    "Learn {topic} with this {format} {context}",
    "Ultimate {topic} {format} {context}",
    "{topic} explained: {format} {context}",
    "Everything about {topic}: {format} {context}"
]

rows = []

for category, info in categories.items():

    used = set()

    while len(used) < 150:

        topic = random.choice(info["topics"])
        format_type = random.choice(info["formats"])
        context = random.choice(info["contexts"])

        text = random.choice(templates).format(
            topic=topic,
            format=format_type,
            context=context
        )

        if random.random() < 0.4:
            text += ". Practical tips and useful information."

        if text.lower() not in used:
            used.add(text.lower())

            rows.append({
                "text": text,
                "category": category
            })

df = pd.DataFrame(rows)

# Shuffle dataset
df = df.sample(frac=1, random_state=2026).reset_index(drop=True)

# IMPORTANT: pandas automatically quotes text containing commas
output = Path("data/training_data.csv")
output.parent.mkdir(exist_ok=True)

df.to_csv(output, index=False, quoting=1)

print("===================================")
print("DATASET CREATED SUCCESSFULLY")
print("===================================")
print(f"Total samples: {len(df)}")
print("\nSamples per category:")
print(df["category"].value_counts().sort_index())
print(f"\nSaved to: {output}")