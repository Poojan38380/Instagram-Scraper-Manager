from modules.interaction_helper import (
    get_comment_for_reel,
    get_last_interacted_reel,
    save_last_interacted_reel,
)
from modules.utils import print_error
import random
import time


def interact_with_reels(
    api,
    username="",
    total_time=60,
    action_probability=0.5,
    keywords=[],
    idle_chance=0.1,  # Chance to "do nothing" for a period of time
    idle_duration=(5, 20),  # Random idle time to simulate distraction
):
    start_time = time.time()  # Record the starting time
    interacted_reels = 0

    # Fetch the last interacted reel for this user
    last_media_pk = get_last_interacted_reel(username) or 0

    try:
        while (time.time() - start_time) < total_time:

            # Fetch the batch of reels with pagination using last_media_pk
            reels = api.explore_reels(15, last_media_pk)

            if not reels:
                print_error(f"{username} : No reels found.")
                return

            for reel in reels:

                # Simulate idle behavior
                if random.random() < idle_chance:
                    idle_time = random.uniform(*idle_duration)
                    print(f"{username} : Taking a break for {idle_time:.2f} seconds...")
                    time.sleep(idle_time)
                reel_pk = reel.pk
                reel_id = reel.id
                reel_code = reel.code
                caption_text = reel.caption_text
                video_duration = reel.video_duration

                try:
                    # Check if the total time limit has been reached
                    if (time.time() - start_time) >= total_time:
                        print(
                            f"{username} : Time limit of {total_time} seconds reached."
                        )
                        print(
                            f"{username} : Finished interacting with {interacted_reels} reels."
                        )
                        return

                    # Check if the caption contains any of the specified keywords
                    contains_keyword = False

                    if keywords:
                        contains_keyword = any(
                            keyword.lower() in caption_text.lower()
                            for keyword in keywords
                        )

                    # If the caption contains keywords, watch for 200-500% of video duration
                    # Otherwise, watch for less than 50% of the video duration
                    if contains_keyword:
                        time_on_reel = (
                            random.uniform(2.0, 5.0) * video_duration
                        )  # 200% to 500% of video duration

                        print(
                            f"{username} : Viewing reel {reel_code} for {time_on_reel:.2f} seconds... ⭐"
                        )
                        api.media_seen([reel_id])  # Mark the media as seen
                        time.sleep(time_on_reel)

                        # Adjust the action and comment probabilities based on whether keywords were found
                        effective_action_probability = action_probability
                        effective_comment_probability = (
                            effective_action_probability / 10
                        )
                        # Randomly decide whether to like the reel
                        if random.random() < effective_action_probability:
                            api.media_like(reel_id)
                            print(f"{username} -- Liked reel {reel_code}.")

                        # Randomly decide whether to comment on the reel
                        if random.random() < effective_comment_probability:
                            comment_with_typos = get_comment_for_reel()
                            api.media_comment(reel_id, comment_with_typos)
                            print(
                                f"{username} -- Commented on reel {reel_code}: {comment_with_typos}"
                            )
                    else:
                        time_on_reel = (
                            random.uniform(0.1, 0.5) * video_duration
                        )  # Less than 50% of video duration

                        print(
                            f"{username} : Viewing reel {reel_code} for {time_on_reel:.2f} seconds..."
                        )
                        api.media_seen([reel_id])  # Mark the media as seen
                        time.sleep(time_on_reel)

                    interacted_reels += 1

                    # Save progress: update the last interacted reel
                    save_last_interacted_reel(username, reel_pk)

                    # Update the last_media_pk after interacting with the reel
                    last_media_pk = reel_pk

                except Exception as e:
                    # Handle feedback_required error
                    error_message = str(e)

                    if "login_required" in error_message:
                        print_error(
                            f"{username} : Critical error encountered: {error_message}"
                        )
                        print_error(
                            f"{username} : Exiting due to login being required. Please login again."
                        )
                        return  # Exit the function immediately

                    if "feedback_required" in error_message:
                        print_error(
                            f"{username} : Critical error encountered: {error_message}"
                        )
                        print_error(
                            f"{username} : Shutting down function to avoid Instagram rate-limiting issues."
                        )
                        return  # Exit the function immediately

                    # Skip the problematic reel but continue the loop for minor errors
                    print_error(
                        f"{username} : Skipping reel {reel_code} due to error: {error_message}"
                    )
                    continue

        print(
            f"{username} : Finished interacting with {interacted_reels} reels in {total_time} seconds."
        )

    except Exception as e:
        print_error(f"{username} : An error occurred while scrolling: {str(e)}")
