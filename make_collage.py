import sys, glob, os
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
files = sorted(f for f in glob.glob(os.path.join(src, "*")) if f.lower().endswith((".jpg",".png")) and os.path.basename(f)[:2].isdigit())
cols, rows, tile, gap = 5, 4, 400, 8
W, H = cols*tile + (cols+1)*gap, rows*tile + (rows+1)*gap
canvas = Image.new("RGB", (W, H), "white")
for i, f in enumerate(files[:cols*rows]):
    im = Image.open(f).convert("RGB")
    ar = im.width / im.height
    if max(ar, 1/ar) > 1.25:  # very wide/tall: letterbox instead of cropping
        im = ImageOps.pad(im, (tile, tile), Image.LANCZOS, color=(20, 20, 20))
    else:
        im = ImageOps.fit(im, (tile, tile), Image.LANCZOS, centering=(0.5, 0.5))
    r, c = divmod(i, cols)
    canvas.paste(im, (gap + c*(tile+gap), gap + r*(tile+gap)))
canvas.save(out, quality=92)
print(len(files), canvas.size)
