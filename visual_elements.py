# visual_elements.py
# Smart visual element placement - only where content needs it

from beautiful_simple_system import beautiful_system


def add_visual_elements_to_slide(slide, slide_data, design_style,
                                  visual_prefs, prs, slide_index=0):
    """
    Build the slide layout and add ONE visual element only where the
    LLM decided it makes sense (via visual_type field).
    """
    try:
        total_slides = getattr(prs, '_total_slides', 10)
        is_last = (slide_index == total_slides - 1)

        # Build slide content (title / thank-you / content)
        layout_type = beautiful_system.create_beautiful_slide(
            slide, slide_data, slide_index, total_slides, design_style
        )

        # Title slide and Thank You slide → no visuals
        if slide_index == 0 or is_last:
            print(f"[VISUAL] Slide {slide_index + 1}: no visual (title/thank-you)")
            return

        # Content slide: add visual only if LLM specified one
        vtype = slide_data.get('visual_type', 'none')

        # Also respect user visual preferences
        if vtype == 'image'  and not visual_prefs.get('images', False):
            vtype = 'none'
        if vtype == 'chart'  and not visual_prefs.get('graphs', False):
            vtype = 'none'
        if vtype == 'pie'    and not visual_prefs.get('pie_charts', False):
            vtype = 'none'
        if vtype == 'table'  and not visual_prefs.get('tables', False):
            vtype = 'none'

        if vtype in ('none', None, ''):
            print(f"[VISUAL] Slide {slide_index + 1}: text-only (no visual needed)")
            return

        added = beautiful_system.add_single_beautiful_visual(
            slide, slide_data, design_style, {}, vtype, slide_index, total_slides
        )

        if added:
            print(f"[VISUAL] Slide {slide_index + 1}: ✓ {vtype} added")
        else:
            print(f"[VISUAL] Slide {slide_index + 1}: visual failed, keeping text-only")

    except Exception as e:
        print(f"[VISUAL] Error on slide {slide_index + 1}: {e}")
        import traceback
        traceback.print_exc()
