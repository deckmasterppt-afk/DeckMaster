# beautiful_simple_system.py
# Professional Presentation System

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import io


class BeautifulSimpleSystem:
    def __init__(self):
        self.slide_width  = Inches(13.333)
        self.slide_height = Inches(7.5)
        self.margin       = Inches(0.8)

    # ─────────────────────────────────────────────
    # PUBLIC ENTRY POINT
    # ─────────────────────────────────────────────

    def create_beautiful_slide(self, slide, slide_data, slide_index,
                               total_slides, design_style='minimal_1'):
        self.current_design_style = design_style
        self._clear_slide(slide)

        is_last = (slide_index == total_slides - 1)

        if slide_index == 0:
            return self._title_slide(slide, slide_data, design_style)
        elif is_last:
            return self._thankyou_slide(slide, slide_data, design_style)
        else:
            return self._content_slide(slide, slide_data, design_style)

    # ─────────────────────────────────────────────
    # TITLE SLIDE
    # ─────────────────────────────────────────────

    def _title_slide(self, slide, slide_data, design_style):
        from design_styles import get_design_style
        from theme_engine import hex_to_rgb
        cfg = get_design_style(design_style)

        cx = self.slide_width / 2
        cy = self.slide_height / 2

        # Main title – centred
        w, h = Inches(10), Inches(2)
        shape = slide.shapes.add_textbox(cx - w/2, cy - h - Inches(0.3), w, h)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        p = tf.paragraphs[0]
        p.text = slide_data.get('title', 'Presentation Title')
        p.alignment = PP_ALIGN.CENTER
        run = p.runs[0]
        run.font.name = 'Calibri Light'
        run.font.size = Pt(52)
        run.font.bold = False
        try:
            run.font.color.rgb = hex_to_rgb(cfg['colors']['title'])
        except Exception:
            run.font.color.rgb = RGBColor(255, 255, 255)

        # Subtitle / first bullet
        bullets = slide_data.get('bullets', [])
        if bullets:
            sw, sh = Inches(8), Inches(1)
            sub = slide.shapes.add_textbox(cx - sw/2, cy + Inches(0.4), sw, sh)
            stf = sub.text_frame
            stf.word_wrap = True
            sp = stf.paragraphs[0]
            sp.text = str(bullets[0]).lstrip('•').strip()
            sp.alignment = PP_ALIGN.CENTER
            sr = sp.runs[0]
            sr.font.name = 'Calibri'
            sr.font.size = Pt(22)
            try:
                sr.font.color.rgb = hex_to_rgb(cfg['colors']['body'])
            except Exception:
                sr.font.color.rgb = RGBColor(220, 220, 220)

        return 'title'

    # ─────────────────────────────────────────────
    # THANK YOU SLIDE
    # ─────────────────────────────────────────────

    def _thankyou_slide(self, slide, slide_data, design_style):
        from design_styles import get_design_style
        from theme_engine import hex_to_rgb
        cfg = get_design_style(design_style)

        cx = self.slide_width / 2
        cy = self.slide_height / 2

        # "Thank You" in elegant script-like font
        w, h = Inches(10), Inches(2.5)
        shape = slide.shapes.add_textbox(cx - w/2, cy - h/2 - Inches(0.5), w, h)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        p = tf.paragraphs[0]
        p.text = slide_data.get('title', 'Thank You')
        p.alignment = PP_ALIGN.CENTER
        run = p.runs[0]
        # Elegant handwriting-style font with fallback chain
        run.font.name = 'Segoe Script'   # Windows elegant script
        run.font.size = Pt(64)
        run.font.bold = False
        try:
            run.font.color.rgb = hex_to_rgb(cfg['colors']['title'])
        except Exception:
            run.font.color.rgb = RGBColor(255, 255, 255)

        # Subtitle line
        bullets = slide_data.get('bullets', [])
        subtitle = bullets[0] if bullets else 'We appreciate your time and attention'
        sw, sh = Inches(9), Inches(1)
        sub = slide.shapes.add_textbox(cx - sw/2, cy + Inches(0.8), sw, sh)
        stf = sub.text_frame
        stf.word_wrap = True
        sp = stf.paragraphs[0]
        sp.text = str(subtitle).lstrip('•').strip()
        sp.alignment = PP_ALIGN.CENTER
        sr = sp.runs[0]
        sr.font.name = 'Calibri Light'
        sr.font.size = Pt(22)
        sr.font.italic = True
        try:
            sr.font.color.rgb = hex_to_rgb(cfg['colors']['body'])
        except Exception:
            sr.font.color.rgb = RGBColor(200, 200, 200)

        return 'title'

    # ─────────────────────────────────────────────
    # CONTENT SLIDE
    # ─────────────────────────────────────────────

    def _content_slide(self, slide, slide_data, design_style):
        from design_styles import get_design_style
        from theme_engine import hex_to_rgb
        cfg = get_design_style(design_style)

        visual_type = slide_data.get('visual_type', 'none')
        has_visual   = visual_type not in ('none', None, '')

        # Layout: if visual → text takes left 58%, visual takes right 38%
        #         no visual → text takes full width
        text_w = Inches(7.2) if has_visual else Inches(11.7)
        text_x = self.margin

        # ── Title ──
        title_shape = slide.shapes.add_textbox(
            text_x, self.margin, text_w, Inches(0.9))
        tf = title_shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP

        p = tf.paragraphs[0]
        p.text = slide_data.get('title', '')
        p.alignment = PP_ALIGN.LEFT
        run = p.runs[0]
        run.font.name = 'Calibri'
        run.font.size = Pt(30)
        run.font.bold = True
        try:
            run.font.color.rgb = hex_to_rgb(cfg['colors']['title'])
        except Exception:
            run.font.color.rgb = RGBColor(31, 56, 100)

        # ── Bullets ──
        bullets = slide_data.get('bullets', [])
        content_top    = self.margin + Inches(1.05)
        content_height = self.slide_height - content_top - self.margin

        content_shape = slide.shapes.add_textbox(
            text_x, content_top, text_w, content_height)
        ctf = content_shape.text_frame
        ctf.word_wrap = True
        ctf.vertical_anchor = MSO_ANCHOR.TOP

        # Adaptive font size based on bullet count
        n = len(bullets)
        if n <= 3:
            fsize, spacing = Pt(20), Pt(14)
        elif n <= 5:
            fsize, spacing = Pt(18), Pt(10)
        else:
            fsize, spacing = Pt(16), Pt(8)

        for i, bullet in enumerate(bullets[:6]):
            para = ctf.paragraphs[0] if i == 0 else ctf.add_paragraph()
            text = str(bullet).strip()
            if not text.startswith('•'):
                text = f'• {text}'
            para.text = text
            para.space_after = spacing
            para.line_spacing = 1.35
            brun = para.runs[0]
            brun.font.name = 'Calibri'
            brun.font.size = fsize
            brun.font.bold = False
            try:
                brun.font.color.rgb = hex_to_rgb(cfg['colors']['body'])
            except Exception:
                brun.font.color.rgb = RGBColor(50, 50, 50)

        return 'content'

    # ─────────────────────────────────────────────
    # VISUAL PLACEMENT (called from visual_elements)
    # ─────────────────────────────────────────────

    def add_single_beautiful_visual(self, slide, slide_data, design_style,
                                    layout_info, visual_type, slide_index=0,
                                    total_slides=10):
        """Add ONE visual element based on content type. Returns True if added."""
        try:
            vtype = slide_data.get('visual_type', 'none')

            if vtype in ('none', None, ''):
                return False

            # Right-side zone
            vis_x = self.slide_width * 0.62
            vis_y = self.margin + Inches(1.0)
            vis_w = self.slide_width * 0.34
            vis_h = self.slide_height - vis_y - self.margin

            if vtype == 'image':
                return self._add_image(slide, slide_data, vis_x, vis_y, vis_w, vis_h)
            elif vtype == 'chart':
                return self._add_chart(slide, slide_data, vis_x, vis_y, vis_w, vis_h, 'bar')
            elif vtype == 'pie':
                return self._add_chart(slide, slide_data, vis_x, vis_y, vis_w, vis_h, 'pie')
            elif vtype == 'table':
                return self._add_table(slide, slide_data, vis_x, vis_y, vis_w, vis_h)
            else:
                return False

        except Exception as e:
            print(f"[VISUAL] Error adding visual: {e}")
            return False

    # ─────────────────────────────────────────────
    # VISUAL HELPERS
    # ─────────────────────────────────────────────

    def _add_image(self, slide, slide_data, x, y, w, h):
        try:
            from image_api_service import image_api
            img_data = image_api.get_image_for_slide(slide_data)
            if img_data and 'url' in img_data:
                img_bytes = image_api.download_image(img_data['url'])
                if img_bytes:
                    slide.shapes.add_picture(io.BytesIO(img_bytes), x, y, w, h)
                    print(f"[VISUAL] ✓ Image added")
                    return True
            return False
        except Exception as e:
            print(f"[VISUAL] Image error: {e}")
            return False

    def _add_chart(self, slide, slide_data, x, y, w, h, chart_type):
        try:
            from chart_service import chart_service
            data   = chart_service.generate_chart_data(slide_data, chart_type)
            img_b  = chart_service.create_chart_image(data, 'modern')
            if img_b:
                slide.shapes.add_picture(io.BytesIO(img_b), x, y, w, h)
                print(f"[VISUAL] ✓ {chart_type} chart added")
                return True
            return False
        except Exception as e:
            print(f"[VISUAL] Chart error: {e}")
            return False

    def _add_table(self, slide, slide_data, x, y, w, h):
        try:
            from chart_service import chart_service
            df    = chart_service.create_table_data(slide_data)
            img_b = chart_service.create_table_image(df, 'modern')
            if img_b:
                slide.shapes.add_picture(io.BytesIO(img_b), x, y, w, h)
                print(f"[VISUAL] ✓ Table added")
                return True
            return False
        except Exception as e:
            print(f"[VISUAL] Table error: {e}")
            return False

    # ─────────────────────────────────────────────
    # UTILITIES
    # ─────────────────────────────────────────────

    def _clear_slide(self, slide):
        for shape in list(slide.shapes):
            try:
                slide.shapes._spTree.remove(shape._element)
            except Exception:
                pass


# Global instance
beautiful_system = BeautifulSimpleSystem()
