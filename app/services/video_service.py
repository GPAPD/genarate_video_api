from app.models.video_request import VideoRequest
from moviepy import *
import numpy as np
import tempfile
import requests
from PIL import Image, ImageOps
import os

from moviepy import *

def generate_video (payload : dict):

    request = VideoRequest(**payload)
    
    clip_template = VideoFileClip(f"./assets/{get_template(request.template)}")
    font = "./assets/font/static/Montserrat-Bold.ttf"
    #j_name = "4 Carat Diamonds Mediterranean Pendant made in 18 Karat White Gold on nice 18 inch Cable Chain. This pendant includes one Round shape .90ct Center Diamond and 154 Round Shape Diamonds each of .02ct each. Diamond Color is H/I and Clarity is I1/I2. Grades are approximates."

    #Item texts 
    item_name_text = TextClip(
        font=font,
        text=wrap_text(request.product_desc),
        font_size=50,
        interline=10,
        color="#fff",
        text_align="left",
        #bg_color="black",
        margin = (25,25)

    )

    item_price_text = TextClip(
        font=font,
        text=f"${request.product_price}",
        font_size=80,
        color="#fff",
        text_align="center",
        margin = (25,25)
    )

    retail_text = TextClip(
        font=font,
        text="Retail Price",
        font_size=70,
        color="#fff",
        text_align="center",
        margin = (25,25)
    )

    sale_text = TextClip(
        font=font,
        text="""Sale Price""",
        font_size=80,
        color="#8B0111",
        text_align="center",
        margin = (25,25)
    )

    offer_price_text = TextClip(
        font=font,
        text=f"Only ${request.product_sale_price}",
        margin = (25,25),
        font_size=90,
        color="#8B0111",
        text_align="center",
    )

    if request.product_image_count > 6 :
        request.product_image_count = 6

    #set product images
    product_images = []
    for i in range(request.product_image_count):
        i += 1
        product_image = (
            ImageClip(
                download_image(
                    f"https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic{request.product_id}-{i}",
                    f"{request.product_id}-{i}",
                    template=request.template
                )
            )
            .resized(width=700)
            .with_duration(8 - i)
            .with_start(2 + i)
            .with_position((100, "center"))
        )
        product_images.append(product_image)
 
    #hr red line 
    price_hr_redline = (
        ImageClip("./assets/Red-Horizontal-Line.png")
                    .resized(width= 100 * item_price_text.aspect_ratio )
                    .with_duration(6)
                    .with_start(4)
                    .with_position((1100, 525))
                    )

    #item price and text
    item_name_text = item_name_text.with_duration(7).with_start(3).with_position((840, 100))

    retail_text = retail_text.with_duration(6).with_start(4).with_position((1000, 375))
    item_price_text = item_price_text.with_duration(6).with_start(4).with_position((1000, 480))

    sale_text = sale_text.with_duration(5).with_start(5).with_position((1000, 650))
    offer_price_text = offer_price_text.with_duration(5).with_start(5).with_position((1000, 750))

    CompositeVideoClip(
    [
        clip_template,
        *product_images,
        item_name_text,
        item_price_text,
        offer_price_text,
        retail_text,
        sale_text,
        price_hr_redline
     ]
    ).write_videofile(f"./gen_videos/{request.product_id}.mp4", fps=20)

    delete_jpg_files("./assets/temp")
    print("Render complete!")
    return request.product_id

# templates
def get_template(template):
    match template:
        case 1:
            return  "VideoGenAkash-1.mp4"
        case 2:
            return "VideoGenAkash-2.mp4"
        case _:
            return  "VideoGenAkash-1.mp4"

 
def wrap_text(text: str, max_chars: int = 35, max_lines: int = 3) -> str:
    words = text.split()
    lines = []
    current = ""

    def push_line(line: str):
        if line:
            lines.append(line)

    i = 0
    while i < len(words) and len(lines) < max_lines:
        word = words[i]

        if not current:
            if len(word) <= max_chars:
                current = word
                i += 1
            else:
                # Split an extremely long word
                current = word[:max_chars]
                words[i] = word[max_chars:]
        else:
            # Try adding " word" to current line
            if len(current) + 1 + len(word) <= max_chars:
                current = f"{current} {word}"
                i += 1
            else:
                push_line(current)
                current = ""

    # Add the last line if there's room
    if current and len(lines) < max_lines:
        push_line(current)

    # If we didn't consume all words, we need ellipsis
    truncated = i < len(words)

    if truncated:
        # Ensure ellipsis fits in the last line
        last = lines[-1]
        if len(last) + 3 <= max_chars:
            lines[-1] = last + "..."
        else:
            # Replace last 3 chars with ellipsis (keeps max length)
            lines[-1] = last[: max_chars - 3].rstrip() + "..."

    return "\n".join(lines)


def download_image(url, image_name, temp_dir="./assets/temp/",template = 1):  # Change this path as needed
    
    os.makedirs(temp_dir, exist_ok=True) 
    temp_file = os.path.join(temp_dir, image_name+".jpg")
    response = requests.get(url)
    
    with open(temp_file, 'wb') as f:
        f.write(response.content)
        img = Image.open(f"./assets/temp/{image_name}.jpg" ).convert("RGBA") 
        # Add border (stroke)
        if template == 1 :
            img_with_border = ImageOps.expand(img, border=20, fill=(29, 38, 107))
        else :
            img_with_border = ImageOps.expand(img, border=20, fill=(255, 191, 0))
            
    return np.array(img_with_border)

import os

def delete_jpg_files(folder_path: str):

    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg"):  # match .jpg or .JPG
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")