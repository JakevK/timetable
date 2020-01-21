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


response = requests.get(sys.argv[1])
img = Image.open(BytesIO(response.content))
#img = Image.open("images/{}.jpg".format(sys.argv[1]))
img = img.convert("RGBA")

cropped = crop(img, dimensions)
width, height = cropped.size

overlay_img = Image.new("RGBA", cropped.size, (0, 0, 0, 0))

draw = ImageDraw.Draw(overlay_img)
box_height = width * (2 / 3)
box_top = height - (box_height * (2/3)) - box_height
draw.rectangle((0, box_top, width, box_height + box_top), \
    fill=(255, 255, 255, 127), outline=(50, 50, 50), width=3)

timetable = scrape.get_timetable()


for i, day in enumerate(timetable):
    for j, period in enumerate(day):
        pos_x = (width / len(timetable)) * i
        pos_y = (box_height / len(day)) * j + box_top
        period_width = width / len(timetable)
        period_margin = period_width / 13
        period_height = box_height / len(day)
        draw.rectangle( \
            (pos_x, pos_y, pos_x + period_width, pos_y + period_height), \
            outline=(50, 50, 50), width=3)
        fontsize = 1
        font = ImageFont.truetype('fonts/Product Sans Bold.ttf', fontsize)
        while font.getsize('WWWWWW')[0] < (period_width - (period_margin * 2)):
            fontsize += 1
            font = ImageFont.truetype("fonts/Product Sans Bold.ttf", fontsize)
        draw.text((pos_x + period_margin, pos_y + period_margin + (period_height * (1/8))), period.subject, font=font, fill=(50, 50, 50))
        fontsize = 1
        font = ImageFont.truetype('fonts/Product Sans Regular.ttf', fontsize)
        while font.getsize('WWW WW')[0] < ((period_width * (3/4)) - (period_margin * 2)):
            fontsize += 1
            font = ImageFont.truetype("fonts/Product Sans Regular.ttf", fontsize)
        draw.text((pos_x + period_margin, pos_y + period_margin + (period_height / 2)), str(period.teacher) + ' - ' + str(period.room), font=font, fill=(50, 50, 50))


result = Image.alpha_composite(cropped, overlay_img)
result = result.convert("RGB")
result.show()
