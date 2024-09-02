import random
from modules.accounts import get_caption_by_username
from modules.utils import print_error, print_success


def get_random_caption():
    try:
        captions_options = [
            """The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.

Here’s a comprehensive overview of its key features and specifications:

Tesla Cybertruck Overview

Design and Structure

• Exterior: The Cybertruck has a distinctive, angular, stainless steel exoskeleton design for durability and passenger protection. It features ultra-hard 30X cold-rolled stainless steel and armored glass.

• Dimensions: Approximately 231.7 inches long, 79.8 inches wide, and 75 inches tall, with a 6.5-foot cargo bed.

Performance and Variants

• Single Motor RWD:
◦ 0-60 mph: ~6.5 seconds
◦ Range: ~250 miles
◦ Towing Capacity: 7,500 pounds
• Dual Motor AWD:
◦ 0-60 mph: ~4.5 seconds
◦ Range: ~300 miles
◦ Towing Capacity: 10,000 pounds
• Tri-Motor AWD:
◦ 0-60 mph: ~2.9 seconds
◦ Range: ~500 miles
◦ Towing Capacity: 14,000 pounds""",
        ]
        return random.choice(captions_options)
    except Exception as e:
        print_error(f"Failed to retrieve random caption: {e}")
        return ""  # Return an empty string to handle the failure gracefully


def generate_caption(username):
    try:
        # Get the random caption
        random_caption = get_random_caption()

        # Check if random_caption retrieval failed
        if not random_caption:
            return None  # Early exit if random_caption failed

        additional_string = f"""
.
Follow @{username} for more daily content
.
All clips used belong to their rightful owners
.
DM @brainrot.network for credits

video #fyp #trending #explorepage #nexusprivatelimitd @nexusprivatelimitd #ssl_media_ @ssl_media__


.
.
.
.
.

"""

        # Get user-specific caption
        user_caption = get_caption_by_username(username)

        # Combine captions
        final_caption = f"""{random_caption}
{additional_string}
{user_caption}"""

        return final_caption
    except Exception as e:
        print_error(f"Failed to generate caption for user '{username}': {e}")
        return ""
