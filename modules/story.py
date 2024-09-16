from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
from moviepy.editor import VideoFileClip
import os
from modules.utils import (
    delete_file,
    print_error,
    print_success,
)
from instagrapi.types import UserShort


def trim_video(file_path, output_dir, max_duration=15):
    try:
        # Ensure file_path is a string
        file_path = str(file_path)
        original_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"story_{original_name}.mp4")

        # Trim the video
        clip = VideoFileClip(file_path)
        trimmed_clip = clip.subclip(0, max_duration)
        trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return output_path
    except Exception as e:
        print_error(f"Error trimming video: {e}")
        delete_file(output_path)
        return None


def get_video_duration(file_path):
    try:
        # Ensure file_path is a string
        file_path = str(file_path)
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.reader.close()  # Properly close the video file   # type: ignore
        return duration
    except Exception as e:
        print_error(f"Error getting video duration: {e}")
        return None


def post_to_story(api, media, media_path, username, download_dir):
    try:

        # Ensure media_path is a string and check if the file exists
        media_path = str(media_path)
        if not os.path.exists(media_path):
            print_error(f"File '{media_path}' does not exist.")
            return

        # Fetch user and hashtag info
        user_info = api.user_info_by_username(username)
        user_short = UserShort(
            pk=user_info.pk,
            username=user_info.username,
            full_name=user_info.full_name,
        )
        hashtag = api.hashtag_info("like")

        # Get video duration and trim if necessary
        duration = get_video_duration(media_path)
        if duration and duration > 15:
            media_path = trim_video(media_path, download_dir)
            if not media_path:
                return

        # Fetch media primary key
        media_pk = api.media_pk_from_url(f"https://www.instagram.com/p/{media.code}/")

        # Upload video to story with mentions, links, and hashtags
        api.video_upload_to_story(
            media_path,
            "",
            mentions=[
                StoryMention(
                    user=user_short,
                    x=0.49892962,
                    y=0.703125,
                    width=0.8333333333333334,
                    height=0.125,
                )
            ],
            links=[StoryLink(webUri=f"https://www.instagram.com/p/{media.code}/")],  # type: ignore
            hashtags=[
                StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)
            ],
            medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
        )

        print_success("Story posted successfully!")

    except Exception as e:
        print_error(f"Error posting story: {e}")
    finally:
        # Clean up the trimmed video file if it exists
        if media_path and os.path.exists(media_path):
            delete_file(media_path)
            story_thumbnail_path = f"{media_path}.jpg"
            delete_file(story_thumbnail_path)
