from pathlib import Path
from typing import Tuple, List

import cv2
import dlib
import numpy as np
from PIL import Image, ImageDraw

PREDICTOR_PATH = Path(__file__).parent.parent / "data" / "shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(str(PREDICTOR_PATH))

Point = Tuple[int, int]
BBox = Tuple[int, int, int, int] 

def detect_visualize_eyes(image_path: Path | str, *_unused) -> tuple[list[BBox], list[Point], Image.Image]:
    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces_rects = detector(gray, 1)
    if not faces_rects:
        return [], [], Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))

    face = faces_rects[0] 
    shape = predictor(gray, face)
    leye_pts = np.array([(shape.part(i).x, shape.part(i).y) for i in range(36, 42)])
    reye_pts = np.array([(shape.part(i).x, shape.part(i).y) for i in range(42, 48)])

    leye_center = tuple(leye_pts.mean(axis=0).astype(int))
    reye_center = tuple(reye_pts.mean(axis=0).astype(int))

    eyes_out: list[Point] = [leye_center, reye_center]
    debug_pil = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(debug_pil)
    for pt in eyes_out:
        draw.ellipse((pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5), outline="red", width=3)
    faces: list[BBox] = [(face.left(), face.top(), face.width(), face.height())]

    return faces, eyes_out, debug_pil


def eyes_angle_degrees(eyes: List[Point]) -> tuple[float, Point, Point]:
    """
    Same helper as before but now relies on dlib-based eyes list.
    """
    if len(eyes) < 2:
        raise ValueError(f"Less than 2 eyes detected… got: {eyes}")

    left_eye, right_eye = sorted(eyes, key=lambda p: p[0])
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = float(np.degrees(np.arctan2(dy, dx)))
    return angle, left_eye, right_eye