from pathlib import Path
from PIL import Image
from lensify.animation import animate_angled_shifted_sunglasses

def lensify_photo(image_path: Path, output_gif: Path):
    sunglasses_img = Image.open("data/glasses3.png").convert("RGBA")
    sun_left_eye_xy = (512, 376)
    sun_right_eye_xy = (1666, 376)
    base_img = Image.open(image_path)
    img_width, img_height = base_img.size
    bezier_control = (img_width // 2, 0)

    print(f"[DEBUG] lensify_photo: Starting with image: {image_path}")
    print(f"[DEBUG] Loaded sunglasses image. Size: {sunglasses_img.size}")
    print(f"[DEBUG] Sun left eye coords: {sun_left_eye_xy}")
    print(f"[DEBUG] Sun right eye coords: {sun_right_eye_xy}")
    print(f"[DEBUG] Bezier control point: {bezier_control}")

    frames = animate_angled_shifted_sunglasses(
        image_path,
        sunglasses_img,
        sun_left_eye_xy,
        sun_right_eye_xy,
        bezier_control,
        num_points=25
    )
    durations = [100] * (len(frames) - 1) + [2000]  
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=5
    )