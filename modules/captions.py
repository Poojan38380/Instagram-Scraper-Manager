import random
from modules.accounts import get_caption_by_username
from modules.utils import print_error, print_success


def get_random_caption():
    try:
        captions_options = [
            """No problem! Here's the information about the Mercedes CLR GTR:

The Mercedes CLR GTR is a remarkable racing car celebrated for its outstanding performance and sleek design. Powered by a potent 6.0-liter V12 engine, it delivers over 600 horsepower. Acceleration from 0 to 100km/h takes approximately 3.7 seconds, with a remarkable top speed surpassing 320km/h. 

Incorporating advanced aerodynamic features and cutting-edge stability technologies, the CLR GTR ensures exceptional stability and control, particularly during high-speed maneuvers. Originally priced around $1.5 million, the Mercedes CLR GTR is considered one of the most exclusive and prestigious racing cars ever produced. 

Its limited production run of just five units adds to its rarity, making it highly sought after by racing enthusiasts and collectors worldwide.""",
            """The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.

Here's a comprehensive overview of its key features and specifications:

Tesla Cybertruck Overview and Structure:

• Exterior: The Cybertruck has a distinctive, angular, stainless steel exoskeleton design for durability and passenger protection. It features ultra-hard 30X cold-rolled stainless steel and armored glass.

• Dimensions: Approximately 231.7 inches long, 79.8 inches wide, and 75 inches tall, with a 6.5-foot cargo bed.

Performance and Variants:

• Single Motor RWD:
  - 0-60 mph: ~6.5 seconds
  - Range: ~250 miles
  - Towing Capacity: 7,500 pounds

• Dual Motor AWD:
  - 0-60 mph: ~4.5 seconds
  - Range: ~300 miles
  - Towing Capacity: 10,000 pounds

• Tri-Motor AWD:
  - 0-60 mph: ~2.9 seconds
  - Range: ~500 miles
  - Towing Capacity: 14,000 pounds""",
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

        additional_string = """
All clips used belong to their rightful owners

DM @brainrot.network for credits
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
