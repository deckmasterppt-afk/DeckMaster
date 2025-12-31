# job_store.py
# Simple job storage and statistics for DeckMaster

import time
from typing import Dict, Any

# Simple in-memory job store
jobs = {}
job_stats = {
    'total_jobs': 0,
    'completed_jobs': 0,
    'failed_jobs': 0,
    'active_jobs': 0
}

def create_job(job_id: str, job_data: Dict[str, Any]) -> None:
    """Create a new job"""
    jobs[job_id] = {
        'id': job_id,
        'status': 'pending',
        'created_at': time.time(),
        'data': job_data,
        'result': None,
        'error': None
    }
    job_stats['total_jobs'] += 1
    job_stats['active_jobs'] += 1

def update_job_status(job_id: str, status: str, result: Any = None, error: str = None) -> None:
    """Update job status"""
    if job_id in jobs:
        jobs[job_id]['status'] = status
        jobs[job_id]['updated_at'] = time.time()
        
        if result:
            jobs[job_id]['result'] = result
        if error:
            jobs[job_id]['error'] = error
            
        if status == 'completed':
            job_stats['completed_jobs'] += 1
            job_stats['active_jobs'] -= 1
        elif status == 'failed':
            job_stats['failed_jobs'] += 1
            job_stats['active_jobs'] -= 1

def get_job(job_id: str) -> Dict[str, Any]:
    """Get job by ID"""
    return jobs.get(job_id, None)

def get_job_stats() -> Dict[str, int]:
    """Get job statistics"""
    return job_stats.copy()

def update_state(job_id: str, state: str) -> None:
    """Update job state (alias for update_job_status)"""
    update_job_status(job_id, state)

def complete_job(job_id: str, result: Any = None) -> None:
    """Mark job as completed"""
    update_job_status(job_id, 'completed', result=result)

def fail_job(job_id: str, error: str = None) -> None:
    """Mark job as failed"""
    update_job_status(job_id, 'failed', error=error)

def cleanup_old_jobs(max_age_hours: int = 24) -> None:
    """Clean up old jobs"""
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    to_remove = []
    for job_id, job in jobs.items():
        if current_time - job.get('created_at', 0) > max_age_seconds:
            to_remove.append(job_id)
    
    for job_id in to_remove:
        del jobs[job_id]