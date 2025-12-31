from pptx.util import Inches, Pt
from pptx.enum.chart import XL_CHART_TYPE
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
import io
from PIL import Image
from beautiful_simple_system import beautiful_system

def add_visual_elements_to_slide(slide, slide_data, design_style, visual_prefs, prs, slide_index=0):
    """Add beautiful, simple visual elements - MAXIMUM ONE per slide"""
    
    try:
        total_slides = len(prs.slides) if hasattr(prs, 'slides') else getattr(prs, '_total_slides', 10)
        
        # Use beautiful simple system - NO MORE MESSY MULTIPLE ELEMENTS
        layout_type = beautiful_system.create_beautiful_slide(
            slide, slide_data, slide_index, total_slides, design_style
        )
        
        # Only add ONE visual element if this is not a title slide
        if slide_index > 0 and layout_type != 'title':
            visual_added = False
            
            # Professional visual distribution with slide context
            if beautiful_system.add_single_beautiful_visual(slide, slide_data, design_style, {}, 'auto', slide_index, total_slides):
                visual_added = True
                print(f"[BEAUTIFUL] ✓ Added professional visual to slide {slide_index + 1}")
            
            if not visual_added and any(visual_prefs.values()):
                # Beautiful placeholder as fallback
                beautiful_system.add_single_beautiful_visual(slide, slide_data, design_style, {}, 'placeholder', slide_index, total_slides)
                print(f"[BEAUTIFUL] ✓ Added beautiful placeholder to slide {slide_index + 1}")
        
        elif slide_index == 0:
            print(f"[BEAUTIFUL] ✓ Created beautiful title slide")
        else:
            print(f"[BEAUTIFUL] ✓ Created beautiful text-only slide {slide_index + 1}")
            
    except Exception as e:
        print(f"[BEAUTIFUL] Error on slide {slide_index + 1}: {e}")
        import traceback
        traceback.print_exc()

# Legacy functions removed - now using beautiful_simple_system exclusively
# All visual elements are handled by the beautiful simple system for clean, uncluttered presentations