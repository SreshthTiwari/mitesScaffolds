"""
feedback.py - Rules that turn landmarks into technique suggestions.

TWO DIFFERENT THINGS LIVE HERE. Keep them separate!
  1. MEASUREMENTS (analyze_pose): facts computed from the photo, e.g.
     "elbow angle is about 95 degrees in this image".
  2. COACHING (build_suggestions): opinions/advice based on those facts,
     the sport, and the athlete's level.

IMPORTANT HONESTY NOTES (shown to users):
  - One photo is one instant. It cannot prove a whole movement is right or wrong.
  - Angles come from a 2D picture. Camera angle changes them a lot.
  - MediaPipe's landmark positions are estimates.
"""

from pose_analysis import calculate_angle, get_point
from sports import get_level_guidance, get_sport_instructions

DISCLAIMER = ("Measurements are approximate and come from a single photo. Camera angle "
              "affects accuracy. This is not a substitute for a qualified coach.")

# Each joint is measured from three landmarks: the angle is at the middle one.
JOINTS = {
    "right elbow": ("right_shoulder", "right_elbow", "right_wrist"),
    "left elbow": ("left_shoulder", "left_elbow", "left_wrist"),
    "right knee": ("right_hip", "right_knee", "right_ankle"),
    "left knee": ("left_hip", "left_knee", "left_ankle"),
}

# Which joints matter for which sport (any other sport gets all four).
SPORT_JOINTS = {
    "basketball": ["right elbow", "left elbow", "right knee"],
    "soccer": ["right knee", "left knee"],
    "volleyball": ["right elbow", "left elbow", "right knee", "left knee"],
    "dance": ["right knee", "left knee", "right elbow", "left elbow"],
}


# ==================================================
# FEATURE 2, PART A: Measurements (provided) and labels (yours)
# ==================================================
def classify_angle(angle):
    """
    Turn a joint angle (in degrees) into one of three plain-language labels:
    "nearly straight", "bent" or "tightly bent".
    """
    if angle > 160:
        return "nearly straight"
    elif angle >= 70:
        return "bent"
    else:
        return "tightly bent"


def analyze_pose(landmarks, sport):
    """
    PROVIDED. Measure the joints that matter for `sport` and return a list like
      [{"name": "Right elbow angle", "value": 142.0, "label": "bent"}]
    `value` is None when a landmark was hidden and the angle could not be measured.
    """
    measurements = []
    for joint in SPORT_JOINTS.get(sport, list(JOINTS)):
        first, middle, last = JOINTS[joint]
        points = [get_point(landmarks, name) for name in (first, middle, last)]
        angle = None if None in points else calculate_angle(*points)
        measurements.append({
            "name": f"{joint.capitalize()} angle",
            "value": angle,
            "label": classify_angle(angle) if angle is not None else "could not measure",
        })
    return measurements


# ==================================================
# FEATURE 2, PART B: Coaching Suggestions (INTERPRETATION)
# ==================================================
def build_suggestions(sport, level, measurements):
    """
    Return a list of suggestion strings for the user.
    These are interpretations of the measurements, not measurements themselves.
    """
    suggestions = [get_sport_instructions(sport), get_level_guidance(level)]

    for m in measurements:
        if m["value"] is None:
            continue
        name, label = m["name"].lower(), m["label"]
        if level == "beginner":
            suggestions.append(f"Your {name} looks {label}. Try a few slow practice reps and see how it feels.")
        elif level == "intermediate":
            suggestions.append(f"Your {name} looks {label} in this photo. You might compare it with a photo of a good rep.")
        else:
            suggestions.append(
                f"{name.capitalize()} reads about {round(m['value'])} degrees ({label}). "
                "Try retaking the photo from the same side to see if the angle holds up.")

    return suggestions
