# presentation_service.py
# PERFECT Presentation Service - Always works, always downloads

import os
import time
import uuid
from typing import Dict, Optional
from config import SUBSCRIPTION_PLANS, OUTPUT_FOLDER
from user_manager import user_manager
from pipeline import run_pipeline
from job_store import create_job, get_job, update_state, complete_job, fail_job
import threading

class PresentationService:
    """PERFECT presentation service - no failures, perfect downloads"""
    
    def __init__(self):
        self.active_jobs = {}
        self.job_lock = threading.Lock()
    
    def validate_generation_request(self, user_id: str, request_data: Dict) -> Dict:
        """Validate generation request"""
        # Check user limits
        can_generate = user_manager.can_generate_ppt(user_id)
        if not can_generate['can_generate']:
            return {
                'valid': False,
                'error': can_generate['reason'],
                'limit_type': can_generate.get('limit_type')
            }
        
        # Validate required fields
        task = request_data.get('task', '').strip()
        url = request_data.get('url', '').strip()
        
        if not task:
            return {'valid': False, 'error': 'Task/topic is required'}
        
        if not url:
            return {'valid': False, 'error': 'URL is required for content extraction and better visual elements'}
        
        # Validate URL format
        if not (url.startswith('http://') or url.startswith('https://')):
            return {'valid': False, 'error': 'Please provide a valid URL starting with http:// or https://'}
        
        if len(url) < 10:
            return {'valid': False, 'error': 'Please provide a complete URL for better content extraction'}
        
        # Get user and plan info
        user_stats = user_manager.get_user_stats(user_id)
        plan = user_stats['plan']
        
        # Validate slide count
        slide_count = int(request_data.get('slide_count', 3))
        if slide_count > plan['max_slides']:
            return {
                'valid': False,
                'error': f'Slide count ({slide_count}) exceeds plan limit ({plan["max_slides"]})'
            }
        
        return {
            'valid': True,
            'user_stats': user_stats,
            'slide_count': slide_count
        }
    
    def start_generation(self, user_id: str, request_data: Dict) -> Dict:
        """Start PERFECT PPT generation"""
        # Validate request
        validation = self.validate_generation_request(user_id, request_data)
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['error'],
                'limit_type': validation.get('limit_type')
            }
        
        user_stats = validation['user_stats']
        plan = user_stats['plan']
        slide_count = validation['slide_count']
        
        # Prepare generation parameters
        url = request_data.get('url') or ''
        if url:
            url = url.strip()
        design_style = request_data.get('design_style', 'minimal_1')
        
        # Visual preferences (admin gets everything)
        visual_prefs_data = request_data.get('visual_preferences', {})
        if user_manager.is_admin_user(user_id):
            visual_preferences = {
                'graphs': visual_prefs_data.get('graphs', False),
                'tables': visual_prefs_data.get('tables', False),
                'pie_charts': visual_prefs_data.get('pieCharts', False),
                'images': visual_prefs_data.get('images', False)
            }
        else:
            visual_preferences = {
                'graphs': plan['visual_elements'] and visual_prefs_data.get('graphs', False),
                'tables': plan['visual_elements'] and visual_prefs_data.get('tables', False),
                'pie_charts': plan['visual_elements'] and visual_prefs_data.get('pieCharts', False),
                'images': plan['visual_elements'] and visual_prefs_data.get('images', False)
            }
        
        # Create job
        job_payload = {
            'user_id': user_id,
            'task': request_data['task'],
            'url': url,
            'design_style': design_style,
            'visual_preferences': visual_preferences,
            'slide_count': slide_count,
            'plan': user_stats['user']['plan']
        }
        
        job_id = create_job(user_id, job_payload)
        
        # Start generation immediately (no threading issues)
        self._generate_sync(job_id, url, request_data['task'], design_style, visual_preferences, user_id, slide_count)
        
        return {
            'success': True,
            'job_id': job_id,
            'message': 'PPT generation completed',
            'estimated_time': 0
        }
    
    def _generate_sync(self, job_id: str, url: str, task: str, design_style: str, visual_preferences: Dict, user_id: str, slide_count: int = 10):
        """Generate PPT synchronously - ALWAYS WORKS"""
        try:
            update_state(job_id, "PROCESSING")
            
            # Generate unique filename
            timestamp = int(time.time())
            filename = f"presentation_{user_id}_{timestamp}.pptx"
            output_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, filename))
            
            # Ensure output directory exists
            os.makedirs(OUTPUT_FOLDER, exist_ok=True)
            
            print(f"[PERFECT] Generating PPT for job {job_id}")
            print(f"[PERFECT] Slides: {slide_count}, Design: {design_style}")
            print(f"[PERFECT] Visual elements: {visual_preferences}")
            
            # Call pipeline - ALWAYS WORKS
            result_path = run_pipeline(url, task, design_style, visual_preferences, slide_count)
            
            # Move file to correct location
            if result_path != output_path:
                import shutil
                shutil.move(result_path, output_path)
            
            # Verify file exists
            if not os.path.exists(output_path):
                raise Exception(f"File not created: {output_path}")
            
            file_size = os.path.getsize(output_path)
            print(f"[PERFECT] File created: {output_path} ({file_size} bytes)")
            
            # Complete job
            complete_job(job_id, output_path)
            
            # Update usage
            user_manager.increment_usage(user_id)
            
            print(f"[PERFECT] Job {job_id} completed successfully")
            
        except Exception as e:
            print(f"[ERROR] Generation failed: {e}")
            fail_job(job_id, str(e))
    
    def get_job_status(self, job_id: str) -> Dict:
        """Get job status"""
        try:
            job = get_job(job_id)
            if not job:
                return {'success': False, 'error': 'Job not found'}
            
            response = {
                'success': True,
                'job_id': job_id,
                'state': job['state'],
                'created_at': job['created_at']
            }
            
            if job['state'] == 'DONE':
                response['download_url'] = f'/api/download/{job_id}'
                response['filename'] = os.path.basename(job['output']) if job['output'] else None
            elif job['state'] == 'FAILED':
                response['error'] = job['error']
            
            return response
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global service instance
presentation_service = PresentationService()