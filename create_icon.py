from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a blue background
img = Image.new('RGB', (512, 512), color=(0, 102, 204))
d = ImageDraw.Draw(img)

# Draw a white circle in the center
d.ellipse((100, 100, 412, 412), fill=(255, 255, 255))

# Draw a blue cross to represent medical/health
d.rectangle((236, 100, 276, 412), fill=(0, 102, 204))
d.rectangle((100, 236, 412, 276), fill=(0, 102, 204))

# Save the image
os.makedirs('image', exist_ok=True)
img.save('image/page_icon.jpeg', 'JPEG')

print("New page icon created successfully!")
