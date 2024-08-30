import pandas as pd
from instagrapi import Client
import matplotlib.pyplot as plt

ACCOUNTS = ["itz.yoursome"]
REELS_TO_FETCH = 10


# Function to fetch reel from given account
def get_reels(account, api):
    user_id = api.user_id_from_username(account)
    medias = api.user_medias(user_id, REELS_TO_FETCH)
    reels = [
        item for item in medias if (item.product_type == "clips", item.media_type == 2)
    ]  # Filter for reels (product_type == 3)
    if not reels:
        print(f"No reels found for account: {account}")
        return []
    return reels


# Function to fetch reels and extract features
def get_reel_features(account, api):
    try:
        reels = get_reels(account, api)

        data = []
        for reel in reels:
            data.append(
                {
                    "view_count": reel.view_count,
                    "like_count": reel.like_count,
                    "comment_count": reel.comment_count,
                    "caption_text": reel.caption_text,
                    "hashtags": [
                        tag for tag in reel.caption_text.split() if tag.startswith("#")
                    ],
                    "taken_at": reel.taken_at,
                    "video_duration": reel.video_duration,
                }
            )
        return data

    except Exception as e:
        print(f"An error occurred while fetching reels for {account}: {e}")
        return []


# Collect data from all accounts
def collect_data(api):
    all_data = []
    for account in ACCOUNTS:
        account_data = get_reel_features(account, api)
        if account_data:  # Ensure data is not empty
            all_data.extend(account_data)
        else:
            print(f"No data collected for account: {account}")

    if not all_data:
        print("No data collected from any account.")
        return pd.DataFrame()

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_data)
    return df


# Login and collect data
if __name__ == "__main__":
    api = Client()
    try:
        api.login("bits.of.past", "bitsofpast@38380")
    except Exception as e:
        print(f"Failed to log in: {e}")
        exit()

    df = collect_data(api)

    if not df.empty:
        df.to_csv("reels_data.csv", index=False)
        print("Data collected and saved to reels_data.csv")
    else:
        print("No data was saved as the DataFrame is empty.")

# Analysis Example
# After collecting data, load the CSV and start analysis
if not df.empty:
    print(df.corr())

    # Example: View count distribution
    plt.hist(df["view_count"], bins=20)
    plt.title("View Count Distribution")
    plt.xlabel("Views")
    plt.ylabel("Frequency")
    plt.show()
else:
    print("No data available for analysis.")
