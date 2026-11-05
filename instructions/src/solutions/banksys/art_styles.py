"""
art_styles.py -- information about art styles.

Everything about *browsing* art styles lives here, so app.py stays small.
"""

# ==================================================
# FEATURE 1: Learn About Art Styles
# ==================================================
# A dictionary maps a "key" (the style name) to a "value" (its description).
#   ART_STYLES["Impressionism"]  ->  "A 19th-century movement ..."
ART_STYLES = {
    "Impressionism": (
        "Loose, visible brushstrokes that capture light and a fleeting moment. "
        "Think Monet's water lilies: soft edges, bright broken color."
    ),
    "Cubism": (
        "Objects are broken into geometric shapes and shown from several "
        "viewpoints at once. Think Picasso's portraits."
    ),
    "Pop Art": (
        "Bold flat color, strong outlines, and imagery from advertising and "
        "comics. Think Andy Warhol and Roy Lichtenstein."
    ),
    "Realism": (
        "Careful, accurate depiction of subjects as they appear in real life, "
        "with attention to light, texture, and proportion."
    ),
}

# OPTIONAL CHALLENGE (do this after everything else works!):
#   1. Add 3+ more styles (Surrealism, Ukiyo-e, Art Nouveau, ...).
#   2. Turn each value into a dictionary, e.g.
#        {"description": "...", "artists": ["Monet", "Renoir"]}
#      then update get_style_description() to show the artists too.
#   3. Add example image URLs and show them with a gr.Image in app.py.


def get_style_names():
    """Return a list of style names for the dropdown. (Already done for you.)"""
    return list(ART_STYLES.keys())


def get_style_description(style_name):
    """Look up a style and return its description as text."""
    if not style_name:
        return "Please choose a style."
    return ART_STYLES.get(style_name, "Unknown style")
