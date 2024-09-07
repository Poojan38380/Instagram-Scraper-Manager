import csv
from pathlib import Path
import instaloader
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

L = instaloader.Instaloader()


def round_to_nearest_half_hour(dt):
    """
    Round the provided datetime object to the nearest half-hour.
    """
    new_minute = 30 * round(dt.minute / 30)

    if new_minute == 60:
        dt += timedelta(hours=1)
        dt = dt.replace(minute=0, second=0, microsecond=0)
    else:
        dt = dt.replace(minute=new_minute, second=0, microsecond=0)

    return dt


def get_top_reels_data(account_to_scrape, max_reels=30):
    """
    Fetch the top reels from an Instagram account and return data such as view count and time of day posted.
    Also, save the data in a CSV file.
    """
    print(f"Gathering top {max_reels} reels data for account: {account_to_scrape}")
    try:
        profile = instaloader.Profile.from_username(L.context, account_to_scrape)
        reel_data_list = []
        reel_count = 0

        # Directory for saving CSV data
        data_directory = Path("reels_data")
        data_directory.mkdir(exist_ok=True)

        # CSV file path
        csv_file_path = data_directory / f"{account_to_scrape}_top_reels.csv"

        # Loop through posts and extract reel data
        for post in profile.get_posts():
            if post.typename == "GraphVideo" and post.is_video and post.video_url:
                reel_count += 1

                posted_time = post.date_local.strftime("%Y-%m-%d %H:%M:%S")
                rounded_time = round_to_nearest_half_hour(post.date_local).strftime(
                    "%H:%M"
                )

                reel_data = {
                    "shortcode": post.shortcode,
                    "views": post.video_view_count,
                    "posted_time": posted_time,
                    "rounded_posted_time": rounded_time,
                }
                reel_data_list.append(reel_data)

                print(
                    f"{reel_countReel} . {post.shortcode}: {post.video_view_count} views, Posted at {posted_time}, Rounded to {rounded_time}"
                )

                if reel_count >= max_reels:
                    break

        if not reel_data_list:
            print(f"No reels found for account: {account_to_scrape}.")
        else:
            # Save the data into a CSV file
            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "shortcode",
                        "views",
                        "posted_time",
                        "rounded_posted_time",
                    ],
                )
                writer.writeheader()
                writer.writerows(reel_data_list)

            print(f"Reel data saved to {csv_file_path}")

            return csv_file_path

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Failed to load profile {account_to_scrape}: {str(e)}")


def get_best_posting_times(csv_file_path):
    """
    Analyze the CSV file and find the top 3 best times to post reels based on views.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Group by rounded_posted_time and calculate the total views for each half-hour period
    grouped = df.groupby("rounded_posted_time")["views"].sum()

    # Sort by views in descending order to get the top 3 times
    best_times = grouped.sort_values(ascending=False).head(3)

    print("Top 3 best posting times (rounded to nearest half-hour):")
    print(best_times)

    return best_times


def plot_views_vs_time(csv_file_path):
    """
    Create a graph showing the relationship between views and posting time (rounded to nearest half-hour).
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Group by rounded_posted_time and calculate the average views for each half-hour period
    grouped = df.groupby("rounded_posted_time")["views"].mean()

    # Create a plot of views vs. posting time
    plt.figure(figsize=(10, 6))
    grouped.plot(kind="bar", color="skyblue")

    plt.title("Average Views vs. Posting Time (Rounded to Nearest Half-Hour)")
    plt.xlabel("Posting Time (Half-Hour)")
    plt.ylabel("Average Views")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()


# Example usage
username_to_scrape = "deepmemepull"
csv_file = get_top_reels_data(username_to_scrape)

if csv_file:
    # Get the best times to post reels
    best_times = get_best_posting_times(csv_file)

    # Plot the views vs time graph
    plot_views_vs_time(csv_file)
