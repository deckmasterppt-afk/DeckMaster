import requests
import gc
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi4-mini:latest"  # Faster model - better for production

def call_llm(prompt: str) -> str:
    """
    Call Ollama LLM with proper timeout for 7B model
    """
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_ctx": 4096,
            "num_predict": 1500,
            "repeat_penalty": 1.1
        }
    }

    try:
        print(f"[LLM] Calling Ollama model: {MODEL}")
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=(10, 300)  # 10s connect, 5min read - enough for 7B model
        )
        response.raise_for_status()

        data = response.json()
        result = data.get("response", "").strip()

        if not result:
            print("[LLM] Empty response from Ollama - using demo mode")
            return generate_demo_response(prompt)

        print(f"[LLM] Got {len(result)} chars from Ollama")
        gc.collect()
        return result

    except requests.exceptions.ConnectionError:
        print("[LLM] Ollama not reachable - using demo mode")
        return generate_demo_response(prompt)
    except requests.exceptions.Timeout:
        print("[LLM] Ollama timed out - using demo mode")
        return generate_demo_response(prompt)
    except Exception as e:
        print(f"[LLM] Error: {e} - using demo mode")
        return generate_demo_response(prompt)


def generate_demo_response(prompt: str) -> str:
    """Generate rich demo response when Ollama is unavailable"""
    import re

    # Extract slide count
    slide_match = re.search(r'(\d+)\s*slides?', prompt.lower())
    slide_count = int(slide_match.group(1)) if slide_match else 5

    # Extract topic
    topic = "Presentation"
    task_match = re.search(r'TASK:\s*([^\n]+)', prompt)
    if task_match:
        topic = task_match.group(1).strip()

    # Extract content from prompt
    content_match = re.search(r'CONTENT TO USE:\s*(.*?)(?=CRITICAL REQUIREMENTS|$)', prompt, re.DOTALL)
    extracted_content = content_match.group(1).strip() if content_match else ""
    content_lines = [l.strip() for l in extracted_content.split('\n') if len(l.strip()) > 40]

    slides = []

    # Title slide
    slides.append({
        "slide_type": "title",
        "title": topic,
        "bullets": []
    })

    # Slide titles based on topic
    slide_titles = [
        f"Introduction to {topic}",
        f"Key Concepts and Fundamentals",
        f"Core Features and Benefits",
        f"Implementation and Best Practices",
        f"Real-World Applications",
        f"Challenges and Solutions",
        f"Future Trends and Opportunities",
        f"Case Studies and Examples",
        f"Strategic Recommendations",
        f"Summary and Key Takeaways"
    ]

    for i in range(1, slide_count):
        title = slide_titles[i - 1] if i - 1 < len(slide_titles) else f"Section {i}"

        # Use real extracted content if available
        if content_lines and len(content_lines) >= 3:
            start = ((i - 1) * 4) % len(content_lines)
            raw_bullets = content_lines[start:start + 5]
            bullets = []
            for b in raw_bullets:
                clean = b[:160] + "..." if len(b) > 160 else b
                bullets.append(f"• {clean}" if not clean.startswith("•") else clean)
            while len(bullets) < 4:
                bullets.append(f"• Key insight related to {topic.lower()}")
        else:
            bullets = [
                f"• Comprehensive overview of {topic.lower()} with detailed analysis",
                f"• Evidence-based strategies and proven methodologies for success",
                f"• Real-world examples demonstrating practical applications",
                f"• Data-driven insights showing measurable impact and results",
                f"• Expert recommendations for effective implementation"
            ]

        slides.append({
            "slide_type": "content",
            "title": title,
            "bullets": bullets[:5]
        })

    return json.dumps({"slides": slides}, indent=2)
