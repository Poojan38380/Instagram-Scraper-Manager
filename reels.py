from utils import check_array_and_proceed


def get_all_reels(account, api, FETCH_LIMIT):
    user_id = api.user_id_from_username(account)
    medias = api.user_medias(user_id, FETCH_LIMIT)
    reels = [
        item for item in medias if (item.product_type == "clips", item.media_type == 2)
    ]  # Filter for reels (product_type == 3)
    return reels


def get_reel(account, api):
    reels = get_all_reels(account, api, 1)
    if not check_array_and_proceed(reels, f"reels for account : {account}"):
        return
    return reels
