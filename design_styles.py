# design_styles.py
# Design styles configuration and functions

from config import AVAILABLE_DESIGN_STYLES

def get_design_style(style_id):
    """Get design style configuration"""
    
    # Design style configurations
    design_configs = {
        # Minimal Designs
        'minimal_1': {
            'name': 'Pure White',
            'colors': {
                'title': '#2c3e50',
                'body': '#34495e',
                'accent': '#3498db'
            },
            'background': {
                'type': 'solid',
                'colors': ['#ffffff']
            }
        },
        'minimal_2': {
            'name': 'Soft Gray',
            'colors': {
                'title': '#2c3e50',
                'body': '#34495e',
                'accent': '#95a5a6'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#f8f9fa', '#e9ecef'],
                'direction': 'vertical'
            }
        },
        'minimal_3': {
            'name': 'Ivory Elegance',
            'colors': {
                'title': '#8b4513',
                'body': '#a0522d',
                'accent': '#daa520'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#fff8dc', '#f5f5dc'],
                'direction': 'vertical'
            }
        },
        
        # Corporate Designs
        'corporate_1': {
            'name': 'Navy Blue',
            'colors': {
                'title': '#ffffff',
                'body': '#f8f9fa',
                'accent': '#ffd700'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#1e3a8a', '#3b82f6'],
                'direction': 'diagonal'
            }
        },
        'corporate_2': {
            'name': 'Deep Blue',
            'colors': {
                'title': '#ffffff',
                'body': '#f1f5f9',
                'accent': '#60a5fa'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#1e40af', '#2563eb'],
                'direction': 'vertical'
            }
        },
        'corporate_3': {
            'name': 'Charcoal',
            'colors': {
                'title': '#ffffff',
                'body': '#e5e7eb',
                'accent': '#10b981'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#374151', '#4b5563'],
                'direction': 'diagonal'
            }
        },
        
        # Tech Designs
        'tech_1': {
            'name': 'Dark Tech',
            'colors': {
                'title': '#ffffff',
                'body': '#e5e7eb',
                'accent': '#06b6d4'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#0f172a', '#1e293b'],
                'direction': 'diagonal'
            }
        },
        'tech_2': {
            'name': 'Cyber Blue',
            'colors': {
                'title': '#ffffff',
                'body': '#f0f9ff',
                'accent': '#0ea5e9'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#0c4a6e', '#0369a1'],
                'direction': 'vertical'
            }
        },
        
        # Modern Designs
        'modern_1': {
            'name': 'Gradient Blue',
            'colors': {
                'title': '#ffffff',
                'body': '#f8fafc',
                'accent': '#f59e0b'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#3b82f6', '#8b5cf6'],
                'direction': 'diagonal'
            }
        },
        'modern_2': {
            'name': 'Sunset Glow',
            'colors': {
                'title': '#ffffff',
                'body': '#fef3c7',
                'accent': '#dc2626'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#f59e0b', '#ef4444'],
                'direction': 'diagonal'
            }
        },
        
        # Creative Designs
        'creative_1': {
            'name': 'Sunset Orange',
            'colors': {
                'title': '#ffffff',
                'body': '#fef3c7',
                'accent': '#dc2626'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#f97316', '#ef4444'],
                'direction': 'diagonal'
            }
        },
        'creative_2': {
            'name': 'Vibrant Pink',
            'colors': {
                'title': '#ffffff',
                'body': '#fdf2f8',
                'accent': '#06b6d4'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#ec4899', '#8b5cf6'],
                'direction': 'diagonal'
            }
        },
        
        # Academic Designs
        'academic_1': {
            'name': 'Forest Green',
            'colors': {
                'title': '#ffffff',
                'body': '#f0fdf4',
                'accent': '#fbbf24'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#166534', '#15803d'],
                'direction': 'vertical'
            }
        },
        'academic_2': {
            'name': 'Oxford Blue',
            'colors': {
                'title': '#ffffff',
                'body': '#eff6ff',
                'accent': '#f59e0b'
            },
            'background': {
                'type': 'gradient',
                'colors': ['#1e3a8a', '#2563eb'],
                'direction': 'vertical'
            }
        }
    }
    
    # Validate and return design style
    if style_id not in design_configs:
        print(f"[WARNING] Invalid design style '{style_id}', using minimal_1 as fallback")
        print(f"[WARNING] Available styles: {list(design_configs.keys())}")
        return design_configs['minimal_1']
    
    print(f"[DESIGN] Using design style: {style_id} ({design_configs[style_id]['name']})")
    return design_configs[style_id]

def apply_design_decorations(slide, design_style, prs):
    """Apply design decorations to slide"""
    try:
        # Get design configuration
        style_config = get_design_style(design_style)
        
        # Apply subtle decorative elements based on design style
        if 'tech' in design_style:
            # Add tech-style elements (minimal for now)
            pass
        elif 'corporate' in design_style:
            # Add corporate-style elements
            pass
        elif 'creative' in design_style:
            # Add creative elements
            pass
        
        # For now, keep decorations minimal to avoid complexity
        
    except Exception as e:
        print(f"[DECORATION] Warning: Could not apply decorations: {e}")

def list_available_designs():
    """List all available design styles"""
    designs = []
    
    for style_id, style_name in AVAILABLE_DESIGN_STYLES.items():
        designs.append({
            'id': style_id,
            'name': style_name,
            'category': style_id.split('_')[0].title()
        })
    
    return designs

def get_design_types():
    """Get available design type categories"""
    types = set()
    for style_id in AVAILABLE_DESIGN_STYLES.keys():
        category = style_id.split('_')[0]
        types.add(category)
    
    return sorted(list(types))

def get_designs_by_type(design_type):
    """Get designs filtered by type"""
    designs = []
    
    for style_id, style_name in AVAILABLE_DESIGN_STYLES.items():
        if style_id.startswith(design_type + '_'):
            designs.append({
                'id': style_id,
                'name': style_name,
                'category': design_type.title()
            })
    
    return designs

# Design type constants
DESIGN_TYPES = {
    'minimal': 'Clean & Simple',
    'corporate': 'Professional & Business',
    'tech': 'Modern & Technical',
    'creative': 'Bold & Artistic',
    'academic': 'Educational & Scholarly',
    'modern': 'Contemporary & Stylish'
}