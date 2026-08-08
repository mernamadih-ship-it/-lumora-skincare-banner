import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 1. Canvas Setup (1200x628 px)
width, height = 1200, 628

# Palette Definitions - warm terracotta / blush skincare tone
C_DARK_BG   = (74, 46, 42)      # #4A2E2A - Deep Terracotta
C_MID_BG    = (156, 99, 82)     # #9C6352 - Clay Rose
C_BLUSH     = (224, 178, 160)   # #E0B2A0 - Blush
C_ACCENT    = (242, 213, 180)   # #F2D5B4 - Warm Sand
C_WHITE     = (255, 255, 255)
C_TEXT_SUB  = (238, 224, 216)

# 2. Radial Gradient & Fine Grain Background
y_coords, x_coords = np.ogrid[:height, :width]
center_x, center_y = width * 0.68, height * 0.45
dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
max_d = np.sqrt((width)**2 + (height)**2) * 0.75
norm_dist = np.clip(dist / max_d, 0, 1)

bg_arr = np.zeros((height, width, 3), dtype=np.float32)
for i in range(3):
    bg_arr[:, :, i] = C_MID_BG[i] * (1 - norm_dist) + C_DARK_BG[i] * norm_dist

np.random.seed(42)
noise = np.random.normal(0, 9, (height, width, 3))
grain_bg = np.clip(bg_arr + noise, 0, 255).astype(np.uint8)
base_img = Image.fromarray(grain_bg).convert('RGBA')

# 3. Vector Arcs (Organic Pen Tool Shapes)
vector_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
v_draw = ImageDraw.Draw(vector_layer)
v_draw.ellipse([550, -250, 1350, 550], fill=(242, 213, 180, 30))
v_draw.ellipse([650, -120, 1250, 480], fill=(224, 178, 160, 35))
v_draw.polygon([(0, 628), (0, 380), (250, 430), (420, 628)], fill=(74, 46, 42, 90))
base_img = Image.alpha_composite(base_img, vector_layer)

# 4. Product Vector Art Showcase (abstract bottle)
prod_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(prod_layer)
px, py = 860, 320

# Radial Glow Rings
for r, alpha in [(230, 18), (190, 34), (150, 55)]:
    p_draw.ellipse([px - r, py - r, px + r, py + r], fill=(242, 213, 180, alpha))

# Soft shadow ellipse
p_draw.ellipse([px - 110, py + 150, px + 110, py + 185], fill=(30, 15, 12, 120))

# Bottle body
p_draw.rounded_rectangle([px - 65, py - 60, px + 65, py + 160], radius=26, fill=C_ACCENT + (245,), outline=C_WHITE, width=2)
# Bottle neck
p_draw.rectangle([px - 22, py - 100, px + 22, py - 55], fill=C_ACCENT + (245,))
# Bottle cap
p_draw.rounded_rectangle([px - 28, py - 125, px + 28, py - 95], radius=8, fill=C_DARK_BG + (255,))
# Label accent stripe
p_draw.rectangle([px - 65, py + 10, px + 65, py + 45], fill=C_MID_BG + (200,))
# Droplet icon above bottle
p_draw.polygon([(px, py - 175), (px - 16, py - 145), (px + 16, py - 145)], fill=C_BLUSH + (255,))
p_draw.ellipse([px - 16, py - 155, px + 16, py - 123], fill=C_BLUSH + (255,))

base_img = Image.alpha_composite(base_img, prod_layer)

# 5. Typography & CTA Layer
text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
t_draw = ImageDraw.Draw(text_layer)

f_logo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 30)
f_head_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 58)
f_head_it = ImageFont.truetype("DejaVuSans.ttf", 58)
f_sub = ImageFont.truetype("DejaVuSans.ttf", 25)
f_cta = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)

tx = 90
# Logo mark
t_draw.ellipse([tx, 68, tx + 38, 106], outline=C_ACCENT, width=3)
t_draw.ellipse([tx + 10, 78, tx + 28, 96], fill=C_ACCENT)
t_draw.text((tx + 52, 68), "LUMORA", font=f_logo, fill=C_WHITE)

# Headline
head_y = 235
t_draw.text((tx, head_y), "Bare Skin,", font=f_head_bold, fill=C_WHITE)
line1_w = t_draw.textlength("Bare Skin,", font=f_head_bold)
t_draw.text((tx, head_y + 72), "Bold Glow.", font=f_head_bold, fill=C_ACCENT)
line2_w = t_draw.textlength("Bold Glow.", font=f_head_bold)
t_draw.rounded_rectangle([tx, head_y + 148, tx + line2_w, head_y + 156], radius=4, fill=C_ACCENT)

# Subhead
t_draw.text((tx, head_y + 185), "Clean, dermatologist-tested skincare.", font=f_sub, fill=C_TEXT_SUB)

# CTA Button with Drop Shadow
cta_x, cta_y, cta_w, cta_h = tx, head_y + 250, 210, 62
shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow_layer)
s_draw.rounded_rectangle([cta_x + 4, cta_y + 6, cta_x + cta_w + 4, cta_y + cta_h + 6], radius=31, fill=(0, 0, 0, 100))
text_layer = Image.alpha_composite(text_layer, shadow_layer.filter(ImageFilter.GaussianBlur(8)))

t_draw = ImageDraw.Draw(text_layer)
t_draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=31, fill=C_ACCENT)
t_draw.ellipse([cta_x + cta_w - 48, cta_y + 13, cta_x + cta_w - 13, cta_y + 48], fill=C_DARK_BG)
t_draw.text((cta_x + 32, cta_y + 17), "Shop Now", font=f_cta, fill=C_DARK_BG)

# Save
final_img = Image.alpha_composite(base_img, text_layer).convert('RGB')
final_img.save("/mnt/user-data/outputs/LUMORA_Skincare_Design.png", "PNG")
print("saved")
