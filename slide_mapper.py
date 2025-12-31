# slide_mapper.py
# Simple slide layout mapping for DeckMaster

def get_slide_layout(slide_type):
    """Get layout information for a slide type"""
    
    layouts = {
        "title": {
            "layout_index": 0,
            "type": "title",
            "has_title": True,
            "has_content": True,
            "max_content_blocks": 1
        },
        "content": {
            "layout_index": 1,
            "type": "content", 
            "has_title": True,
            "has_content": True,
            "max_content_blocks": 3
        },
        "summary": {
            "layout_index": 1,
            "type": "content",
            "has_title": True, 
            "has_content": True,
            "max_content_blocks": 2
        }
    }
    
    return layouts.get(slide_type, layouts["content"])