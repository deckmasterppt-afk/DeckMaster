# stability_tester.py
# OPTIONAL: Test PPT generation stability - not needed for production
# This file can be used for testing but is not required for normal operation

import time
import gc
import os
from performance_monitor import start_monitoring, checkpoint, finish_monitoring, get_memory_stats, trigger_cleanup
from ppt_generator import generate_ppt
from job_store import create_job, get_job_stats, complete_job, fail_job

def create_test_slides(count: int):
    """Create test slides for stability testing"""
    slides = []
    
    # Title slide
    slides.append({
        "slide_type": "title",
        "title": f"Stability Test - {count} Slides",
        "bullets": [f"Testing PPT generation with {count} slides", "Memory optimization validation", "Error handling verification"]
    })
    
    # Content slides
    for i in range(1, count):
        slide = {
            "slide_type": "content",
            "title": f"Test Slide {i}",
            "bullets": [
                f"This is bullet point 1 for slide {i}",
                f"This is bullet point 2 for slide {i}",
                f"This is bullet point 3 for slide {i}",
                f"Memory usage should remain stable at slide {i}",
                f"No crashes should occur at slide {i}"
            ]
        }
        slides.append(slide)
    
    return slides

# This file is for testing only - not required for production use

def test_slide_generation(slide_counts: list, design_styles: list = None, visual_configs: list = None):
    """Test PPT generation with different slide counts and configurations"""
    
    if design_styles is None:
        design_styles = ["minimal_1", "corporate_1", "tech_1"]
    
    if visual_configs is None:
        visual_configs = [
            {"graphs": False, "tables": False, "pie_charts": False, "images": False},  # No visuals
            {"graphs": True, "tables": False, "pie_charts": False, "images": False},   # Graphs only
            {"graphs": False, "tables": True, "pie_charts": False, "images": False},   # Tables only
            {"graphs": True, "tables": True, "pie_charts": False, "images": False},    # Graphs + Tables
        ]
    
    results = []
    
    print("=" * 80)
    print("PPT GENERATION STABILITY TEST")
    print("=" * 80)
    
    for slide_count in slide_counts:
        for design_style in design_styles:
            for visual_config in visual_configs:
                
                test_name = f"{slide_count}slides_{design_style}_{_config_name(visual_config)}"
                print(f"\n[TEST] {test_name}")
                print("-" * 60)
                
                # Create job for tracking
                job_payload = {
                    "slides": create_test_slides(slide_count),
                    "design_style": design_style,
                    "visual_preferences": visual_config
                }
                job_id = create_job("stability_test", job_payload)
                
                try:
                    # Record initial state
                    initial_memory = get_memory_stats()
                    initial_time = time.time()
                    
                    # Generate test slides
                    slides = create_test_slides(slide_count)
                    
                    # Start monitoring
                    start_monitoring(slide_count)
                    
                    # Generate PPT
                    output_path = f"outputs/stability_test_{test_name}.pptx"
                    generate_ppt(
                        slides=slides,
                        output_path=output_path,
                        design_style=design_style,
                        visual_preferences=visual_config
                    )
                    
                    # Finish monitoring
                    performance_report = finish_monitoring()
                    
                    # Calculate results
                    end_time = time.time()
                    final_memory = get_memory_stats()
                    
                    test_result = {
                        "test_name": test_name,
                        "slide_count": slide_count,
                        "design_style": design_style,
                        "visual_config": visual_config,
                        "success": True,
                        "total_time": end_time - initial_time,
                        "time_per_slide": (end_time - initial_time) / slide_count,
                        "initial_memory": initial_memory.get('current_mb', 0),
                        "final_memory": final_memory.get('current_mb', 0),
                        "memory_delta": final_memory.get('current_mb', 0) - initial_memory.get('current_mb', 0),
                        "memory_warnings": performance_report.get('warnings', 0) if performance_report else 0,
                        "gc_collections": performance_report.get('gc_collections', 0) if performance_report else 0,
                        "output_file": output_path,
                        "file_size_mb": os.path.getsize(output_path) / 1024 / 1024 if os.path.exists(output_path) else 0,
                        "error": None
                    }
                    
                    # Mark job as complete
                    complete_job(job_id, output_path)
                    
                    print(f"[SUCCESS] {test_name}")
                    print(f"  Time: {test_result['total_time']:.1f}s ({test_result['time_per_slide']:.1f}s/slide)")
                    print(f"  Memory: {test_result['memory_delta']:.1f}MB delta")
                    print(f"  Warnings: {test_result['memory_warnings']}")
                    print(f"  File: {test_result['file_size_mb']:.1f}MB")
                    
                except Exception as e:
                    test_result = {
                        "test_name": test_name,
                        "slide_count": slide_count,
                        "design_style": design_style,
                        "visual_config": visual_config,
                        "success": False,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                    
                    # Mark job as failed
                    fail_job(job_id, e)
                    
                    print(f"[FAILED] {test_name}: {e}")
                
                results.append(test_result)
                
                # Cleanup between tests
                trigger_cleanup()
                time.sleep(1)  # Brief pause between tests
    
    return results

def _config_name(visual_config):
    """Generate a short name for visual configuration"""
    enabled = [k for k, v in visual_config.items() if v]
    if not enabled:
        return "no_visuals"
    return "_".join(enabled)

def run_comprehensive_stability_test():
    """Run a comprehensive stability test covering various scenarios"""
    
    print("Starting comprehensive stability test...")
    
    # Test scenarios
    slide_counts = [5, 10, 15, 20, 25]  # Progressive slide counts
    design_styles = ["minimal_1", "corporate_1"]  # Reduced for faster testing
    visual_configs = [
        {"graphs": False, "tables": False, "pie_charts": False, "images": False},  # Safest
        {"graphs": False, "tables": True, "pie_charts": False, "images": False},   # Tables only
    ]
    
    results = test_slide_generation(slide_counts, design_styles, visual_configs)
    
    # Analyze results
    print("\n" + "=" * 80)
    print("STABILITY TEST RESULTS SUMMARY")
    print("=" * 80)
    
    total_tests = len(results)
    successful_tests = len([r for r in results if r.get('success', False)])
    failed_tests = total_tests - successful_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    # Find the highest successful slide count
    successful_results = [r for r in results if r.get('success', False)]
    if successful_results:
        max_slides = max(r['slide_count'] for r in successful_results)
        print(f"Maximum successful slide count: {max_slides}")
        
        # Average performance for successful tests
        avg_time_per_slide = sum(r.get('time_per_slide', 0) for r in successful_results) / len(successful_results)
        avg_memory_delta = sum(r.get('memory_delta', 0) for r in successful_results) / len(successful_results)
        
        print(f"Average time per slide: {avg_time_per_slide:.1f}s")
        print(f"Average memory delta: {avg_memory_delta:.1f}MB")
    
    # Report failures
    failed_results = [r for r in results if not r.get('success', False)]
    if failed_results:
        print(f"\nFAILED TESTS:")
        for result in failed_results:
            print(f"  {result['test_name']}: {result.get('error', 'Unknown error')}")
    
    # Job store statistics
    job_stats = get_job_stats()
    print(f"\nJob store statistics:")
    print(f"  Total jobs: {job_stats.get('total_jobs', 0)}")
    print(f"  Memory estimate: {job_stats.get('memory_usage_estimate', 0)}MB")
    
    return results

if __name__ == "__main__":
    # Run the comprehensive test
    results = run_comprehensive_stability_test()
    
    # Save results to file
    import json
    with open("outputs/stability_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to outputs/stability_test_results.json")