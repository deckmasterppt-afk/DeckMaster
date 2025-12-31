# beautiful_simple_system.py
# Simple, Beautiful Presentation System - Focus on Looking Good

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import io

class BeautifulSimpleSystem:
    def __init__(self):
        # Simple, beautiful dimensions
        self.slide_width = Inches(13.333)
        self.slide_height = Inches(7.5)
        
        # Beautiful, generous spacing
        self.beautiful_margin = Inches(1.5)  # Very generous margins
        self.content_width = self.slide_width - (self.beautiful_margin * 2)
        self.content_height = self.slide_height - (self.beautiful_margin * 2)
    
    def create_beautiful_slide(self, slide, slide_data, slide_index, total_slides, design_style='minimal_1'):
        """Create simple, beautiful slide that actually looks good"""
        
        # Store design style for use in visual methods
        self.current_design_style = design_style
        
        # Completely clear slide
        self._clear_slide_completely(slide)
        
        if slide_index == 0:
            return self._create_beautiful_title_slide(slide, slide_data, design_style)
        else:
            return self._create_beautiful_content_slide(slide, slide_data, slide_index, total_slides, design_style)
    
    def _create_beautiful_title_slide(self, slide, slide_data, design_style):
        """Create beautiful, elegant title slide with proper design colors"""
        
        # Get design style configuration
        from design_styles import get_design_style
        from theme_engine import hex_to_rgb
        style_config = get_design_style(design_style)
        
        # Title - centered, elegant, lots of space
        title_left = self.beautiful_margin
        title_top = self.slide_height * 0.35  # Better vertical centering
        title_width = self.content_width
        title_height = Inches(1.5)  # Controlled height
        
        title_shape = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
        title_frame = title_shape.text_frame
        title_frame.text = slide_data.get('title', 'Presentation Title')
        title_frame.margin_left = 0
        title_frame.margin_right = 0
        title_frame.margin_top = 0
        title_frame.margin_bottom = 0
        title_frame.vertical_anchor = MSO_ANCHOR.TOP  # Start from top
        title_frame.word_wrap = True
        
        # Beautiful title styling
        title_para = title_frame.paragraphs[0]
        title_para.alignment = PP_ALIGN.CENTER
        title_para.line_spacing = 1.1
        
        title_font = title_para.runs[0].font
        title_font.name = 'Calibri Light'  # Beautiful, modern font
        title_font.size = Pt(48)  # Large but controlled
        title_font.bold = False
        
        # Apply design style colors
        try:
            title_font.color.rgb = hex_to_rgb(style_config['colors']['title'])
            print(f"[DESIGN] Applied title color: {style_config['colors']['title']}")
        except Exception as e:
            print(f"[DESIGN] Title color fallback: {e}")
            title_font.color.rgb = RGBColor(31, 56, 100)  # Fallback
        
        # Add subtitle if available
        bullets = slide_data.get('bullets', [])
        if bullets and len(bullets) > 0:
            subtitle_top = title_top + title_height + Inches(0.3)
            subtitle_height = Inches(0.8)
            
            subtitle_shape = slide.shapes.add_textbox(title_left, subtitle_top, title_width, subtitle_height)
            subtitle_frame = subtitle_shape.text_frame
            subtitle_frame.text = bullets[0]
            subtitle_frame.margin_left = 0
            subtitle_frame.margin_right = 0
            subtitle_frame.margin_top = 0
            subtitle_frame.margin_bottom = 0
            subtitle_frame.vertical_anchor = MSO_ANCHOR.TOP
            subtitle_frame.word_wrap = True
            
            subtitle_para = subtitle_frame.paragraphs[0]
            subtitle_para.alignment = PP_ALIGN.CENTER
            subtitle_font = subtitle_para.runs[0].font
            subtitle_font.name = 'Calibri'
            subtitle_font.size = Pt(24)
            subtitle_font.bold = False
            
            try:
                subtitle_font.color.rgb = hex_to_rgb(style_config['colors']['body'])
            except:
                subtitle_font.color.rgb = RGBColor(68, 84, 106)
        
        return 'title'
    
    def _create_beautiful_content_slide(self, slide, slide_data, slide_index, total_slides, design_style):
        """Create beautiful content slide with proper text positioning and design colors"""
        
        # Get design style configuration
        from design_styles import get_design_style
        from theme_engine import hex_to_rgb
        style_config = get_design_style(design_style)
        
        # Beautiful title area - fixed positioning
        title_left = self.beautiful_margin
        title_top = self.beautiful_margin
        title_width = self.content_width * 0.55  # Leave space for visuals
        title_height = Inches(0.8)  # Controlled height
        
        title_shape = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
        title_frame = title_shape.text_frame
        title_frame.text = slide_data.get('title', 'Slide Title')
        title_frame.margin_left = 0
        title_frame.margin_right = 0
        title_frame.margin_top = 0
        title_frame.margin_bottom = 0
        title_frame.vertical_anchor = MSO_ANCHOR.TOP  # Start from top
        title_frame.word_wrap = True
        
        # Beautiful title styling with design colors
        title_para = title_frame.paragraphs[0]
        title_para.alignment = PP_ALIGN.LEFT
        title_font = title_para.runs[0].font
        title_font.name = 'Calibri'
        title_font.size = Pt(28)  # Readable size
        title_font.bold = True
        
        # Apply design style colors
        try:
            title_font.color.rgb = hex_to_rgb(style_config['colors']['title'])
            print(f"[DESIGN] Applied title color: {style_config['colors']['title']}")
        except Exception as e:
            print(f"[DESIGN] Title color fallback: {e}")
            title_font.color.rgb = RGBColor(31, 56, 100)  # Fallback
        
        # Beautiful content area - proper positioning
        content_left = self.beautiful_margin
        content_top = title_top + title_height + Inches(0.4)  # Below title with spacing
        content_width = self.content_width * 0.55  # Leave space for visuals
        content_height = self.slide_height - content_top - self.beautiful_margin  # Fit within slide
        
        content_shape = slide.shapes.add_textbox(content_left, content_top, content_width, content_height)
        content_frame = content_shape.text_frame
        content_frame.word_wrap = True
        content_frame.vertical_anchor = MSO_ANCHOR.TOP  # Start from top, not bottom!
        content_frame.margin_left = 0
        content_frame.margin_right = 0
        content_frame.margin_top = 0
        content_frame.margin_bottom = 0
        
        # Beautiful bullets - controlled and properly positioned
        bullets = slide_data.get('bullets', [])
        max_bullets = 4  # Limit to prevent overflow
        
        for i, bullet in enumerate(bullets[:max_bullets]):
            if i == 0:
                para = content_frame.paragraphs[0]
            else:
                para = content_frame.add_paragraph()
            
            # Clean bullet text
            bullet_text = str(bullet).strip()
            if not bullet_text.startswith('•'):
                bullet_text = f"• {bullet_text}"
            
            # Limit bullet text length to prevent overflow
            if len(bullet_text) > 80:
                bullet_text = bullet_text[:77] + "..."
            
            para.text = bullet_text
            para.level = 0
            para.space_after = Pt(16)  # Controlled spacing
            para.line_spacing = 1.4  # Readable line spacing
            
            # Beautiful bullet styling with design colors
            bullet_font = para.runs[0].font
            bullet_font.name = 'Calibri'
            bullet_font.size = Pt(20)  # Readable size
            bullet_font.bold = False
            
            # Apply design style colors
            try:
                bullet_font.color.rgb = hex_to_rgb(style_config['colors']['body'])
            except Exception as e:
                print(f"[DESIGN] Body color fallback: {e}")
                bullet_font.color.rgb = RGBColor(68, 84, 106)  # Fallback
        
        return 'content'
    
    def _clear_slide_completely(self, slide):
        """Completely clear slide"""
        shapes_to_remove = []
        for shape in slide.shapes:
            shapes_to_remove.append(shape)
        
        for shape in shapes_to_remove:
            try:
                slide.shapes._spTree.remove(shape._element)
            except:
                pass

    def add_single_beautiful_visual(self, slide, slide_data, design_style, layout_info, visual_type, slide_index=0, total_slides=10):
        """Add ONE beautiful visual element with professional distribution"""
        
        try:
            # Professional visual distribution pattern
            if visual_type == 'auto':
                visual_type = self._get_professional_visual_type(slide_index, total_slides, slide_data)
            
            # Smart visual type selection based on content (secondary)
            title = slide_data.get('title', '').lower()
            bullets = ' '.join(slide_data.get('bullets', [])).lower()
            content = f"{title} {bullets}"
            
            # Override with content-specific visuals when appropriate
            if visual_type == 'auto':
                if any(word in content for word in ['revenue', 'quarterly', 'performance', 'growth', 'trends', 'monthly']):
                    visual_type = 'chart'
                elif any(word in content for word in ['distribution', 'segment', 'channel', 'portfolio', 'mix']):
                    visual_type = 'pie'
                elif any(word in content for word in ['metrics', 'kpi', 'financial', 'summary', 'analysis', 'competitive']):
                    visual_type = 'table'
                else:
                    visual_type = 'image'
            
            # Add the visual element
            if visual_type == 'image':
                success = self._add_beautiful_image(slide, slide_data, design_style)
                if success:
                    print(f"[BEAUTIFUL] ✓ Added beautiful image to slide {slide_index + 1}")
                return success
            elif visual_type == 'chart':
                success = self._add_beautiful_chart(slide, slide_data, design_style, 'bar')
                if success:
                    print(f"[BEAUTIFUL] ✓ Added beautiful bar chart to slide {slide_index + 1}")
                return success
            elif visual_type == 'pie':
                success = self._add_beautiful_chart(slide, slide_data, design_style, 'pie')
                if success:
                    print(f"[BEAUTIFUL] ✓ Added beautiful pie chart to slide {slide_index + 1}")
                return success
            elif visual_type == 'table':
                success = self._add_beautiful_table(slide, slide_data, design_style)
                if success:
                    print(f"[BEAUTIFUL] ✓ Added beautiful table to slide {slide_index + 1}")
                return success
            else:
                return self._add_beautiful_placeholder(slide, slide_data, design_style)
                
        except Exception as e:
            print(f"[BEAUTIFUL] Error adding visual: {e}")
            return False
    
    def _get_professional_visual_type(self, slide_index, total_slides, slide_data):
        """Get professional visual type with balanced distribution"""
        
        # Skip title slide
        if slide_index == 0:
            return 'none'
        
        # Professional distribution patterns for different presentation lengths
        if total_slides <= 5:
            # Short presentation: Image, Chart, Table, Pie, Image
            pattern = ['image', 'chart', 'table', 'pie', 'image']
        elif total_slides <= 10:
            # Medium presentation: Balanced mix
            pattern = ['image', 'chart', 'table', 'pie', 'image', 'chart', 'table', 'pie', 'image', 'chart']
        elif total_slides <= 15:
            # Long presentation: More variety
            pattern = ['image', 'chart', 'pie', 'table', 'image', 'chart', 'table', 'pie', 'image', 'chart', 'pie', 'table', 'image', 'chart', 'table']
        else:
            # Very long presentation: Repeating professional pattern
            base_pattern = ['image', 'chart', 'pie', 'table', 'image', 'chart', 'table', 'pie']
            pattern = (base_pattern * ((total_slides // 8) + 1))[:total_slides]
        
        # Get visual type for this slide (adjust for 0-based indexing)
        if slide_index - 1 < len(pattern):
            return pattern[slide_index - 1]
        else:
            # Fallback for edge cases
            cycle = ['image', 'chart', 'table', 'pie']
            return cycle[(slide_index - 1) % 4]
    
    def _add_beautiful_image(self, slide, slide_data, design_style):
        """Add beautiful image from API"""
        try:
            from image_api_service import image_api
            
            # Get image from API
            image_data = image_api.get_image_for_slide(slide_data)
            
            if image_data and 'url' in image_data:
                # Download image
                image_bytes = image_api.download_image(image_data['url'])
                
                if image_bytes:
                    # Beautiful positioning - right side with generous margins
                    img_left = self.slide_width * 0.6  # More space for text
                    img_top = self.beautiful_margin + Inches(1.5)  # Below title
                    img_width = self.slide_width * 0.35  # Reasonable size
                    img_height = self.slide_height * 0.5  # Not too tall
                    
                    # Add image
                    image_stream = io.BytesIO(image_bytes)
                    slide.shapes.add_picture(image_stream, img_left, img_top, img_width, img_height)
                    return True
            
            # Fallback to placeholder
            return self._add_beautiful_placeholder(slide, slide_data, design_style)
            
        except Exception as e:
            print(f"[BEAUTIFUL_IMAGE] Error: {e}")
            return self._add_beautiful_placeholder(slide, slide_data, design_style)
    
    def _add_beautiful_chart(self, slide, slide_data, design_style, chart_type='bar'):
        """Add beautiful chart"""
        try:
            from chart_service import chart_service
            
            # Determine chart type based on content or parameter
            title = slide_data.get('title', '').lower()
            if chart_type == 'pie' or 'distribution' in title or 'segment' in title or 'mix' in title:
                chart_data = chart_service.generate_chart_data(slide_data, 'pie')
                chart_image_bytes = chart_service.create_chart_image(chart_data, 'modern')
            else:
                chart_data = chart_service.generate_chart_data(slide_data, 'bar')
                chart_image_bytes = chart_service.create_chart_image(chart_data, 'modern')
            
            if chart_image_bytes:
                # Beautiful positioning - right side
                chart_left = self.slide_width * 0.6
                chart_top = self.beautiful_margin + Inches(1.5)
                chart_width = self.slide_width * 0.35
                chart_height = self.slide_height * 0.5
                
                # Add chart
                image_stream = io.BytesIO(chart_image_bytes)
                slide.shapes.add_picture(image_stream, chart_left, chart_top, chart_width, chart_height)
                return True
            
            return False
            
        except Exception as e:
            print(f"[BEAUTIFUL_CHART] Error: {e}")
            return False
    
    def _add_beautiful_table(self, slide, slide_data, design_style):
        """Add beautiful table positioned on the right side to avoid text overlap"""
        try:
            from chart_service import chart_service
            
            # Generate table
            df = chart_service.create_table_data(slide_data)
            table_image_bytes = chart_service.create_table_image(df, 'modern')
            
            if table_image_bytes:
                # FIXED: Position table on RIGHT SIDE to avoid text overlap
                table_left = self.slide_width * 0.6  # Right side like images/charts
                table_top = self.beautiful_margin + Inches(1.5)  # Below title
                table_width = self.slide_width * 0.35  # Same width as other visuals
                table_height = self.slide_height * 0.5  # Reasonable height
                
                print(f"[BEAUTIFUL_TABLE] Positioning table on RIGHT SIDE to avoid text overlap")
                print(f"[BEAUTIFUL_TABLE] Position: left={table_left}, top={table_top}")
                
                # Add table
                image_stream = io.BytesIO(table_image_bytes)
                slide.shapes.add_picture(image_stream, table_left, table_top, table_width, table_height)
                return True
            
            return False
            
        except Exception as e:
            print(f"[BEAUTIFUL_TABLE] Error: {e}")
            return False
    
    def _add_beautiful_placeholder(self, slide, slide_data, design_style):
        """Add beautiful placeholder when no visual is available"""
        try:
            # Beautiful placeholder - right side
            placeholder_left = self.slide_width * 0.6
            placeholder_top = self.beautiful_margin + Inches(1.5)
            placeholder_width = self.slide_width * 0.35
            placeholder_height = self.slide_height * 0.4
            
            # Create beautiful rounded rectangle
            placeholder = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                placeholder_left, placeholder_top, placeholder_width, placeholder_height
            )
            
            # Beautiful styling
            placeholder.fill.solid()
            placeholder.fill.fore_color.rgb = RGBColor(248, 249, 250)  # Light gray
            placeholder.line.color.rgb = RGBColor(220, 220, 220)
            placeholder.line.width = Pt(1)
            
            # Beautiful text
            text_frame = placeholder.text_frame
            text_frame.clear()
            text_frame.margin_top = Inches(0.3)
            text_frame.margin_bottom = Inches(0.3)
            text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            # Add beautiful icon
            para = text_frame.paragraphs[0]
            para.text = "📊"
            para.alignment = PP_ALIGN.CENTER
            para.font.size = Pt(36)
            
            # Add subtitle
            para2 = text_frame.add_paragraph()
            para2.text = "Visual Content"
            para2.alignment = PP_ALIGN.CENTER
            para2.font.size = Pt(14)
            para2.font.color.rgb = RGBColor(108, 117, 125)
            
            return True
            
        except Exception as e:
            print(f"[BEAUTIFUL_PLACEHOLDER] Error: {e}")
            return False

# Global instance
beautiful_system = BeautifulSimpleSystem()