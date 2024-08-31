from modules.utils import print_error, print_success
import random

from modules.utils import print_error, print_success


class Location:
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return f"Location(name='{self.name}', lat={self.lat}, lng={self.lng})"


def initial_follow_accounts(api):
    """
    Follow multiple Instagram accounts using the provided API client.

    :param api: The authenticated instagrapi Client instance.
    """
    usernames_to_follow = [
        "creators",
        "brainrot.network",
    ]  # Hardcoded list of usernames to follow

    for username in usernames_to_follow:
        try:
            user_id = api.user_id_from_username(username)
            if api.user_follow(user_id):
                print(f"Successfully followed the account '{username}'.")
            else:
                print_error(f"Failed to follow the account '{username}'.")
        except Exception as e:
            print_error(f"Error occurred while trying to follow '{username}': {e}")

    print_success("Followed all the initial follow accounts")


def should_save_reel(post):
    """
    Check if the reel should be saved based on the number of views.

    :param post: The Instaloader Post object.
    :return: True if the reel should be saved, False otherwise.
    """
    MIN_VIEWS = 10000
    try:
        if post.video_view_count is not None and post.video_view_count >= MIN_VIEWS:
            return True
        else:
            print(
                f"Skipping Reel {post.shortcode} due to insufficient views: {post.video_view_count} views."
            )
            return False
    except AttributeError:
        print_error(f"Could not retrieve view count for Reel {post.shortcode}.")
        return False


def get_instagram_location(api):
    try:
        rawloc = get_random_location()
        locations = api.location_search(rawloc.lat, rawloc.lng)
        if locations:
            return locations[0]  # Return the first matching location
        else:
            print_error("No matching Instagram location found.")
            return None
    except Exception as e:
        print_error(f"Failed to get Instagram location: {str(e)}")
        return None


def get_random_location():
    locations = [
        Location(lat=59.96, lng=30.29),
        Location(lat=40.71, lng=-74.01),
        Location(lat=35.68, lng=139.76),
        Location(lat=-33.87, lng=151.21),
        Location(lat=-22.91, lng=-43.17),
        Location(lat=48.86, lng=2.35),
        Location(lat=51.51, lng=-0.13),
        Location(lat=39.91, lng=116.40),
        Location(lat=52.52, lng=13.41),
        Location(lat=43.65, lng=-79.38),
        Location(lat=41.90, lng=12.50),
        Location(lat=19.08, lng=72.88),
        Location(lat=-33.93, lng=18.42),
        Location(lat=19.43, lng=-99.13),
        Location(lat=-34.61, lng=-58.38),
        Location(lat=37.57, lng=126.98),
        Location(lat=41.01, lng=28.97),
        Location(lat=40.42, lng=-3.70),
        Location(lat=30.04, lng=31.24),
        Location(lat=1.35, lng=103.82),
        Location(lat=55.75, lng=37.62),
        Location(lat=13.75, lng=100.50),
        Location(lat=-6.21, lng=106.85),
        Location(lat=59.33, lng=18.07),
        Location(lat=52.37, lng=4.90),
        Location(lat=25.20, lng=55.27),
    ]

    return random.choice(locations)
