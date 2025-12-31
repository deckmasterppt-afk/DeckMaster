import requests
import gc
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct"

def call_llm(prompt: str) -> str:
    """
    Call Ollama LLM - simple and working
    """
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_ctx": 2048,
            "num_predict": 1024,
            "repeat_penalty": 1.1
        }
    }

    timeout = 120
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        result = data.get("response", "").strip()
        
        # Force garbage collection after LLM call
        gc.collect()
        
        return result
        
    except requests.exceptions.ConnectionError:
        print("⚠️ Ollama not running - using demo mode")
        return generate_demo_response(prompt)
    except Exception as e:
        print(f"⚠️ Ollama error: {e} - using demo mode")
        return generate_demo_response(prompt)

def generate_demo_response(prompt: str) -> str:
    """Generate RICH demo response using extracted content from prompt"""
    import re
    
    # Extract slide count from prompt
    slide_match = re.search(r'(\d+)\s*slides?', prompt.lower())
    slide_count = int(slide_match.group(1)) if slide_match else 5
    
    # Extract topic from TASK line in prompt
    topic = "Your Topic"
    task_match = re.search(r'TASK:\s*([^\n]+)', prompt)
    if task_match:
        topic = task_match.group(1).strip()
    
    # Extract content from prompt for rich information
    content_match = re.search(r'CONTENT TO USE:\s*(.*?)(?=CRITICAL REQUIREMENTS|$)', prompt, re.DOTALL)
    extracted_content = content_match.group(1).strip() if content_match else ""
    
    # Parse content into meaningful sections
    content_lines = [line.strip() for line in extracted_content.split('\n') if len(line.strip()) > 30]
    
    slides = []
    
    # FIRST SLIDE: Title slide only (no bullets, no visuals)
    slides.append({
        "slide_type": "title",
        "title": topic,
        "bullets": []
    })
    
    # Generate content slides with REAL information from extracted content
    for i in range(1, slide_count):
        slide_title = f"Key Aspects of {topic}" if i == 1 else f"Advanced Concepts in {topic}"
        
        # Use real content if available, otherwise generate contextual content
        if content_lines and len(content_lines) >= 4:
            # Use different sections of content for each slide
            start_idx = ((i - 1) * 3) % len(content_lines)
            slide_content = content_lines[start_idx:start_idx + 6]
            
            bullets = []
            for j, line in enumerate(slide_content[:6]):
                if len(line) > 40:
                    # Clean and format the line as a bullet point
                    clean_line = line[:150] + "..." if len(line) > 150 else line
                    if not clean_line.startswith('•'):
                        clean_line = f"• {clean_line}"
                    bullets.append(clean_line)
            
            # Ensure we have at least 4 bullets
            while len(bullets) < 4:
                bullets.append(f"• Additional insights and analysis related to {topic.lower()}")
                
        else:
            # Fallback to contextual content
            bullets = [
                f"• Comprehensive analysis of key factors and considerations in {topic.lower()}",
                f"• Detailed implementation strategies with proven methodologies and best practices",
                f"• Real-world examples and practical applications across various industry sectors",
                f"• Statistical data showing measurable improvements and performance metrics",
                f"• Expert recommendations based on extensive research, testing, and field studies"
            ]
        
        # Generate unique slide titles based on content
        if i == 1:
            slide_title = f"Introduction to {topic}"
        elif i == 2:
            slide_title = f"Key Components and Features"
        elif i == 3:
            slide_title = f"Implementation and Best Practices"
        elif i == 4:
            slide_title = f"Benefits and Applications"
        elif i == 5:
            slide_title = f"Advanced Strategies and Methods"
        else:
            slide_title = f"Detailed Analysis - Part {i-5}"
        
        slides.append({
            "slide_type": "content",
            "title": slide_title,
            "bullets": bullets[:6]  # Limit to 6 bullets max
        })
    
    result = {"slides": slides}
    return json.dumps(result, indent=2)