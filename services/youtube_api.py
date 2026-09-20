import os
import sys
import requests

from dotenv import load_dotenv

# Allow importing from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.classifier import classify_content


load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_youtube(query, max_results=5):

    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY is missing from .env")

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "order": "relevance",
        "regionCode": "IN",
        "relevanceLanguage": "en",
        "key": API_KEY
    }

    response = requests.get(
        YOUTUBE_SEARCH_URL,
        params=params,
        timeout=15
    )

    if response.status_code != 200:
        raise Exception(
            f"YouTube API Error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    videos = []

    for item in data.get("items", []):

        video_id = item["id"].get("videoId")
        snippet = item["snippet"]

        if not video_id:
            continue

        title = snippet.get("title", "")
        description = snippet.get("description", "")

        # Combine title + description for AI classification
        content_text = f"{title} {description}"

        category, confidence = classify_content(content_text)

        videos.append({
            "video_id": video_id,
            "title": title,
            "description": description,
            "channel": snippet.get("channelTitle", ""),
            "published_at": snippet.get("publishedAt", ""),
            "thumbnail": snippet.get("thumbnails", {})
                .get("medium", {})
                .get("url", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "category": category,
            "confidence": confidence
        })

    return videos


if __name__ == "__main__":

    print("\nAI Digital Content Organizer")
    print("============================\n")

    query = input("Enter search topic: ")

    try:

        results = search_youtube(query, max_results=5)

        print(f"\nFound {len(results)} videos\n")

        for i, video in enumerate(results, 1):

            print(f"{i}. {video['title']}")
            print(f"   Channel: {video['channel']}")
            print(f"   Category: {video['category']}")
            print(f"   Confidence: {video['confidence']:.2%}")
            print(f"   URL: {video['url']}")
            print("-" * 70)

    except Exception as e:

        print(f"Error: {e}")