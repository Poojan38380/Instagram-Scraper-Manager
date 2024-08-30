import instaloader
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
import logging
from collections import Counter

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Initialize Instaloader
L = instaloader.Instaloader()

# List of Instagram accounts to scrape reels from
ACCOUNTS = ["ifti.hi"]


# Function to fetch reels from a given account
def get_reels(account, max_reels=40):
    reels = []
    profile = instaloader.Profile.from_username(L.context, account)

    # Iterate through posts and collect up to max_reels reels
    for post in profile.get_posts():
        if post.typename == "GraphVideo" and post.is_video and post.video_url:
            reels.append(post)
        if len(reels) >= max_reels:
            break

    return reels


# Function to fetch reels and extract features
def get_reel_features(account):
    try:
        reels = get_reels(account)
        reel_data = []

        for reel in reels:
            utc_post_time = reel.date_utc.replace(tzinfo=timezone.utc)
            ist_post_time = utc_post_time.astimezone(
                timezone(timedelta(hours=5, minutes=30))
            )
            hashtags = reel.caption_hashtags
            reel_data.append(
                {
                    "utc_time": utc_post_time,
                    "ist_time": ist_post_time,
                    "views": reel.video_view_count,
                    "likes": reel.likes,
                    "comments": reel.comments,
                    "hashtags": hashtags,
                }
            )
            logging.info(
                f"Fetched reel posted on {utc_post_time} UTC with {reel.video_view_count} views"
            )

        return reel_data

    except Exception as e:
        logging.error(f"An error occurred while fetching reels for {account}: {e}")
        return []


# Function to collect data from all accounts
def collect_data():
    all_reel_data = []

    for account in ACCOUNTS:
        logging.info(f"Collecting data for account: {account}")
        reel_data = get_reel_features(account)
        all_reel_data.extend(reel_data)

    return all_reel_data


# Function to analyze hashtags and posting times
def analyze_data(reel_data):
    hashtag_counter = Counter()
    time_view_map = {}

    for data in reel_data:
        for hashtag in data["hashtags"]:
            hashtag_counter[hashtag] += data["views"]

        hour = data["ist_time"].hour
        if hour not in time_view_map:
            time_view_map[hour] = []
        time_view_map[hour].append(data["views"])

    best_hashtags = hashtag_counter.most_common(10)
    avg_views_by_hour = {
        hour: sum(views) / len(views) for hour, views in time_view_map.items()
    }
    best_hour_to_post = max(avg_views_by_hour, key=avg_views_by_hour.get)

    logging.info(f"Top 10 Hashtags: {best_hashtags}")
    logging.info(
        f"Best Hour to Post (IST): {best_hour_to_post} with avg views: {avg_views_by_hour[best_hour_to_post]}"
    )

    return best_hashtags, best_hour_to_post


# Function to plot the relation between posting hour and reel views
def plot_reel_data(reel_data):
    ist_hours = [data["ist_time"].hour for data in reel_data]
    views = [data["views"] for data in reel_data]

    plt.figure(figsize=(12, 6))

    plt.scatter(ist_hours, views)
    plt.title("Reel Views vs. Posting Hour (IST)")
    plt.xlabel("Hour of the Day (IST)")
    plt.ylabel("Views")

    plt.xticks(range(24))
    plt.grid(True)
    plt.show()


# Main function to login and collect data
if __name__ == "__main__":
    reel_data = collect_data()
    if reel_data:
        best_hashtags, best_hour_to_post = analyze_data(reel_data)
        plot_reel_data(reel_data)
        logging.info("Data collection, analysis, and plotting completed successfully.")
    else:
        logging.warning("No data to analyze or plot.")
