from app.models.video_request import VideoRequest
from moviepy import *
import numpy as np
import tempfile
import requests
from PIL import Image, ImageOps
import os

from moviepy import *

def generate_video (request : VideoRequest):
    
    clip_template = VideoFileClip(f"./assets/{get_template(request.template)}")
    font = "./assets/font/static/Montserrat-Bold.ttf"
    #hr line
    hr_redLine = "./assets/Red-Horizontal-Line.png"
    j_name = "2 Carat Round Shape Lab Grown Diamond Ring In 14K White Gold, Solitaire"
    jwl_key = "61415"
    # URLs of the images
    url1 = "https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic61415-1"
    url2 = "https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic61415-2"
    url3 = "https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic61415-3"
    url4 = "https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic61415-4"
    url5 = "https://media.superjeweler.com/f_auto,fl_lossy,q_auto,c_scale/Images/Products/700x700/pic61415-5"

    #Item texts 
    item_name_text = TextClip(
        font=font,
        text=wrap_text(j_name),
        font_size=50,
        interline=10,
        color="#fff",
        text_align="left",
        bg_color="black",
        margin = (25,25)

    )

    item_price_text = TextClip(
    font=font,
    text="$99,999.97",
    font_size=80,
    color="#fff",
    text_align="center",
    )

    retail_text = TextClip(
    font=font,
    text="Retail Price",
    font_size=70,
    color="#fff",
    text_align="center",
    margin=(20, 20)
    )

    offer_price_text = TextClip(
    font=font,
    text="Only $79,999.97",
    margin = (10,10),
    font_size=90,
    color="Red",
    text_align="center",
    )


    sale_text = TextClip(
    font=font,
    text="Sale Price",
    font_size=80,
    color="Red",
    text_align="center",
    margin=(20, 20)
    )

    print('service called',clip_template)


    #product images
    item_image = (
        ImageClip(download_image(url1,"1"))
                .resized(width=700)
                .with_duration(2)
                .with_start(2)
                .with_position((100, "center"))
                )

    item_image2 = (
        ImageClip(download_image(url2,"2"))
                .resized(width=700)
                .with_duration(2)
                .with_start(3)
                .with_position((100, "center"))
                )

    item_image3 = (
        ImageClip(download_image(url3,"3"))
                    .resized(width=700)
                    .with_duration(2)
                    .with_start(4)
                    .with_position((100, "center"))
                    )

    item_image4 = (
        ImageClip(download_image(url4,"4"))
                    .resized(width=700)
                    .with_duration(2)
                    .with_start(6)
                    .with_position((100, "center"))
                    )

    item_image5 = (
        ImageClip(download_image(url5,"5"))
                    .resized(width=700)
                    .with_duration(2)
                    .with_start(8)
                    .with_position((100, "center"))
                    )

    #hr red line 
    price_hr_redline = (
        ImageClip(hr_redLine)
                    .resized(width=400)
                    .with_duration(6)
                    .with_start(4)
                    .with_position((1100, 500))
                    )

    #item price and text
    item_name = item_name_text.with_duration(7).with_start(3).with_position((840, 100))

    retail_text = retail_text.with_duration(6).with_start(4).with_position((1100, 375))
    item_price = item_price_text.with_duration(6).with_start(4).with_position((1100, 480))

    sale_text = sale_text.with_duration(5).with_start(5).with_position((1100, 650))
    offer_price = offer_price_text.with_duration(5).with_start(5).with_position((1050, 750))

    quick_compo = CompositeVideoClip(
    [
        clip_template,
        item_image,
        item_image2,
        item_image3,
        item_image4,
        item_image5,
        item_name,
        item_price,
        offer_price,
        retail_text,
        sale_text,
        price_hr_redline
     ]
    )

    quick_compo.write_videofile(f"./gen_videos/{jwl_key}.mp4", fps=10)
    print("Render complete!")


def get_template(template):
    match template:
        case 1:
            return  "VideoGenAkash-1.mp4"
        case _:
            return  "VideoGenAkash-1.mp4"

def wrap_text (text):
    words = text.split()
    new_text = []
    text

    for i in range(len(words)):
        currntLine=i+1
        new_text.append(" "+ words[i])

        if(currntLine % 6==0):
            new_text.append("\n")
    text = "".join(new_text)
    return text      

def download_image(url, image_name, temp_dir=".assets/temp/"):  # Change this path as needed

    os.makedirs(temp_dir, exist_ok=True) 
    temp_file = os.path.join(temp_dir, image_name+".jpg")
    response = requests.get(url)
    
    with open(temp_file, 'wb') as f:
        f.write(response.content)
        ##
        img = Image.open(f".assets/temp/{image_name}.jpg" ).convert("RGBA")  # Ensure the image has an alpha channel
        # Add border (stroke)
        img_with_border = ImageOps.expand(img, border=20, fill=(29, 38, 107))
        ##
    return np.array(img_with_border)