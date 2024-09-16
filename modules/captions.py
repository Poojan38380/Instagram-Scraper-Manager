import random
from modules.accounts import get_caption_by_username
from modules.utils import print_error


def get_random_caption():
    try:
        captions_options = [
            """The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.

Here's a comprehensive overview of its key features and specifications:

Tesla Cybertruck Overview

Design and Structure

Exterior: The Cybertruck has a distinctive, angular, stainless steel exoskeleton design for durability and passenger protection. It features ultra-hard 30X cold-rolled stainless steel and armored glass.

Dimensions: Approximately 231.7 inches long, 79.8 inches wide, and 75 inches tall, with a 6.5-foot cargo bed. 262 Performance and Variants

Performance and Variants

Single Motor RWD:
0-60 mph: ~6.5 seconds
Range: ~250 miles
Towing Capacity: 7,500 pounds

Dual Motor AWD:
0-60 mph: ~4.5 seconds
Range: ~300 miles
Towing Capacity: 10,000 pounds

Tri-Motor AWD:
0-60 mph: ~2.9 seconds
Range: ~500 miles
Towing Capacity: 14,000 pounds
""",
            """An interesting fact is that bananas are berries, but strawberries are not. In botanical terms, a berry is a fleshy fruit produced from a single ovary and containing one or more seeds. By this definition, bananas, along with kiwis, grapes, and tomatoes, are true berries. On the other hand, strawberries, which develop from a flower with multiple ovaries, are classified as “aggregate fruits” rather than berries.
This classification quirk arises from the complexities of fruit development in flowering plants. While many fruits commonly referred to as berries do not meet the botanical criteria, those that do often surprise us. For instance, watermelons and pumpkins are also technically berries, while raspberries and blackberries are not.
This is an interesting fact because it challenges our everyday understanding of common fruits and highlights the intriguing details of plant biology. It also illustrates how scientific classification can differ significantly from culinary or popular usage, encouraging us to explore and appreciate the natural world’s diversity in greater depth. This surprising reclassification prompts a reexamination of what we think we know about the foods we eat and their botanical origins.""",
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
DM @brainrot.network for Credit/removal. No Copyright intended!
©All rights and credits reserved to the respective owner(s)

video #fyp #trending #explorepage

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
