from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
from modules.utils import delete_file, print_error, print_success
import numpy as np


def add_margins_to_reel(
    reel_path,
    margin_horizontal=108,
    margin_vertical=108,
    top_text="",
    font_size=40,
    font_color="black",
):
    try:
        # Load the original video
        video = VideoFileClip(str(reel_path))

        # Calculate the new size with margins
        new_width = video.w + 2 * margin_horizontal
        new_height = video.h + 2 * margin_vertical

        # Create a color clip for the margin (e.g., white) with the same duration as the original video
        margin_clip = ColorClip((new_width, new_height), color=(0, 0, 0)).set_duration(
            video.duration
        )

        # Create an image for the text
        if top_text:
            # Create an image with the text
            img = Image.new("RGB", (new_width, margin_vertical), color=(225, 225, 225))
            d = ImageDraw.Draw(img)

            # Load the font with the specified size
            font = ImageFont.truetype("arial.ttf", font_size)

            # Get the bounding box of the text
            text_bbox = d.textbbox((0, 0), top_text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

            text_position = (
                (new_width - text_size[0]) // 2,
                (margin_vertical - text_size[1]) // 2,
            )
            d.text(text_position, top_text, fill=font_color, font=font)

            # Convert the PIL image to a NumPy array and then to a MoviePy ImageClip
            text_img = np.array(img)
            text_clip = (
                ImageClip(text_img)
                .set_duration(video.duration)
                .set_position(("center", 0))
            )

            # Overlay the original video onto the margin clip with text
            video_with_margin = CompositeVideoClip(
                [margin_clip, video.set_position(("center", "center")), text_clip]
            )
        else:
            video_with_margin = CompositeVideoClip(
                [margin_clip, video.set_position(("center", "center"))]
            )

        # Save the modified video with a margin and text
        # Adjust the output path to remove '_raw' from the file name
        output_file_name = reel_path.name.replace("_raw", "")
        output_path = reel_path.parent / output_file_name
        video_with_margin.write_videofile(str(output_path), codec="libx264")

        print_success(f"Margins and text added successfully. Saved to {output_path}")
        delete_file(reel_path)
        return output_path

    except Exception as e:
        print_error(f"Failed to add margins or text to reel: {str(e)}")
        return reel_path
