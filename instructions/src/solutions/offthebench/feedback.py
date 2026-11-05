"""
feedback.py - Simple rules that turn landmarks into technique suggestions.

TWO DIFFERENT THINGS LIVE HERE. Keep them separate!
  1. MEASUREMENTS (analyze_pose): facts computed from the photo, e.g.
     "elbow angle is about 95 degrees in this image".
  2. COACHING (build_suggestions): opinions/advice based on those facts,
     the sport, and the athlete's level.

IMPORTANT HONESTY NOTES (show these to users!):
  - One photo is one instant. It cannot prove a whole movement is right or wrong.
  - Angles come from a 2D picture. Camera angle changes them a lot.
  - MediaPipe's landmark positions are estimates.
"""

from pose_analysis import calculate_angle, get_point
from sports import get_level_guidance, get_sport_instructions

DISCLAIMER = ("Measurements are approximate and come from a single photo. Camera angle "
              "affects accuracy. This is not a substitute for a qualified coach.")


# ==================================================
# FEATURE 5: Analyze Body Position (MEASUREMENTS)
# ==================================================
def measure_joint_angle(landmarks, first, middle, last):
    """
    Angle at `middle` between `first` and `last` (all landmark names), or None
    if any landmark is missing / not visible.
    Example: measure_joint_angle(landmarks, "right_shoulder", "right_elbow", "right_wrist")
    """
    points = [get_point(landmarks, name) for name in (first, middle, last)]
    if None in points:
        return None
    return calculate_angle(*points)


def classify_elbow_angle(angle):
    """Turn an elbow angle into a plain-language label."""
    if angle > 160:
        return "nearly straight"
    elif angle >= 70:
        return "bent"
    else:
        return "tightly bent"


def classify_knee_angle(angle):
    """Turn a knee angle into a plain-language label."""
    if angle > 165:
        return "nearly straight"
    elif angle >= 110:
        return "slightly bent"
    else:
        return "deeply bent"


# One entry per joint: (display name, first landmark, middle landmark, last landmark, classifier)
ELBOWS = [
    ("Right elbow angle", "right_shoulder", "right_elbow", "right_wrist", classify_elbow_angle),
    ("Left elbow angle", "left_shoulder", "left_elbow", "left_wrist", classify_elbow_angle),
]
KNEES = [
    ("Right knee angle", "right_hip", "right_knee", "right_ankle", classify_knee_angle),
    ("Left knee angle", "left_hip", "left_knee", "left_ankle", classify_knee_angle),
]


def analyze_pose(landmarks, sport):
    """
    Return a list of measurement dictionaries, e.g.
      [{"name": "Right elbow angle", "value": 142.0, "label": "bent"}]
    `value` is None when the measurement could not be made.
    """
    measurements = []

    # Which joints matter depends on the sport.
    if sport == "basketball":
        joints = ELBOWS
    elif sport == "soccer":
        joints = KNEES
    else:  # volleyball, tennis, dance, anything new: look at arms and legs
        joints = ELBOWS + KNEES

    for name, first, middle, last, classify in joints:
        angle = measure_joint_angle(landmarks, first, middle, last)
        if angle is None:
            label = "could not measure (landmark hidden)"
        else:
            label = classify(angle)
        measurements.append({"name": name, "value": angle, "label": label})

    return measurements


# ==================================================
# FEATURE 2 + 5: Coaching Suggestions (INTERPRETATION)
# ==================================================
DRILLS = {
    "basketball": "Try a wall shooting drill: stand close to a wall and focus on a smooth elbow and wrist follow-through.",
    "soccer": "Try a plant-foot drill: place your plant foot beside a marker on 10 slow kicks and notice your knee bend.",
    "volleyball": "Try 20 slow overhead sets against a wall, keeping your elbows bent and hands high.",
    "dance": "Practice the pose at a mirror, holding for five slow counts and checking your leg lines.",
    "tennis": "Shadow-swing slowly in front of a mirror, pausing at contact to check your elbow and knees.",
}


def suggestion_for(measurement, level):
    """One coaching sentence for one measurement, worded for the athlete's level."""
    name = measurement["name"].lower()
    label = measurement["label"]
    if level == "beginner":
        return f"Your {name} looks {label} in this photo. Notice how that feels, and try small changes."
    elif level == "intermediate":
        return (f"Your {name} looks {label} (about {round(measurement['value'])} degrees). "
                "You might compare it with a second photo from the same side.")
    else:
        return (f"Your {name} is {label} at roughly {round(measurement['value'])} degrees "
                "in this frame. It might be worth checking how it changes through the whole movement.")


def build_suggestions(sport, level, measurements):
    """
    Return a list of suggestion strings for the user.
    These are interpretations of the measurements, not measurements themselves.
    """
    suggestions = [get_sport_instructions(sport), get_level_guidance(level)]

    for m in measurements:
        if m["value"] is not None:
            suggestions.append(suggestion_for(m, level))

    if sport in DRILLS:
        suggestions.append(DRILLS[sport])

    return suggestions


# ==================================================
# FEATURE 7: Optional Extensions (ideas only)
# ==================================================
# - Video: read frames with OpenCV, run detect_pose on each, and look at how an
#   angle CHANGES over time (a movement is a sequence, not one pose).
# - Compare two frames (e.g. before and after takeoff) and report the difference.
# - Draw measured angles on the annotated image.
# - Skill-specific drills chosen from the measurements.
