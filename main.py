from PIL import Image, ImageDraw, ImageFont
import sys
import requests
from io import BytesIO
from classes import Period
import scrape

def crop(image, target_dimensions):
    width, height = image.size
    target_x, target_y = target_dimensions

    if (width / height) < (target_x / target_y):
        # width stays the same
        x = width
        y = width / (target_x / target_y)
    else:
        # height stays the same
        x = height / (target_y / target_x)
        y = height

    left = (width - x) / 2
    right = width - (width - x) / 2
    top = (height - y) / 2
    bottom = height - (height - y) / 2

    return image.crop((left, top, right, bottom))



dimensions = (750, 1334)

def product(img_url = 'https://cdn57.androidauthority.net/wp-content/uploads/2019/05/android-q-beta-3-wallpaper-1.png'):

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    #img = Image.open("images/{}.jpg".format(sys.argv[1]))
    img = img.convert("RGBA")

    cropped = crop(img, dimensions)
    width, height = cropped.size

    overlay_img = Image.new("RGBA", cropped.size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(overlay_img)
    box_height = width * (2 / 3)
    box_top = height - (box_height * (1/2)) - box_height
    draw.rectangle((0, box_top, width, box_height + box_top), \
        fill=(255, 255, 255, 127), outline=(50, 50, 50), width=3)

    print('retrieving timetable')
    timetable = scrape.get_timetable()
    print('retrieved')

    period_width = width / len(timetable)
    period_margin = period_width / 13

    fontsize = 1
    subject_font = ImageFont.truetype('fonts/Product Sans Bold.ttf', fontsize)
    while subject_font.getsize('WWWWWW')[0] < (period_width - (period_margin * 2)):
        fontsize += 1
        subject_font = ImageFont.truetype("fonts/Product Sans Bold.ttf", fontsize)

    fontsize = 1
    teacher_font = ImageFont.truetype('fonts/Product Sans Regular.ttf', fontsize)
    while teacher_font.getsize('WWW WW')[0] < ((period_width * (3/4)) - (period_margin * 2)):
        fontsize += 1
        teacher_font = ImageFont.truetype("fonts/Product Sans Regular.ttf", fontsize)


    for i, day in enumerate(timetable):
        for j, period in enumerate(day):
            period_height = box_height / len(day)
            pos_x = (width / len(timetable)) * i
            pos_y = (box_height / len(day)) * j + box_top
            draw.rectangle( \
                (pos_x, pos_y, pos_x + period_width, pos_y + period_height), \
                outline=(50, 50, 50), width=3)
            draw.text((pos_x + period_margin, pos_y + period_margin + (period_height * (1/8))), period.subject, font=subject_font, fill=(50, 50, 50))
            draw.text((pos_x + period_margin, pos_y + period_margin + (period_height / 2)), str(period.teacher) + ' - ' + str(period.room), font=teacher_font, fill=(50, 50, 50))


    result = Image.alpha_composite(cropped, overlay_img)
    result = result.convert("RGB")
    return result

if __name__ == "__main__":
    result = product(sys.argv[1])
    result.save('images/timetable.jpg', 'JPEG')
    print('complete')
