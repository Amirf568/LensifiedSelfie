from PIL import Image
from lensify.imaging import base_plus_lens

def bezier_curve(p0, p1, p2, n_points=25):
    """Quadratic Bézier curve points."""
    return [
        (
            int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]),
            int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]),
        )
        for t in [i / n_points for i in range(n_points + 1)]
    ]

def animate_angled_shifted_sunglasses(
    image_filename,
    sunglasses_img,
    sun_leye,
    sun_reye,
    bezier_ctrl,
    num_points: int = 25,
):
    from lensify.detection import detect_visualize_eyes, eyes_angle_degrees
    from lensify.imaging import compute_rotated_lens_dest, distance_2d_points

    faces, eyes, base_img = detect_visualize_eyes(image_filename, "eye_tree_eyeglasses")
    if len(eyes) < 2:  
        faces, eyes, base_img = detect_visualize_eyes(image_filename, "eye")
    angle, img_leye, img_reye = eyes_angle_degrees(eyes)

    img_width, img_height = base_img.size

    scale = distance_2d_points(img_leye, img_reye) / distance_2d_points(
        sun_leye, sun_reye
    )
    scale += (img_width / 2000) * 0.1
    scale = max(0.3, min(scale, 2.0))  
    scale *= 0.70  
    dest = compute_rotated_lens_dest(
    img_leye, img_reye,
    sun_leye, sun_reye,
    sunglasses_img.width, sunglasses_img.height,
    angle, scale  
)

    curve = bezier_curve(p0=(0, 0), p1=bezier_ctrl, p2=dest, n_points=num_points)
    frames: list[Image.Image] = []
    for point in curve:
        frame = base_plus_lens(
            base_img, sunglasses_img, dest=point, scale=scale, angle=angle
        )
        frames.append(frame)
    final_frame = frames[-1]
    frames.extend([final_frame] * 10)  

    return frames