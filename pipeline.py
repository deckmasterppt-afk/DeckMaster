import json
import os
import gc
import sys
from extractor import extract_main, build_prompt
from llm_client import call_llm
from ppt_generator import generate_ppt  # Use the beautiful system
from performance_monitor import start_monitoring, checkpoint, finish_monitoring, get_memory_stats, trigger_cleanup
from job_store import get_job_stats

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_pipeline(url: str, task: str, design_style: str, visual_preferences: dict, slide_count: int = 10) -> str:
    """
    Run the complete PPT generation pipeline with robust error handling and memory management
    """
    output_path = None
    
    try:
        print("[PIPELINE] Starting PPT generation pipeline...")
        
        # Initial memory check
        initial_stats = get_memory_stats()
        print(f"[MEMORY] Initial usage: {initial_stats.get('current_mb', 0):.1f}MB")
        
        print("[1] Extracting content...")
        if not url or not url.strip():
            raise ValueError("URL is required for content extraction and better visual elements generation.")
        
        content = extract_main(url)
        if not content or len(content.strip()) < 100:
            raise ValueError("Could not extract sufficient content from URL. Please provide a URL with substantial content.")
        
        print(f"[1] Extracted {len(content)} characters from URL")

        print("[2] Building prompt...")
        prompt = build_prompt(content, task, slide_count)
        
        # Clear content from memory after prompt building
        content = None
        gc.collect()

        print("[3] Calling LLM...")
        raw = call_llm(prompt)
        
        # Clear prompt from memory
        prompt = None
        gc.collect()

        if not raw:
            raise ValueError("LLM returned empty response")

        # Remove accidental markdown
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "").strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"\n[ERROR] JSON Parse Error: {e}")
            print(f"[DEBUG] RAW LLM OUTPUT (first 500 chars):\n{raw[:500]}...")
            raise ValueError(f"LLM did not return valid JSON: {e}")

        # Clear raw response from memory
        raw = None
        gc.collect()

        if "slides" not in data:
            raise ValueError("JSON missing 'slides' key")

        # CRITICAL FIX: Intelligent slide limiting based on system resources
        slides = data["slides"]
        original_count = len(slides)
        
        # Memory-based slide limiting
        memory_stats = get_memory_stats()
        current_memory = memory_stats.get('current_mb', 0)
        
        if current_memory > 300:  # High memory usage already
            max_slides = 15
        elif current_memory > 200:
            max_slides = 20
        else:
            max_slides = 25
        
        if original_count > max_slides:
            print(f"[OPTIMIZATION] Limiting slides from {original_count} to {max_slides} for stability (current memory: {current_memory:.1f}MB)")
            slides = slides[:max_slides]
        elif original_count > 30:
            print(f"[SAFETY] Hard limit: Truncating from {original_count} to 30 slides")
            slides = slides[:30]

        # Clear original data to save memory
        data = None
        gc.collect()

        # Start performance monitoring
        slide_count = len(slides)
        start_monitoring(slide_count)
        checkpoint(0, "llm_complete")
        
        # Log memory and job statistics
        memory_stats = get_memory_stats()
        job_stats = get_job_stats()
        print(f"[STATS] Memory: {memory_stats.get('current_mb', 0):.1f}MB, Active jobs: {job_stats.get('total_jobs', 0)}")

        print(f"[4] Generating BEAUTIFUL PPT ({slide_count} slides)...")
        print(f"[DESIGN] Requested design style: {design_style}")
        print(f"[DESIGN] Visual preferences: {visual_preferences}")

        output_path = os.path.join(OUTPUT_DIR, "generated_ppt.pptx")
        
        # Generate PPT with BEAUTIFUL SYSTEM
        try:
            generate_ppt(
                slides=slides,
                output_path=output_path,
                design_style=design_style,
                visual_preferences=visual_preferences
            )
            print(f"[BEAUTIFUL] ✅ Created beautiful presentation with {slide_count} slides")
        except Exception as ppt_error:
            print(f"[ERROR] Beautiful PPT generation failed: {ppt_error}")
            
            # Attempt recovery with minimal settings
            print("[RECOVERY] Attempting recovery with minimal visual elements...")
            minimal_prefs = {k: False for k in visual_preferences.keys()}
            
            generate_ppt(
                slides=slides,
                output_path=output_path,
                design_style="minimal_1",  # Use beautiful default
                visual_preferences=minimal_prefs
            )
            print("[RECOVERY] Successfully generated beautiful PPT with minimal settings")

        # Clear slides from memory
        slides = None
        gc.collect()

        # Finish monitoring and log results
        performance_report = finish_monitoring()
        
        # Log final performance summary
        if performance_report:
            total_time = performance_report.get("total_time", 0)
            final_memory = performance_report.get("final_memory", 0)
            memory_delta = performance_report.get("memory_delta", 0)
            warnings = performance_report.get("warnings", 0)
            
            time_per_slide = total_time / slide_count if slide_count > 0 else 0
            
            # Performance rating
            if warnings == 0 and memory_delta < 200 and time_per_slide < 5:
                rating = "EXCELLENT"
            elif warnings <= 2 and memory_delta < 400 and time_per_slide < 10:
                rating = "GOOD"
            elif warnings <= 5 and memory_delta < 600:
                rating = "ACCEPTABLE"
            else:
                rating = "POOR"
            
            print(f"[PERFORMANCE] Rating: {rating}")
            print(f"[PERFORMANCE] Time: {total_time:.1f}s ({time_per_slide:.1f}s/slide)")
            print(f"[PERFORMANCE] Memory: {final_memory:.1f}MB (delta: +{memory_delta:.1f}MB)")
            print(f"[PERFORMANCE] Warnings: {warnings}")

        # Verify output file exists
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Generated PPT file not found at {output_path}")
        
        file_size = os.path.getsize(output_path) / 1024 / 1024  # MB
        print(f"[SUCCESS] Generated PPT: {output_path} ({file_size:.1f}MB)")

        return output_path

    except Exception as e:
        print(f"[PIPELINE ERROR] {type(e).__name__}: {e}")
        
        # Cleanup on error
        trigger_cleanup()
        
        # If we have a partial output file, remove it
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
                print(f"[CLEANUP] Removed partial output file: {output_path}")
            except:
                pass
        
        raise
    
    finally:
        # Final cleanup regardless of success/failure
        trigger_cleanup()
        
        # Log final memory state
        final_stats = get_memory_stats()
        print(f"[CLEANUP] Final memory usage: {final_stats.get('current_mb', 0):.1f}MB")
