# extractor.py

import requests
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """
    Remove junk, scripts, excessive whitespace.
    Keep more content for better slide generation.
    """
    lines = [line.strip() for line in text.splitlines()]
    # Lower threshold to keep more content (was 40, now 30)
    lines = [line for line in lines if len(line) > 30]
    # Remove very short lines but keep more medium-length content
    lines = [line for line in lines if len(line) > 0]
    return "\n".join(lines)


def extract_main(url: str, max_chars: int = 25000) -> str:
    """Extract DETAILED content for rich slide generation"""
    try:
        print(f"[EXTRACT] Fetching content from: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "aside", "advertisement"]):
            tag.decompose()

        # Extract main content areas
        main_content = ""
        
        # Try to find main content areas
        content_selectors = [
            'main', 'article', '.content', '.main-content', 
            '.post-content', '.entry-content', '.article-content',
            '#content', '#main', '.container'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    main_content += element.get_text(separator="\n") + "\n"
                break
        
        # If no main content found, get all text
        if not main_content:
            main_content = soup.get_text(separator="\n")

        # Clean and process the text
        cleaned = clean_detailed_text(main_content)
        
        print(f"[EXTRACT] Extracted {len(cleaned)} characters of content")
        return cleaned[:max_chars]
        
    except Exception as e:
        print(f"[EXTRACT] Error: {e}")
        return ""

def clean_detailed_text(text: str) -> str:
    """
    Clean text but keep detailed information for rich slides
    """
    lines = [line.strip() for line in text.splitlines()]
    
    # Remove very short lines but keep informative ones
    cleaned_lines = []
    for line in lines:
        # Keep lines that have substantial content
        if len(line) > 20 and not line.lower().startswith(('cookie', 'privacy', 'terms', 'subscribe', 'follow')):
            # Remove excessive whitespace
            line = ' '.join(line.split())
            cleaned_lines.append(line)
    
    # Join lines and ensure we have paragraphs
    result = "\n".join(cleaned_lines)
    
    # Remove duplicate lines
    seen_lines = set()
    final_lines = []
    for line in result.split('\n'):
        if line not in seen_lines and len(line) > 20:
            seen_lines.add(line)
            final_lines.append(line)
    
    return "\n".join(final_lines)

def build_prompt(content: str, task: str, slide_count: int = 10) -> str:
    return f"""
You are an expert presentation creator. Create a comprehensive presentation with DETAILED, INFORMATIVE content.

TASK: {task}
SLIDES REQUIRED: {slide_count} slides (MUST generate exactly {slide_count} unique slides)

CONTENT TO USE:
{content[:4000]}

CRITICAL REQUIREMENTS:
1. FIRST SLIDE: Title slide only with just the main topic title (no bullets, no content)
2. REMAINING SLIDES (2-{slide_count}): Content slides with detailed information
3. Each content slide must have 4-6 detailed bullet points with specific information
4. Use the provided content to create informative, educational slides with real facts
5. NO generic headings - use specific, descriptive titles based on the content
6. Include facts, statistics, examples, and detailed explanations from the source material
7. Make each slide substantive and informative with unique, non-repeating content

SLIDE STRUCTURE:
- Slide 1: Title only (slide_type: "title", no bullets)
- Slides 2-{slide_count}: Content slides (slide_type: "content", with detailed bullets)

EXAMPLE OF PERFECT STRUCTURE:
{{
  "slides": [
    {{
      "slide_type": "title",
      "title": "Artificial Intelligence in Healthcare",
      "bullets": []
    }},
    {{
      "slide_type": "content", 
      "title": "AI-Powered Medical Imaging and Diagnostics",
      "bullets": [
        "• AI algorithms can detect cancer in medical scans with 94% accuracy, surpassing human radiologists in speed and precision",
        "• Deep learning models analyze CT scans and MRIs 150 times faster than traditional diagnostic methods",
        "• Google's DeepMind AI reduced false positives in breast cancer screening by 5.7% while maintaining sensitivity",
        "• Machine learning systems can identify diabetic retinopathy from retinal photographs with 90% accuracy",
        "• AI-assisted pathology helps detect rare diseases that human pathologists might miss in tissue samples"
      ]
    }}
  ]
}}

OUTPUT FORMAT (EXACT JSON):
{{
  "slides": [
    {{
      "slide_type": "title",
      "title": "Main Topic Title Here",
      "bullets": []
    }},
    {{
      "slide_type": "content",
      "title": "Specific Descriptive Subtitle Based on Content",
      "bullets": [
        "• Detailed informative bullet point with specific facts from the source",
        "• Another detailed point with examples, statistics, or real data",
        "• Third point with practical applications or concrete benefits",
        "• Fourth point with real-world examples or case studies from content",
        "• Fifth point with specific conclusions or actionable insights"
      ]
    }}
  ]
}}

GENERATE EXACTLY {slide_count} SLIDES WITH RICH, DETAILED INFORMATION FROM THE PROVIDED CONTENT:
"""

