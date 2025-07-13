from PIL import Image
import math

def distance_2d_points(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def rotate_img_coords(x,y,w,h, theta_radians=0):
    r = math.sqrt(x**2 + y**2)
    gamma = math.atan2(y,x)
    net_rotation = gamma - theta_radians
    x_bar = r * math.cos(net_rotation)
    y_bar = r * math.sin(net_rotation)

    if theta_radians <= 0:
        x_new = x_bar + h * math.sin(theta_radians)
        y_new = y_bar

    else:
        x_new = x_bar
        y_new = y_bar + w * math.sin(theta_radians)

    return int(x_new), int(y_new)

def compute_rotated_lens_dest(
    img_left_eye_xy, img_right_eye_xy,
    sun_left_eye_xy, sun_right_eye_xy,
    w, h, angle_degrees, scale
):
    img_cx = (img_left_eye_xy[0] + img_right_eye_xy[0]) // 2
    img_cy = (img_left_eye_xy[1] + img_right_eye_xy[1]) // 2

    sun_cx = (sun_left_eye_xy[0] + sun_right_eye_xy[0]) // 2
    sun_cy = (sun_left_eye_xy[1] + sun_right_eye_xy[1]) // 2

    sun_cx_scaled = sun_cx * scale
    sun_cy_scaled = sun_cy * scale
    dx = int(img_cx - sun_cx_scaled)
    dy = int(img_cy - sun_cy_scaled)

    return (dx, dy)

def base_plus_lens(base, lens, dest=(0,0), scale=1.0, angle=0.0):
    pasted = base.convert("RGBA")
    lens = lens.convert("RGBA")
    lens = lens.rotate(-angle, expand=True)
    new_size = (max(1, round(scale * lens.width)), max(1, round(scale * lens.height)))
    lens = lens.resize(new_size)
    pasted.paste(lens, dest, mask=lens)
    return pasted
    
    