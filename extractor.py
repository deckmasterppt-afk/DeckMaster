# extractor.py

import requests
from bs4 import BeautifulSoup


def extract_main(url: str, max_chars: int = 25000) -> str:
    """Extract detailed content for rich slide generation"""
    try:
        print(f"[EXTRACT] Fetching content from: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "aside"]):
            tag.decompose()

        main_content = ""
        for selector in ['main', 'article', '.content', '.main-content', '#content', '#main']:
            elements = soup.select(selector)
            if elements:
                for el in elements:
                    main_content += el.get_text(separator="\n") + "\n"
                break

        if not main_content:
            main_content = soup.get_text(separator="\n")

        cleaned = _clean_text(main_content)
        print(f"[EXTRACT] Extracted {len(cleaned)} characters of content")
        return cleaned[:max_chars]

    except Exception as e:
        print(f"[EXTRACT] Error: {e}")
        return ""


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    seen = set()
    result = []
    for line in lines:
        if (len(line) > 25
                and line not in seen
                and not line.lower().startswith(('cookie', 'privacy', 'terms', 'subscribe', 'follow', 'click', 'sign up'))):
            seen.add(line)
            result.append(' '.join(line.split()))
    return "\n".join(result)


def build_prompt(content: str, task: str, slide_count: int = 10) -> str:
    # Reserve last slide for Thank You
    content_slides = slide_count - 2  # minus title + thank you

    return f"""You are an expert presentation designer. Create a professional, detailed presentation.

TASK: {task}
TOTAL SLIDES: {slide_count}

CONTENT SOURCE:
{content[:3000]}

STRICT RULES:
1. Slide 1: Title slide ONLY - just the main title, no bullets
2. Slides 2 to {slide_count - 1}: Content slides - each must have 5 DETAILED bullet points
3. Slide {slide_count}: Thank You slide - title "Thank You" and one subtitle line only
4. Every bullet point must be a COMPLETE sentence with real facts, data, or insights
5. NO generic filler text - every point must be specific and informative
6. NO repeated information across slides - each slide covers a unique aspect
7. Bullet points should be 15-25 words each - detailed but concise
8. Use numbers, percentages, and specific examples wherever possible

VISUAL HINTS (add "visual_type" to each content slide):
- Use "chart" for slides about growth, trends, statistics, comparisons, performance
- Use "table" for slides about features, comparisons, specifications, structured data
- Use "pie" for slides about distribution, breakdown, segments, percentages, shares
- Use "image" for slides about concepts, introductions, overviews, applications
- Use "none" for slides where text alone is sufficient (definitions, conclusions)
- NEVER repeat the same visual_type on consecutive slides

OUTPUT (valid JSON only, no extra text):
{{
  "slides": [
    {{
      "slide_type": "title",
      "title": "Your Main Title Here",
      "bullets": [],
      "visual_type": "none"
    }},
    {{
      "slide_type": "content",
      "title": "Specific Descriptive Slide Title",
      "bullets": [
        "First detailed bullet point with specific facts and data from the content",
        "Second detailed bullet point covering a different aspect with examples",
        "Third bullet point with statistics, numbers or concrete information",
        "Fourth bullet point with real-world applications or case studies",
        "Fifth bullet point with conclusions, benefits or actionable insights"
      ],
      "visual_type": "chart"
    }},
    {{
      "slide_type": "title",
      "title": "Thank You",
      "bullets": ["We appreciate your time and attention"],
      "visual_type": "none"
    }}
  ]
}}

GENERATE ALL {slide_count} SLIDES NOW:"""
