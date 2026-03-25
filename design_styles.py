# design_styles.py
# Thin wrapper - all real design logic lives in design_engine.py

from design_engine import get_design, apply_design, list_designs, DESIGNS


def get_design_style(style_id: str) -> dict:
    """Return design config dict for a given style ID."""
    return get_design(style_id)


def apply_design_decorations(slide, design_style: str, prs):
    """Apply full design decorations (background + accents) to a slide."""
    try:
        apply_design(slide, prs, design_style)
    except Exception as e:
        print(f"[DESIGN] Decoration error: {e}")


def list_available_designs():
    return list_designs()


def get_design_types():
    return sorted({d['category'] for d in DESIGNS.values()})
