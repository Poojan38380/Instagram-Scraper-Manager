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
            """Drake, born Aubrey Drake Graham on October 24, 1986, in Toronto, Canada, is a prominent figure in the music industry, widely recognized for his contributions to hip-hop and R&B. His journey from an actor on the teen drama series “Degrassi: The Next Generation” to a global music icon is a testament to his versatility, talent, and relentless work ethic.""",
            """Sure thing! Here’s the statistics about the Honda Civic Type R:

The Honda Civic Type R is a remarkable performance car renowned for its agile handling and sporty design. Equipped with a robust 2.0-liter turbocharged engine, it delivers over 300 horsepower.

Acceleration from 0 to 100 km/h takes approximately 5.7 seconds, with an impressive top speed exceeding 270 km/h.

Incorporating advanced aerodynamics and state-of-the-art stability systems, the Civic Type R ensures exceptional handling and control, especially during spirited driving.

Originally priced around $35,000, the Honda Civic Type R offers outstanding value for its performance capabilities.

With its limited availability and high demand, the Civic Type R is highly coveted by enthusiasts and collectors alike.""",
            """No problem! Here’s the information about “She Is Not Special”:

“She Is Not Special” is a social media platform that delves into the realities of dating and relationships from a red pill perspective. The content is aimed at unveiling what is perceived as the true nature of modern women, challenging common societal narratives, and promoting a more pragmatic approach to relationships.

The platform provides insights and advice on various topics, including:

1. **Understanding Female Psychology**: Offering explanations and theories about women’s behavior and motivations in dating and relationships.
2. **Dating Strategies**: Sharing tips and techniques for men to navigate the dating world more effectively, focusing on confidence, self-improvement, and strategic thinking.
3. **Red Pill Philosophy**: Emphasizing awareness of societal dynamics, gender roles, and the importance of maintaining masculine strength and independence.
4. **Debunking Myths**: Challenging popular beliefs about romance and relationships, encouraging a more realistic and self-reliant mindset.

“She Is Not Special” positions itself as a counter-narrative to mainstream dating advice, advocating for men to prioritize their personal growth and to approach relationships with a critical and informed perspective.""",
            """Want to earn a million in 2024?
Here are the top 5 promising remote business ideas:

1. Freelancing and Consulting:
- Content writing
- Copywriting
- Graphic design
- Branding services

2. E-commerce and Dropshipping:
- Start an online store
- Sell products without holding inventory

3. Online Coaching and Courses:
- Share your expertise
- Create and sell courses

4. Digital Marketing and Social Media Management:
- SEO
- Content marketing
- Paid advertising
- Social media management

5. Virtual Assistance and Remote Administrative Services:
- Support businesses remotely
- Manage emails, appointments, customer inquiries, and bookkeeping  """,
            """The Porsche 911 is an iconic sports car known for its distinctive rear-engine layout and timeless design.

Since its debut in 1964, it has evolved through multiple generations while maintaining core features like the sloping roofline and round headlights.

Renowned for its performance and driving dynamics, the 911 offers a range of models from the base Carrera to high-performance variants like the Turbo and GT3.

It also boasts a rich motorsport legacy, having competed successfully in events like the 24 Hours of Le Mans and the Monte Carlo Rally.""",
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
