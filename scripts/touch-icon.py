from PIL import Image, ImageDraw, ImageFont

S = 180
im = Image.new("RGB", (S, S), (11, 14, 19))
d = ImageDraw.Draw(im)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=40, fill=255)
font = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 96)
d.text((S / 2, S / 2 - 6), "S", font=font, fill=(199, 162, 76), anchor="mm")
d.rounded_rectangle([58, 120, 122, 124], radius=2, fill=(199, 162, 76))
out = Image.new("RGB", (S, S), (255, 255, 255))
out.paste(im, (0, 0), mask)
out.save("assets/marca/apple-touch-icon.png")
print("apple-touch-icon.png", out.size)
