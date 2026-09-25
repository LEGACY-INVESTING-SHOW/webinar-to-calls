"""Contact sheet: python3 tools/contact.py out.png img1.png img2.png ... (3 columns)"""
import sys
from PIL import Image
out, *files = sys.argv[1:]
ims = [Image.open(f) for f in files]
w = 640; h = int(w * ims[0].height / ims[0].width); cols = 3
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 12) + 12), (221, 212, 190))
for k, im in enumerate(ims):
    r, c = divmod(k, cols)
    sheet.paste(im.resize((w, h)), (12 + c * (w + 12), 12 + r * (h + 12)))
sheet.save(out)
print(out, sheet.size)
