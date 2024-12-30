from PIL import Image, ImageDraw

img = Image.open("sample.jpg")

bbox = [
122.66092681884766,
                151.4235382080078,
                273.17242431640625,
                202.11581420898438
]

convert_to_ltrb = [bbox[0], bbox[1], bbox[2], bbox[3]]

# draw bbox
draw = ImageDraw.Draw(img)
draw.rectangle(bbox, outline="red", width=3)
#draw dot
# draw.point(convert_to_ltrb, fill="red")
#draw line
img.show()
