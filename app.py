import gradio as gr
from collections import Counter
from urllib.parse import urlparse, parse_qs
import csv
import os
import json

from services.youtube_api import search_youtube


# =====================================================
# CATEGORY ICONS
# =====================================================

CATEGORY_ICONS = {
    "Education": "📚",
    "Technology": "💻",
    "Fitness": "🏋️",
    "Food": "🍔",
    "Travel": "✈️",
    "Entertainment": "🎬",
    "Fashion": "👗",
    "Gaming": "🎮"
}


# =====================================================
# GET YOUTUBE VIDEO ID
# =====================================================

def get_video_id(url):
    """Extract YouTube video ID from a URL."""

    try:

        parsed = urlparse(url)

        # Example:
        # https://youtu.be/ABC123
        if parsed.hostname == "youtu.be":
            return parsed.path.strip("/")

        # Example:
        # https://www.youtube.com/watch?v=ABC123
        if parsed.hostname and "youtube.com" in parsed.hostname:

            return parse_qs(
                parsed.query
            ).get("v", [None])[0]

    except Exception:
        pass

    return None


# =====================================================
# GET YOUTUBE THUMBNAIL
# =====================================================

def get_thumbnail(url):
    """Generate YouTube thumbnail URL."""

    video_id = get_video_id(url)

    if video_id:

        return (
            f"https://img.youtube.com/vi/"
            f"{video_id}/hqdefault.jpg"
        )

    return ""


# =====================================================
# SAVE CONTENT TO CSV
# =====================================================

def save_to_csv(videos):

    os.makedirs("data", exist_ok=True)

    file_path = "data/organized_content.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Title",
            "Channel",
            "Category",
            "Confidence",
            "YouTube URL"
        ])

        for video in videos:

            writer.writerow([
                video.get("title", ""),
                video.get("channel", ""),
                video.get("category", ""),
                f"{video.get('confidence', 0) * 100:.2f}%",
                video.get("url", "")
            ])

    return file_path


# =====================================================
# PERSONAL CONTENT LIBRARY
# =====================================================

LIBRARY_PATH = "data/my_content_library.json"


def load_library():
    """Load saved content from the local persistent library."""
    try:
        if os.path.exists(LIBRARY_PATH):
            with open(LIBRARY_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
    except Exception:
        pass
    return []


def save_library(videos):
    """Persist saved content locally as JSON."""
    os.makedirs("data", exist_ok=True)
    with open(LIBRARY_PATH, "w", encoding="utf-8") as file:
        json.dump(videos, file, indent=2, ensure_ascii=False)


def merge_library(existing, new_videos):
    """Add new videos without creating duplicate URLs."""
    by_url = {item.get("url"): item for item in existing if item.get("url")}
    for video in new_videos:
        url = video.get("url")
        if url:
            by_url[url] = video
    return list(by_url.values())


def library_html(videos, search_text="", category="All"):
    """Render the persistent personal library with search and category filtering."""
    search_text = (search_text or "").strip().lower()
    category = category or "All"

    filtered = []
    for video in videos:
        title = str(video.get("title", ""))
        channel = str(video.get("channel", ""))
        video_category = str(video.get("category", "Other"))

        matches_search = (
            not search_text
            or search_text in title.lower()
            or search_text in channel.lower()
            or search_text in video_category.lower()
        )
        matches_category = category == "All" or video_category == category

        if matches_search and matches_category:
            filtered.append(video)

    counts = Counter(
        str(video.get("category", "Other")) for video in videos
    )

    html = f"""
    <div class="library-header">
        <div>
            <h2>📚 My Content Library</h2>
            <p>{len(videos)} saved item(s) • {len(filtered)} currently shown</p>
        </div>
    </div>

    <div class="library-stats">
        <div><strong>{len(videos)}</strong><span>Total Saved</span></div>
        <div><strong>{len(counts)}</strong><span>Categories</span></div>
        <div><strong>{sum(counts.values())}</strong><span>Organized Items</span></div>
    </div>
    """

    if not filtered:
        html += """
        <div class="empty-box">
            🔎 No saved content matches your search/filter.
        </div>
        """
        return html

    for video in filtered:
        title = video.get("title", "Untitled Video")
        channel = video.get("channel", "Unknown Channel")
        url = video.get("url", "#")
        category_name = video.get("category", "Other")
        confidence = float(video.get("confidence", 0)) * 100
        icon = CATEGORY_ICONS.get(category_name, "📂")
        thumbnail = get_thumbnail(url)

        html += f"""
        <div class="library-card">
            <div class="library-thumb">
        """

        if thumbnail:
            html += f'<img src="{thumbnail}" class="thumbnail" alt="YouTube thumbnail">'
        else:
            html += '<div class="no-thumbnail">▶</div>'

        html += f"""
            </div>
            <div class="library-content">
                <h3>{title}</h3>
                <p class="channel">👤 {channel}</p>
                <div class="video-meta">
                    <span class="badge">{icon} {category_name}</span>
                    <span class="confidence">🧠 {confidence:.2f}%</span>
                </div>
                <a href="{url}" target="_blank" class="watch-button">▶ Watch on YouTube</a>
            </div>
        </div>
        """

    return html


def save_current_to_library(current_videos):
    """Save the latest search results to the persistent library."""
    current_videos = current_videos or []
    if not current_videos:
        library = load_library()
        return library_html(library), "⚠️ Search for content first."

    library = merge_library(load_library(), current_videos)
    save_library(library)
    added = len(library) - len(load_library()) if False else len(current_videos)
    return library_html(library), f"✅ Saved {len(current_videos)} result(s) to My Library. Duplicates are automatically avoided."


def refresh_library():
    library = load_library()
    return library_html(library), gr.update(choices=["All"] + sorted({v.get("category", "Other") for v in library}))


def filter_library(search_text, category):
    library = load_library()
    return library_html(library, search_text, category)


def clear_library():
    save_library([])
    return library_html([]), "🗑️ My Library has been cleared."


# =====================================================
# MAIN ORGANIZER FUNCTION
# =====================================================

def organize_content(query, max_results):

    if not query or not query.strip():

        return (
            """
            <div class="empty-box">
                🔎 Enter a topic to organize digital content.
            </div>
            """,
            None
        )

    try:

        # ---------------------------------------------
        # SEARCH YOUTUBE
        # ---------------------------------------------

        videos = search_youtube(
            query=query.strip(),
            max_results=int(max_results)
        )

        if not videos:

            return (
                """
                <div class="empty-box">
                    ❌ No content found.
                </div>
                """,
                None,
                []
            )

        # ---------------------------------------------
        # SAVE RESULTS
        # ---------------------------------------------

        csv_file = save_to_csv(videos)

        # ---------------------------------------------
        # ORGANIZE BY CATEGORY
        # ---------------------------------------------

        organized = {}

        for video in videos:

            category = video.get(
                "category",
                "Other"
            )

            if category not in organized:

                organized[category] = []

            organized[category].append(video)

        # ---------------------------------------------
        # STATISTICS
        # ---------------------------------------------

        total_videos = len(videos)

        total_categories = len(organized)

        confidence_values = [
            float(video.get("confidence", 0)) * 100
            for video in videos
        ]

        if confidence_values:

            average_confidence = (
                sum(confidence_values)
                / len(confidence_values)
            )

        else:

            average_confidence = 0

        # ---------------------------------------------
        # CATEGORY COUNTS
        # ---------------------------------------------

        category_counts = Counter(
            video.get(
                "category",
                "Other"
            )
            for video in videos
        )

        # ---------------------------------------------
        # START HTML
        # ---------------------------------------------

        html = f"""

        <div class="dashboard">

            <!-- HERO -->

            <div class="hero">

                <div class="hero-icon">
                    🤖
                </div>

                <div>

                    <h1>
                        AI Digital Content Organizer
                    </h1>

                    <p>
                        Real-time digital content discovery
                        and intelligent AI classification.
                    </p>

                </div>

            </div>


            <!-- STATISTICS -->

            <div class="stats">

                <div class="stat-card">

                    <div class="stat-icon">
                        📺
                    </div>

                    <div class="stat-number">
                        {total_videos}
                    </div>

                    <div class="stat-label">
                        Videos Analyzed
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon">
                        📂
                    </div>

                    <div class="stat-number">
                        {total_categories}
                    </div>

                    <div class="stat-label">
                        Categories Found
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon">
                        🧠
                    </div>

                    <div class="stat-number">
                        {average_confidence:.1f}%
                    </div>

                    <div class="stat-label">
                        Average AI Confidence
                    </div>

                </div>

            </div>


            <!-- CONTENT DISTRIBUTION -->

            <div class="summary-card">

                <h2>
                    📊 Content Distribution
                </h2>

                <div class="category-summary">

        """

        # ---------------------------------------------
        # CATEGORY SUMMARY
        # ---------------------------------------------

        for category, count in category_counts.most_common():

            icon = CATEGORY_ICONS.get(
                category,
                "📂"
            )

            percentage = (
                count / total_videos
            ) * 100

            html += f"""

                <div class="summary-item">

                    <div class="summary-top">

                        <span>
                            {icon}
                            <strong>
                                {category}
                            </strong>
                        </span>

                        <span>
                            {count}
                            video{"s" if count != 1 else ""}
                        </span>

                    </div>


                    <div class="progress-bg">

                        <div
                            class="progress-bar"
                            style="width:{percentage:.1f}%"
                        ></div>

                    </div>


                    <div class="percentage">

                        {percentage:.1f}%

                    </div>

                </div>

            """

        html += """

                </div>

            </div>


            <!-- SEARCH INFORMATION -->

            <div class="search-info">

                🔎 Searching for:

                <strong>
        """

        html += query

        html += """

                </strong>

            </div>

        """

        # =================================================
        # CATEGORY SECTIONS
        # =================================================

        for category in sorted(organized.keys()):

            icon = CATEGORY_ICONS.get(
                category,
                "📂"
            )

            category_videos = organized[
                category
            ]

            html += f"""

            <div class="category-section">

                <!-- CATEGORY HEADER -->

                <div class="category-header">

                    <div>

                        <span class="category-icon">
                            {icon}
                        </span>

                        <span class="category-title">
                            {category}
                        </span>

                    </div>


                    <span class="count">

                        {len(category_videos)}
                        video{"s" if len(category_videos) != 1 else ""}

                    </span>

                </div>

            """

            # ---------------------------------------------
            # VIDEO CARDS
            # ---------------------------------------------

            for video in category_videos:

                title = video.get(
                    "title",
                    "Untitled Video"
                )

                channel = video.get(
                    "channel",
                    "Unknown Channel"
                )

                url = video.get(
                    "url",
                    "#"
                )

                confidence = (
                    float(
                        video.get(
                            "confidence",
                            0
                        )
                    ) * 100
                )

                thumbnail = get_thumbnail(
                    url
                )

                # -----------------------------------------
                # CONFIDENCE LEVEL
                # -----------------------------------------

                if confidence >= 70:

                    confidence_level = "High"

                elif confidence >= 40:

                    confidence_level = "Medium"

                else:

                    confidence_level = "Low"

                # -----------------------------------------
                # VIDEO CARD
                # -----------------------------------------

                html += """

                <div class="video-card">

                """

                # -----------------------------------------
                # THUMBNAIL
                # -----------------------------------------

                if thumbnail:

                    html += f"""

                    <div class="thumbnail-container">

                        <img
                            src="{thumbnail}"
                            class="thumbnail"
                            alt="YouTube thumbnail"
                        >

                    </div>

                    """

                else:

                    html += """

                    <div class="thumbnail-container">

                        <div class="no-thumbnail">
                            ▶
                        </div>

                    </div>

                    """

                # -----------------------------------------
                # VIDEO INFORMATION
                # -----------------------------------------

                html += f"""

                    <div class="video-content">

                        <h3>
                            {title}
                        </h3>


                        <p class="channel">
                            👤 {channel}
                        </p>


                        <div class="video-meta">

                            <span class="badge">

                                {icon}
                                {category}

                            </span>


                            <span class="confidence">

                                🧠
                                {confidence:.2f}%

                            </span>


                            <span class="confidence-level">

                                {confidence_level}

                            </span>

                        </div>


                        <a
                            href="{url}"
                            target="_blank"
                            class="watch-button"
                        >

                            ▶ Watch on YouTube

                        </a>

                    </div>

                </div>

                """

            html += """

            </div>

            """

        # ---------------------------------------------
        # END DASHBOARD
        # ---------------------------------------------

        html += """

        </div>

        """

        return html, csv_file, videos

    # =================================================
    # ERROR HANDLING
    # =================================================

    except Exception as e:

        return (

            f"""

            <div class="error-box">

                <h2>
                    ❌ Something went wrong
                </h2>

                <p>
                    {str(e)}
                </p>

                <p>
                    Check your YouTube API key and
                    internet connection.
                </p>

            </div>

            """,

            None

        )


# =====================================================
# CUSTOM CSS
# =====================================================

css = """
/* =========================
   GLOBAL PINK / PURPLE THEME
   ========================= */

html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: linear-gradient(135deg, #fff5fb 0%, #f7f0ff 50%, #fff8fb 100%) !important;
}

body {
    color: #35213d !important;
}

.gradio-container {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 28px 3vw 50px !important;
    background: transparent !important;
}

/* Main Gradio markdown/header */
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container p,
.gradio-container label,
.gradio-container span,
.gradio-container strong {
    opacity: 1 !important;
}

/* =========================
   HERO
   ========================= */

.hero {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%) !important;
    border: 1px solid #f3b4d5 !important;
    margin-bottom: 22px;
    box-shadow: 0 14px 35px rgba(168, 85, 247, 0.16);
    color: #ffffff !important;
}

.hero h1,
.hero p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.hero h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 900;
}

.hero p {
    margin: 7px 0 0;
    font-size: 14px;
    opacity: 0.95 !important;
}

.hero-icon {
    font-size: 52px;
}

/* =========================
   STATISTICS
   ========================= */

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 22px;
}

.stat-card {
    padding: 24px;
    min-height: 115px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.86) !important;
    border: 1px solid #f0d7e7 !important;
    text-align: left;
    box-shadow: 0 10px 28px rgba(70, 35, 80, 0.06);
    color: #35213d !important;
}

.stat-icon {
    font-size: 28px;
    margin-bottom: 6px;
}

.dashboard .stat-number {
    display: block !important;
    margin: 3px 0 3px !important;
    color: #9d174d !important;
    -webkit-text-fill-color: #9d174d !important;
    font-size: 30px !important;
    line-height: 1.1 !important;
    font-weight: 900 !important;
    opacity: 1 !important;
}

.dashboard .stat-label {
    display: block !important;
    color: #6b5b70 !important;
    -webkit-text-fill-color: #6b5b70 !important;
    font-size: 13px !important;
    line-height: 1.3 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* =========================
   CONTENT SUMMARY
   ========================= */

.summary-card {
    padding: 22px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.84) !important;
    border: 1px solid #f0d8e8 !important;
    margin-bottom: 22px;
    box-shadow: 0 10px 28px rgba(70, 35, 80, 0.05);
    color: #35213d !important;
}

.dashboard .summary-card h2 {
    margin: 0 0 16px !important;
    color: #35213d !important;
    -webkit-text-fill-color: #35213d !important;
    font-size: 21px !important;
    font-weight: 900 !important;
}

.category-summary {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
}

.summary-item {
    padding: 13px 0;
    color: #4b3b50 !important;
}

.summary-top {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 12px;
    margin-bottom: 8px;
    color: #514255 !important;
    font-size: 14px;
}

.summary-top span,
.summary-top strong {
    color: #514255 !important;
    -webkit-text-fill-color: #514255 !important;
    opacity: 1 !important;
}

.progress-bg {
    height: 9px;
    background: #f2dce9 !important;
    border-radius: 999px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #ec4899, #8b5cf6) !important;
    border-radius: 999px;
}

.dashboard .percentage {
    color: #b21f68 !important;
    -webkit-text-fill-color: #b21f68 !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    margin-top: 4px;
}

/* =========================
   SEARCH INFORMATION
   ========================= */

.search-info {
    padding: 13px 17px;
    background: #fff0f7 !important;
    border-radius: 14px;
    border: 1px solid #f4cde0 !important;
    margin-bottom: 22px;
    color: #765d70 !important;
    -webkit-text-fill-color: #765d70 !important;
    font-size: 13px;
}

.search-info strong {
    color: #be185d !important;
    -webkit-text-fill-color: #be185d !important;
}

/* =========================
   CATEGORY SECTIONS
   ========================= */

.category-section {
    margin-bottom: 25px;
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid #efd9e7 !important;
    background: rgba(255, 255, 255, 0.88) !important;
    box-shadow: 0 10px 26px rgba(70, 35, 80, 0.05);
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 22px;
    background: linear-gradient(90deg, #fff0f7, #f8f0ff) !important;
    border-bottom: 1px solid #f1dce8;
}

.category-icon {
    font-size: 23px;
    margin-right: 8px;
}

.dashboard .category-title {
    color: #3e2947 !important;
    -webkit-text-fill-color: #3e2947 !important;
    font-size: 20px !important;
    font-weight: 900 !important;
}

.dashboard .count {
    color: #be185d !important;
    -webkit-text-fill-color: #be185d !important;
    background: #fce7f3 !important;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px !important;
    font-weight: 800 !important;
}

/* =========================
   VIDEO CARDS
   ========================= */

.video-card {
    display: flex;
    gap: 20px;
    padding: 20px;
    border-top: 1px solid #f1e1ea;
    background: rgba(255, 255, 255, 0.7) !important;
}

.thumbnail-container {
    width: 240px;
    min-width: 240px;
    height: 135px;
    overflow: hidden;
    border-radius: 12px;
    background: #f8e8f1;
}

.thumbnail {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.no-thumbnail {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 40px;
    background: #f8e8f1 !important;
    color: #9a7189 !important;
}

.video-content {
    flex: 1;
}

.dashboard .video-content h3 {
    margin: 0 0 8px 0;
    color: #35263c !important;
    -webkit-text-fill-color: #35263c !important;
    font-size: 17px !important;
    font-weight: 800 !important;
}

.dashboard .channel,
.dashboard .video-meta,
.dashboard .video-card p {
    color: #756978 !important;
    -webkit-text-fill-color: #756978 !important;
    opacity: 1 !important;
}

.video-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
}

.badge,
.confidence,
.confidence-level {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    background: #fce7f3 !important;
    color: #9d174d !important;
    -webkit-text-fill-color: #9d174d !important;
}

.dashboard .confidence-level {
    color: #7c3aed !important;
    -webkit-text-fill-color: #7c3aed !important;
    background: #f3e8ff !important;
}

.watch-button {
    display: inline-block;
    padding: 9px 15px;
    border-radius: 10px;
    background: linear-gradient(90deg, #ec4899, #8b5cf6) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-decoration: none !important;
    font-size: 13px;
    font-weight: 800;
}

.watch-button:hover {
    opacity: 0.88;
}

/* =========================
   EMPTY / ERROR
   ========================= */

.empty-box {
    padding: 50px;
    text-align: center;
    border-radius: 18px;
    background: #fff0f7 !important;
    border: 1px solid #f4cde0 !important;
    color: #765d70 !important;
}

.error-box {
    padding: 25px;
    border-radius: 18px;
    background: #fff1f2 !important;
    border: 1px solid #fecdd3 !important;
    color: #be123c !important;
}

.error-box h2,
.error-box p {
    color: #be123c !important;
    -webkit-text-fill-color: #be123c !important;
}

/* =========================
   PERSONAL LIBRARY
   ========================= */

.library-header,
.library-stats div,
.library-card {
    border: 1px solid #f0d8e8 !important;
    background: rgba(255, 255, 255, 0.86) !important;
    color: #35213d !important;
    box-shadow: 0 8px 22px rgba(70, 35, 80, 0.04);
}

.library-header {
    padding: 18px 22px;
    border-radius: 18px;
    margin: 20px 0 12px;
}

.library-header h2,
.library-header p,
.library-stats strong,
.library-stats span,
.library-content h3,
.library-content .channel {
    opacity: 1 !important;
}

.library-header h2 {
    color: #35213d !important;
    -webkit-text-fill-color: #35213d !important;
    margin: 0 0 5px;
}

.library-header p,
.library-stats span {
    color: #756978 !important;
    -webkit-text-fill-color: #756978 !important;
}

.library-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 15px;
}

.library-stats div {
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

.library-stats strong {
    display: block;
    color: #9d174d !important;
    -webkit-text-fill-color: #9d174d !important;
    font-size: 24px;
}

.library-stats span {
    font-size: 12px;
}

.library-card {
    display: flex;
    gap: 18px;
    padding: 18px;
    margin-bottom: 12px;
    border-radius: 16px;
}

.library-thumb {
    width: 210px;
    min-width: 210px;
    height: 118px;
    overflow: hidden;
    border-radius: 10px;
    background: #f8e8f1;
}

.library-content {
    flex: 1;
}

.library-content h3 {
    margin: 0 0 7px;
    color: #35263c !important;
    -webkit-text-fill-color: #35263c !important;
    font-size: 16px;
}

/* =========================
   GRADIO CONTROLS
   ========================= */

.gradio-container input,
.gradio-container textarea,
.gradio-container select {
    border-color: #edc9dd !important;
}

.gradio-container button.primary {
    background: linear-gradient(90deg, #ec4899, #8b5cf6) !important;
    border: none !important;
}

/* =========================
   DASHBOARD FORCE OVERRIDE
   Prevent Gradio's light theme from
   changing dynamic HTML text to white.
   ========================= */

.dashboard,
.dashboard * {
    box-sizing: border-box;
}

.dashboard,
.dashboard div,
.dashboard span,
.dashboard p,
.dashboard strong,
.dashboard h1,
.dashboard h2,
.dashboard h3,
.dashboard a {
    opacity: 1 !important;
}

.dashboard .stat-number { color: #9d174d !important; -webkit-text-fill-color: #9d174d !important; }
.dashboard .stat-label { color: #6b5b70 !important; -webkit-text-fill-color: #6b5b70 !important; }
.dashboard .summary-card h2 { color: #35213d !important; -webkit-text-fill-color: #35213d !important; }
.dashboard .summary-top span,
.dashboard .summary-top strong { color: #514255 !important; -webkit-text-fill-color: #514255 !important; }
.dashboard .percentage { color: #b21f68 !important; -webkit-text-fill-color: #b21f68 !important; }
.dashboard .search-info { color: #765d70 !important; -webkit-text-fill-color: #765d70 !important; }
.dashboard .search-info strong { color: #be185d !important; -webkit-text-fill-color: #be185d !important; }
.dashboard .category-title { color: #3e2947 !important; -webkit-text-fill-color: #3e2947 !important; }
.dashboard .count { color: #be185d !important; -webkit-text-fill-color: #be185d !important; }
.dashboard .video-card h3 { color: #35263c !important; -webkit-text-fill-color: #35263c !important; }
.dashboard .video-card p,
.dashboard .channel { color: #756978 !important; -webkit-text-fill-color: #756978 !important; }
.dashboard .confidence-level { color: #7c3aed !important; -webkit-text-fill-color: #7c3aed !important; }

/* =========================
   MOBILE
   ========================= */

@media (max-width: 700px) {
    .gradio-container {
        padding: 18px 4vw 40px !important;
    }

    .stats,
    .category-summary,
    .library-stats {
        grid-template-columns: 1fr;
    }

    .video-card,
    .library-card,
    .hero {
        flex-direction: column;
        align-items: stretch;
    }

    .thumbnail-container,
    .library-thumb {
        width: 100%;
        min-width: 0;
        height: 200px;
    }

    .hero h1 {
        font-size: 25px;
    }
}
"""



# =====================================================
# GRADIO APPLICATION
# =====================================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI Digital Content Organizer",
    css=css
) as app:

    gr.Markdown(
        """
# 🤖 AI Digital Content Organizer

### Intelligent organization of real digital content using Artificial Intelligence

**YouTube API** → **Content Extraction** → **Machine Learning Classification** → **Category-wise Organization** → **Personal Library**
"""
    )

    with gr.Row():
        search_box = gr.Textbox(
            label="🔎 Search Topic",
            placeholder="Try: Python programming, fitness, travel, gaming...",
            scale=4
        )
        results_slider = gr.Slider(
            minimum=5, maximum=20, value=10, step=5,
            label="📺 Number of Videos", scale=1
        )

    organize_button = gr.Button(
        "🚀 ORGANIZE CONTENT", variant="primary", size="lg"
    )

    output = gr.HTML()
    current_results = gr.State([])

    with gr.Row():
        save_button = gr.Button("💾 Save Current Results to My Library", variant="secondary")
        refresh_button = gr.Button("🔄 Refresh Library")

    library_message = gr.Markdown()

    with gr.Row():
        library_search = gr.Textbox(
            label="🔎 Search My Library",
            placeholder="Search title, channel or category...",
            scale=3
        )
        library_category = gr.Dropdown(
            choices=["All"], value="All",
            label="🏷️ Filter Category", scale=1
        )

    library_output = gr.HTML(value=library_html(load_library()))

    with gr.Row():
        clear_button = gr.Button("🗑️ Clear My Library", variant="stop")
        download_file = gr.File(
            label="📥 Download Current Search CSV", interactive=False
        )

    organize_button.click(
        fn=organize_content,
        inputs=[search_box, results_slider],
        outputs=[output, download_file, current_results]
    )

    search_box.submit(
        fn=organize_content,
        inputs=[search_box, results_slider],
        outputs=[output, download_file, current_results]
    )

    save_button.click(
        fn=save_current_to_library,
        inputs=[current_results],
        outputs=[library_output, library_message]
    ).then(
        fn=refresh_library,
        inputs=[],
        outputs=[library_output, library_category]
    )

    refresh_button.click(
        fn=refresh_library,
        inputs=[],
        outputs=[library_output, library_category]
    )

    library_search.change(
        fn=filter_library,
        inputs=[library_search, library_category],
        outputs=[library_output]
    )

    library_category.change(
        fn=filter_library,
        inputs=[library_search, library_category],
        outputs=[library_output]
    )

    clear_button.click(
        fn=clear_library,
        inputs=[],
        outputs=[library_output, library_message]
    ).then(
        fn=refresh_library,
        inputs=[],
        outputs=[library_output, library_category]
    )


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.launch()