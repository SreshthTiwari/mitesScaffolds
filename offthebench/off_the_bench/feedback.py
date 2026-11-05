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
    # TODO 3: Use if/elif/else to classify the angle. For example:
    #         above ~160 -> "nearly straight", ~70-160 -> "bent", below ~70 -> "tightly bent".
    #         Pick thresholds you can defend, and test them on real photos.
    return "not classified yet (finish TODO 3)"


def analyze_pose(landmarks, sport):
    """
    Return a list of measurement dictionaries, e.g.
      [{"name": "Right elbow angle", "value": 142.0, "label": "bent"}]
    `value` is None when the measurement could not be made.
    """
    measurements = []

    # TODO 1: Find the shoulder, elbow, and wrist landmarks. (Right arm is below
    #         as an example; add the LEFT arm too.)
    angle = measure_joint_angle(landmarks, "right_shoulder", "right_elbow", "right_wrist")

    # TODO 2: Calculate the approximate elbow angle (done by the helper above).
    #         Then add another joint: knee (hip, knee, ankle) is a good one.

    # TODO 4: Return a simple observation to the UI. Handle angle being None
    #         (landmark hidden) with a friendly message instead of a crash.
    measurements.append({
        "name": "Right elbow angle",
        "value": angle,
        "label": classify_elbow_angle(angle) if angle is not None else "could not measure",
    })

    # TODO 5: Use `sport` to choose WHICH joints matter (if/elif/else).
    #         A basketball shot cares about the elbow; a soccer kick about the plant-foot knee.

    return measurements


# ==================================================
# FEATURE 2 + 5: Coaching Suggestions (INTERPRETATION)
# ==================================================
def build_suggestions(sport, level, measurements):
    """
    Return a list of suggestion strings for the user.
    These are interpretations of the measurements, not measurements themselves.
    """
    suggestions = [get_sport_instructions(sport), get_level_guidance(level)]

    # TODO 6: Loop over `measurements`. For each one with a value, add a suggestion
    #         that depends on the label AND the level (beginners: gentle and simple;
    #         advanced: more specific). Use language like "might" and "try",
    #         not "wrong" or "correct".
    #
    # TODO 7 (optional extension): Add a drill suggestion per skill
    #         (see sports.get_skills). Example: "wall shooting drill" for basketball.

    return suggestions


# ==================================================
# FEATURE 7: Optional Extensions (ideas only)
# ==================================================
# - Video: read frames with OpenCV, run detect_pose on each, and look at how an
#   angle CHANGES over time (a movement is a sequence, not one pose).
# - Compare two frames (e.g. before and after takeoff) and report the difference.
# - Draw measured angles on the annotated image.
# - Skill-specific drills chosen from the measurements.
