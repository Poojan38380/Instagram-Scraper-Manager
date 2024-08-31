import instaloader


def get_reel_info(reel_code):
    # Create an instance of Instaloader
    L = instaloader.Instaloader()

    # Attempt to load the reel using its code
    try:
        post = instaloader.Post.from_shortcode(L.context, reel_code)

        # Fetching and printing all available info about the reel
        print(f"Shortcode: {post.shortcode}")
        print(f"Username: {post.owner_username}")
        print(f"User ID: {post.owner_id}")
        print(f"Caption: {post.caption}")
        print(f"Hashtags: {post.caption_hashtags}")
        print(f"Mentions: {post.caption_mentions}")
        print(f"Likes: {post.likes}")
        print(f"Comments: {post.comments}")
        print(f"Date: {post.date}")
        print(f"Location: {post.location}")
        print(f"URL: {post.url}")
        print(f"Video URL: {post.video_url}")
        print(f"Is Video: {post.is_video}")
        print(f"Video View Count: {post.video_view_count}")
        print(f"Tagged Users: {post.tagged_users}")
        print(f"Is Sponsored: {post.is_sponsored}")
        print(f"Type: {post.typename}")
        print(f"Caption Mentions: {post.caption_mentions}")
        print(f"Accessibility Caption: {post.accessibility_caption}")
        print(f"Location Name: {post.location.name if post.location else 'N/A'}")

        # Handling sidecar nodes (i.e., carousel posts with multiple media items)
        if post.typename == "GraphSidecar":
            print("This post is a sidecar (carousel) with the following media items:")
            for i, node in enumerate(post.get_sidecar_nodes(), start=1):
                print(f" - Item {i}: {node['display_url']}")

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error fetching reel info: {e}")


if __name__ == "__main__":
    # Replace 'your_reel_code' with the actual reel code you want to fetch info for
    reel_code = "C_Q35Mcv10p"
    get_reel_info(reel_code)
