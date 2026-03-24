# job_store.py
# Simple job storage for DeckMaster

import time
import uuid
from typing import Dict, Any

# In-memory job store
jobs = {}

def create_job(user_id: str, job_data: Dict[str, Any]) -> str:
    """Create a new job and return job_id"""
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        'id': job_id,
        'state': 'PENDING',       # state field (not status)
        'created_at': time.time(),
        'data': job_data,
        'output': None,            # output file path
        'error': None,
        'user_id': user_id
    }
    
    return job_id

def get_job(job_id: str) -> Dict[str, Any]:
    """Get job by ID"""
    return jobs.get(job_id, None)

def update_state(job_id: str, state: str) -> None:
    """Update job state"""
    if job_id in jobs:
        jobs[job_id]['state'] = state
        jobs[job_id]['updated_at'] = time.time()

def complete_job(job_id: str, output_path: str = None) -> None:
    """Mark job as completed with output file path"""
    if job_id in jobs:
        jobs[job_id]['state'] = 'DONE'
        jobs[job_id]['output'] = output_path   # store as 'output'
        jobs[job_id]['updated_at'] = time.time()

def fail_job(job_id: str, error: str = None) -> None:
    """Mark job as failed"""
    if job_id in jobs:
        jobs[job_id]['state'] = 'FAILED'
        jobs[job_id]['error'] = error
        jobs[job_id]['updated_at'] = time.time()

def get_job_stats() -> Dict[str, int]:
    """Get job statistics"""
    total = len(jobs)
    done = sum(1 for j in jobs.values() if j['state'] == 'DONE')
    failed = sum(1 for j in jobs.values() if j['state'] == 'FAILED')
    active = sum(1 for j in jobs.values() if j['state'] in ('PENDING', 'PROCESSING'))
    return {
        'total_jobs': total,
        'completed_jobs': done,
        'failed_jobs': failed,
        'active_jobs': active
    }

def cleanup_old_jobs(max_age_hours: int = 24) -> None:
    """Clean up old jobs"""
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    to_remove = [
        job_id for job_id, job in jobs.items()
        if current_time - job.get('created_at', 0) > max_age_seconds
    ]
    for job_id in to_remove:
        del jobs[job_id]
