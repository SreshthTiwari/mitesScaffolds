"""
pose_analysis.py - Body landmark detection with MediaPipe (OPTIONAL).

WHAT IS A "LANDMARK"?
  MediaPipe looks at a photo and guesses where 33 key body points are:
  nose, shoulders, elbows, wrists, hips, knees, ankles, etc.
  Each landmark has:
    x, y   -> position as a fraction of the image (0.0 = left/top, 1.0 = right/bottom)
    z      -> rough depth (we mostly ignore it)
    visibility -> how confident MediaPipe is that the point is really visible (0 to 1)
  We also convert x and y into pixels (x_px, y_px) so they're easy to draw/measure.

  NOTE: "left" and "right" mean the PERSON's left and right, not the image's.

THIS FILE IS ISOLATED ON PURPOSE: the rest of the app only calls
detect_pose(), get_point() and calculate_angle(). If MediaPipe isn't
installed, the app still runs and shows a status message.

SETUP: the newer MediaPipe "Tasks" API needs a model file.
  Run:  python pose_analysis.py --download
  (saves models/pose_landmarker_lite.task)
"""

import math
import os
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "pose_landmarker_lite.task")
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
             "pose_landmarker_lite/float16/latest/pose_landmarker_lite.task")

# MediaPipe returns 33 landmarks in this fixed order.
LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer", "left_ear", "right_ear",
    "mouth_left", "mouth_right", "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow", "left_wrist", "right_wrist",
    "left_pinky", "right_pinky", "left_index", "right_index",
    "left_thumb", "right_thumb", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
    "left_heel", "right_heel", "left_foot_index", "right_foot_index",
]

# Pairs of landmarks to connect with lines when drawing the "skeleton".
SKELETON_LINES = [
    ("left_shoulder", "right_shoulder"), ("left_hip", "right_hip"),
    ("left_shoulder", "left_hip"), ("right_shoulder", "right_hip"),
    ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"),
    ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"),
    ("left_hip", "left_knee"), ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"), ("right_knee", "right_ankle"),
]


# ==================================================
# Setup Checks and Model Download
# ==================================================
def check_pose_setup():
    """Return (is_ready, message). Never raises, so the app can always launch."""
    try:
        import mediapipe  # noqa: F401
    except ImportError:
        return False, "MediaPipe is not installed (pip install mediapipe). Pose detection is off."
    if not os.path.exists(MODEL_PATH):
        return False, "Pose model file missing. Run: python pose_analysis.py --download"
    return True, "Pose detection is ready."


def download_model():
    """Download the pose model (about 6 MB) into the models/ folder."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"Downloading {MODEL_URL} ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"Saved to {MODEL_PATH}")


# ==================================================
# Detect Landmarks in a Still Image (PROVIDED)
# ==================================================
def detect_pose(image):
    """
    Try to find body landmarks in an image.

    image: NumPy array of shape (height, width, 3), RGB, values 0-255.
           (This is what Gradio's Image component gives us.)

    Returns a dictionary:
      {
        "found": True/False,
        "status": "human-readable message",
        "landmarks": {"right_elbow": {"x":..,"y":..,"z":..,"visibility":..,
                                      "x_px":..,"y_px":..}, ...},
        "annotated_image": image with dots and lines drawn on it
      }
    """
    result = {"found": False, "status": "", "landmarks": {}, "annotated_image": image}

    # --- Check the image is usable ---
    if image is None:
        result["status"] = "No image provided."
        return result
    if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] < 3:
        result["status"] = "Image must be a color photo (height x width x 3)."
        return result
    image = np.ascontiguousarray(image[:, :, :3], dtype=np.uint8)  # drop alpha channel if any
    result["annotated_image"] = image

    # --- Check MediaPipe and the model are available ---
    ready, message = check_pose_setup()
    if not ready:
        result["status"] = message
        return result

    # --- Run MediaPipe (imported here so the app works without it) ---
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision

        options = vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=vision.RunningMode.IMAGE,  # one still photo
            num_poses=1,                            # look for one person
        )
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        with vision.PoseLandmarker.create_from_options(options) as landmarker:
            detection = landmarker.detect(mp_image)
    except Exception as error:  # beginner-friendly catch-all for setup problems
        result["status"] = f"Pose detection failed: {error}"
        return result

    if not detection.pose_landmarks:
        result["status"] = ("No person/pose detected. Try a clearer photo with your "
                            "whole body visible and good lighting.")
        return result

    # --- Convert MediaPipe's output into a simple dictionary ---
    height, width = image.shape[:2]
    for name, lm in zip(LANDMARK_NAMES, detection.pose_landmarks[0]):
        result["landmarks"][name] = {
            "x": lm.x, "y": lm.y, "z": lm.z,
            "visibility": lm.visibility if lm.visibility is not None else 0.0,
            "x_px": lm.x * width, "y_px": lm.y * height,
        }

    result["found"] = True
    result["status"] = "Pose detected. Landmark positions are estimates and may be off."
    result["annotated_image"] = draw_landmarks(image, result["landmarks"])
    return result


def draw_landmarks(image, landmarks, min_visibility=0.5):
    """Return a copy of the image with the skeleton drawn on it."""
    picture = Image.fromarray(image)
    draw = ImageDraw.Draw(picture)
    size = max(3, picture.width // 150)  # scale dots/lines with image size

    for start, end in SKELETON_LINES:
        a, b = get_point(landmarks, start, min_visibility), get_point(landmarks, end, min_visibility)
        if a and b:
            draw.line([a, b], fill=(0, 200, 255), width=size)
    for name in landmarks:
        p = get_point(landmarks, name, min_visibility)
        if p:
            draw.ellipse([p[0] - size, p[1] - size, p[0] + size, p[1] + size], fill=(255, 60, 60))
    return np.array(picture)


# ==================================================
# Helpers for Examining Landmarks (PROVIDED)
# ==================================================
def get_point(landmarks, name, min_visibility=0.5):
    """
    Return (x_px, y_px) for a landmark, or None if it is missing or not
    visible enough. ALWAYS check for None before using the result!
    """
    lm = landmarks.get(name)
    if lm is None or lm["visibility"] < min_visibility:
        return None
    return (lm["x_px"], lm["y_px"])


def calculate_angle(a, b, c):
    """
    Angle (in degrees) at point b, formed by the lines b->a and b->c.
    Example: a=shoulder, b=elbow, c=wrist gives the elbow angle.
      ~180 = straight arm, ~90 = right angle, small = tightly bent.
    Each point is an (x, y) pair. Returns None if the angle can't be computed.

    This measures the angle as it appears IN THE 2D PHOTO. If the arm points
    toward or away from the camera, the real angle can look very different.
    """
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    length = math.hypot(*ba) * math.hypot(*bc)
    if length == 0:
        return None
    cosine = (ba[0] * bc[0] + ba[1] * bc[1]) / length
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))



if __name__ == "__main__":
    if "--download" in sys.argv:
        download_model()
    else:
        print(check_pose_setup()[1])
        print("Use --download to fetch the model file.")
