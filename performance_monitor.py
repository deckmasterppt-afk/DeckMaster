# performance_monitor.py
# Performance monitoring for PPT generation stability

import time
import gc
import sys
from typing import Dict, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[WARNING] psutil not available - memory monitoring will be limited")

class PerformanceMonitor:
    """Monitor system performance during PPT generation with memory leak detection"""
    
    def __init__(self):
        self.start_time = None
        self.metrics = {}
        self.checkpoints = []
        self.memory_baseline = 0
        self.memory_threshold_mb = 500  # Alert if memory usage exceeds this per slide
    
    def start_monitoring(self, slide_count: int):
        """Start performance monitoring with memory baseline"""
        self.start_time = time.time()
        self.slide_count = slide_count
        self.memory_baseline = self._get_memory_usage()
        
        self.metrics = {
            "slide_count": slide_count,
            "start_time": self.start_time,
            "memory_baseline": self.memory_baseline,
            "memory_peak": self.memory_baseline,
            "checkpoints": [],
            "memory_warnings": 0,
            "gc_collections": 0  # Initialize this key
        }
        print(f"[MONITOR] Starting generation of {slide_count} slides - Baseline memory: {self.memory_baseline:.1f}MB")
    
    def checkpoint(self, slide_index: int, stage: str):
        """Record a checkpoint with memory leak detection"""
        if not self.start_time:
            return
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        memory = self._get_memory_usage()
        memory_delta = memory - self.memory_baseline
        
        # Update peak memory
        if memory > self.metrics.get("memory_peak", 0):
            self.metrics["memory_peak"] = memory
        
        checkpoint = {
            "slide_index": slide_index,
            "stage": stage,
            "elapsed_time": elapsed,
            "memory_mb": memory,
            "memory_delta": memory_delta,
            "timestamp": current_time
        }
        
        self.checkpoints.append(checkpoint)
        
        # Memory leak detection
        if slide_index > 0:
            memory_per_slide = memory_delta / slide_index
            if memory_per_slide > self.memory_threshold_mb:
                self.metrics["memory_warnings"] += 1
                print(f"[MEMORY WARNING] Slide {slide_index} - {memory_per_slide:.1f}MB/slide exceeds threshold")
                self._trigger_aggressive_cleanup()
        
        # Log every 3 slides or important stages
        if slide_index % 3 == 0 or stage in ["llm_complete", "ppt_complete", "slide_batch_complete"]:
            print(f"[MONITOR] Slide {slide_index}/{self.slide_count} - {stage} - {elapsed:.1f}s - {memory:.1f}MB (+{memory_delta:.1f}MB)")
    
    def _get_memory_usage(self):
        """Get current memory usage in MB"""
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            except:
                pass
        
        # Fallback to sys.getsizeof approximation
        try:
            return sys.getsizeof(gc.get_objects()) / 1024 / 1024
        except:
            return 0.0
    
    def _trigger_aggressive_cleanup(self):
        """Trigger aggressive garbage collection"""
        print("[CLEANUP] Triggering aggressive memory cleanup...")
        
        # Initialize gc_collections if not present
        if "gc_collections" not in self.metrics:
            self.metrics["gc_collections"] = 0
        
        # Multiple GC passes
        for i in range(3):
            collected = gc.collect()
            self.metrics["gc_collections"] += 1
            if collected > 0:
                print(f"[CLEANUP] GC pass {i+1}: collected {collected} objects")
    
    def get_memory_stats(self):
        """Get current memory statistics"""
        current_memory = self._get_memory_usage()
        return {
            "current_mb": current_memory,
            "baseline_mb": self.memory_baseline,
            "delta_mb": current_memory - self.memory_baseline,
            "peak_mb": self.metrics.get("memory_peak", current_memory),
            "warnings": self.metrics.get("memory_warnings", 0),
            "gc_collections": self.metrics.get("gc_collections", 0)
        }
    
    def finish_monitoring(self):
        """Finish monitoring and provide summary"""
        if not self.start_time:
            return
        
        end_time = time.time()
        total_time = end_time - self.start_time
        final_memory = self._get_memory_usage()
        memory_delta = final_memory - self.memory_baseline
        
        print(f"[MONITOR] Generation completed in {total_time:.1f}s")
        print(f"[MONITOR] Memory usage: {final_memory:.1f}MB (delta: +{memory_delta:.1f}MB)")
        print(f"[MONITOR] Peak memory: {self.metrics.get('memory_peak', final_memory):.1f}MB")
        print(f"[MONITOR] Memory warnings: {self.metrics.get('memory_warnings', 0)}")
        print(f"[MONITOR] GC collections: {self.metrics.get('gc_collections', 0)}")
        
        return {
            "total_time": total_time,
            "final_memory": final_memory,
            "memory_delta": memory_delta,
            "peak_memory": self.metrics.get("memory_peak", final_memory),
            "warnings": self.metrics.get("memory_warnings", 0),
            "gc_collections": self.metrics.get("gc_collections", 0),
            "slides_completed": self.slide_count
        }


# Global monitor instance
_monitor = PerformanceMonitor()

def start_monitoring(slide_count: int):
    """Start performance monitoring"""
    _monitor.start_monitoring(slide_count)

def checkpoint(slide_index: int, stage: str):
    """Record a checkpoint"""
    _monitor.checkpoint(slide_index, stage)

def get_memory_stats():
    """Get current memory statistics"""
    return _monitor.get_memory_stats()

def finish_monitoring():
    """Finish monitoring and get summary"""
    return _monitor.finish_monitoring()

def trigger_cleanup():
    """Manually trigger aggressive cleanup"""
    _monitor._trigger_aggressive_cleanup()
    
    def finish_monitoring(self) -> Dict[str, Any]:
        """Finish monitoring and return performance report"""
        if not self.start_time:
            return {}
            
        end_time = time.time()
        total_time = end_time - self.start_time
        final_memory = self._get_memory_usage()
        memory_growth = final_memory - self.metrics["memory_start"]
        
        report = {
            "slide_count": self.slide_count,
            "total_time_seconds": total_time,
            "time_per_slide": total_time / self.slide_count if self.slide_count > 0 else 0,
            "memory_start_mb": self.metrics["memory_start"],
            "memory_end_mb": final_memory,
            "memory_growth_mb": memory_growth,
            "checkpoints": self.checkpoints,
            "performance_rating": self._calculate_performance_rating(total_time, memory_growth)
        }
        
        print(f"[MONITOR] Generation complete: {total_time:.1f}s, {memory_growth:+.1f}MB memory")
        return report
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except:
            return 0.0
    
    def _calculate_performance_rating(self, total_time: float, memory_growth: float) -> str:
        """Calculate performance rating based on time and memory usage"""
        time_per_slide = total_time / self.slide_count if self.slide_count > 0 else 0
        
        # Rating criteria
        if time_per_slide < 2.0 and memory_growth < 50:
            return "EXCELLENT"
        elif time_per_slide < 5.0 and memory_growth < 100:
            return "GOOD"
        elif time_per_slide < 10.0 and memory_growth < 200:
            return "ACCEPTABLE"
        else:
            return "NEEDS_OPTIMIZATION"


# Global monitor instance
monitor = PerformanceMonitor()


def start_monitoring(slide_count: int):
    """Start performance monitoring"""
    monitor.start_monitoring(slide_count)


def checkpoint(slide_index: int, stage: str):
    """Record a checkpoint"""
    monitor.checkpoint(slide_index, stage)


def finish_monitoring() -> Dict[str, Any]:
    """Finish monitoring and get report"""
    return monitor.finish_monitoring()


def log_performance_warning(slide_count: int):
    """Log performance warnings for large presentations"""
    if slide_count > 20:
        print(f"[WARNING] Large presentation ({slide_count} slides) - expect longer generation time")
        print("[TIP] For faster generation, consider splitting into multiple smaller presentations")
    elif slide_count > 15:
        print(f"[INFO] Medium presentation ({slide_count} slides) - visual elements disabled for stability")